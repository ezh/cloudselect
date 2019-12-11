# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module defining Instance object."""
from collections import namedtuple


class Instance(
    namedtuple(
        "Instance",
        ["id", "host", "key", "user", "port", "jumphost", "metadata", "representation"],
    ),
):
    """Instance class based on namedtuple implementation."""

    def to_dict(self):
        """Convert namedtuple to dictionary."""
        return {
            "host": self.host,
            "key": self.key,
            "user": self.user,
            "port": self.port,
            "jumphost": self.jumphost.to_dict() if self.jumphost else None,
            "metadata": self.metadata,
        }
