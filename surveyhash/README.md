# Survey Hash Plugin *Created by Luke Stevens*
#### Stewart Wehmeyer, UF CTS-IT

## Description

This plugin lets you search for a project and associated record form a survey hash. Note: the survey hash is the alphanumeric string at the end of the survey url. For example, http://redcap.dev/redcap/surveys/index.php?s=p2YusQVmxe is the url a customer sees while taking a survey. The portion after index.php?s= is the survey hash, i.e., "p2YusQVmxe". With this plugin, you can put a hash into the survey hash serach bar in order to find the associated project, survey, and record. The survey also provides the pid of the project and links to: the project setup page, the online designer page, and the data entry form for the specific record. This is especially helpful when a customer sends a survey url, without a project name, in a help request.

![Image of Survey Hash Hook](https://github.com/StewartUF/redcap_deployment/blob/develop/surveyhash/search_result_image.png)

## Requirements

This plugin requires a working instance of REDCap and needs to be placed in the appropriate plugins directory. As of 6/15/2017, use at UF requires only a very minor change to the original index.php file. The require_once needs to point to `require_once("/var/www/redcap/redcap_connect.php");`

### TO-DO

Alter the require_once variable to be "<redcap_dir>/redcap_connect.php".