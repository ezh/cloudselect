# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module that represents list of selected instances as pretty print output."""
import json

from cloudselect import Container

from . import ReportService


class Json(ReportService):
    """Json reporter implementation."""

    def run(self, selected):
        """Represent instances as pretty print output."""
        # get first instance
        # assume that all instances match the same group/pattern
        instance = next(iter(selected), None)
        options = Container.options("option", instance)
        report = {"instances": [i.to_dict() for i in selected], "option": options}
        print(json.dumps(report, sort_keys=True))
