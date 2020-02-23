# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module providing Discovery service base class and service provider."""
import collections.abc
import copy
from datetime import datetime

import dependency_injector.providers as providers

from cloudselect import Container


class DiscoveryService:
    """Base class for discovery service."""

    log = None

    @staticmethod
    def run():
        """Get list of instances."""
        return []

    @staticmethod
    def config():
        """Return discovery configuration."""
        return Container.config().get("discovery", {})

    def enrich_representation(self, representation, metadata):
        """Collect additional representation items from metadata."""
        for field in self.config().get("fzf_extra", []):
            if field in metadata:
                if isinstance(metadata[field], dict):
                    values = []
                    for dict_key in metadata[field]:
                        if metadata[field][dict_key]:
                            values.append(dict_key + ":" + metadata[field][dict_key])
                        else:
                            values.append(dict_key)
                    representation.append(",".join(values))
                elif isinstance(metadata[field], list):
                    representation.append(",".join(metadata[field]))
                else:
                    representation.append(str(metadata[field]))
            elif ":" in field:
                value = metadata
                path = field.split(":")
                for dict_key in path:
                    value = value.get(dict_key)
                    if not value:
                        self.log.debug(
                            "Unable to find key %s in %s", dict_key, metadata,
                        )
                        break
                representation.append(str(value))

    @staticmethod
    def simplify_metadata(m_dict):
        """Convert metadata keys to string."""
        metadata = copy.deepcopy(m_dict)

        def map_nested_dicts_modify(obj, func):
            """Apply function to object."""
            filtered = {k: v for k, v in obj.items() if v is not None}
            obj.clear()
            obj.update(filtered)
            for key, value in obj.items():
                if isinstance(value, collections.Mapping):
                    map_nested_dicts_modify(value, func)
                elif isinstance(value, list):
                    obj[key] = list(map(func, value))
                else:
                    obj[key] = func(value)

        def to_string(value):
            """Convert object to string."""
            if isinstance(value, collections.Mapping):
                map_nested_dicts_modify(value, to_string)
                return value
            if isinstance(value, datetime):
                return str(value)
            return value

        map_nested_dicts_modify(metadata, to_string)
        return metadata


class DiscoveryServiceProvider(providers.Singleton):
    """Service provider for discovery plugins."""

    provided_type = DiscoveryService
