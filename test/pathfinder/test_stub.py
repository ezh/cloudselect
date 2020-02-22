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
from cloudselect.pathfinder import PathFinderServiceProvider
from cloudselect.pathfinder.stub import Stub

INSTANCE = CloudInstance(1, "127.0.0.1", "key", "user", 22, [], {}, [])


def test_stub_pathfinder(cfgdir):
    """
    Testing Stub initializaion.

    Is fabric creating Stub by default?
    Does Stub return {}?
    Is Stub singleton?
    """
    cloud = CloudSelect(cfgdir)
    # Read shared part
    profile = cloud.configuration_read()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.pathfinder().__class__.__name__ == "Stub"
    assert Container.pathfinder().run(INSTANCE, [INSTANCE]) == INSTANCE
    assert Container.pathfinder() == Container.pathfinder()


def test_stub_behaviour(mocker, cfgdir):
    """Assert calling run() for "cloudselect.pathfinder.stub" plugin."""
    cloud = CloudSelect(cfgdir)
    service_provider = cloud.plugin(
        "cloudselect.pathfinder.stub", PathFinderServiceProvider,
    )
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run(INSTANCE, [INSTANCE])
    Stub.run.assert_called_once_with(INSTANCE, [INSTANCE])
