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

$action = '';	// Script action
##### RUNNING AS DET - PART 1 #####
if ( $_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['redcap_url']) ) {
    $action = 'det';
    define('NOAUTH',true);	// Turn off Authentication - running on server
    $_GET['pid'] = $_POST['project_id'];	// Set the pid from POST so context is Project rather than Global
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
    $index = intval($_POST['addTrigger']) + 1;
    echo AutoNotify::renderTrigger($index);
    exit;
}


#### VIEW LOG ####
# Called by Ajax
if (isset($_POST['viewLog'])) {
    global $project_id;
    $project_id = $an->project_id;
    viewLog($log_file);
    exit;
}


##### BEGIN NORMAL PAGE RENDERING #####
# Display the project header
require_once APP_PATH_DOCROOT . 'ProjectGeneral/header.php';

# Inject the plugin tabs (must come after including tabs.php)
include APP_PATH_DOCROOT . "ProjectSetup/tabs.php";
injectPluginTabs($pid, $_SERVER["REQUEST_URI"], 'AutoNotify');


// Super user warnings
if (defined('SUPER_USER') && SUPER_USER) {
    if (!file_exists($log_file)) {
        $msg = "The log file for this plugin <b>$log_file</b> does not appear to exist.  If this path is correct, try refreshing the page.<br>
  				If this error recurs, then:<br>
					- Make sure the directory is correct - you can change it by modifying the source code of this file: <b>" . __FILE__ . "</b><br>
					- Make sure your webserver has permissions to write to <b>$log_file</b><br>
					- If you do not want to log, you can set the variable to empty, e.g. (<code>\$log_file = ''</code>) to stop plugin logging.<br><br>
					<i>This warning message is only displayed to SuperUsers</i>";
        $html = RCView::div(array('id'=>$id,'class'=>'red','style'=>'margin-top:20px;padding:10px 10px 15px;'),
            RCView::div(array('style'=>'text-align:center;font-size:20px;font-weight:bold;padding-bottom:5px;'), "Log File Warning").
            RCView::div(array(), $msg)
        );
        print $html;
    } else {
        $msg = "As a super user, you can view the AutoNotify log to help troubleshoot: <button class='jqbutton ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only' name='viewLog'>View Log</button>";
        $html = RCView::div(array('id'=>$id,'class'=>'yellow','style'=>'margin-top:20px;padding:10px 10px 15px;'),
            RCView::div(array('style'=>'text-align:center;font-size:20px;font-weight:bold;padding-bottom:5px;')).
            RCView::div(array(), $msg)
        );
        print $html;
    }
}

# Check to see if we are saving a previously posted trigger
if (isset($_POST['save']) && $_POST['save']) {
//	logIt(__FUNCTION__ . ": POST: ".print_r($_POST,true), "DEBUG");

    // Build Parameters
    $params = $_POST;
    unset($params['save']);
    $params['last_saved'] = date('Y-m-d h:i:s');
    $params['modified_by'] = USERID;
    $an->config = $params;
    $an->saveConfig();
    renderTemporaryMessage('The automatic notification has been updated', 'Automatic Notification Saved');
}

# Load the Configuration if present
if ( $an->loadConfig() ) {
//	renderTemporaryMessage("Existing Auto Notify configuration loaded");
} else {
    renderTemporaryMessage("To create an Auto Notify configuration, complete the form below and save", "New " . AutoNotify::PluginName . " Configuration");
};

# Load an existing template from the DET if present in the query string
global $data_entry_trigger_url;
if ( !empty($data_entry_trigger_url) && $an->isDetUrlNotAutoNotify() ) {
    $msg = "It appears you may have an existing DET url: <b>$data_entry_trigger_url</b><br/></br>Autonotify needs to use your DET url to function and upon saving will set it to <b>" . $an->getDetUrl() . "</b><br/><br/>
		";
    if ( isset($an->config['pre_script_det_url']) && !empty ($an->config['pre_script_det_url']) ) {
        // We have a different DET url AND we already have a pre-script_det_url...
        $msg .= "Since you already have a Pre-AutoNotify DET URL configured, your existing DET will be lost unless you copy it to one of the DET url locations below.";
    } else {
        $msg .= "To preserve your existing DET url,  it must be copied to the Pre-AutoNotification DET Url input at the bottom of this form.<br>
				<button class='jqbuttonmed ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only' name='copyDet' data-url='$data_entry_trigger_url'>Move existing DET to this AutoNotify config</button>";
        //$an->config['pre_script_det_url'] = $data_entry_trigger_url;
    }

    $html = RCView::div(array('id'=>$id,'class'=>'red','style'=>'margin-top:20px;padding:10px 10px 15px;'),
        RCView::div(array('style'=>'text-align:center;font-size:20px;font-weight:bold;padding-bottom:5px;'), "Warning: Existing DET Defined").
        RCView::div(array(), $msg)
    );
    echo $html;
}

######## HTML PAGE ###########
?>
<style type='text/css'>
    td.td1 {vertical-align:text-top;}
    td.td2 {vertical-align:text-top; padding-top: 5px; padding-right:15px; width:70px;}
    td.td2 label {font-variant:small-caps; font-size: 12px;}
    td.td3 {vertical-align:middle;}
    div.desc {font-variant:normal; font-style:italic; font-size: smaller; padding-top:5px; width:70px;}
    table.tbi input {width: 500px; display: inline; height:20px}
    table.tbi input[type='radio'] {width: 14px; display: normal;}
    table.tbi textarea {width: 500px; display:inline; height:50px;}
    .modified {	font-style: italic; color: #9a9faa }
    .radio-option {margin-right: 10px; margin-bottom: 5px; position:relative; top:-5px;}
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
        RCView::p(array(), 'You can run additional Data Entry Triggers before or after this auto-notification test by inserting a pipe-separated (e.g. | char) list of complete DET urls below.<br><i>Please note that these DET urls will be called each time this DET is called, whether the conditional logic evaluates to true or not.</i>').
        RCView::table(array('cellspacing'=>'5', 'class'=>'tbi'),
            AutoNotify::renderRow('pre_script_det_url','Pre-notification DET Url',$an->config['pre_script_det_url']).
            AutoNotify::renderRow('post_script_det_url','Post-notification DET Url',$an->config['post_script_det_url'])
        )

    );

$last_modified = "<div class='modified'>" . ( empty($an->config['last_saved']) ? "This configuration has not been saved" : "Last saved " . $an->config['last_saved'] . " by " . $an->config['modified_by'] ) . "</div>";

$page = RCView::div(array('class'=>'autonotify_config'),
    RCView::h3(array(),'AutoNotify: a DET-based Notification Plugin').
    $last_modified.
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

    function save() {
        var params = new Object;	// Info to save
        // Loop through each trigger
        var triggers = new Object;
        i=0;
        $('div.trigger', '#triggers_config').each (function (index1, value1) {
            i++;
            triggers[i] = new Object;

            // Loop through each input inside the trigger
            $('*:input', $(this)).each (function (index2, value2) {
                // Skip buttons or other attributes that don't have an ID
                if ($(this).attr('id')) {
                    // Replace any -x suffix in the stored array (e.g. logic-1 becomes logic)
                    triggers[i][$(this).attr('id').replace(/\-\d+/,'')] = $(this).val();
                }
            });
            triggers[i]['enabled'] = $('input[name^=enabled]:checked', $(this)).val();
            triggers[i]['scope'] = $('input[name^=scope]:checked', $(this)).val();
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
        post('', params);
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

        $('button[name="copyDet"').bind('click',function() {
            $('#pre_script_det_url').val($(this).data("url")).effect("highlight", {}, 1500);
        });

        $('button[name="viewLog"').bind('click',function() {
            post('', {viewLog: 1, pid: pid});
        });
    });
</script>

<?php
//Display the project footer
require_once APP_PATH_DOCROOT . 'ProjectGeneral/footer.php';
?>
