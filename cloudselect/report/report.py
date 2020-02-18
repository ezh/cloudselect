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

from cloudselect import Container


class ReportService:  # pylint: disable=too-few-public-methods
    """Base class for reporting service."""

    @staticmethod
    def run(selected):
        """Prepare report based on list of selected instances."""
        pp = pprint.PrettyPrinter()
        options = ReportService.get_option(selected)
        report = {"instances": [i.to_dict() for i in selected], "option": options}
        pp.pprint(report)
        return report

    @staticmethod
    def get_option(selected):
        """Get option block for report."""
        # get first instance
        # assume that all instances match the same group/pattern
        instance = next(iter(selected), None)
        if instance:
            return Container.options("option", instance.metadata)
        return Container.options("option")


class ReportServiceProvider(providers.Singleton):
    """Service provider for reporting plugins."""

    provided_type = ReportService
