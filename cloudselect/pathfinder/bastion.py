# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module that enrich instances with jumphosts."""
import logging

from cloudselect import Container, Instance

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
                jumphost = Instance(
                    -1,
                    arguments["host"],
                    arguments.get("key"),
                    arguments.get("user"),
                    arguments.get("port", 22),
                    None,
                    {},
                    [],
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
                return Instance(
                    instance.id,
                    instance.host,
                    instance.key,
                    instance.user,
                    instance.port,
                    jumphost,
                    instance.metadata,
                    instance.representation,
                )
        return instance

    def find_jumphost(self, metadata_key, value_pattern, instance):
        """Find jumphost among instances."""
        value = instance.metadata
        for key_part in metadata_key.split("."):
            try:
                value = value.get(key_part)
                if not value:
                    self.logger.debug(
                        "Unable to find metadata key {}".format(key_part),
                    )
                    break
            except Exception:
                self.logger.debug("Unable to find key {}".format(key_part))
                break
            if value_pattern in value:
                self.logger.debug(
                    "Match pattern {} and value {}".format(value_pattern, value),
                )
                return instance
        return None
