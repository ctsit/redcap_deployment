# redcap-plugin-autonotify
A plugin to send custom notifications based on DET events

In the index.php file, be sure to modify the log location to a suitable path for your server:
```$log_prefix = "/var/log/redcap/autonotify";```

## Installation ##
Typically these files are placed in your root redcap folder as:
/plugins/autonotify/index.php
/plugins/autonotify/common.php

They should be 'outside' your redcap_vx.y.z folders (as siblings).

If you place these files further down or up in the directory structure you will need to modify the:
```require_once "../../redcap_connect.php";``` file by adding or removing "../" to find the redcap_connect file accordingly.

If things do not work out at first, FIND YOUR PHP ERROR LOG!  This is the key to debugging any issues.

## Configure ##
To configure this for your project add a bookmark to the autonotify plugin:
```
/plugins/autonotify/
```

Be sure to check the box to append the current project_id information.

Then click on the new plugin link on the left sidebar.  From here you should be able to create a new autonotify configuration.
Upon saving, it will create a DET url with your encoded settings.  If you have existing DETs, they will be managed inside the
autonotify plugin.

Happy REDCapping!
