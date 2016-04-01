<?php

/**

	This plugin is designed to help create automatic email notifications when sensitive
	responses are received from a survey.

	It must be used in conjunction with a data entry trigger to function in real-time.
	The settings for each project are stored as an encoded variable (an) in the query string of the DET.

**/

// File path and prefix for log file - make sure web user has write permissions
//$log_prefix = "/Users/andy123/Documents/local REDCap server/redcap/temp/autonotify";
$log_prefix = "/var/log/redcap/autonotify";



error_reporting(E_ALL);

$action = '';	// Script action

##### RUNNING AS DET - PART 1 #####
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_GET['an'])) {
	$action = 'det';
	define('NOAUTH',true);	// Turn off Authentication - running on server
	$_GET['pid'] = $_POST['project_id'];	// Set the pid from POST so context is Project rather than Global
}

// Include required files
require_once "../../redcap_connect.php";
require_once "common.php";

// Create an AutoNotify Object
$an = new AutoNotify();

##### RUNNING AS DET - PART 2 #####
if ($action == 'det') {
	// Execute AutoNotify script if called from DET trigger
	$an->loadFromDet();
	$an->execute();
	exit;
}
