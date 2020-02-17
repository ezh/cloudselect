# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module returning appropriate options per group of instances."""
import logging
import re

from . import GroupService


class Simple(GroupService):
    """Simple group implementation."""

    def __init__(self):
        """Class constructor."""
        self.default_priority = 1000
        self.logger = logging.getLogger("cloudselect.group.Simple")

    def run(self, name, metadata):
        """Return dictionary with options for the group of instances."""
        for group in self.config().get("options", []):
            self.logger.debug("Process group %s", group)
            entry = group.get("match")
            if not entry:
                self.logger.warning("Unable to find 'match' key in %s", group)
                continue
            if ":" not in entry:
                self.logger.warning(
                    "Unable to parse 'match' value %s for %s", entry, group,
                )
                continue
            key, pattern = entry.split(":", 1)
            regex = re.compile(pattern)
            value = metadata
            for key_part in key.split("."):
                try:
                    value = value.get(key_part)
                    if not value:
                        self.logger.debug("Unable to find key %s", key_part)
                        break
                except (AttributeError, NameError):
                    self.logger.debug("Unable to find key %s", key_part)
                    break
                if isinstance(value, str) and regex.match(value):
                    self.logger.debug(
                        "Match pattern %s and value %s", pattern, value,
                    )
                    result = group.get(name)
                    if result is not None:
                        return result
        return {}
