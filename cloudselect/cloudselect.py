import json
import logging
import os
import subprocess
from os.path import expanduser

import boto3


class CloudSelect:
    config = None
    configpath = os.path.join(
        os.environ.get("APPDATA")
        or os.environ.get("XDG_CONFIG_HOME")
        or os.path.join(expanduser("~"), ".config"),
        "cloudselect",
    )
    configfile = os.path.join(configpath, "cloudselect.json")
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.AWSelect")
        if not os.path.exists(self.configpath):
            os.mkdir(self.configpath)
        try:
            self.config = self.profile_read(self.configfile)
        except:
            print("Unable to read {}".format(self.configfile))

    def get_editor(self):
        if "editor" in self.config and self.config["editor"] is not None:
            return self.config["editor"]
        for key in "VISUAL", "EDITOR":
            rv = os.environ.get(key)
            if rv:
                return rv
        for editor in "vim", "nano":
            if os.system("which %s >/dev/null 2>&1" % editor) == 0:
                return editor
        return "vi"

    def edit(self, file):
        self.logger.debug("Edit '{}'".format(file))
        if not os.path.isfile(file):
            self.logger.info("{} does not exists".format(file))
        editor = self.get_editor()
        os.execvp(editor, [editor, file])

    def execute(self, program, args, **kwargs):
        """Executes a command in a subprocess and returns its standard output."""
        return (
            subprocess.run([program, *args], stdout=subprocess.PIPE, **kwargs)
            .stdout.decode()
            .strip()
        )

    def run(self, args):
        if args.edit is None or args.edit:
            if args.edit is None:
                self.edit(self.configfile)
            else:
                profile = os.path.join(
                    self.configpath, "{}.cloudselect.json".format(args.edit)
                )
                self.edit(profile)
        if not args.profile:
            self.profile_list()
        else:
            self.profile_process(args.profile, args)

    def profile_list(self):
        self.logger.debug("List all available profiles from {}".format(self.configpath))
        empty = True
        print("AWSelect profiles:")
        for file in os.listdir(self.configpath):
            if file.endswith(".cloudselect.json"):
                empty = False
                print("- {}".format(file.replace(".cloudselect.json", "")))
        if empty:
            print("- NO PROFILES -")

    def profile_process(self, profile_name, args):
        self.logger.debug("Process profile '{}'".format(profile_name))
        profile = os.path.join(
            self.configpath, "{}.cloudselect.json".format(profile_name)
        )
        if not os.path.isfile(profile):
            print("Profile {} does not exists".format(profile))
            self.logger.warn("Profile {} does not exists".format(profile))
            return False
        configuration = self.profile_read(profile)
        instances = self.instances_find(configuration)
        selected = self.instances_select(instances)
        selected = self.instances_enrich(configuration, selected)
        print(json.dumps(selected, sort_keys=True))

    def profile_read(self, profile):
        with open(profile, "r") as f:
            return json.load(f)

    def instances_enrich(self, profile, instances):
        def filter(filters):
            for filter in filters:
                if filter == "*":
                    return filters[filter]
                if filter in instance["InstanceId"]:
                    return filters[filter]
                if filter in self.instance_tag(instance, "Name"):
                    return filters[filter]
            return None

        for instance in instances:
            region = instance["Placement"]["AvailabilityZone"][:-1]
            profile_name = profile.get("profile_name")
            instance["cloudselect"] = {"profile": profile_name, "region": region}
            # delete unnecessary datetime elements
            instance.pop("BlockDeviceMappings", None)
            instance.pop("LaunchTime", None)
            instance.pop("NetworkInterfaces", None)
            # add secret keys
            self.logger.debug("Search for SSH key {}".format(instance["KeyName"]))
            instance["cloudselect"]["key"] = (
                self.config.get("key", {})
                .get(profile_name, {})
                .get(region, {})
                .get(instance["KeyName"])
                or self.config.get("key", {})
                .get(profile_name, {})
                .get(instance["KeyName"])
                or self.config.get("key", {}).get(region, {}).get(instance["KeyName"])
                or self.config.get("key", {}).get(instance["KeyName"])
            )
            # add user
            instance["cloudselect"]["user"] = filter(
                self.config.get("user", {}).get(profile_name, {}).get(region, {})
                or self.config.get("user", {}).get(profile_name, {})
                or self.config.get("user", {}).get(region, {})
                or self.config.get("user", {})
            )
            # add host
            ip = filter(
                self.config.get("ip", {}).get(profile_name, {}).get(region, {})
                or self.config.get("ip", {}).get(profile_name, {})
                or self.config.get("ip", {}).get(region, {})
                or self.config.get("ip", {})
            )
            if ip == "public":
                instance["cloudselect"]["host"] = instance["PublicIpAddress"]
            elif ip == "private":
                instance["cloudselect"]["host"] = instance["PrivateIpAddress"]
            elif ip == "public_private":
                instance["cloudselect"]["host"] = instance["PublicIpAddress"]
            elif ip == "private_public":
                instance["cloudselect"]["host"] = instance["PrivateIpAddress"]
            else:
                instance["cloudselect"]["host"] = instance["PublicIpAddress"]
        return instances

    def instances_find(self, profile):
        session = None
        if "profile_name" in profile and "region" in profile:
            session = boto3.Session(
                profile_name=profile["profile_name"], region=profile["region"]
            )
        elif "profile_name" in profile:
            session = boto3.Session(profile_name=profile["profile_name"])
        elif "region" in profile:
            session = boto3.Session(region=profile["region"])
        else:
            session = boto3.Session()
        ec2 = session.client("ec2")
        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )["Reservations"]
        return [
            item for sublist in [i["Instances"] for i in response] for item in sublist
        ]

    def instances_select(self, instances):
        def find(instance_id):
            return next(x for x in instances if x["InstanceId"] == instance_id)

        fzf_input = "\n".join(
            "\t".join(self.instance_filter(i)) for i in instances
        ).encode()
        selected = self.execute("fzf", ["-m"], input=fzf_input)
        return [find(i.split("\t", 1)[0]) for i in selected.split("\n")]

    def instance_filter(self, instance):
        result = []
        result.append(instance["InstanceId"])
        if self.config.get("ip") == "public":
            result.append(instance["PublicIpAddress"])
        elif self.config.get("ip") == "private":
            result.append(instance["PrivateIpAddress"])
        elif self.config.get("ip") == "public_private":
            result.append(instance["PublicIpAddress"])
        elif self.config.get("ip") == "private_public":
            result.append(instance["PrivateIpAddress"])
        else:
            result.append(instance["PublicIpAddress"])
        for i in self.config.get("instance_fields"):
            if i in instance:
                result.append(instance[i])
            elif i.startswith("tag:"):
                result.append(self.instance_tag(instance, i.replace("tag:", "")))
        return result

    def instance_tag(self, instance, tag):
        tags = instance["Tags"]
        return ",".join([i["Value"] for i in tags if i["Key"] == tag])
