# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from AWS cloud."""
import copy
import logging

import boto3

from cloudselect import CloudInstance, Container

from . import DiscoveryService


class AWS(DiscoveryService):
    """Class implementing discovery service plugin."""

    log = None

    def __init__(self):
        """Class constructor."""
        self.log = logging.getLogger("cloudselect.discovery.AWS")

    def run(self):
        """Collect AWS instances."""
        self.log.debug("Discover AWS instances")
        instances = list(self.instances())
        representation = instances[-1]
        del instances[-1]
        return (representation, instances)

    def instances(self):
        """Collect AWS instances."""
        # Array with maximum field length for each element in representation
        fields_length = []
        for i in self.find():
            instance_id = i["InstanceId"]
            metadata = self.get_metadata(i)
            config = Container.options("discovery", metadata)

            ip = self.get_ip(i, config)
            key = self.get_key(i, config)
            user = self.get_user(i, config)

            representation = [instance_id, ip]
            self.enrich_representation(representation, metadata)

            # Update maximum field length
            for idx, value in enumerate(representation):
                if idx >= len(fields_length):
                    fields_length.append(len(value))
                else:
                    fields_length[idx] = max(fields_length[idx], len(value))

            instance = CloudInstance(
                instance_id, ip, None, metadata, representation, key, user, 22,
            )
            yield instance
        yield fields_length

    @staticmethod
    def find():
        """Discover instances in AWS cloud."""
        config = Container.config.discovery
        session = None
        if config.profile_name() and config.region():
            session = boto3.Session(
                profile_name=config.profile_name(), region_name=config.region(),
            )
        elif config.profile_name():
            session = boto3.Session(profile_name=config.profile_name())
        elif config.region():
            session = boto3.Session(region_name=config.region())
        else:
            session = boto3.Session()
        ec2 = session.client("ec2")
        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}],
        )["Reservations"]
        return [
            item for sublist in [i["Instances"] for i in response] for item in sublist
        ]

    @staticmethod
    def get_option(options, option_name, profile, region):
        """Get an option from more precise to more general."""
        # value
        result = options
        if isinstance(result, str):
            return result
        # profile:region:option_name
        result = options.get(profile, {}).get(region, {})
        if isinstance(result, dict):
            result = result.get(option_name)
        if isinstance(result, str):
            return result
        # profile:option_name
        result = options.get(profile, {})
        if isinstance(result, dict):
            result = result.get(option_name)
        if isinstance(result, str):
            return result
        # region:key_name
        result = options.get(region, {})
        if isinstance(result, dict):
            result = result.get(option_name)
        if isinstance(result, str):
            return result
        # key_name
        result = options
        if isinstance(result, dict):
            result = result.get(option_name)
        return None

    def get_ip(self, instance, config):
        """Get instance IP."""
        profile_name = Container.args().profile
        region = instance["Placement"]["AvailabilityZone"][:-1]

        ip = self.get_option(config.get("ip", {}), None, profile_name, region)
        if ip == "public":
            return instance.get("PublicIpAddress", "")
        if ip == "private":
            return instance.get("PrivateIpAddress", "")
        if ip == "public_private":
            return instance.get("PublicIpAddress", instance.get("PrivateIpAddress", ""))
        if ip == "private_public":
            return instance.get("PrivateIpAddress", instance.get("PublicIpAddress", ""))

        return instance.get("PublicIpAddress", instance.get("PrivateIpAddress", ""))

    def get_key(self, instance, config):
        """Get instance key."""
        profile_name = Container.config.discovery.profile_name()
        region = instance["Placement"]["AvailabilityZone"][:-1]

        self.log.debug("Search for SSH key %s", instance["KeyName"])
        return self.get_option(
            config.get("key", {}), instance["KeyName"], profile_name, region,
        )

    @staticmethod
    def get_metadata(instance):
        """Get instance metadata."""
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

    def get_user(self, instance, config):
        """Get instance user."""
        profile_name = Container.config.discovery.profile_name()
        region = instance["Placement"]["AvailabilityZone"][:-1]

        return self.get_option(config.get("user", {}), None, profile_name, region)

    @staticmethod
    def tag(instance, tag):
        """Flatten instance tags."""
        tags = instance.get("Tags", [])
        return ",".join([i["Value"] for i in tags if i["Key"] == tag])
