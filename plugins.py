from fabric.api import *
import os
import re

__all__ = []

@task
def test(plugin_path):
    """
    Symbolically link a host file that contains a redcap plugin into the ./redcap/plugins folder

    :param plugin_path: path to plugin folder relative to VagrantFile
    :return:
    """
    if not os.path.exists(plugin_path):
        abort("The folder %s does not exist.  Please provide a relative path to a plugin folder you would like to test in the local vm" % plugin_path)
    redcap_root = env.live_project_full_path
    source_path = "/vagrant/" + plugin_path
    target_folder = "/".join([redcap_root, env.plugins_path])

    with settings(user=env.deploy_user):
            run("ln -sf %s %s" % (source_path, target_folder))
