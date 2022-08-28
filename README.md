# lxdware-dashboard
This is a juju charm which sets up lxdware and allows you to manage it over time.

Your can find it on charmhub.io: https://charmhub.io/lxd-dashboard

Its developed with the ops framework for juju.

See full documentation: [lxd-dashboard/README.md](lxd-dashboard/README.md)


## Building/Developing the charm

Start your lxd development instance:

    lxc launch ubuntu:20.04 lxd01 --vm
    lxc shell lxd01  # Add your ssh pubkey to /home/ubuntu/.ssh/authorized_keys
   
Create a juju model and deploy lxd to the machine.
 
    juju add-model lxdwaredev
    juju add-machine ssh:ubuntu@ip.ip.ip.ip
    juju deploy lxd --num-units 1 --config snap-channel="5.0/stable" --config lxd-listen-https=true --to 0

    # Code away
    cd lxd-dashboard
    charmcraft pack

## Releasing

    charmcraft upload lxd-dashboard_ubuntu-22.04-amd64.charm --name lxd-dashboard
