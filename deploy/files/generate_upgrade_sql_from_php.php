<?php
/*
    Run a redcap upgrade_N.MM.OO.php file against a redcap database
    to generate the resultant sql statements.  The resulting SQL statements
    can be applied to a redcap database as part of a sequence of SQL upgrades
    from an old version to some new version.

    This file must be copied into the redcap/redcap_vN.M.O directory for
    the relative paths to work correctly.

    Input:  This command requires the path to redcap upgrade_N.MM.OO.php as an
            input parameter.

    Output: On success the command will output the resultand SQL statments
            to STDOUT.
            If the input file does not exist the command returns 2

*/

// Included the standard REDCap functions
require_once dirname(__FILE__) . '/Config/init_functions.php';

// Adjust the max time upwards incase processing is lengthy.
System::increaseMaxExecTime(3600);

// Set constants from /root/rc_v.new/upgrade.php to mimic the manual upgrade process
$app_path_webroot_parent = dirname(dirname($_SERVER['PHP_SELF']));
if ($app_path_webroot_parent == DIRECTORY_SEPARATOR) $app_path_webroot_parent = '';
define("APP_PATH_WEBROOT_PARENT", "$app_path_webroot_parent/");
// TODO: this should be APP_PATH_WEBROOT_PARENT . "redcap_v" . env.new . "/"
// this works for now though
define("APP_PATH_WEBROOT", dirname(__FILE__) . DS);
// Declare current page with full path
define("PAGE_FULL", 			$_SERVER['PHP_SELF']);
// Declare current page
define("PAGE", 					basename(PAGE_FULL));
// Docroot will be used by php includes
define("APP_PATH_DOCROOT", 		dirname(__FILE__) . DS);
// Webtools folder path
define("APP_PATH_WEBTOOLS",		dirname(APP_PATH_DOCROOT) . "/webtools2/");
// Classes
define("APP_PATH_CLASSES",  	APP_PATH_DOCROOT . "Classes/");
// Controllers
define("APP_PATH_CONTROLLERS", 	APP_PATH_DOCROOT . "Controllers/");
// Image repository
define("APP_PATH_IMAGES",		APP_PATH_WEBROOT . "Resources/images/");
// CSS
define("APP_PATH_CSS",			APP_PATH_WEBROOT . "Resources/css/");
// External Javascript
define("APP_PATH_JS",			APP_PATH_WEBROOT . "Resources/js/");
// Webpack
define('APP_PATH_WEBPACK', 	    APP_PATH_WEBROOT . "Resources/webpack/");
// Other constants
// Get server name (i.e. domain), server port, and if using SSL (boolean)
list ($server_name, $port, $ssl, $page_full) = getServerNamePortSSL();
define("SERVER_NAME", $server_name);
define("SSL", $ssl);
define("PORT", str_replace(":", "", $port)); // Set PORT as numeric w/o colon
define("APP_PATH_WEBROOT_FULL",		(SSL ? "https" : "http") . "://" . SERVER_NAME . $port . ((strlen(dirname(APP_PATH_WEBROOT)) <= 1) ? "" : dirname(APP_PATH_WEBROOT)) . "/");

// Process and run the translated upgade*.sql file
$input_file = $argv[1];

if (file_exists($input_file)) {
    include $input_file;
} else {
    fwrite(STDERR, "-- WARNING: The file $input_file does not exist. SQL statements could not be generated\n");
    exit(2);
}
