# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module defining Instance object."""
import attr


@attr.s
class Instance:
    """Base instance class."""

    instance_id = attr.ib()
    host = attr.ib()
    jumphost = attr.ib()
    metadata = attr.ib()
    representation = attr.ib()

    def to_dict(self):
        """Convert class to dictionary."""
        return {
            "id": self.instance_id,
            "host": self.host,
            "jumphost": self.jumphost.to_dict() if self.jumphost else None,
            "metadata": self.metadata,
        }


@attr.s
class CloudInstance(Instance):
    """Cloud instance class."""

    key = attr.ib()
    user = attr.ib()
    port = attr.ib()

    def to_dict(self):
        """Convert class to dictionary."""
        return {
            "id": self.instance_id,
            "host": self.host,
            "jumphost": self.jumphost.to_dict() if self.jumphost else None,
            "key": self.key,
            "port": self.port,
            "user": self.user,
            "metadata": self.metadata,
        }


@attr.s  # pylint: disable=too-many-instance-attributes
class PodContainer(Instance):
    """Kubernetes container class."""

    aws_profile = attr.ib()
    aws_region = attr.ib()
    configuration = attr.ib()
    container = attr.ib()
    context = attr.ib()
    ip = attr.ib()
    namespace = attr.ib()
    node_ip = attr.ib()

    def to_dict(self):
        """Convert class to dictionary."""
        return {
            "id": self.instance_id,
            "aws_profile": self.aws_profile,
            "aws_region": self.aws_region,
            "configuration": self.configuration,
            "container": self.container,
            "context": self.context,
            "host": self.host,
            "ip": self.ip,
            "jumphost": self.jumphost.to_dict() if self.jumphost else None,
            "metadata": self.metadata,
            "namespace": self.namespace,
            "node_ip": self.node_ip,
        }
