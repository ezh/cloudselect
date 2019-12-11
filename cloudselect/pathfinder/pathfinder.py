# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module providing PathFinder service base class and service provider."""
import dependency_injector.providers as providers

from cloudselect import Container


class PathFinderService(object):
    """Base class for pathfinder service."""

    @staticmethod
    def run(instance, instances):
        """Enrich instance object with jump hosts."""
        return instance

    @staticmethod
    def config():
        """Return pathfinder configuration."""
        return Container.config().get("pathfinder", {})


class PathFinderServiceProvider(providers.Singleton):
    """Service provider for pathfinder plugins."""

    provided_type = PathFinderService
