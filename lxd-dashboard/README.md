# lxd-dashboard

## Description

`lxd-dashboard` is a GUI for lxd. Once deployed, it exposes itself with an initial login.

Future versions will allow for SSL/TLS and perhaps some intial configuration.

## Usage

    juju deploy lxd-dashboard

Once deployed, visit http://your-unit-ip

Complete the installation and get the client-certificate (Via the GUI).

On your lxd host, add the client-certificate:

    lxc config trust add <certificate>

Finally, add the LXD host by also using the GUI.

## Chosing version of lxd-dashboard
By default, the charm tries to get and install the latest release from the gihub repo of lxdware: https://github.com/lxdware/lxd-dashboard

This can be overridden if you want a specific release tag with a config at deploytime:

    juju deploy lxd-dashboard --config github-release-tag="v3.4.0"

Future versions of this charm can support upgrade.

## Relations

No relations yet. Future version might implement this.

## Actions

No actions yet. Future version might implement this.

## Contributing

See: [CONTRIBUTING.md](CONTRIBUTING.md) for developer guidance. 
## Attributions

Massive attribution to https://lxdware.com/ at https://lxdware.com/.
