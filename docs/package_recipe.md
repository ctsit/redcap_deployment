# Creating a REDCap package for deployment

This guide provides the sequence of commands needed to package a version of REDCap software for deployment or upgrade. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

### Prerequisites  
This workflow assumes you have a REDCap zip file exactly as downloaded from the REDCap Consortium. The version of REDCap is up to you, but the zip file needs to be named in the original format of redcap#.#.#.zip (standalone package) OR redcap#.#.#_upgrade.zip (upgrade package). The zip file needs to be in the same directory as the file fabfile.py. The fabric commands will be entered into the command line from this directory.

## Fabric Command Sequence
While you're in the directory that contains both the fabfile and the desired redcap zip file, execute the command `$ fab package:(redcap_zip)`. The redcap\_zip is your redcap zip file or it will default to the most recent redcap zip in the directory. This will remove any existing build directories (builddirs) and create a new one for the build. The new builddir is populated with the extracted contents of the zip file found/specified, and hooks and plugins if provided. The resultant package file will be named redcap-#.#.#.tgz or redcap-#.#.#_upgrade.tgz according to the name of the redcap.zip used to create this package.

Optionally, you can specify an instance you are building for. This will allow you to specify configurable languages and patches to be included in the package. To do that you would name the instance just before package like this:

    fab instance:vagrant package:redcap7.2.2.zip

## Adding language files

To add a REDCap language file to your REDCap package, download the language file from the REDCap community site, copy it into the same directory as fabfile.py, and add an entry like this to your instance's configuration file:

    [instance]
    languages = [ "Chinese.6.4.3.ini" ]

The languages variable will be interpreted as a JSON list. If you want to load multiple language files, separate their file names with commas:

    [instance]
    languages = [ "Chinese.6.4.3.ini", "German6.10.1.ini" ]


## Adding patches

To apply a patch the REDCap core code, you will need to create a specially formatted git repository with the patch file and a script named `deploy.sh` that can deploy it into the builddir.  That deploy.sh file would look something like this: 

    #!/bin/bash
    # deployment script for the redcap_security_settings GLID patch
    # Clone the repo that has this file via
    #
    #   git clone git@ctsit-forge.ctsi.ufl.edu:redcap_security_settings.git
    #
    # Call this script with two parameters:
    #
    #   REDCAP_ROOT - the top level redcap directory.  typically this directory contains cron.php
    #   REDCAP_VERSION - the version of the code being patched/deployed.
    #

    set -e

    export REDCAP_ROOT=$1
    export REDCAP_VERSION=$2

    # determine the directory where this script resides
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    cd $REDCAP_ROOT/redcap_v$REDCAP_VERSION/ControlCenter/
    patch -p1 < $DIR/security_settings.php.patch

The script must be named `deploy.sh`.  It must accept two parameters, `REDCAP_ROOT` and `REDCAP_VERSION`.  It must use these two variables to determine in which directory it should apply the patch.

With this git repository created, you must reference it in the instance configuration file like this:

    [instance]
    patch_repos = [ "git@ctsit-forge.ctsi.ufl.edu:redcap_security_settings.git" ]

As with the language files, you may specify multiple patches in a comma-separated list. 

The `package` task will checkout each of these repositories and run ./deploy.sh in the root of the repository.  

## Adding Plugins

You can add a plugin by creating deployment script for that plugin at deploy/plugins/`plugin_name`/deploy.sh. The `package` task runs each of deploy/plugins/`plugin_name`/deploy.sh scripts. The deploy.sh scripts swill need to put the plugin files in the right places underneath `builddir`/redcap/plugins/. Whether the deploy/plugins/`plugin_name` directory also contains the plugin files or if the deploy.sh script fetches them from an authoritative source is entirely up to you. The `package` task will pass the a full path to directory where the deploy.sh should copy the plugin files.  deploy.sh must use this *target directory* to as the target when it copies the files into the build directory.

This example is a deploy.sh that clones a git repository and deploys the plugin files into build space to be packaged.

    #!/bin/bash
    set -e

    export MYTARGETDIR=$1

    # determine the directory where this script resides
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    # get source files
    TEMPDIR=`mktemp -d`
    git clone https://github.com/ctsit/redcap-custom-dashboard.git $TEMPDIR

    # copy files to the correct target locations
    mkdir -p $MYTARGETDIR
    cp $TEMPDIR/index.php $MYTARGETDIR
    cp $TEMPDIR/custom_dashboard.js $MYTARGETDIR

    rm -rf $TEMPDIR

## Adding hooks 

You can add hooks in much the same way as plugins. Add a deploy.sh at deploy/hooks/`hook_name`/deploy.sh.  The hook must follow the same rules as plugins. The `package` task will pass a target directory that looks like `builddir`/redcap/hooks/library/`hook_function`/`hook_name`/, where `hook_function` is one of the built in REDCap hook_functions:

    redcap_add_edit_records_page
    redcap_control_center
    redcap_custom_verify_username
    redcap_data_entry_form
    redcap_data_entry_form_top
    redcap_every_page_before_render
    redcap_every_page_top
    redcap_project_home_page
    redcap_save_record
    redcap_survey_complete
    redcap_survey_page
    redcap_survey_page_top
    redcap_user_rights

The features in the `package` task only know how to build a library of hook code. It does not activate any of the hooks in any project or globally. That task is managed via manually via a hook framework as described in the next section.


## Hook framework

These deployments tools use the University of Florida's hook framework described at [https://github.com/ctsit/extensible-redcap-hooks](https://github.com/ctsit/extensible-redcap-hooks) This differs from the one written by Andy Martin (see [https://github.com/123andy/redcap-hook-framework](https://github.com/123andy/redcap-hook-framework)) in that the UF framework uses a different directory layout, PHP [anonymous functions](http://php.net/manual/en/functions.anonymous.php), and depends heavily on symbolic links to activate hooks.

The anonymous functions require the code not name the functin they are hooking. The name of the file in which the hook code resides will provide the function name. If you have hook named `my_cool_hook.php` and you make a symlink to the global hook directory with the name `redcap_data_entry_form.php`, the anonymous funciton in the file will hook the `redcap_data_entry_form` function.  

See [https://github.com/ctsit/extensible-redcap-hooks](https://github.com/ctsit/extensible-redcap-hooks) for more details on how to activate hooks using this framework.
