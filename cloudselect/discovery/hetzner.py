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

from cloudselect import Container, Instance

from . import DiscoveryService


class Hetzner(DiscoveryService):
    """Class implementing discovery service plugin."""

    logger = None

    def __init__(self):
        """Class constructor."""
        self.logger = logging.getLogger("cloudselect.discovery.AWS")

    def run(self):
        """Collect AWS instances."""
        self.logger.debug("Discover AWS instances")
        return list(self.instances())

    def instances(self):
        """Collect AWS instances."""
        for i in self.find():
            instance_id = i["id"]
            metadata = i
            config = Container.options("discovery", metadata)
            ip = self.get_ip(i, config)
            key = self.get_key(i, config)
            port = self.get_port(i, config)
            user = self.get_user(i, config)

            representation = [instance_id, ip]
            for field in self.config().get("fzf_extra", []):
                if field in i:
                    if isinstance(i[field], dict):
                        values = []
                        for dict_key in i[field]:
                            if i[field][dict_key]:
                                values.append(dict_key + ":" + i[field][dict_key])
                            else:
                                values.append(dict_key)
                        representation.append(",".join(values))
                    elif isinstance(i[field], list):
                        representation.append(",".join(i[field]))
                    else:
                        representation.append(str(i[field]))
                elif ":" in field:
                    value = metadata
                    path = field.split(":")
                    for dict_key in path:
                        value = value.get(dict_key)
                        if not value:
                            self.logger.debug(
                                "Unable to find key %s in %s", dict_key, metadata,
                            )
                            break
                    representation.append(str(value))

            instance = Instance(
                instance_id, ip, key, user, port, None, metadata, representation,
            )
            yield instance

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
    def get_ip(instance, config):
        """Get instance IP."""
        return instance["public_net"]["ipv4"].get("ip", "")

    @staticmethod
    def get_key(instance, config):
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
    def get_port(instance, config):
        """Get instance port."""
        return config.get("port")

    @staticmethod
    def get_user(instance, config):
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
