#
# Copyright (C) 2017 Gao Liang <gaoliangim@gmail.com>
#
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# mirror is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mirror. If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.
#
#
import subprocess
import logging
import os

import mirror.component as component
from mirror.pluginbase import PluginBase

_plugin_name = "fedorareport"

log = logging.getLogger(_plugin_name)


class Plugin(PluginBase):
    DEFAULT_CONFIG_FILE = '/etc/mirrormanager-client/report_mirror.conf'

    def enable(self):
        plugin_manager = component.get("PluginManager")
        config = plugin_manager.config
        try:
            self.config_file = config[_plugin_name]["config_file"]
        except:
            self.config_file = self.DEFAULT_CONFIG_FILE
            log.info(("Didn't set `config_file` in plugin.ini in `%s` section"
                      ", use default one: %s"), _plugin_name, self.config_file)
        if not os.path.isfile(self.config_file):
            log.error("Can not find the config file `%s`. Plugin enable failed".format(self.config_file))

        self.enabled = True
        event_manager = component.get("EventManager")
        event_manager.register_event_handler("TaskStopEvent",
                                             self.__on_task_stop)

    def disable(self):
        pass

    def __on_task_stop(self, taskname, pid, exitcode):
        if taskname == "fedora" and exitcode == 0:
            try:
                out_bytes = subprocess.check_output(['report_mirror', '-c', self.config_file], stderr=subprocess.STDOUT)
                log.info("report_mirror success ")
            except subprocess.CalledProcessError as e:
                log.warning("report_mirror returned (), failed: %s", e.returncode, e.output)
