# Deployment README for the REDCap Autonotify Plugin

The deploy.sh script in this can make most of the changes needed to deploy this plug on a Debian Linux host using apache to host REDCap.
However, the data event trigger will need unauthenticated access to det.php.  To turn off authentication for this page while leaving it _on_ for index.php use something like the included file, autonotify.conf.example.  This file is tailored to a shibboleth environment and has IPs that will not apply to your environment even if you do have shibboleth.  You will need to adapt this file for your site's needs.

Deploy.sh creates a folder /etc/apache2/ssl-includes/ and adds a directive in the apache ssl site file to include all *.conf files in /etc/apache2/ssl-includes/.  Place the autonotify.conf for your environment in /etc/apache2/ssl-includes/ and restart apache to test the new directives.
