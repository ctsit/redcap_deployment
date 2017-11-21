from fabric.api import *
import os
import re

__all__ = []

@task
def activate(hook_function, hook_name, redcap_root, pid):
    """
    Activate the hook `hook_name` as type of `hook_function` for the project named by `pid`.

    If PID is omitted, the hook will be activated globally.

    :param hook_function: one of the 13 named REDCap 'hook functions'
    :param hook_name: the name of the hook file with or without the .php extension
    :param redcap_root: the directory which contains the redcap instance
    :param pid: the ID of the project on which this hook should be activated. If left blank the hook will be activated globally
    :return:
    """
    valid_hook_functions=["redcap_add_edit_records_page",
    "redcap_control_center",
    "redcap_custom_verify_username",
    "redcap_data_entry_form",
    "redcap_data_entry_form_top",
    "redcap_every_page_before_render",
    "redcap_every_page_top",
    "redcap_project_home_page",
    "redcap_save_record",
    "redcap_survey_complete",
    "redcap_survey_page",
    "redcap_survey_page_top",
    "redcap_user_rights"]
    if not hook_function in valid_hook_functions:
        print ("Hook_function parameter not recognized. Please choose from " + str(valid_hook_functions))
        abort("Try again with a valid hook function.")
    if not re.match('.*\.php$', hook_name):
        hook_name = hook_name + '.php'
    hook_source_path = "/".join([env.hooks_library_path, hook_function, hook_name])

    hooks_dir = "/".join(env.hooks_framework_path.rsplit('/')[:-1])
    if len(pid)==0:
        hook_source_relative_path = "/".join(['..', env.hooks_library_path.rsplit('/').pop(), hook_function, hook_name])
        hook_target_folder = "/".join([hooks_dir, hook_function])
    elif re.match('^[0-9]+$', pid):
        hook_source_relative_path = "/".join(['..', '..', env.hooks_library_path.rsplit('/').pop(), hook_function, hook_name])
        hook_target_folder = "/".join([hooks_dir, 'pid'+pid, hook_function])
    else:
        abort("pid must be a numeric REDCap project id. '%s' is not a valid pid" % pid)

    with cd("%s" % redcap_root):
        with settings(warn_only=True):
            if run(" test -e %s" % hook_source_path).failed:
                abort("Check your parameters. The hook was not found at %s" % hook_source_path)
        with settings(user=env.deploy_user):
            run("mkdir -p %s" % hook_target_folder)
            run("ln -sf %s %s" % (hook_source_relative_path, hook_target_folder))


@task
def test(hook_function, hook_path):
    """
    Symbolically link a host file that contains a redcap hook into the hooks library space and activate that hook globally

    :param hook_function: one of the 13 named REDCap 'hook functions'
    :param hook_path: path to hook file relative to VagrantFile
    :return:
    """
    if not os.path.exists(hook_path):
        abort("The file %s does not exist.  Please provide a relative path to a hook you would like to test in the local vm" % hook_path)
    hook_name = hook_path.rsplit('/').pop()
    redcap_root = env.live_project_full_path
    hook_source_path = "/vagrant/" + hook_path
    hook_target_folder = "/".join([redcap_root, env.hooks_library_path, hook_function])

    run("mkdir -p %s" % hook_target_folder)
    run("ln -sf %s %s" % (hook_source_path, hook_target_folder))
    activate(hook_function, hook_name, redcap_root, "")
