#### FZF Cloud Select

[![Build Status](https://travis-ci.org/ezh/cloudselect.svg?branch=master)](https://travis-ci.org/ezh/cloudselect)
[![codecov](https://codecov.io/gh/ezh/cloudselect/branch/master/graph/badge.svg)](https://codecov.io/gh/ezh/cloudselect)
[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg)](/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudselect)](https://pypi.org/project/cloudselect/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/124d1f6ec45e45deaf924e740670087f)](https://www.codacy.com/manual/ezh/cloudselect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ezh/cloudselect&amp;utm_campaign=Badge_Grade)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable)

## Purpose

We have to jump between nodes quickly. There is a list of cloud accounts. Each account has multiple regions. Some nodes are publicity available, some of them not. Dozen of nodes sit behind bastion hosts. And few of them sit behind a group of jump points. And they all have different SSH keys.

There is a ~/.ssh/config, but it is not enough because of the dynamic nature of the cloud. It is too clumsy. It is not suitable for cases when IP addresses are changing instantly, and instances are creating and destroying in minutes.

I tried to structure that hell with shell scripts, but the shell is not enough. I believe that tools like C/C++/Java/Node.JS/Go?/Rust are too heavy for this case. Python is the exact thing. I like to have a dynamic and lightweight solution. Cloud Select is fast enough to go through thousands of nodes. Maybe if my scope will be higher, then I'll create something other.

## Implementation

CloudSelect retrieves node list from the cloud, pass that list to FZF, add some useful information to selected nodes (like jump hosts, `sudo -i` command, etc...) and returns JSON dictionary that could be used by other programs. CloudSelect is a team player in a shell environment. We can automatically open multiple interactive SSH sessions and provide passwords to `sudo -i` under TMUX environment. It is valuable. There are a lot of questions on StackOverflow how to do this but no answers. This tool is the answer.

# License

[MIT][mit] © [Alexey Aksenov][author] et [al][contributors]

[mit]: https://opensource.org/licenses/MIT

[author]: https://github.com/ezh

[contributors]: https://github.com/ezh/cloudselect/graphs/contributors

[license-badge]: https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square
