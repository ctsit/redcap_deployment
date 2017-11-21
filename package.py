from fabric.api import *
from fabric.contrib.files import exists
from fabric.utils import abort
import string, random, os
import json
import re


def make_builddir(builddir="build"):
    """
    Create the local build directory.
    """

    with settings(warn_only=True):
        if local("test -e %s" % builddir).failed:
            local("mkdir %s" % builddir)
        else:
            print ("Directory %s already exists!" % builddir)


@task
def clean(builddir="build"):
    """
    Clean the local build directory.
    """
    local("rm -rf %s" % builddir)


def latest_redcap(sourcedir="."):
    env.latest_redcap = local("ls %s/redcap*.zip | grep 'redcap[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}\.zip' | sort -n | tail -n 1" % sourcedir, capture=True).stdout
    return env.latest_redcap


def extract_redcap(redcap_zip="."):
    print (redcap_zip)
    # TODO determine if redcap_zip is a RC.zip or a path
    with settings(warn_only=True):
        if local("test -d %s" % redcap_zip).succeeded:
            redcap_path = latest_redcap(redcap_zip)
        elif local("test -e %s" % redcap_zip).succeeded:
            redcap_path = redcap_zip
        else:
            abort("The redcap version specified is neither a zip file nor a path.")
    print (redcap_path)
    match = re.search(r"(redcap)(\d+.\d+.\d+)(|_upgrade)(.zip)", redcap_path)
    print(match.group(2))
    env.redcap_version = match.group(2)
    redcap_version_and_package_type = match.group(2) + match.group(3)
    local("unzip -qo %s -d %s" % (redcap_path, env.builddir))
    return redcap_version_and_package_type


def deploy_hooks_framework_into_build_space(target_within_build_space="redcap/hooks/"):
    """
    Deploy UF's REDCap hooks framework
    """
    # make sure the target directory exists
    source_dir = env.hook_framework_deployment_source
    this_target ='/'.join([env.builddir, target_within_build_space])
    deploy_extension_to_build_space(source_dir, this_target)


def deploy_third_party_dependencies_into_build_space(target_within_build_space="redcap/"):
    """
    Deploy third-party dependencies with Composer
    """
    # make sure the target directory exists
    source_dir = env.composer_deployment_source
    this_target ='/'.join([env.builddir, target_within_build_space])
    deploy_extension_to_build_space(source_dir, this_target)


def deploy_modules_framework_into_build_space(target_within_build_space="redcap/external_modules/"):
    """
    Deploy UF's REDCap modules framework
    """
    # make sure the target directory exists
    source_dir = env.module_framework_deployment_source
    this_target ='/'.join([env.builddir, target_within_build_space])
    deploy_extension_to_build_space(source_dir, this_target)


def deploy_hooks_into_build_space(target_within_build_space="redcap/hooks/library"):
    """
    Deploy each extension into build space by running its own deploy.sh.
    Lacking a deploy.sh, copy the extension files to the build space.
    For each extension run test.sh if it exists.
    """
    # make sure the target directory exists
    extension_dir_in_build_space='/'.join([env.builddir, target_within_build_space])
    with settings(warn_only=True):
        if local("test -d %s" % extension_dir_in_build_space).failed:
            local("mkdir -p %s" % extension_dir_in_build_space)

    # For each type of hook, make the target directory and deploy its children
    for feature in os.listdir(env.hooks_deployment_source):
        # make the target directory
        feature_fp_in_src = '/'.join([env.hooks_deployment_source, feature])
        if os.path.isdir(feature_fp_in_src):
            # file is a hook type
            feature_fp_in_target = extension_dir_in_build_space
            if not os.path.exists(feature_fp_in_target):
                os.mkdir(feature_fp_in_target)

            deploy_extension_to_build_space(feature_fp_in_src, feature_fp_in_target)


def deploy_modules_into_build_space():
    """
    Deploy each module into build space.
    """
    if not os.path.exists(env.modules_deployment_source):
        return
    with open(env.modules_deployment_source) as f:
        for module in json.load(f):
            tempdir = local("mktemp -d 2>&1", capture = True)
            local("git clone -b %s %s %s" % (module['branch'],module['repo'],tempdir))
            local("mkdir %s/redcap/modules/%s_v%s" % (env.builddir,module['name'],module['version']))
            local("cp -r %s/* %s/redcap/modules/%s_v%s" % (tempdir,env.builddir,module['name'],module['version']))
            local("rm -rf %s" % tempdir)


def deploy_plugins_into_build_space(target_within_build_space="/redcap/plugins"):
    """
    Deploy each extension into build space by running its own deploy.sh.
    Lacking a deploy.sh, copy the extension files to the build space.
    For each extension run test.sh if it exists.
    """
    # make sure the target directory exists
    extension_dir_in_build_space=env.builddir + target_within_build_space
    with settings(warn_only=True):
        if local("test -d %s" % extension_dir_in_build_space).failed:
            local("mkdir -p %s" % extension_dir_in_build_space)

    # locate every directory plugins_deployment_source/*
    for (dirpath, dirnames, filenames) in os.walk(env.plugins_deployment_source):
        for dir in dirnames:
            source_dir = '/'.join([dirpath,dir])
            this_target = os.path.join(extension_dir_in_build_space, dir)
            deploy_extension_to_build_space(source_dir, this_target)


def deploy_extension_to_build_space(source_dir="", build_target=""):
    if not os.path.exists(build_target):
        os.mkdir(build_target)

    # run the deployment script
    this_deploy_script = os.path.join(source_dir,'deploy.sh')
    if os.path.isfile(this_deploy_script):
        local("bash %s %s" % (this_deploy_script, build_target))
    else:
        # copy files to target
        local("cp %s/* %s" % (source_dir, build_target))

    # run test deployment script
    this_test_script = os.path.join(source_dir,'test.sh')
    if os.path.isfile(this_test_script):
        local("bash %s " % this_test_script)


def deploy_language_to_build_space():
    source_dir = env.languages
    target_dir = env.builddir + "/redcap/languages"

    if re.match(r'^\[.+\]$', source_dir) is not None:
        for language in json.loads(env.languages):
            if os.path.exists(language):
                local("mkdir -p %s" % target_dir)
                local('cp %s %s' % (language, target_dir))
            else:
                abort("the language file %s does not exist" % language)
    elif local('find %s/*.ini -maxdepth 1 -type f | wc -l' % source_dir, capture = True) != '0':
        if os.path.exists(source_dir) and os.path.exists(target_dir):
            local('find %s/*.ini -maxdepth 1 -type f -exec rsync {} %s \;' %(source_dir, target_dir))
    else:
        print("Warning: The languages where not provided. English will be used by default.")

def apply_patches():
    for repo in json.loads(env.patch_repos):
        tempdir = local('mktemp -d 2>&1', capture = True)
        local('git clone %s %s' % (repo,tempdir))
        local('%s/deploy.sh %s/redcap %s' % (tempdir, env.builddir, env.redcap_version))
        local('rm -rf %s' % tempdir)


def add_db_upgrade_script():
    target_dir = '/'.join([env.builddir, "redcap", "redcap_v%s" % env.redcap_version])
    print target_dir
    local('cp deploy/files/generate_upgrade_sql_from_php.php %s' % target_dir)


@task(default=True)
def package(redcap_zip="."):
    """
    Create a REDCap package from a redcapM.N.O.zip or redcapM.N.O_upgrade.zip

    The resulting file will be named redcap-M.N.O.tgz
    """

    # Build the app
    clean(env.builddir)
    make_builddir(env.builddir)
    redcap_version_and_package_type = extract_redcap(redcap_zip)
    deploy_plugins_into_build_space()
    deploy_modules_into_build_space()
    deploy_modules_framework_into_build_space()
    deploy_hooks_into_build_space()
    deploy_hooks_framework_into_build_space()
    deploy_language_to_build_space()
    deploy_third_party_dependencies_into_build_space()
    apply_patches()
    add_db_upgrade_script()

    # Get variables to tell us where to write the package
    env.package_name = '%s-%s.tgz' % (env.project_name, redcap_version_and_package_type)
    cwd = os.getcwd()
    # create the package
    local("cd %s && tar -cz --exclude='.DS_Store' \
    -f %s/%s \
    redcap" % (env.builddir, cwd, env.package_name))
