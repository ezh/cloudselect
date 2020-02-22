# Copyright 2019-2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Stub pathfinder plugin."""
from cloudselect import CloudInstance, Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.pathfinder.bastion import Bastion

INSTANCE = CloudInstance(1, "127.0.0.1", None, {}, [], "key", "user", 22)


def test_bastion_initialization(cfgdir):
    """Assert plugin initialization."""
    cloud = CloudSelect(cfgdir)
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["pathfinder"] = {"type": "bastion"}
    cloud.fabric(configuration, args)

    assert isinstance(Container.pathfinder(), Bastion)

    result = Container.pathfinder().run(INSTANCE, [INSTANCE])
    assert result.jumphost is None


def test_bastion_behaviour(cfgdir):
    """Assert bastion returning correct result."""
    cloud = CloudSelect(cfgdir)
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["pathfinder"] = {"type": "bastion", "host": "my-bastion-hostname"}
    cloud.fabric(configuration, args)

    assert isinstance(Container.pathfinder(), Bastion)

    result = Container.pathfinder().run(INSTANCE, [INSTANCE])

    assert isinstance(result.jumphost, CloudInstance)
    assert result.jumphost.host == "my-bastion-hostname"
    # assert result.jumphost is None
