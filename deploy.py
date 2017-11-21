from fabric.api import *
from tempfile import mkstemp
import re
import os
import utility
import utility_redcap

def update_redcap_connection(db_settings_file="database.php", salt="abc"):
    """
    Update the database.php file with settings from the chosen environment
    """

    redcap_database_settings_path = "/".join([env.backup_pre_path, env.remote_project_name, db_settings_file])
    with settings(user=env.deploy_user):
        run('echo \'$hostname   = "%s";\' >> %s' % (env.database_host, redcap_database_settings_path))
        run('echo \'$db   = "%s";\' >> %s' % (env.database_name, redcap_database_settings_path))
        run('echo \'$username   = "%s";\' >> %s' % (env.database_user, redcap_database_settings_path))
        run('echo \'$password   = "%s";\' >> %s' % (env.database_password, redcap_database_settings_path))
        run('echo \'$salt   = "%s";\' >> %s' % (salt, redcap_database_settings_path))


def create_database():
    """
    Create an empty database in MySQL dropping the existing database if need be.
    """

    # Only run on a local testing environment
    if not env.vagrant_instance:
        abort("create_database can only be run against the Vagrant instance")

    # generate the DROP/CREATE command
    create_database_sql="""
    DROP DATABASE IF EXISTS %(database_name)s;
    CREATE DATABASE %(database_name)s;

    GRANT
        SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
    ON
        %(database_name)s.*
    TO
        '%(database_user)s'@'%(database_host)s'
    IDENTIFIED BY
        '%(database_password)s';""" % env

    # run the DROP/CREATE command as root
    with settings(user=env.deploy_user):
        run('echo "%s" | mysql -u root -p%s' % (create_database_sql, env.database_root_password))


def create_redcap_tables(resource_path = "Resources/sql"):
    """
    Create redcap tables via the remote host
    """
    print("Creating redcap tables")
    redcap_sql_root_dir = os.path.join(env.backup_pre_path,env.remote_project_name)
    with settings(user=env.deploy_user):
        redcap_name = run("ls %s | grep 'redcap_v[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}' | sort -n | tail -n 1" % redcap_sql_root_dir)
    redcap_sql_dir = os.path.join(redcap_sql_root_dir,redcap_name,resource_path)
    match = re.search('redcap_v(\d+.\d+.\d+)', redcap_name)
    version = match.group(1)
    with settings(user=env.deploy_user):
        run('mysql < %s/install.sql' % redcap_sql_dir)
        run('mysql < %s/install_data.sql' % redcap_sql_dir)
        run('mysql -e "UPDATE %s.redcap_config SET value = \'%s\' WHERE field_name = \'redcap_version\' "' % (env.database_name, version))

        files = run('ls -v1 %s/create_demo_db*.sql' % redcap_sql_dir)
        for file in files.splitlines():
            print("Executing sql file %s" % file)
            run('mysql < %s' % file)


def move_edocs_folder():
    """
    Move the redcap/edocs folder out of web space.
    """
    default_edoc_path = '%s/edocs' % env.live_project_full_path
    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if run("test -e %s" % env.edoc_path).succeeded:
                utility_redcap.set_redcap_config('edoc_path',env.edoc_path)
            if run("test -e %s" % default_edoc_path).succeeded:
                with settings(warn_only=False):
                    file_name = run('ls -1 %s' % default_edoc_path)
                    if file_name == "index.html":
                        run('rm -r %s' % default_edoc_path)


def configure_redcap_cron(deploy=False, force_deployment_of_redcap_cron=False):
    crond_for_redcap = '/etc/cron.d/%s' % env.project_path
    with settings(warn_only=True):
        if deploy:
            if run("test -e %s" % crond_for_redcap).failed or force_deployment_of_redcap_cron:
                sudo('echo "# REDCap Cron Job (runs every minute)" > %s' % crond_for_redcap)
                sudo('echo "* * * * * root /usr/bin/php %s/cron.php > /dev/null" >> %s' \
                    % (env.live_project_full_path, crond_for_redcap))
        else:
            warn("Not deploying REDCap Cron. Set deploy_redcap_cron=True in instance's ini to deploy REDCap Cron.")

def inlcude_go_prod_plugin(name):
    """
    Add go_prod plugin to redcap instance
    """
    file_name = name.split('.')[0]
    plugins_folder = "/var/www/redcap/plugins"
    with settings(warn_only=True):
        if run("test -e /vagrant/%s" % name).succeeded:
            run("unzip /vagrant/%s -d %s" % (name,plugins_folder))
            run("mv %s/%s %s/go_prod/" % (plugins_folder,file_name,plugins_folder))
            if run("test -e %s/__MACOSX" % plugins_folder).succeeded:
                run("rm -r %s/__MACOSX" % plugins_folder)


@task(default=True)
def deploy(name,force=""):
    """
    Deploy a new REDCap instance defined by <package_name>, optionally forcing redcap cron deployment
    """
    utility_redcap.make_upload_target()
    utility_redcap.upload_package_and_extract(name)
    update_redcap_connection()
    utility.write_remote_my_cnf()
    if env.vagrant_instance:
        create_database()
    create_redcap_tables()
    utility_redcap.move_software_to_live()
    move_edocs_folder()
    utility_redcap.set_redcap_base_url()
    utility_redcap.set_hook_functions_file()
    utility_redcap.deploy_external_modules()
    force_deployment_of_redcap_cron = utility.is_affirmative(force)
    configure_redcap_cron(env.deploy_redcap_cron, force_deployment_of_redcap_cron)
    utility_redcap.test()
    inlcude_go_prod_plugin()
    utility.delete_remote_my_cnf()

