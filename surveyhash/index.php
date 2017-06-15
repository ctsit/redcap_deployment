<?php

/**⁄
 * Enter a survey hash and get the details of the survey, including link to form
 * Luke Stevens, Murdoch Childrens Research Institute 
 * 11-May-2017
 **/
 
#require_once "../../redcap_connect.php"; # non-UF setting -6/15/2017
require_once("/var/www/redcap/redcap_connect.php");

$hash = REDCap::escapeHtml($_REQUEST['hash']);
$surveyDetails = getSurveyDetails($hash); // params sanitized in init_functions, db_escape in sql

if ($isAjax) {
        exit(count($surveyDetails) > 0) ? json_encode($surveyDetails) : '0';
}

$page = new HtmlPage();
$page->PrintHeaderExt();

if (!SUPER_USER) {
        displayMsg('You do not have permission to view this page', 'errorMsg','center','red','exclamation_frame.png', 600);
        $page->PrintFooterExt();
        exit;
}

include APP_PATH_VIEWS . 'HomeTabs.php';
?>
<style type="text/css">#pagecontent { margin-top: 70px; }</style>
<?php
renderPageTitle('Find Survey from Survey Hash');

print RCView::div(array(),'Enter a suvey hash to find the corresponding data entry form.');

print RCView::form(
        array('name'=>'form',  'method'=>'get'),
        RCView::div(
                array('class'=>'form-group', 'style'=>'margin:10px 0 20px 0'),
                RCView::label(array('for'=>'hash'),'Survey hash').
                RCView::input(
                        array('type'=>'text','class'=>'form-control', 'style'=>'display:inline;width:200px;margin:0 5px',
                            'name'=>'hash','value'=>$hash)
                ).
                RCView::button(
                        array('class'=>'btn','type'=>'submit'),
                        'Find'
                )
        )
);

if ($hash==='') {
        // no hash - no display
    
} else if (isset($surveyDetails) && count($surveyDetails) > 0) {
        // valid hash - display survey details
        //print_array($surveyDetails);

        $Proj = new Project($surveyDetails['project_id'], true);
        $event = '';
        if ($Proj->longitudinal) {
                if ($Proj->multiple_arms) {
                        $eventName = $Proj->eventInfo[$surveyDetails['event_id']]['name_ext'];
                } else {
                        $eventName = $Proj->eventInfo[$surveyDetails['event_id']]['name'];
                }
                $eventName = " ($eventName)";
        }
        
        print RCView::div(
                array('class'=>'container well', 'style'=>'width:inherit; font-size:120%;'),
                RCView::div(
                        array('class'=>'row'),
                        RCView::div(
                                array('class'=>'col-sm-3 col-md-3 col-lg-2', 'style'=>'color:#555'),
                                'Project'
                        ).
                        RCView::div(
                                array('class'=>'col-sm-7 col-md-6 col-lg-7'),
                                strip_tags($surveyDetails['app_title']).' (id='.$surveyDetails['project_id'].')'
                        ).
                        RCView::div(
                                array('class'=>'col-sm-2 col-md-3 col-lg-3'),
                                RCView::a(
                                        array('class'=>'btn btn-xs btn-default', 'target'=>'_blank', 'style'=>'text-align:center;width:150px',
                                            'href'=>APP_PATH_WEBROOT.'ProjectSetup/index.php?pid='.$surveyDetails['project_id']),
                                        'Project Setup'.
                                        RCView::img(array('src'=>APP_PATH_IMAGES.'chain_arrow.png', 'style'=>'margin-left:3px'))
                                )
                        )
                ).
                RCView::div(
                        array('class'=>'row', 'style'=>'margin-top:20px;margin-bottom:20px;'),
                        RCView::div(
                                array('class'=>'col-sm-3 col-md-3 col-lg-2', 'style'=>'color:#555'),
                                'Survey'
                        ).
                        RCView::div(
                                array('class'=>'col-sm-7 col-md-6 col-lg-7'),
                                strip_tags($surveyDetails['title'])
                        ).
                        RCView::div(
                                array('class'=>'col-sm-2 col-md-3 col-lg-3'),
                                RCView::a(
                                        array('class'=>'btn btn-xs btn-default', 'target'=>'_blank', 'style'=>'text-align:center;width:150px',
                                            'href'=>APP_PATH_WEBROOT.'Design/online_designer.php?pid='.$surveyDetails['project_id']),
                                        'Online Designer'.
                                        RCView::img(array('src'=>APP_PATH_IMAGES.'chain_arrow.png', 'style'=>'margin-left:3px'))
                                )
                        )
                ).
                RCView::div(
                        array('class'=>'row'),
                        RCView::div(
                                array('class'=>'col-sm-3 col-md-3 col-lg-2', 'style'=>'color:#555'),
                                'Record'
                        ).
                        RCView::div(
                                array('class'=>'col-sm-7 col-md-6 col-lg-7'),
                                strip_tags($surveyDetails['record']).$eventName
                        ).
                        RCView::div(
                                array('class'=>'col-sm-2 col-md-3 col-lg-3'),
                                RCView::a(
                                        array('class'=>'btn btn-xs btn-default', 'target'=>'_blank', 'style'=>'text-align:center;width:150px',
                                            'href'=>APP_PATH_WEBROOT.'DataEntry/index.php'.
                                                '?pid='.$surveyDetails['project_id'].
                                                '&id='.$surveyDetails['record'].
                                                '&event_id='.$surveyDetails['event_id'].
                                                '&page='.$surveyDetails['form_name'].
                                                '&instance='.$surveyDetails['instance']
                                        ),
                                        'Data Entry Form'.
                                        RCView::img(array('src'=>APP_PATH_IMAGES.'chain_arrow.png', 'style'=>'margin-left:3px'))
                                )
                        )
                )
        );
} else {
        // invalid has - display error message
        print RCView::div(array('class'=>'red'),"Survey hash '$hash' not found.");
}

$page->PrintFooterExt();
exit;


function getSurveyDetails($hash) {
    
        $details = array();

        if (isset($hash) && $hash!=='') {
                $sql = "SELECT s.survey_id,s.project_id,pr.app_title,s.form_name,s.title,p.participant_id,p.event_id,p.hash,r.response_id,r.record,r.instance,r.start_time,r.first_submit_time,r.completion_time,r.return_code,r.results_code ".
                "FROM redcap_surveys s ".
                "INNER JOIN redcap_projects pr ON s.project_id = pr.project_id ".
                "INNER JOIN redcap_surveys_participants p ON s.survey_id = p.survey_id ".
                "INNER JOIN redcap_surveys_response r ON p.participant_id = r.participant_id ".
                "WHERE hash = '".prep($hash)."' LIMIT 1";

                $result = db_query($sql);

                $details = db_fetch_assoc($result);
                db_free_result($result);
        }

        return $details;
}
