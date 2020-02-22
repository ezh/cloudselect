# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module that enrich instances with jumphosts."""
import logging

import attr

from cloudselect import CloudInstance, Container

from . import PathFinderService


class Bastion(PathFinderService):
    """Bastion implementation."""

    logger = None

    def __init__(self):
        """Class constructor."""
        self.logger = logging.getLogger("cloudselect.pathfinder.Bastion")

    def run(self, instance, instances):
        """Enrich instance with jumphost if any."""
        if not instance:
            raise ValueError("instance must be something, not None")
        arguments = Container.options("pathfinder", instance.metadata)
        if arguments:
            jumphost = None
            if "host" in arguments:
                jumphost = CloudInstance(
                    -1,
                    arguments["host"],
                    None,
                    {},
                    [],
                    arguments.get("key"),
                    arguments.get("user"),
                    arguments.get("port", 22),
                )
            elif "metadata" in arguments and ":" in arguments["metadata"]:
                key, pattern = arguments["metadata"].split(":", 1)
                for i in instances:
                    point = self.find_jumphost(key, pattern, i)
                    if point:
                        if point == instance:
                            break  # We don't like to add bastion for itself
                        jumphost = point
                        break
            if jumphost:
                return attr.evolve(instance, jumphost=jumphost)
        return instance

    def find_jumphost(self, metadata_key, value_pattern, instance):
        """Find jumphost among instances."""
        value = instance.metadata
        for key_part in metadata_key.split("."):
            try:
                value = value.get(key_part)
                if not value:
                    self.logger.debug("Unable to find metadata key %s", key_part)
                    break
            except Exception:
                self.logger.debug("Unable to find key %s", key_part)
                break
            if value_pattern in value:
                self.logger.debug("Match pattern %s and value %s", value_pattern, value)
                return instance
        return None
