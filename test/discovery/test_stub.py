# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Stub discovery plugin."""
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery import DiscoveryServiceProvider
from cloudselect.discovery.stub import Stub


def test_stub_discovery():
    """
    Testing Stub initializaion.

    Is fabric creating Stub by default?
    Does Stub return []?
    Is Stub singleton?
    """
    cloud = CloudSelect()
    # Read shared part
    profile = cloud.configuration_read()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.discovery().__class__.__name__ == "Stub"
    assert Container.discovery().run() == []
    assert Container.discovery() == Container.discovery()


def test_stub_behaviour(mocker):
    """Assert calling run() for "cloudselect.discovery.stub" plugin."""
    cloud = CloudSelect()
    service_provider = cloud.plugin(
        "cloudselect.discovery.stub", DiscoveryServiceProvider,
    )
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run()
    Stub.run.assert_called_once_with()
