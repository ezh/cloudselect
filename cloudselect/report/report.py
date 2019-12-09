# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module providing Report service base class and service provider."""
import pprint

import dependency_injector.providers as providers


class ReportService(object):
    """Base class for reporting service."""

    @staticmethod
    def run(selected):
        """Prepare report based on list of selected instances."""
        pp = pprint.PrettyPrinter()
        pp.pprint(selected)
        return selected


class ReportServiceProvider(providers.Singleton):
    """Service provider for reporting plugins."""

    provided_type = ReportService
