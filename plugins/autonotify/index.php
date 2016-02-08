<?php

/**
	
	This plugin is designed to help create automatic email notifications when sensitive
	responses are received from a survey.
	
	It must be used in conjunction with a data entry trigger to function in real-time.
	The settings for each project are stored as an encoded variable (an) in the query string of the DET.

**/

error_reporting(E_ALL);
// File path and prefix for log file - make sure web user has write permissions
$log_prefix = "/var/log/redcap/autonotify";
//$log_prefix = "/Users/andy123/Documents/local REDCap server/redcap/temp/autonotify";

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


##### VALIDATION #####
# Make sure user has permissions for project or is a super user
$these_rights = REDCap::getUserRights(USERID);
$my_rights = $these_rights[USERID];
if (!$my_rights['design'] && !SUPER_USER) {
	showError('Project Setup rights are required to add/modify automatic notifications');
	exit;
}
# Make sure the user's rights have not expired for the project
if ($my_rights['expiration'] != "" && $my_rights['expiration'] < TODAY) {
	showError('Your user account has expired for this project.  Please contact the project admin.');
	exit;
}

##### TEST POST #####
# Check to see if we are running a test if the logic (called from AJAX - be sure to include PID in ajax call!)
# logic = condition to be tested
# record = record to test with
# ** TO BE IMPROVED **
if (isset($_POST['test']) && $_POST['test']) {
	logIt('REQUEST:',print_r($_REQUEST,true),'DEBUG');
	$logic = htmlspecialchars_decode($_POST['logic'], ENT_QUOTES);
	$record = $_POST['record'];
	$event_id = $_POST['event_id'];
	$an->record = $record;
	$an->redcap_event_name = REDCap::getEventNames(TRUE,FALSE,$event_id);
//	logIt('AN:',print_r($an,true),'DEBUG');
	echo $an->testLogic($logic);
	exit;
}

#### ADD TRIGGER ####
# Called by Ajax
if (isset($_POST['addTrigger'])) {
	$index = $_POST['addTrigger'] + 1;
	echo AutoNotify::renderTrigger($index);
	exit;
}


##### BEGIN NORMAL PAGE RENDERING #####
# Display the project header
require_once APP_PATH_DOCROOT . 'ProjectGeneral/header.php';

# Inject the plugin tabs (must come after including tabs.php)
include APP_PATH_DOCROOT . "ProjectSetup/tabs.php";
injectPluginTabs($pid, $_SERVER["REQUEST_URI"], 'AutoNotify');


# Check to see if we are saving a previously posted trigger
if (isset($_POST['save']) && $_POST['save']) {
	// Save Trigger
	//	echo ("POST: <pre>".print_r($_POST,true));
	$params = $_POST;
	unset($params['save']);
	$params['last_saved'] = date('y-m-d h:i:s');
	$params['modified_by'] = USERID;
	$encoded = $an->encode($params);
	$an->updateDetUrl($encoded);
	renderTemporaryMessage('The automatic notification has been updated', 'Automatic Notification Saved');
}

# Load an existing template from the DET if present in the query string
if (!empty($data_entry_trigger_url)) {
	$query = parse_url($data_entry_trigger_url, PHP_URL_QUERY);
	if ($query) parse_str($query,$params);
	$config_encoded = isset($params['an']) ? $params['an'] : '';

	if ($config_encoded) {
		$an->loadEncodedConfig($config_encoded);
	} else {
		$html = RCView::div(array('id'=>$id,'class'=>'red','style'=>'margin-top:20px;padding:10px 10px 15px;'),
				RCView::div(array('style'=>'text-align:center;font-size:20px;font-weight:bold;padding-bottom:5px;'), "Warning: Existing DET Defined").
				RCView::div(array(), "A data entry trigger was already defined for this project: <b>$data_entry_trigger_url</b><br>If you save this AutoNotification configuration you will replace this DET.  Your old DET has been moved to the pre-notification area and will be executed before this script unless otherwise changed.")
		);
		echo $html;
		$an->config['pre_script_det_url'] = $data_entry_trigger_url;
	}
}


######## HTML PAGE ###########
?>
<style type='text/css'>
	td.td1 {vertical-align:text-top;}
	td.td2 {vertical-align:text-top; padding-top: 5px; padding-right:15px; width:70px;}
	td.td2 label {font-variant:small-caps; font-size: 12px;}
	div.desc {font-variant:normal; font-style:italic; font-size: smaller; padding-top:5px; width:70px;}
	table.tbi input {width: 500px; display: inline; height:20px}
	table.tbi input[type='radio'] {width: 14px; display: normal;}
	table.tbi textarea {width: 500px; display:inline; height:50px;}
</style>

<?php

$instructions = "The Auto-Notification plugin is tested each time a record is saved in your project.  When the condition is 'true' a message will be sent as configured.  A message is written to the log recording the record, event, and name of the trigger.  A given record-event-trigger will only be fired once.";

$section = $an->renderTriggers().
	RCView::div(array(),
		RCView::button(array('class'=>'jqbuttonmed ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only','onclick'=>'javascript:addTrigger();'), RCView::img(array('src'=>'add.png', 'class'=>'imgfix')).' Add another trigger')
	).
RCView::div(array('class'=>'round chklist','id'=>'notification_config'),
	// Alert Message
	RCView::div(array('class'=>'chklisthdr','style'=>'color:rgb(128,0,0);margin-top:10px;'), "Configure Notification Email").
	RCView::p(array(), 'This notification email will include a link to the record and will therefore include the value of the '.REDCap::getRecordIdField().' field.  For this reasons, this first field <b>SHOULD NOT INCLUDE PHI</b>.  It is recommended to use an auto-numbering first field as best practice and include PHI as a secondary identifier.').
	RCView::table(array('cellspacing'=>'5', 'class'=>'tbi'),
		AutoNotify::renderRow('to','To',$an->config['to']).
		AutoNotify::renderRow('from','From',$an->config['from']).
		AutoNotify::renderRow('subject','Subject',(empty($an->config['subject']) ? 'SECURE:' : $an->config['subject'])).
		AutoNotify::renderRow('message','Message',$an->config['message'])
	)
).
RCView::div(array('class'=>'round chklist','id'=>'det_config'),
	// Pre and Post AutoNotification -DAG URL to be executed
	RCView::div(array('class'=>'chklisthdr','style'=>'color:rgb(128,0,0);margin-top:10px;'), "Pre- and Post- AutoNotification DET Triggers").
	RCView::p(array(), 'You can run additional Data Entry Triggers before or after this auto-notification test by inserting a comma-separated list of complete DET urls below.<br><i>Please note that these DET urls will be called each time this DET is called, whether the conditional logic evaluates to true or not.</i>').
	RCView::table(array('cellspacing'=>'5', 'class'=>'tbi'),
		AutoNotify::renderRow('pre_script_det_url','Pre-notification DET Url',$an->config['pre_script_det_url']).
		AutoNotify::renderRow('post_script_det_url','Post-notification DET Url',$an->config['post_script_det_url'])
	)
	
);

$page = RCView::div(array('class'=>'autonotify_config'),
	RCView::h3(array(),'AutoNotify: a DET-based Notification Plugin').
	$section.
	RCView::div(array(),
		RCView::button(array('class'=>'jqbuttonmed ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only','onclick'=>'javascript:save();'), RCView::img(array('src'=>'bullet_disk.png', 'class'=>'imgfix')).'<b>Save Configuration</b>').
		" ".
		RCView::button(array('class'=>'jqbuttonmed ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only','onclick'=>'javascript:refresh();'), 'Refresh')
	)
);

print $page;
print AutoNotify::renderHelpDivs();


?>

<script type="text/javascript">

	// Take all input elements inside our autonotify_config div and post them to this page
	function save() {
		var params = new Object;	// Info to save
		// Loop through each trigger
		var triggers = new Object;
		i=0;
		$('div.trigger', '#triggers_config').each (function (index1, value1) {
			i++;
			triggers[i] = new Object;
			$('*:input', $(this)).each (function (index2, value2) {
				// Skip buttons or other attributes that don't have an ID
				if ($(this).attr('id')) {
					// Replace any -x suffix in the stored array (e.g. logic-1 becomes logic)
					triggers[i][$(this).attr('id').replace(/\-\d/,'')] = $(this).val();
				}
			});
			triggers[i]['enabled'] = $('input[name^=enabled]:checked', $(this)).val();
		});
		params['triggers'] = JSON.stringify(triggers);
		
		// Get the notification settings
		$('*:input', '#notification_config').each (function (index, value) {
			if ($(this).attr('id')) params[$(this).attr('id')] = $(this).val();
		});
		
		// Get the DET settings
		$('*:input', '#det_config').each (function (index, value) {
			if ($(this).attr('id')) params[$(this).attr('id')] = $(this).val();
		});
		params['save'] = 1;
		//if (confirm('Press OK to SAVE')) {
		//	console.log(params);
			post('', params);
		//}
	}

	function refresh() {
		window.location = window.location.href;
	}
	
	function addTrigger() {
		max = 0;
		$('div.trigger', '#triggers_config').each(
			function (index,value) {
				idx = parseInt($(this).attr('idx'));
				if (idx > max) {
					max = idx;
				};
			}
		);
		$.post('',{addTrigger: max, project_id: pid },
			function(data) {
				//alert (data_entry_trigger_url);
				$('#triggers_config').append(data);
				updatePage();
			}
		);
	}

	function removeTrigger(id) {
		//console.log('Remove Trigger');
		if ($('div.trigger').length == 1) {
			alert ('You can not delete the last trigger.');
		} else {
			$('div.trigger[idx='+id+']').remove();
		}
	}

	function testLogic(trigger) {
		var record = $('#test_record-'+trigger).val();
		var event_id = $('#test_event-'+trigger).val();
		var logic = $('#logic-'+trigger).val();
		var dest = $('#result-'+trigger);
		$(dest).html('<img src="'+app_path_images+'progress_circle.gif" class="imgfix"> Evaluating...');
		//console.log(dest);
		//console.log('Trigger ' + trigger + ' with record ' + record + ' with logic ' + logic);
		$.post('',{test: 1, record: record, event_id: event_id, logic: logic, project_id: pid },
			function(data) {
				var msg = data;
				$(dest).html(msg);
			}
		);
	}

	// Post to the provided URL with the specified parameters.
	function post(path, params) {
		var form = $('<form></form>');
		form.attr("method", "POST");
		form.attr("action", path);
		$.each(params, function(key, value) {
			var field = $('<input />');
			field.attr("type", "hidden");
			field.attr("name", key);
			field.attr("value", value);
			form.append(field);
		});
		// The form needs to be a part of the document in
		// order for us to be able to submit it.
		$(document.body).append(form);
		form.submit();
	}

	function updatePage() {
		// Prepare help buttons
		$('a.info').off('click').click(function(){
			var e = $(this).attr("info");
			$('#'+e).dialog({ title: 'AutoNotification Help', bgiframe: true, modal: true, width: 400, 
				open: function(){fitDialog(this)}, 
				buttons: { Close: function() { $(this).dialog('close'); } } });
		});		
		$('#title').css('font-weight','bold');
	}

	// Add click event to all help buttons to show help
	$(document).ready(function() {
		updatePage();
	});
</script>

<?php
//Display the project footer
require_once APP_PATH_DOCROOT . 'ProjectGeneral/footer.php';
?>
