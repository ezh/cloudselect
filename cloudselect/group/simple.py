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
        self.log = logging.getLogger("cloudselect.group.Simple")

    def run(self, name, metadata):
        """Return dictionary with options for the group of instances."""
        options = self.config().get("options")
        if not options:
            self.log.warning("%s: 'options' block not found in %s", name, self.config())
            return None
        if not isinstance(options, list):
            self.log.warning(
                "%s: 'options' block should be list of dictionaries in %s",
                name,
                self.config(),
            )
            return None
        for group in self.config().get("options", []):
            try:
                self.log.debug("%s: Process group %s", name, group)
                entry = group.get("match")
                if not entry:
                    self.log.warning(
                        "%s: Unable to find 'match' key in %s", name, group,
                    )
                    continue
                if ":" not in entry:
                    self.log.warning(
                        "%s: Unable to parse 'match' value %s for %s",
                        name,
                        entry,
                        group,
                    )
                    continue
                key, pattern = entry.split(":", 1)
                regex = re.compile(pattern)
                value = metadata
                for key_part in key.split("."):
                    try:
                        value = value.get(key_part)
                        if value is None:
                            self.log.debug("%s: Unable to find key %s", name, key_part)
                            break
                    except (AttributeError, NameError):
                        self.log.debug("%s: Unable to find key %s", name, key_part)
                        break
                    if isinstance(value, str) and regex.match(value) is not None:
                        self.log.debug(
                            "%s: Pattern %s and value %s is matched",
                            name,
                            pattern,
                            value,
                        )
                        result = group.get(name)
                        if result is not None:
                            return result
            except AttributeError:
                self.log.warning("%s: Unable to find 'match' key in %s", name, group)
        return None
