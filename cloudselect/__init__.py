# Copyright 2019 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.

from __future__ import absolute_import, division, print_function

import dependency_injector.containers as containers
from .instance import *

__all__ = (
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
)

__title__ = "awselect"
__summary__ = "AWS FZF selector"
__uri__ = "https://github.com/ezh/awselect"

__version__ = "19.1"

__author__ = "Alexey Aksenov and individual contributors"
__email__ = "ezh@ezh.msk.ru"

__license__ = "MIT License"
__copyright__ = "Copyright 2019 Alexey Aksenov and individual contributors"


Container = containers.DynamicContainer()
