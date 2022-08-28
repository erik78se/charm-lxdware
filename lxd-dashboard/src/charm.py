#!/usr/bin/env python3
# Copyright 2022 erik@dwellir.com
# See LICENSE file for licensing details.

""" 
    A juju charm for lxd-dashboard: https://lxdware.com
"""

import logging
import os
from pathlib import Path
import subprocess
import sys

import sourcemanager

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus, BlockedStatus

logger = logging.getLogger(__name__)


class LxdDashboardCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self._stored.set_default(current_tarfile="/None")
        self._stored.set_default(current_dashboard_version="")

    def _on_install(self, event):
        self.unit.status = MaintenanceStatus("required packages ...")
        os.system('apt update && apt install wget nginx php-fpm php-curl sqlite3 php-sqlite3 -y')
        self.unit.set_workload_version( self._installlxddashboard() )


    def _on_config_changed(self, _):
        """
        config-changed
        """
        self.unit.status = MaintenanceStatus("restarting nginx")
        os.system('systemctl restart nginx')
        self._on_update_status(None)


    def _installlxddashboard(self):
        """
        Returns the version that was installed.
        """
        self.unit.status = MaintenanceStatus("fetching lxd-dashboard...")
        
        # Dont fetch/extract if its already fetched.

        if not Path(self._stored.current_tarfile).exists():
            logger.debug("Downloading: " + self.config['github-release-tag'])
            dl = sourcemanager.fetchGithub('lxdware','lxd-dashboard', tag_name=self.config['github-release-tag'])
            self._stored.current_tarfile = str(dl[1])
        else:
            logger.debug("Release tarfile already available: " + self._stored.current_tarfile + " skip download.")
        try:
            self.unit.status = MaintenanceStatus("Extracting lxd-dashboard ...")
            logger.debug("Trying to extract: " + self._stored.current_tarfile)
            extractdir = str(sourcemanager.extractReleaseFile(self._stored.current_tarfile))

            cmd1 = f"cp -a {extractdir}/default /etc/nginx/sites-available/"
            cmd2 = f"cp -a {extractdir}/lxd-dashboard /var/www/html/"
            cmd3 = "mkdir -p /var/lxdware/data/sqlite"
            cmd4 = "mkdir -p /var/lxdware/data/lxd"
            cmd5 = "mkdir -p /var/lxdware/backups"
            cmd6 = "chown -R www-data:www-data /var/lxdware/"
            cmd7 = "chown -R www-data:www-data /var/www/html"

            subprocess.run(cmd1.split(), check = True)
            subprocess.run(cmd2.split(), check = True)
            subprocess.run(cmd3.split(), check = True)
            subprocess.run(cmd4.split(), check = True)
            subprocess.run(cmd5.split(), check = True)
            subprocess.run(cmd6.split(), check = True)
            subprocess.run(cmd7.split(), check = True)
            self._stored.current_dashboard_version = str(dl[0])

        except Exception as e:
            print("Error fetching/installing sofware release", str(e))
            sys.exit(1)
        
        #TODO: Return the actual version.
        
        return self._stored.current_dashboard_version

    def _on_update_status(self, event):
        """
            This runs every 5 minutes.
            Have one place to figure out status for the charm is a good strategy for a beginner charmer.
        """
        if not os.system('systemctl is-active nginx.service') == 0:
            logger.info("nginx service is not active.")
            self.unit.status = BlockedStatus("Inactive - nginx not active.")
        else:
            logger.info(f"nginx service is running.")
            self.unit.status = ActiveStatus("Operational")
            self.unit.set_workload_version(self._stored.current_dashboard_version)
        

if __name__ == "__main__":
    main(LxdDashboardCharm)
