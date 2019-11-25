# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
from . import FilterService


class Simple(FilterService):
    def run(self, dictionary):
        for filter in dictionary:
            if filter == "*":
                return dictionary[filter]
        return None
