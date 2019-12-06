# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import logging
import subprocess

from cloudselect import Container, Instance

from . import DiscoveryService


class Local(DiscoveryService):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.discovery.Local")

    def run(self):
        logging.debug("Discover local instances")
        return list(self.instances())

    def instances(self):
        pathfinder = Container.pathfinder()
        config = Container.config.discovery

        stdout = subprocess.check_output(config.cmd(), shell=True)
        output = sorted(
            filter(lambda item: item.strip() != "", stdout.decode().split("\n")),
            reverse=True,
        )
        for index, host in enumerate(output):
            id = str(index)
            ip = host
            key = self.get_key(host)
            metadata = {"host": host}
            representation = [id, host]
            user = self.get_user(host)
            instance = Instance(id, ip, key, user, None, [], metadata, representation)
            yield pathfinder.run(instance)

    def config(self):
        return Container.config().get("discovery", {})

    def get_key(self, host):
        self.logger.debug("Search SSH key for {}".format(host))
        config = Container.options("discovery", host)
        return (
            config.get("key")
            or config.get("key", {}).get(host)
            or config.get("key", {}).get("*")
        )

    def get_user(self, host):
        self.logger.debug("Search user for {}".format(host))
        config = Container.options("discovery", host)
        return (
            config.get("user")
            or config.get("user", {}).get(host)
            or config.get("user", {}).get("*")
        )
