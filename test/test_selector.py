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
from cloudselect.cloudselect import CloudSelect, Selector
from cloudselect.discovery.local import Local


def test_completer(capsys):
    """Testing that Selector completer process .cloud.json .cloud.yml and .cloud.yaml profiles."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args([])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    selector.complete("", 0)
    captured = capsys.readouterr()
    assert captured.out == "a\nb\nc\nempty\nsingle\n"
    assert captured.err == ""


def test_profile_list(capsys):
    """Testing that Selector profile_list process .cloud.json .cloud.yml and .cloud.yaml profiles."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args([])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    selector.profile_list()
    captured = capsys.readouterr()
    assert captured.out == "CloudSelect profiles:\n- a\n- b\n- c\n- empty\n- single\n"
    assert captured.err == ""


def test_select_edit(mocker):
    """Testing that Selector invoking edit for base configuration properly."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args(["-e"])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    mocker.patch.object(Selector, "edit")
    selector.select()
    Selector.edit.assert_called_once_with(  # pylint: disable=no-member
        os.path.join(os.path.dirname(__file__), "fixture", "cloud.json"),
    )


def test_select_edit_json_profile(mocker):
    """Testing that Selector invoking edit for JSON profile properly."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args(["-e", "a"])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    mocker.patch.object(Selector, "edit")
    selector.select()
    Selector.edit.assert_called_once_with(  # pylint: disable=no-member
        os.path.join(os.path.dirname(__file__), "fixture", "a.cloud.json"),
    )


def test_select_edit_yaml_profile(mocker):
    """Testing that Selector invoking edit for YAML profile properly."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args(["-e", "b"])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    mocker.patch.object(Selector, "edit")
    selector.select()
    Selector.edit.assert_called_once_with(  # pylint: disable=no-member
        os.path.join(os.path.dirname(__file__), "fixture", "b.cloud.yaml"),
    )


def test_select_edit_yml_profile(mocker):
    """Testing that Selector invoking edit for YML profile properly."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args(["-e", "c"])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    mocker.patch.object(Selector, "edit")
    selector.select()
    Selector.edit.assert_called_once_with(  # pylint: disable=no-member
        os.path.join(os.path.dirname(__file__), "fixture", "c.cloud.yml"),
    )


def test_select_edit_non_existent_profile(mocker, capsys):
    """Testing that Selector shows error on if profile doesn't exist."""
    cloud = CloudSelect(os.path.join(os.path.dirname(__file__), "fixture"))
    args = cloud.parse_args(["-v", "-e", "non-existent"])
    configuration = cloud.configuration_read()
    selector = cloud.fabric(configuration, args)
    mocker.patch.object(Selector, "edit")
    selector.logger.disabled = False
    selector.select()
    Selector.edit.assert_not_called()  # pylint: disable=no-member
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.endswith("Profile 'non-existent' does not exist\n")


def test_select_empty(tmpdir):
    """Testing that Selector exits if there is no any instances."""
    profile = os.path.join(os.path.dirname(__file__), "fixture", "empty.cloud.json")
    cloud = CloudSelect(tmpdir)
    args = cloud.parse_args([profile])
    configuration = cloud.configuration_read()
    configuration = cloud.merge(configuration, cloud.configuration_read(args.profile))
    assert args.profile == profile
    selector = cloud.fabric(configuration, args)
    assert isinstance(Container.discovery(), Local)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        selector.select()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "Error: No instances found"


def test_select_single(tmpdir):
    """Testing that Selector automaticaly select the only one available instance."""
    profile = os.path.join(os.path.dirname(__file__), "fixture", "single.cloud.json")
    cloud = CloudSelect(tmpdir)
    args = cloud.parse_args([profile])
    configuration = cloud.configuration_read()
    configuration = cloud.merge(configuration, cloud.configuration_read(args.profile))
    assert args.profile == profile
    selector = cloud.fabric(configuration, args)
    assert isinstance(Container.discovery(), Local)
    report = selector.select()
    assert len(report) == 1
    assert report[0].host == "my.cloud.instance"
