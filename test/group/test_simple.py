# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Simple group plugin."""
import json
import logging
import os

from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.group.simple import Simple


def test_options(cfgdir):
    """
    Test options behaviour of simple plugin.

    It should returns {} if there is no options.
    It should returns shared dictionary if there is no any matched filters.
    It should returns clarified dictionary if there is matched filter.
    """
    cloud = CloudSelect(cfgdir)
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["group"] = {"type": "simple"}
    cloud.fabric(configuration, args)

    assert isinstance(Container.group(), Simple)

    assert Container.options("test") == {}
    assert Container.options("plugin") == configuration["plugin"]
    assert Container.options("log") == configuration["log"]

    assert Container.options("option") == {}
    options_a = {"ssh": "-t", "ssh_command": "sudo -i"}
    options_b = {"ssh": "-t", "ssh_command": "su"}
    options_c = {"ssh": "-t", "ssh_command": None}
    configuration["option"] = options_a
    assert Container.options("option") == options_a

    configuration["group"]["options"] = [{"match": "x:y", "option": options_a}]
    assert Container.options("option") == options_a
    assert Container.options("option", {"a": {"b": "c123"}}) == options_a

    configuration["group"]["options"].append({"match": "a.b:c123", "option": options_b})
    assert Container.options("option") == options_a
    assert Container.options("option", {"a": {"b": "c123"}}) == options_b

    configuration["group"]["options"].append(
        {"match": "a.b:c(.*3|111)", "option": options_c},
    )
    assert Container.options("option") == options_a
    assert Container.options("option", {"a": {"b": "c1nnnn3"}}) == options_c
    assert Container.options("option", {"a": {"b": "c111111"}}) == options_c
    assert Container.options("option", {"a": {"b": "c112111"}}) == options_a


def test_options_errors(caplog, cfgdir):
    """Test error messages when options block is incorrect."""
    caplog.set_level(logging.INFO)
    configuration = os.path.join(
        os.path.dirname(__file__), "..", "fixture", "metadata.json",
    )

    logging.Logger.manager.loggerDict.clear()
    cloud = CloudSelect(cfgdir)
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["group"] = {"type": "simple"}
    cloud.fabric(configuration, args)
    assert isinstance(Container.group(), Simple)

    caplog.clear()
    Container.options("option")
    assert len(caplog.records) == 1
    assert (
        caplog.records[0].getMessage()
        == "option: 'options' block not found in {'type': 'simple'}"
    )

    caplog.clear()
    configuration["group"]["options"] = 123
    Container.options("option")
    assert len(caplog.records) == 1
    assert (
        caplog.records[0].msg
        == "%s: 'options' block should be list of dictionaries in %s"
    )


def test_options_regex(cfgdir):
    """Test regex against metadata mock."""
    metadata = os.path.join(os.path.dirname(__file__), "..", "fixture", "metadata.json")

    cloud = CloudSelect(cfgdir)
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["group"] = {
        "type": "simple",
        "options": [{"match": "Tags.Name:my-app.abc", "option": {}}],
    }
    configuration["option"] = {"ssh": "-t"}
    cloud.fabric(configuration, args)
    assert isinstance(Container.group(), Simple)

    with open(metadata) as json_file:
        data = json.load(json_file)
        assert Container.options("option") == {"ssh": "-t"}
        assert Container.options("option", data) == {}
