# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import logging

from . import FilterService


class Simple(FilterService):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("cloudselect.filter.Simple")

    def run(self, service, metadata):
        for group in self.config().get("group", []):
            filter = group.get("filter")
            if filter:
                if filter == "*":
                    result = group.get(service)
                    if result:
                        return result
                elif ":" in filter:
                    key, pattern = filter.split(":")
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
                        arguments = group.get(service)
                        if arguments:
                            return arguments
            else:
                self.logger.warning(
                    "Unable to find filter definition for {}".format(group)
                )
        return {}
