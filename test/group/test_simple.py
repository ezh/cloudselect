# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.group.simple import Simple


def test_options():
    cloud = CloudSelect()
    configuration = cloud.read_configuration()
    args = cloud.parse_args([])
    configuration["group"] = {"type": "simple"}
    cloud.fabric(configuration, args)

    assert type(Container.group()) == Simple

    assert Container.options("test") == {}
    assert Container.options("plugin") == configuration["plugin"]
    assert Container.options("log") == configuration["log"]

    assert Container.options("option") == {}
    a = {"ssh": "-t", "ssh_command": "sudo -i"}
    b = {"ssh": "-t", "ssh_command": "su"}
    c = {"ssh": "-t", "ssh_command": None}
    configuration["option"] = a
    assert Container.options("option") == a

    configuration["group"]["*"] = {"option": a}
    assert Container.options("option") == a
    assert Container.options("option", {"a": {"b": "c"}}) == a

    configuration["group"]["*"] = {"option": b}
    assert Container.options("option") == b
    assert Container.options("option", {"a": {"b": "c"}}) == b

    configuration["group"]["0 a.b:c"] = {"option": c}
    assert Container.options("option") == b
    assert Container.options("option", {"a": {"b": "c"}}) == c
    assert Container.options("option", {"a": {"b": "d"}}) == b
    assert Container.options("option", {"a": {"b": "long string with c inside"}}) == c
