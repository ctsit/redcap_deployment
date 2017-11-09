# Deployment README for the REDCap Autonotify3 Plugin

The `deploy.sh` script in this can make most of the changes needed to deploy this plugin on a Debian Linux host using apache to host REDCap.
However, the data event trigger will need unauthenticated access to index.php. To turn off authentication for this page, you can use the apache configuration file `99-<instance_name>-autonotify3.conf.example` as an example. This file is tailored to a shibboleth environment and has IPs that will not apply to your environment even if you do have shibboleth. You will need to adapt this file for your site's needs.

The `post-deploy.sh` script creates a folder `/etc/apache2/ssl-includes/` and adds a directive in the apache ssl file to include all `*.conf` files in `/etc/apache2/ssl-includes/`.  Place the `99-<instance_name>-autonotify3.conf` for your environment in `/etc/apache2/ssl-includes/` and restart apache to test the new directives.
