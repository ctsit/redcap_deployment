<?php

/** 
	This is a custom PDF download plugin that is basically a copy of the REDCap code with a few tweaks
	
	You can supply a few optional parameters to specify the form(s) you want to summarize.
	By default, blank fields are not included in the PDF and unchecked options are also skipped.  This helps compact the output.
	
	If you want to include a field even if it is blank, you should append a comma-separated list of fields with the
		always_include parameter.
	
	If you want to exclude a field no matter what, you should append a comma-separated list of fields with the
		always_exclude parameter
	
	To specify which forms, you can use 'all' for all forms, '' for current form, or a comma-separated list for specified forms:
		forms=all (for all forms)
		forms=form_name1, form_name2
	
	
	Example Usage:
	
	https://redcap.stanford.edu/plugins/pdf_modified/index.php
		?forms=all
		&always_exclude=record_id,division_mgr_summary,faculty_review_summary,cf_sunet,cf_sid,cf_wrvu_fy14,cf_wrvu_fy14_inpt,cf_wrvu_fy14_oupt,
			cf_wrvu_fy14_proc,cf_visit_fy14,cf_newvis_fy14,cf_retvis_fy14,cf_consult_vis_fy14,cf_tot_fte_fy14,cf_cfte_fy14,cf_tfte_fy14,
			cf_rfte_fy14,cf_afte_fy14,cf_ofte_fy14,cfa_comments
		&always_include=chief_attest,chief_signature,review_date,chief_comments
**/

// Call the REDCap Connect file in the main "redcap" directory
require_once "../../redcap_connect.php";
//include APP_PATH_DOCROOT . '/ProjectGeneral/header.php';

$project_id = isset($_GET['pid']) ? $_GET['pid'] : '';
$record = isset($_GET['record']) ? $_GET['record'] : '';
$forms = isset($_GET['forms']) ? $_GET['forms'] : '';
$always_include = isset($_GET['always_include']) ? $_GET['always_include'] : '';
$always_exclude = isset($_GET['always_exclude']) ? $_GET['always_exclude'] : '';

//$keep_fields is array of all fields that should be printed, incorporating those that are populated with those that are forced included and excluded.
$keep_fields = array();

if (!$record) {
	displayMessage("<b>ERROR:</b> This must be called from a particular record.  Please select a participant first and then press the link again or check that the bookmark link has the record and project boxes checked.");
	exit;
}

// Must have PHP extention "mbstring" installed in order to render UTF-8 characters properly AND also the PDF unicode fonts installed
$pathToPdfUtf8Fonts = APP_PATH_WEBTOOLS . "pdf" . DS . "font" . DS . "unifont" . DS;
if (function_exists('mb_convert_encoding') && is_dir($pathToPdfUtf8Fonts)) {
	// Define the UTF-8 PDF fonts' path
	define("FPDF_FONTPATH",   APP_PATH_WEBTOOLS . "pdf" . DS . "font" . DS);
	define("_SYSTEM_TTFONTS", APP_PATH_WEBTOOLS . "pdf" . DS . "font" . DS);
	// Set contant
	define("USE_UTF8", true);
	// Use tFPDF class for UTF-8 by default
	if ($project_encoding == 'chinese_utf8') {
		require_once APP_PATH_CLASSES . "PDF_Unicode.php";
	} else {
		require_once APP_PATH_CLASSES . "tFPDF.php";
	}
} else {
	// Set contant
	define("USE_UTF8", false);
	// Use normal FPDF class
	require_once APP_PATH_CLASSES . "FPDF.php";
}
// If using language 'Japanese', then use MBFPDF class for multi-byte string rendering
if ($project_encoding == 'japanese_sjis')
{
	require_once APP_PATH_CLASSES . "MBFPDF.php"; // Japanese
	// Make sure mbstring is installed
	if (!function_exists('mb_convert_encoding'))
	{
		exit("ERROR: In order for multi-byte encoded text to render correctly in the PDF, you must have the PHP extention \"mbstring\" installed on your web server.");
	}
}

// Include other files needed
require_once APP_PATH_DOCROOT . 'ProjectGeneral/form_renderer_functions.php';
require_once APP_PATH_DOCROOT . "PDF/functions.php"; // This MUST be included AFTER we include the FPDF class

// Set the text that replaces data for de-id fields
define("DEID_TEXT", "[*DATA REMOVED*]");

/***************************************************/
$_GET['id']=$record;

$included = array_map('trim',explode(",",$always_include));
$excluded = array_map('trim',explode(",",$always_exclude));

$piping_record_data = (isset($Data[''])) ? array() : Records::getData('array', array_keys($Data));
//echo "<hr><pre> PIPING RECORD DATA:  ".print_r($piping_record_data,true)."</pre>";

$referer = $_SERVER['HTTP_REFERER'];

//get page from referer
preg_match('/.*&page=([\w]*).*/',
$referer, $matches);
$page = $matches[1];

if ($page) {
	$_GET['page']=$page;
}

//get event_id from referer
preg_match('/.*&event_id=([\w]*).*/',
$referer, $matches);
$event_id = $matches[1];

if (!$event_id) {
	$event_id = getSingleEvent($project_id);
}
$_GET['event_id']=$event_id;


/***************************************************/


// Save fields into metadata array
$draftMode = false;
if ($forms=='all') {
	$Query = "select * from redcap_metadata where project_id = $project_id and
	(field_name != concat(form_name,'_complete') or field_name = '$table_pk') order by field_order";
	
} else {
	// Check if we should get metadata for draft mode or not
	$draftMode = ($status > 0 && isset($_GET['draftmode']));
	$metadata_table = ($draftMode) ? "redcap_metadata_temp" : "redcap_metadata";
	// Make sure form exists first
	if ((!$draftMode && !isset($Proj->forms[$_GET['page']])) || ($draftMode && !isset($Proj->forms_temp[$_GET['page']]))) {
		exit('ERROR!');
	}
	$Query = "select * from $metadata_table where project_id = $project_id and ((form_name = '{$_GET['page']}'
	and field_name != concat(form_name,'_complete')) or field_name = '$table_pk') order by field_order";
	
}

$QQuery = db_query($Query);
$metadata = array();
while ($row = db_fetch_assoc($QQuery))
{
	// If field is an "sql" field type, then retrieve enum from query result
	if ($row['element_type'] == "sql") {
		$row['element_enum'] = getSqlFieldEnum($row['element_enum']);
	}
	// If PK field...
	if ($row['field_name'] == $table_pk) {
		// Ensure PK field is a text field
		$row['element_type'] = 'text';
		// When pulling a single form other than the first form, change PK form_name to prevent it being on its own page
		if (isset($_GET['page'])) {
			$row['form_name'] = $_GET['page'];
		}
	}
	// Store metadata in array
	$metadata[] = $row;
}


// In case we need to output the Draft Mode version of the PDF, set $Proj object attributes as global vars
if ($draftMode) {
	$ProjMetadata = $Proj->metadata_temp;
	$ProjForms = $Proj->forms_temp;
	$ProjMatrixGroupNames = $Proj->matrixGroupNamesTemp;
} else {
	$ProjMetadata = $Proj->metadata;
	$ProjForms = $Proj->forms;
	$ProjMatrixGroupNames = $Proj->matrixGroupNames;
}

// Initialize values
$Data = array();
$study_id_event = "";
$logging_description = "Download data entry form as PDF" . (isset($_GET['id']) ? " (with data)" : "");

$id = trim($_GET['id']);

// Check export rights
if ((isset($_GET['id']) || isset($_GET['allrecords'])) && $user_rights['data_export_tool'] == '0') {
	exit($lang['data_entry_233']);
}

if ($forms=='all') {
	// GET SINGLE RECORD'S DATA (ALL FORMS/ALL EVENTS)
	
	// Set logging description
	$logging_description = "Download all data entry forms as PDF (with data)";
	// Get all data for this record
	$Data = Records::getData('array', $_GET['id'], array(), array(), $user_rights['group_id']);
	if (!isset($Data[$_GET['id']])) $Data = array();	
	
} else {
// GET SINGLE RECORD'S DATA (SINGLE FORM ONLY)
// Ensure the event_id belongs to this project, and additionally if longitudinal, can be used with this form
if (isset($_GET['event_id'])) {
	if (!$Proj->validateEventId($_GET['event_id'])
			// Check if form has been designated for this event
			|| !$Proj->validateFormEvent($_GET['page'], $_GET['event_id'])
			|| ($id == "") )
	{
		if ($longitudinal) {
			redirect(APP_PATH_WEBROOT . "DataEntry/grid.php?pid=" . PROJECT_ID);
		} else {
			redirect(APP_PATH_WEBROOT . "DataEntry/index.php?pid=" . PROJECT_ID . "&page=" . $_GET['page']);
		}
	}
}
// Get all data for this record
$Data = Records::getData('array', $id, array_merge(array($table_pk), array_keys($Proj->forms[$_GET['page']]['fields'])),
		(isset($_GET['event_id']) ? $_GET['event_id'] : array()), $user_rights['group_id']);

}

if (!isset($Data[$id])) $Data = array();

//make a metadata_lookup to 
$metadata_lookup = array();

foreach ($metadata as $index => $value) {
	$metadata_lookup[$value['field_name']] = $index;
}

##XXYJL: SUPPRESS ANY BLANKS
if (!isset($Data[''])) {
	foreach ($Data as $this_record=>&$event_data) {
		foreach ($event_data as $this_event_id=>&$field_data) {
			foreach ($field_data as $this_field=>$this_value) {
				// If value is  blank, unset it
				if ($this_value == '') {
					unset($Data[$this_record][$this_event_id][$this_field]);
				}
			}
			//unset any always_exclude
			foreach ($excluded as &$value) {
				unset($Data[$this_record][$this_event_id][$value]);			
			}
			
			$keep_fields = array_unique(array_merge(array_keys($field_data), $included));

		}
	}
}

## REFORMAT DATES AND/OR REMOVE DATA VALUES FOR DE-ID RIGHTS
if (!isset($Data[''])) {
	// Get all validation types to use for converting DMY and MDY date formats
	$valTypes = getValTypes();
	$dateTimeFields = $dateTimeValTypes = array();
	foreach ($valTypes as $valtype=>$attr) {
		if (in_array($attr['data_type'], array('date', 'datetime', 'datetime_seconds'))) {
			$dateTimeValTypes[] = $valtype;
		}
	}
	// Create array of MDY and DMY date/time fields
	$field_names = array();
	foreach ($metadata as $attr) {
		$field_names[] = $attr['field_name'];
		if (in_array($attr['element_validation_type'], $dateTimeValTypes)) {
			$dateFormat = substr($attr['element_validation_type'], -3);
			if ($dateFormat == 'mdy' || $dateFormat == 'dmy') {
				$dateTimeFields[$attr['field_name']] = $dateFormat;
			}
		}
	}
	// If user has de-id rights, then get list of fields
	$deidFieldsToRemove = ($user_rights['data_export_tool'] > 1)
	? DataExport::deidFieldsToRemove($field_names, ($user_rights['data_export_tool'] == '3'))
	: array();
	$deidFieldsToRemove = array_fill_keys($deidFieldsToRemove, true);
	unset($field_names);
	// Set flags
	$checkDateTimeFields = !empty($dateTimeFields);
	$checkDeidFieldsToRemove = !empty($deidFieldsToRemove);
	// Loop through all data values
	if ($checkDateTimeFields || $checkDeidFieldsToRemove) {
		foreach ($Data as $this_record=>&$event_data) {
			foreach ($event_data as $this_event_id=>&$field_data) {
				foreach ($field_data as $this_field=>$this_value) {
					// If value is not blank
					if ($this_value != '') {
						// If a DMY or MDY datetime field, then convert value
						if ($checkDeidFieldsToRemove && isset($deidFieldsToRemove[$this_field])) {
							// If this is the Record ID field, then merely hash it IF the user has de-id or remove identifiers export rights
							if ($this_field == $Proj->table_pk) {
								if ($Proj->table_pk_phi) {
									$Data[$this_record][$this_event_id][$this_field] = md5($salt . $this_record . $__SALT__);
								}
							} else {
								$Data[$this_record][$this_event_id][$this_field] = DEID_TEXT;
							}
						}
						// If a DMY or MDY datetime field, then convert value
						elseif ($checkDateTimeFields && isset($dateTimeFields[$this_field])) {
							$Data[$this_record][$this_event_id][$this_field] = DateTimeRC::datetimeConvert($this_value, 'ymd', $dateTimeFields[$this_field]);
						}
					}
				}
			}
		}
	}
}


// If form was downloaded from Shared Library and has an Acknowledgement, render it here
$acknowledgement = getAcknowledgement($project_id, $_GET['page']);

//XXYJL: Remove all metadata that don't have a corresponding data 
$metadata = array_filter($metadata,"blankFilter") ;

//if Data is an [element_type] => SELECT or RADIO, then check metadata and suppress the unset fields
foreach ($metadata as &$attr) {
	
	$field = $attr['field_name'];
	
	//IF TYPE IS SELECT/RADIO, CONVERT IT TO TEXT
	if ((($attr['element_type']=='select') or ($attr['element_type']=='radio') or ($attr['element_type']=='yesno')) and (!in_array($field,$included))) {
		//$enum is the choice label values
		$enum = explode('\n',$attr['element_enum']);
		
		if ($attr['element_type']=='yesno') {
			$enum[] = '0, No';
			$enum[] = '1, Yes';
		}
				
		//$target is the coded value of this choice
		$target = $Data[$record][$event_id][$field];
		
		//go through enum and set the $attr[element_enum] to be the correct one
		foreach ($enum as $val) {
			//parse out the code from the choice label (ex: 1, Some String)
			//Don't use explode as sometimes there are commas in string
			preg_match('/(\d+),(.*)/', $val,$matches);
			$radio = array($matches[1],trim($matches[2]));
		  
		  	if ($radio[0]==$target) {
		  		//We are going to convert to text field in an effort to remove the [x]
		  		//And replace the $Data field to be the choice value (with code removed)
		  		$attr['element_type']='text';
		  		$Data[$record][$event_id][$field]=trim($radio[1]);
		  	} 
		  
		}
	}
	
	//IF TYPE IS CHECKBOX AND ANY WERE CHECKED: remove all whose values are 0
	if (($attr['element_type']=='checkbox') and (!in_array($field,$included))) {
		//Check that any were selected
		$enums = parseEnum($attr['element_enum']);
		if (!in_array(1, $Data[$record][$event_id][$field])) {
			
			unset($Data[$record][$event_id][$field]);
			unset($metadata[$metadata_lookup[$field]]);
	    } else {	
		
		$target = $Data[$record][$event_id][$field];

		//Unset all checkboxes which are set to 0
		foreach ($Data[$record][$event_id][$field] as $i => $value) {
			if ($value == 0) {	
				unset($Data[$record][$event_id][$field][$i]);
			}				
		}

		//$checked_off are the ones that have been set
		$checked_off = array_keys($Data[$record][$event_id][$field]);

		//$enum is the choice label values
		$enum = explode('\n',$attr['element_enum']);

		$new_value = array();
				
		foreach ($enum as $val) {				
			preg_match('/(\d+),(.*)/', $val,$matches);
			$checkbox = array($matches[1],trim($matches[2]));

//			echo "<hr><pre> KEEPTHESE:  ".print_r($checked_off,true)."</pre>"; 
			if (in_array($checkbox[0],$checked_off)) {
				if ($checkbox[1] != '') {						
					// IF there are any piped values, replace them here
					$foo = strip_tags(Piping::replaceVariablesInLabel($checkbox[1], $record, $event_id, $piping_record_data));
//					echo "<hr><pre> AFTER".print_r($foo, true)."</pre>";
				}				
				$new_value[] = print_r($foo, true);
			} 
		}
		
		//Convert to text field in an effort to remove the [x]
		//And replace the $Data field to be the choice value (with code removed)
		$attr['element_type']='text';
		$attr['element_enum'] = '';
		$Data[$record][$event_id][$field]=implode('&#xA;', $new_value);
	    }
	}

}

 
  
// Loop through metadata and replace any &nbsp; character codes with spaces
foreach ($metadata as &$attr) {
	$attr['element_label'] = str_replace('&nbsp;', ' ', $attr['element_label']);
	$attr['element_enum'] = str_replace('&nbsp;', ' ', $attr['element_enum']);
	//$attr['element_note'] = str_replace('&nbsp;', ' ', $attr['element_note']);
	//suppress all element_note;
	unset($attr['element_note']);
	$attr['element_preceding_header'] = str_replace('&nbsp;', ' ', $attr['element_preceding_header']);
}

// Logging (but don't do it if this script is being called via the API or via a plugin)
if (!defined("API") && !defined("PLUGIN")) {
	log_event("","redcap_metadata","MANAGE",$_GET['page'],"form_name = '{$_GET['page']}'",$logging_description);
}


//   echo "<hr><pre>".print_r($metadata,true)."</pre>";
//   echo "<hr><pre> DATA: ".print_r($Data,true)."</pre>";

// exit;

if ($forms=='all') {
	$filename=formatFilename(strip_tags(label_decode($app_title)));
} else {
	$filename = formatFilename(strip_tags(label_decode($page)));	
}

// Render the PDF
header('Content-Type: application/x-download');
header('Content-Disposition: attachment; filename='.$filename);
renderPDF($metadata, $acknowledgement, strip_tags(label_decode($app_title)), $Data);


/* Display a message */
function displayMessage($msg = '') {
	// Display any messages
	if (strlen($msg) > 0) {
		if (strpos($msg,'ERROR') !== false) {
			// Display Error Message
			echo "<p class='red' style='margin:20px 0 10px; text-align:center;'><b>$msg</b></p>";
		} else {
			// Display normal message
			echo "<p class='green' style='margin:20px 0 10px; text-align:center;'><b>$msg</b></p>";
		}
	}
}

function formatFilename($project_name) {
	
	// Remove special characters from title for using as filename
	$project_name = strip_tags($project_name);
	
	$filename .= str_replace(" ", "", ucwords(preg_replace("/[^a-zA-Z0-9]/", " ", $project_name)));
		
	// Make sure filename is not too long
	if (strlen($filename) > 30) {
		$filename = substr($filename, 0, 30);
	}
	// Add timestamp if data in PDF
	if (isset($_GET['id']) || isset($_GET['allrecords'])) {
		$filename .= date("_Y-m-d_Hi");
	}
	
	return $filename.".pdf";
}

//array filter to filter out metadata to keep using list of populated fields
function blankFilter($attr) {
	global $keep_fields;
	
	if (in_array($attr['field_name'], $keep_fields)) {
		return  true;
	}
	return false;
}


?>