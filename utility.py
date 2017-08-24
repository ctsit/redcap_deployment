from fabric.api import *
from tempfile import mkstemp
from datetime import datetime
import os, re
try:
    import configparser
except:
    from six.moves import configparser

__all__ = []


def timestamp():
    return datetime.now().strftime("%Y%m%dT%H%M%Z")


def get_config(key,settings_file_path="", section="instance"):
    config.read(settings_file_path)
    return config.get(section, key)


def convert_version_to_int(version):
    """
    Convert a redcap version number to integer
    """
    version = int("%d%02d%02d" % tuple(map(int,version.split('.'))))
    return version


def extract_version_from_string(string):
    """
    extracts version number from string
    """
    match = re.search(r"(\d+\.\d+\.\d+)", string)
    version=match.group(1)
    return version


def is_affirmative(response):
    """
    Turn strings that mean 'yes' into a True value, else False
    """

    if re.match("^(force|true|t|yes|y)$", response, re.IGNORECASE):
        return True
    else:
        return False


def delete_all_tables(confirm=""):
    """
    Delete all tables for the database specified in the instance. You must confirm this command.
    """
    if is_affirmative(confirm):
        write_remote_my_cnf()
        with settings(user=env.deploy_user):
            run("mysqldump --add-drop-table --no-data --single-transaction --databases %s | grep -e '^DROP \| FOREIGN_KEY_CHECKS' | mysql %s" \
                % (env.database_name, env.database_name))
        delete_remote_my_cnf()
    else:
        print "\nProvide a confirmation string (e.g. 'y', 'yes') if you want to delete all MySQL tables for this instance."


def apply_local_sql_to_db(sql_file=""):
    """
    Copy a local SQL file to the remote host and run it against mysql

    """
    if local('test -e %s' % sql_file).succeeded:
        with settings(user=env.deploy_user):
            remote_sql_path = run('mktemp')
            put(sql_file, remote_sql_path)
            apply_remote_sql_to_db(remote_sql_path)
            run('rm %s' % remote_sql_path)


def apply_remote_sql_to_db(sql_file=""):
    """
    Apply a SQL file on a remote host against the mysql DB

    """
    with settings(user=env.deploy_user):
        remote_sql_path = sql_file
        if run('test -e %s' % remote_sql_path).succeeded:
            write_remote_my_cnf()
            run('mysql < %s' % remote_sql_path)
            delete_remote_my_cnf()


def write_my_cnf():
    _, file = mkstemp()
    f = open(file, 'w')
    f.write("[mysqldump]" + "\n")
    f.write("user=" + env.database_user + "\n")
    f.write("password='" + env.database_password + "'\n")
    f.write("" + "\n")
    f.write("[client]" + "\n")
    f.write("user=" + env.database_user + "\n")
    f.write("password='" + env.database_password + "'\n")
    f.write("database=" + env.database_name + "\n")
    f.write("host=" + env.database_host + "\n")
    f.close()
    return file


def write_remote_my_cnf():
    """
    Write a .my.cnf into the deploy user's home directory.
    """
    global w_counter
    file = write_my_cnf()
    with settings(user=env.deploy_user):
        target_path = '/home/%s/.my.cnf' % get_config('deploy_user')
        put(file, target_path , use_sudo=False)
        run('chmod 600 %s' % target_path)
    os.unlink(file)
    w_counter = w_counter+1


def delete_remote_my_cnf():
    """
    Delete .my.cnf from the deploy user's home directory.
    """
    global w_counter
    w_counter = w_counter-1
    if w_counter == 0:
        my_cnf = '/home/%s/.my.cnf' % get_config('deploy_user')
        with settings(user=env.deploy_user):
            if run("test -e %s" % my_cnf).succeeded:
                run('rm -rf %s' % my_cnf)


config = configparser.ConfigParser()
w_counter = 0