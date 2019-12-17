# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from shell output."""
import logging
import subprocess

from cloudselect import Container, Instance

from . import DiscoveryService


class Local(DiscoveryService):
    """Class implementing discovery service plugin."""

    logger = None

    def __init__(self):
        """Class constructor."""
        self.logger = logging.getLogger("cloudselect.discovery.Local")

    def run(self):
        """Collect instances from shell output."""
        self.logger.debug("Discover local instances")
        return list(self.instances())

    def instances(self):
        """Collect instances from shell output."""
        config = Container.config.discovery

        stdout = subprocess.check_output(config.cmd(), shell=True)  # noqa: DUO116
        output = sorted(
            filter(lambda item: item.strip() != "", stdout.decode().split("\n")),
            reverse=True,
        )
        for index, host in enumerate(output):
            host_id = str(index)
            ip = host
            key = self.get_key(host)
            metadata = {"host": host}
            representation = [host_id, host]
            user = self.get_user(host)
            instance = Instance(
                host_id, ip, key, user, None, None, metadata, representation,
            )
            yield instance

    def get_key(self, host):
        """Get key for ssh host."""
        self.logger.debug("Search SSH key for {}".format(host))
        config = Container.options("discovery", host)
        return (
            config.get("key")
            or config.get("key", {}).get(host)
            or config.get("key", {}).get("*")
        )

    def get_user(self, host):
        """Get user for SSH host."""
        self.logger.debug("Search user for {}".format(host))
        config = Container.options("discovery", host)
        return (
            config.get("user")
            or config.get("user", {}).get(host)
            or config.get("user", {}).get("*")
        )
