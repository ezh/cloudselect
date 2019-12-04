# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.filter import FilterServiceProvider
from cloudselect.filter.stub import Stub

metadata = {"hello": "world"}


def test_stub_filter():
    cloud = CloudSelect()
    # Read shared part
    profile = cloud.read_configuration()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.filter().__class__.__name__ == "Stub"
    assert Container.filter().run("aws", metadata) is None
    assert Container.filter() == Container.filter()


def test_stub_behaviour(mocker):
    cloud = CloudSelect()
    service_provider = cloud.plugin("cloudselect.filter.stub", FilterServiceProvider)
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run("aws", metadata)
    Stub.run.assert_called_once_with("aws", metadata)
