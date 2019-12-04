# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
from cloudselect import Container, Instance
from cloudselect.cloudselect import CloudSelect
from cloudselect.pathfinder import PathFinderServiceProvider
from cloudselect.pathfinder.stub import Stub

instance = Instance(1, "127.0.0.1", "key", "user", 22, [], {}, [])


def test_stub_pathfinder():
    cloud = CloudSelect()
    # Read shared part
    profile = cloud.read_configuration()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.pathfinder().__class__.__name__ == "Stub"
    assert Container.pathfinder().run(instance) == instance
    assert Container.pathfinder() == Container.pathfinder()


def test_stub_behaviour(mocker):
    cloud = CloudSelect()
    service_provider = cloud.plugin(
        "cloudselect.pathfinder.stub", PathFinderServiceProvider
    )
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run(instance)
    Stub.run.assert_called_once_with(instance)
