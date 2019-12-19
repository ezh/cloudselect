## Requirements

CloudSelect is a Python software. <br/>
It is tested against [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudselect)](https://pypi.org/project/cloudselect/)<br/>
The latest version is [![PyPI version](https://img.shields.io/pypi/v/cloudselect.svg)](https://pypi.org/project/cloudselect/)

## Installation

`pip install cloudselect` to install cloudselect.<br/>
`git clone git@github.com:ezh/cloudselect.git` to clone the git repository for scripts and examples.<br/>
You may find shell scripts for cloud select and an example of configurations in the <a href="https://github.com/ezh/cloudselect/tree/master/example" target="_blank">example</a> directory.<br/>
You may find a demo configuration that was used for animated gif in <a href="https://github.com/ezh/cloudselect/tree/master/docs/demo" target="_blank">docs/demo</a>. Swarm of servers for the demo was created with Terraform.

## Usage

Execute `cloudselect` to see the list of profiles. It should be empty. <br/>
Do `cp example/known_hosts.cloud.json ~/.config/cloudselect/` to copy `known_hosts` profile to `.config` directory. <br/>
Execute `cloudselect` one more time to see the list of profiles. It should contain `known_hosts` profile. <br/>
Run `cloudselect known_hosts` to invoke FZF selector on your local hosts and get a JSON result. <br/><br/>
**Feel free to copy shell scripts in the example directory to your local `bin` folder.**

P.S. You may find a list of profiles in the configuration directory. Typical user config directories are:

```sh
Mac OS X:               ~/Library/Preferences/cloudselect
Unix:                   ~/.config/cloudselect     # or in $XDG_CONFIG_HOME, if defined
Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\cloudselect
Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application Data\cloudselect
Win 7+  (not roaming):  C:\Users\<username>\AppData\Local\cloudselect
Win 7+  (roaming):      C:\Users\<username>\AppData\Roaming\cloudselect
```

## Tips

Edit configuration with `cloudselect -e`<br/>
Edit profile with `cloudselect -e known_hosts`<br/>
Use SSH with `sh example/cloudssh known_hosts`<br/>
Open multiple SSH connections in a TMUX window with `sh example/cloudssh-tmux known_hosts`<br/>
Add bash profile autocompletion `complete -C cloudselect_completer <executable>`<br/>
   like `complete -C cloudselect_completer cloudselect` or `complete -C cloudselect_completer cloudssh`
