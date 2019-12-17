# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Stub pathfinder plugin."""
from cloudselect import Container, Instance
from cloudselect.cloudselect import CloudSelect
from cloudselect.pathfinder.bastion import Bastion

instance = Instance(1, "127.0.0.1", "key", "user", 22, None, {}, [])


def test_bastion_initialization(mocker):
    """Assert plugin initialization."""
    cloud = CloudSelect()
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["pathfinder"] = {"type": "bastion"}
    cloud.fabric(configuration, args)

    assert type(Container.pathfinder()) == Bastion

    result = Container.pathfinder().run(instance, [instance])
    assert result.jumphost is None


def test_bastion_behaviour(mocker):
    """Assert bastion returning correct result."""
    cloud = CloudSelect()
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["pathfinder"] = {"type": "bastion", "host": "my-bastion-hostname"}
    cloud.fabric(configuration, args)

    assert type(Container.pathfinder()) == Bastion

    result = Container.pathfinder().run(instance, [instance])

    assert type(result.jumphost) == Instance
    assert result.jumphost.host == "my-bastion-hostname"
    # assert result.jumphost is None
