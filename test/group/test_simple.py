# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Simple group plugin."""
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.group.simple import Simple


def test_options():
    """
    Test options behaviour for simple plugin.

    It should returns {} if there is no options.
    It should returns shared dictionary if there is no any matched filters.
    It should returns clarified dictionary if there is * filter.
    It should returns clarified dictionary if there is matched filter.
    """
    cloud = CloudSelect()
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    configuration["group"] = {"type": "simple"}
    cloud.fabric(configuration, args)

    assert type(Container.group()) == Simple

    assert Container.options("test") == {}
    assert Container.options("plugin") == configuration["plugin"]
    assert Container.options("log") == configuration["log"]

    assert Container.options("option") == {}
    options_a = {"ssh": "-t", "ssh_command": "sudo -i"}
    options_b = {"ssh": "-t", "ssh_command": "su"}
    options_c = {"ssh": "-t", "ssh_command": None}
    configuration["option"] = options_a
    assert Container.options("option") == options_a

    configuration["group"]["*"] = {"option": options_a}
    assert Container.options("option") == options_a
    assert Container.options("option", {"a": {"b": "c"}}) == options_a

    configuration["group"]["*"] = {"option": options_b}
    assert Container.options("option") == options_b
    assert Container.options("option", {"a": {"b": "c"}}) == options_b

    configuration["group"]["0 a.b:c"] = {"option": options_c}
    assert Container.options("option") == options_b
    assert Container.options("option", {"a": {"b": "c"}}) == options_c
    assert Container.options("option", {"a": {"b": "d"}}) == options_b
    assert (
        Container.options("option", {"a": {"b": "long string with c inside"}})
        == options_c
    )
