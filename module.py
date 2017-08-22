from fabric.api import *
import os
import re
import utility

@task
def enable(module_name, module_version="", pid=""):
    utility.write_remote_my_cnf()
    add_module_to_tables(module_name, module_version, pid)
    utility.delete_remote_my_cnf()


@task
def disable(module_name, module_version="", pid=""):
    utility.write_remote_my_cnf()
    remove_module_from_tables(module_name, module_version, pid)
    utility.delete_remote_my_cnf()


def add_module_to_tables(module_name, module_version, pid):
    """
        Adds modules to redcap tables
    """
    add_to_redcap_external_modules = """
        INSERT INTO redcap_external_modules (directory_prefix)
        SELECT * FROM (SELECT '%s') AS rem
        WHERE NOT EXISTS (
        SELECT directory_prefix FROM redcap_external_modules WHERE directory_prefix = '%s'
        ) LIMIT 1;
        """ %(module_name,module_name)
    find_id = """
        SELECT external_module_id FROM redcap_external_modules WHERE directory_prefix='%s';
        """ %(module_name)
    
    with settings(user=env.deploy_user):
        run('mysql -e "%s"' %add_to_redcap_external_modules)
        external_module_id = run('mysql -s -N -e "%s"' %find_id)

    insert_version = """
        INSERT INTO redcap_external_module_settings
        SELECT * FROM (SELECT %s, NULL, 'version', 'string', '%s') AS tmp
        WHERE NOT EXISTS (
        SELECT external_module_id, project_id FROM redcap_external_module_settings WHERE external_module_id = %s AND type = 'string'
        ) LIMIT 1;
        """ %(external_module_id, module_version, external_module_id)
            
    with settings(user=env.deploy_user):
        run('mysql -e "%s"' %insert_version)

    # Activate module for an specific project
    if pid != "":
        insert_pid = """
            INSERT INTO redcap_external_module_settings
            SELECT * FROM (SELECT %s as t1, %s as t2, 'enabled' as t3, 'boolean' as t4, 'true' as t5) AS rems
            WHERE NOT EXISTS (
            SELECT * FROM redcap_external_module_settings WHERE external_module_id = %s AND project_id = %s
            ) LIMIT 1;
            """ %(external_module_id, pid, external_module_id, pid)

        with settings(user=env.deploy_user):
            run('mysql -e "%s"' %insert_pid)
    # Activate module for all the projects




def remove_module_from_tables(module_name, module_version, pid):
    """
        Deletes modules from redcap tables
        """
    add_to_redcap_external_modules = """
        INSERT INTO redcap_external_modules (directory_prefix)
        SELECT * FROM (SELECT '%s') AS tmp
        WHERE NOT EXISTS (
        SELECT directory_prefix FROM redcap_external_modules WHERE directory_prefix = '%s'
        ) LIMIT 1;
        """ %(module_name,module_name)
    find_id = """
        SELECT external_module_id FROM redcap_external_modules WHERE directory_prefix='%s';
        """ %(module_name)
    
    with settings(user=env.deploy_user):
        run('mysql -e "%s"' %add_to_redcap_external_modules)
        external_module_id = run('mysql -s -N -e "%s"' %find_id)
    
    # Remove module for an specific project
    if pid != "":
        remove_pid = """
            DELETE FROM redcap_external_module_settings WHERE project_id = %s AND external_module_id = %s LIMIT 1;
            """ %(pid, external_module_id)
        
        with settings(user=env.deploy_user):
            run('mysql -e "%s"' %remove_pid)
    # Remove module for all the projects
    else:
        remove_all = """
            DELETE FROM redcap_external_module_settings WHERE external_module_id = %s;
            """ %(external_module_id)
                
        with settings(user=env.deploy_user):
            run('mysql -e "%s"' %remove_all)
