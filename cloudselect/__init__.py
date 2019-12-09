# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""CloudSelect package."""
from __future__ import absolute_import, division, print_function

import dependency_injector.containers as containers
import pkg_resources

from .instance import Instance

__all__ = ["Instance"]

__title__ = "awselect"
__summary__ = "AWS FZF selector"
__uri__ = "https://github.com/ezh/awselect"

__author__ = "Alexey Aksenov and individual contributors"
__email__ = "ezh@ezh.msk.ru"

__license__ = "MIT License"


try:
    __version__ = pkg_resources.get_distribution("cloudselect").version
except Exception:
    __version__ = "unknown"

Container = containers.DynamicContainer()
