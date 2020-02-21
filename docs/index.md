## Environments

-   [Amazon Web Services (AWS)](https://aws.amazon.com/)
-   [Hetzner cloud](https://www.hetzner.com/cloud)
-   Discovery results from local command

## Purpose

We should jump between nodes quickly, having a pack of cloud accounts. Each account could be in a different region. Some nodes are publicity available, some of them not. Dozen of nodes sit behind bastion hosts. And a few of them sit behind a group of jump points. And they all have different SSH keys.

There is a `~/.ssh/config`, but it is not enough because of the dynamic nature of the cloud. It is too clumsy and not suitable for cases when IP addresses are changing instantly, and instances are creating and destroying in minutes.

I tried to structure that chaos with shell scripts, but the shell is not enough. I believe that tools like _C_/_C++_/_Java_/_Node.JS_/_Go_?/_Rust_ are too heavy for this case. Python is the exact thing. I like to have a dynamic and lightweight solution. Cloud Select is fast enough to go through thousands of nodes. Maybe if my scope will be higher, then I'll create something other.

Cloud Select is useful for diving inside geo-distributed onion enterprise environments with weird security settings.

## Implementation

CloudSelect retrieves node list from the cloud, passes that list to FZF, adds some useful information to selected nodes (like jump hosts, `sudo -i` command, etc...), and returns dictionary that could be used by other programs. CloudSelect is a team player in a shell environment. We can automatically open interactive SSH sessions in parallel and provide passwords to `sudo -i` under TMUX environment.

## Demo

[![demo](https://raw.githubusercontent.com/ezh/cloudselect/master/docs/demo/2019-12-11_23-04-56%20cloudselect%20demo.gif)](https://github.com/ezh/cloudselect/tree/master/docs/demo)

The tool is:

1.  connecting to bastion host with public IP 54.171.154.230
2.  using locally stored key on bastion because the usage of ssh-agent is restricted by security team ?lol? and sshd settings are `AllowTcpForwarding no`, `GatewayPorts no`
3.  jumping to 4 EC2 web instances in development environment that located in private subnet 172.30.x.x
4.  running `sudo -i` at startup
5.  entering `sudo` password 12345678

_And after that, we have four ready to use interactive sessions in our terminal..._

You may find a demo files in <a href="https://github.com/ezh/cloudselect/tree/master/docs/demo" target="_blank">docs/demo</a> directory.

## Basic usage

-   Connect to a single known_hosts server
-   Connect to a single EC2 AWS instance

P.S. To be exact, _connect_ or _run_ command or whatever you like

## Advanced usage

-   Connect to multiple known_hosts servers, run `sudo -i` command at startup and enter `sudo` password
-   Connect to multiple EC2 AWS instances, run `sudo -i` command at startup and enter `sudo` password
-   Connect to multiple EC2 AWS instances through a _bastion_ host, run `sudo -i` command at startup and enter `sudo` password

P.S. To be exact, _connect_ or _run_ command or whatever you like

## Features

:rocket: We may use jump hosts even if jump host hasn't been configured to allow remote port forwarding and we have the following settings in sshd_config:

```sh
  AllowTcpForwarding no
  GatewayPorts no
```
