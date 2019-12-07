# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Cloud.options(...) behaviour."""
from cloudselect.cloudselect import CloudSelect


def test_options():
    """
    Testing cloud.options(...) behaviour.

    There should be {} if there is no any options.
    There should be dictionary if there is required option.
    """
    cloud = CloudSelect()
    configuration = cloud.configuration_read()
    args = cloud.parse_args([])
    cloud.fabric(configuration, args)

    assert cloud.options("test") == {}
    assert cloud.options("plugin") == configuration["plugin"]
    assert cloud.options("log") == configuration["log"]
