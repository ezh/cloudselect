# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module providing Group service base class and service provider."""
import dependency_injector.providers as providers

from cloudselect import Container


class GroupService(object):
    """Base class for group service."""

    @staticmethod
    def run(name, metadata):
        """Get options for name regard with metadata."""
        return {}

    @staticmethod
    def config():
        """Return group configuration."""
        return Container.config().get("group", {})


class GroupServiceProvider(providers.Singleton):
    """Service provider for group plugins."""

    provided_type = GroupService
