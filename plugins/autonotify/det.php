<?php

/*
 *
 * This plugin is designed to help create automatic email notifications when sensitive
 * responses are received from a survey.
 *
 * As of 2016-03-01 Autonotify was modified to store the configuration in the log instead of using the DET query string.
 * This was done to alleviate issues around maximum query string length.  The new version offers the ability to upgrade existing
 * autonitfy configurations on first use.
 *
 * It must be used in conjunction with a data entry trigger to function in real-time.
 * The settings for each project are stored as an encoded variable (an) in the query string of the DET.
 *
 *
 *
 * Andrew Martin, Stanford University, 2016
 *
**/
error_reporting(E_ALL);



// MANUAL LOG FILE
// $log_file = "/Users/andy123/Documents/local REDCap server/redcap/temp/autonotify.log";

// MANUAL OVERRIDE OF HTTPS - Add your url domain to this array if you want to only use http
$http_only = array('stanford.edu');

// OPTIONAL SPECIAL LOG FILE FOR THIS PLUGIN (OTHERWISE WILL WRITE TO REDCAP TEMP)
//$log_file = "/var/log/redcap/autonotify.log";


////////////// DONT EDIT BELOW HERE //////////////

$action = '';   // Script action
##### RUNNING AS DET - PART 1 #####
if ( $_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['redcap_url']) ) {
    $action = 'det';
    define('NOAUTH',true);  // Turn off Authentication - running on server
    $_GET['pid'] = $_POST['project_id'];    // Set the pid from POST so context is Project rather than Global
}

// Include required files
require_once "../../redcap_connect.php";
require_once "common.php";

// If a log file hasn't been set, then let's default to the REDCap temp folder
if (!isset($log_file)) {
    $log_file = APP_PATH_TEMP . "autonotify_plugin.log";
}

// Create an AutoNotify Object
$an = new AutoNotify($project_id);
//error_log("Here");

logIt("Starting AutoNotify on project $project_id");
//logIt("DET URL: " . $an->getDetUrl(), "DEBUG");


##### RUNNING AS DET - PART 2 #####
if ($action == 'det') {
    // Execute AutoNotify script if called from DET trigger
    $an->loadDetPost();
    $an->loadConfig();
    $an->execute();
    exit;
}
