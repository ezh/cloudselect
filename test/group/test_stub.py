# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Stub group plugin."""
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.group import GroupServiceProvider
from cloudselect.group.stub import Stub

metadata = {"hello": "world"}


def test_stub_group():
    """
    Testing Stub initializaion.

    Is fabric creating Stub by default?
    Does Stub return {}?
    Is Stub singleton?
    """
    cloud = CloudSelect()
    # Read shared part
    profile = cloud.configuration_read()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.group().__class__.__name__ == "Stub"
    assert Container.group().run("aws", metadata) == {}
    assert Container.group() == Container.group()


def test_stub_behaviour(mocker):
    """Assert calling run() for "cloudselect.group.stub" plugin."""
    cloud = CloudSelect()
    service_provider = cloud.plugin("cloudselect.group.stub", GroupServiceProvider)
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run("aws", metadata)
    Stub.run.assert_called_once_with("aws", metadata)
