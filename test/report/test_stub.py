# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Stub report plugin."""
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.report import ReportServiceProvider
from cloudselect.report.stub import Stub


def test_stub_report(cfgdir):
    """
    Testing Stub initializaion.

    Is fabric creating Stub by default?
    Does Stub return []?
    Is Stub singleton?
    """
    cloud = CloudSelect(cfgdir)
    # Read shared part
    profile = cloud.configuration_read()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.report().__class__.__name__ == "Stub"
    assert Container.report().run([]) == {"instances": [], "option": {}}
    assert Container.report() == Container.report()


def test_stub_behaviour(mocker, cfgdir):
    """Assert calling run() for "cloudselect.report.stub" plugin."""
    cloud = CloudSelect(cfgdir)
    service_provider = cloud.plugin("cloudselect.report.stub", ReportServiceProvider)
    stub = service_provider()
    mocker.patch.object(Stub, "run")
    stub.run([])
    Stub.run.assert_called_once_with([])
