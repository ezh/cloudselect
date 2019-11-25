# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
import json

from cloudselect import Container

from . import ReportService


class Json(ReportService):
    def run(self, selected):
        report = dict(instances=selected, options=Container.config.option())
        print(json.dumps(report, sort_keys=True))
