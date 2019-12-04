# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import copy
import logging

import boto3

from cloudselect import Container, Instance

from . import DiscoveryService


class AWS(DiscoveryService):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.discovery.AWS")

    def run(self):
        return list(self.instances())

    def instances(self):
        pathfinder = Container.pathfinder()

        for i in self.find():
            id = i["InstanceId"]
            ip = self.get_ip(i)
            key = self.get_key(i)
            metadata = self.get_metadata(i)
            representation = [i["InstanceId"], ip]
            user = self.get_user(i)
            for field in self.config().get("fzf_extra", []):
                if field in i:
                    representation.append(i[field])
                elif field.startswith("tag:"):
                    representation.append(self.tag(i, field.replace("tag:", "")))
            instance = Instance(id, ip, key, user, 22, [], metadata, representation)
            yield pathfinder.run(instance)

    def config(self):
        return Container.config().get("discovery", {})

    def filter(self, filters, instance):
        for filter in filters:
            if filter == "*":
                return filters[filter]
            if filter in instance["InstanceId"]:
                return filters[filter]
            if filter in self.tag(instance, "Name"):
                return filters[filter]
        return None

    def find(self):
        config = Container.config.discovery
        session = None
        if config.profile_name() and config.region():
            session = boto3.Session(
                profile_name=config.profile_name(), region_name=config.region()
            )
        elif config.profile_name():
            session = boto3.Session(profile_name=config.profile_name())
        elif config.region():
            session = boto3.Session(region=config.region())
        else:
            session = boto3.Session()
        ec2 = session.client("ec2")
        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )["Reservations"]
        return [
            item for sublist in [i["Instances"] for i in response] for item in sublist
        ]

    def get_ip(self, instance):
        profile_name = Container.args().profile
        region = instance["Placement"]["AvailabilityZone"][:-1]

        ip = self.filter(
            self.config().get("ip", {}).get(profile_name, {}).get(region, {})
            or self.config().get("ip", {}).get(profile_name, {})
            or self.config().get("ip", {}).get(region, {})
            or self.config().get("ip", {}),
            instance,
        )
        if ip == "public":
            return instance.get("PublicIpAddress", "")
        elif ip == "private":
            return instance.get("PrivateIpAddress", "")
        elif ip == "public_private":
            return instance.get("PublicIpAddress", instance.get("PrivateIpAddress", ""))
        elif ip == "private_public":
            return instance.get("PrivateIpAddress", instance.get("PublicIpAddress", ""))
        else:
            return instance.get("PublicIpAddress", instance.get("PrivateIpAddress", ""))

    def get_key(self, instance):
        filter = Container.filter()
        profile_name = Container.config.discovery.profile_name()
        region = instance["Placement"]["AvailabilityZone"][:-1]

        self.logger.debug("Search for SSH key {}".format(instance["KeyName"]))
        return (
            filter.run("discovery", self.get_metadata(instance)).get("key")
            or self.config()
            .get("key", {})
            .get(profile_name, {})
            .get(region, {})
            .get(instance["KeyName"])
            or self.config()
            .get("key", {})
            .get(profile_name, {})
            .get(instance["KeyName"])
            or self.config().get("key", {}).get(region, {}).get(instance["KeyName"])
            or self.config().get("key", {}).get(instance["KeyName"])
        )

    def get_metadata(self, instance):
        profile_name = Container.config.discovery.profile_name()
        region = instance["Placement"]["AvailabilityZone"][:-1]

        metadata = copy.copy(instance)
        metadata["Tags"] = dict(
            [i.get("Key"), i.get("Value")] for i in metadata.get("Tags", [])
        )
        metadata["region"] = region
        metadata["profile"] = profile_name
        # delete unnecessary datetime elements
        metadata.pop("BlockDeviceMappings", None)
        metadata.pop("LaunchTime", None)
        metadata.pop("NetworkInterfaces", None)
        return metadata

    def get_user(self, instance):
        profile_name = Container.config.discovery.profile_name()
        region = instance["Placement"]["AvailabilityZone"][:-1]

        return self.filter(
            self.config().get("user", {}).get(profile_name, {}).get(region, {})
            or self.config().get("user", {}).get(profile_name, {})
            or self.config().get("user", {}).get(region, {})
            or self.config().get("user", {}),
            instance,
        )

    def tag(self, instance, tag):
        tags = instance.get("Tags", [])
        return ",".join([i["Value"] for i in tags if i["Key"] == tag])
