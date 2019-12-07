# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Selector class."""
import os

import pytest

from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery.local import Local


def test_select_empty():
    """Testing that Selector exits if there is no any instances."""
    profile = os.path.join(os.path.dirname(__file__), "fixture", "empty.cloud.json")
    cloud = CloudSelect()
    args = cloud.parse_args([profile])
    configuration = cloud.configuration_read()
    configuration = cloud.merge(configuration, cloud.configuration_read(args.profile))
    assert args.profile == profile
    selector = cloud.fabric(configuration, args)
    assert type(Container.discovery()) == Local
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        selector.select()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "Error: No instances found"


def test_select_single():
    """Testing that Selector automaticaly select the only one available instance."""
    profile = os.path.join(os.path.dirname(__file__), "fixture", "single.cloud.json")
    cloud = CloudSelect()
    args = cloud.parse_args([profile])
    configuration = cloud.configuration_read()
    configuration = cloud.merge(configuration, cloud.configuration_read(args.profile))
    assert args.profile == profile
    selector = cloud.fabric(configuration, args)
    assert type(Container.discovery()) == Local
    report = selector.select()
    assert len(report) == 1
    assert report[0].host == "my.cloud.instance"
