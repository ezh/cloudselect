# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module providing Discovery service base class and service provider."""
import dependency_injector.providers as providers

from cloudselect import Container


class DiscoveryService(object):
    """Base class for discovery service."""

    @staticmethod
    def run():
        """Get list of instances."""
        return []

    @staticmethod
    def config():
        """Return discovery configuration."""
        return Container.config().get("discovery", {})


class DiscoveryServiceProvider(providers.Singleton):
    """Service provider for discovery plugins."""

    provided_type = DiscoveryService
