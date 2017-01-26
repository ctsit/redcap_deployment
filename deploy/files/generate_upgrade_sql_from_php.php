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

$input_file = $argv[1];

if (file_exists($input_file)) {
    include $input_file;
} else {
    fwrite(STDERR, "-- WARNING: The file $input_file does not exist. SQL statements could not be generated\n");
    exit(2);
}
