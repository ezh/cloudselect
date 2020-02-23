# Copyright 2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from Hetzner cloud."""
import logging

from hcloud import Client
from hcloud.datacenters.domain import Datacenter
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.servers.domain import IPv4Address, IPv6Network

from cloudselect import CloudInstance, Container

from . import DiscoveryService


class Hetzner(DiscoveryService):
    """Class implementing discovery service plugin."""

    log = None

    def __init__(self):
        """Class constructor."""
        self.log = logging.getLogger("cloudselect.discovery.Hetzner")

    def run(self):
        """Collect Hetzner instances."""
        self.log.debug("Discover Hetzner instances")
        instances = list(self.instances())
        representation = instances[-1]
        del instances[-1]
        return (representation, instances)

    def instances(self):
        """Collect Hetzner instances."""
        # Array with maximum field length for each element in representation
        fields_length = []
        for i in self.find():
            instance_id = i["id"]
            metadata = i
            config = Container.options("discovery", metadata)
            ip = self.get_ip(i)
            key = self.get_key(config)
            port = self.get_port(config)
            user = self.get_user(config)

            representation = [instance_id, ip]
            self.enrich_representation(representation, metadata)

            # Update maximum field length
            for idx, value in enumerate(representation):
                if idx >= len(fields_length):
                    fields_length.append(len(value))
                else:
                    fields_length[idx] = max(fields_length[idx], len(value))

            instance = CloudInstance(
                instance_id, ip, None, metadata, representation, key, user, port,
            )
            yield instance
        yield fields_length

    @staticmethod
    def find():
        """Discover instances in Hetzner cloud."""
        config = Container.config.discovery
        client = Client(token=config.token())
        servers = client.servers.get_all(status="running")
        for server in servers:
            yield {
                "created": str(server.data_model.created),
                "datacenter": Hetzner.get_model_data(
                    Datacenter, server.data_model.datacenter.data_model,
                ),
                "id": str(server.data_model.id),
                "included_traffic": server.data_model.included_traffic,
                "ingoing_traffic": server.data_model.ingoing_traffic,
                "image": Hetzner.get_model_data(
                    Image, server.data_model.image.data_model,
                ),
                "labels": server.data_model.labels,
                "locked": server.data_model.locked,
                "name": server.data_model.name,
                "outgoing_traffic": server.data_model.outgoing_traffic,
                "private_net": server.data_model.private_net,
                "protection": server.data_model.protection,
                "public_net": {
                    "floating_ips": server.data_model.public_net.floating_ips,
                    "ipv4": Hetzner.get_model_data(
                        IPv4Address, server.data_model.public_net.ipv4,
                    ),
                    "ipv6": Hetzner.get_model_data(
                        IPv6Network, server.data_model.public_net.ipv6,
                    ),
                },
                "rescue_enabled": server.data_model.rescue_enabled,
                "server_type": Hetzner.get_model_data(
                    ServerType, server.data_model.server_type.data_model,
                ),
                "status": server.data_model.status,
            }

    @staticmethod
    def get_ip(instance):
        """Get instance IP."""
        return instance["public_net"]["ipv4"].get("ip", "")

    @staticmethod
    def get_key(config):
        """Get instance key."""
        return config.get("key")

    @staticmethod
    def get_model_data(model_type, model_object):
        """Get all data attributes from a model."""
        raw = (
            (name, getattr(model_object, name))
            for name in dir(model_type)
            if not name.startswith("__")
        )
        return dict(Hetzner.process(raw))

    @staticmethod
    def get_port(config):
        """Get instance port."""
        return config.get("port")

    @staticmethod
    def get_user(config):
        """Get instance user."""
        return config.get("user")

    @staticmethod
    def process(items):
        """Return only meaningful fields from item sequence."""
        for (name, value) in items:
            if isinstance(value, str):
                yield (name, value)
            if isinstance(value, int):
                yield (name, value)
            if isinstance(value, dict):
                yield (name, value)
            if isinstance(value, list):
                yield (name, value)
