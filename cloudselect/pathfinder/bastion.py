# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
from cloudselect import Container, Instance

from . import PathFinderService


class Bastion(PathFinderService):
    def run(self, instance):
        arguments = Container.options("pathfinder", instance.metadata)
        if arguments:
            jumphost = {}
            if "host" in arguments:
                jumphost["host"] = arguments["host"]
            if jumphost:
                return Instance(
                    instance.id,
                    instance.host,
                    instance.key,
                    instance.user,
                    instance.port,
                    [jumphost],
                    instance.metadata,
                    instance.representation,
                )
        return instance
