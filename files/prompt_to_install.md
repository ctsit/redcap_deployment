## Time to install REDCap!

Congratulations!  Your webserver is up.  It's time to install REDCap using the Fabric tools.

Please deploy REDCap using the _fab_ commands below.
They show a sample deployment for REDCap 7.2.2. Change the export command to install
the redcap zip you have copied into the root of the repository.

    export REDCAP_VERSION=7.2.2
    fab vagrant server_setup
    fab vagrant package:redcap$REDCAP_VERSION.zip
    fab vagrant delete_all_tables deploy:redcap-$REDCAP_VERSION.tgz
