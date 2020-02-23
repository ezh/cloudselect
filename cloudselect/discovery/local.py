# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from shell output."""
import logging
import subprocess

from cloudselect import CloudInstance, Container

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
        instances = list(self.instances())
        representation = instances[-1]
        del instances[-1]
        return (representation, instances)

    def instances(self):
        """Collect instances from shell output."""
        config = Container.config.discovery

        # Array with maximum field length for each element in representation
        fields_length = []
        stdout = subprocess.check_output(config.cmd(), shell=True)  # noqa: DUO116
        output = sorted(
            filter(lambda item: item.strip() != "", stdout.decode().split("\n")),
            reverse=True,
        )
        for index, host in enumerate(output):
            host_id = str(index)
            metadata = {"host": host}

            representation = [host_id, host]
            self.enrich_representation(representation, metadata)

            # Update maximum field length
            for idx, value in enumerate(representation):
                if idx >= len(fields_length):
                    fields_length.append(len(value))
                else:
                    fields_length[idx] = max(fields_length[idx], len(value))

            yield CloudInstance(
                host_id,
                host,
                None,
                metadata,
                representation,
                self.get_key(host),
                self.get_user(host),
                None,
            )
        yield fields_length

    def get_key(self, host):
        """Get key for ssh host."""
        self.logger.debug("Search SSH key for %s", host)
        config = Container.options("discovery", host)
        return (
            config.get("key")
            or config.get("key", {}).get(host)
            or config.get("key", {}).get("*")
        )

    def get_user(self, host):
        """Get user for SSH host."""
        self.logger.debug("Search user for %s", host)
        config = Container.options("discovery", host)
        return (
            config.get("user")
            or config.get("user", {}).get(host)
            or config.get("user", {}).get("*")
        )
