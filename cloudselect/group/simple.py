# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import logging

from . import GroupService


class Simple(GroupService):
    default_priority = 1000
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.group.Simple")

    def run(self, name, metadata):
        groups_by_priority = list(self.get_groups_with_priority(self.config()))

        for priority, filters, group in sorted(groups_by_priority, key=lambda x: x[0]):
            self.logger.debug("Process group {} {}".format(priority, filters))
            for filter in filters:
                if filter == "*":
                    result = group.get(name)
                    if result:
                        return result
                elif ":" in filter:
                    key, pattern = filter.split(":", 1)
                    value = metadata
                    for key_part in key.split("."):
                        try:
                            value = value.get(key_part)
                            if not value:
                                self.logger.debug(
                                    "Unable to find key {}".format(key_part)
                                )
                                break
                        except Exception:
                            self.logger.debug("Unable to find key {}".format(key_part))
                            break
                        if pattern in value:
                            self.logger.debug(
                                "Match pattern {} and value {}".format(pattern, value)
                            )
                            result = group.get(name)
                            if result:
                                return result
                else:
                    self.logger.warning(
                        "Unable to find filter definition for {}".format(group)
                    )
        return {}

    def get_groups_with_priority(self, groups):
        for pattern in groups:
            group = groups[pattern]
            if not isinstance(group, dict):
                logging.debug("Skip group with pattern {}".format(pattern))
                continue
            filters = pattern.split(" ", 1)
            priority = self.default_priority
            if len(filters) == 2 and filters[0].isdigit():
                priority = int(filters[0])
                filters = filters[-1].split(",")
            else:
                filters = pattern
            yield [priority, filters, group]
