-- test_with_table_based_authentication.sql
-- Add three users and activate table based authentication
-- Users:
--   admin - the Admin Account
--   alice - the Account Manager
--   bob   - a user with basic permissions
--   carol - a user with basic permissions
--   dan   - a user with basic permissions
--
-- The password for each user is 'password'
-- All email address are fake addresses at projectredcap.org
--
-- Please change passwords and email addresses on any system that is more than a isolated, local test system.
-- Alternatively, just delete these accounts after the roles have been assigned to new accounts.
-- Written for 6.18.1.
-- Tested on 6.18.1 and 7.2.2
-- Set paswords to the the md5 of the the password with the salt append.  e.g.
--  md5('password'.'my_salt_string')
REPLACE INTO `redcap_auth` VALUES ('admin',md5(concat('password', 'my_salt_string')),'my_salt_string',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('alice',md5(concat('password', 'my_salt_string')),'my_salt_string',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('bob',  md5(concat('password', 'my_salt_string')),'my_salt_string',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('carol',md5(concat('password', 'my_salt_string')),'my_salt_string',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('dan',  md5(concat('password', 'my_salt_string')),'my_salt_string',0,0,NULL,NULL,NULL,NULL);

REPLACE INTO `redcap_config` VALUES ('auth_meth_global','table');

REPLACE INTO `redcap_user_information`
(ui_id,
username,
user_email,
user_email2,
user_email3,
user_phone,
user_phone_sms,
user_firstname,
user_lastname,
user_inst_id,
super_user,
account_manager,
user_creation,
user_firstvisit,
user_firstactivity,
user_lastactivity,
user_lastlogin,
user_suspended_time,
user_expiration,
user_access_dashboard_view,
user_access_dashboard_email_queued,
user_sponsor,
user_comments,
allow_create_db,
email_verify_code,
email2_verify_code,
email3_verify_code,
datetime_format,
number_format_decimal,
number_format_thousands_sep,
two_factor_auth_secret,
display_on_email_users,
two_factor_auth_twilio_prompt_phone,
two_factor_auth_code_expiration,
api_token,
messaging_email_preference,
messaging_email_urgent_all,
messaging_email_ts)
VALUES (1,'site_admin','joe.user@projectredcap.org',NULL,NULL,NULL,NULL,'Joe','User',NULL,0,0,NULL,'2017-02-02 14:07:08','2017-02-02 14:15:52','2017-02-02 14:22:19','2017-02-02 14:15:15',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','PYCDZD4KK2ST2AYZ',1,1,2,NULL,'NONE',1,NULL);

REPLACE INTO `redcap_user_information`
(ui_id,
username,
user_email,
user_email2,
user_email3,
user_phone,
user_phone_sms,
user_firstname,
user_lastname,
user_inst_id,
super_user,
account_manager,
user_creation,
user_firstvisit,
user_firstactivity,
user_lastactivity,
user_lastlogin,
user_suspended_time,
user_expiration,
user_access_dashboard_view,
user_access_dashboard_email_queued,
user_sponsor,
user_comments,
allow_create_db,
email_verify_code,
email2_verify_code,
email3_verify_code,
datetime_format,
number_format_decimal,
number_format_thousands_sep,
two_factor_auth_secret,
display_on_email_users,
two_factor_auth_twilio_prompt_phone,
two_factor_auth_code_expiration,
api_token,
messaging_email_preference,
messaging_email_urgent_all,
messaging_email_ts)
VALUES (2,'admin','joe.admin@projectredcap.org','','',NULL,NULL,'Joe','Admin','',1,0,'2017-02-02 14:15:52','2017-02-02 14:23:03','2017-02-02 14:22:41','2017-02-02 14:23:03','2017-02-02 14:22:42',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','7HXAGUD5HJD7QP3I',1,1,2,NULL,'NONE',1,NULL);

REPLACE INTO `redcap_user_information`
(ui_id,
username,
user_email,
user_email2,
user_email3,
user_phone,
user_phone_sms,
user_firstname,
user_lastname,
user_inst_id,
super_user,
account_manager,
user_creation,
user_firstvisit,
user_firstactivity,
user_lastactivity,
user_lastlogin,
user_suspended_time,
user_expiration,
user_access_dashboard_view,
user_access_dashboard_email_queued,
user_sponsor,
user_comments,
allow_create_db,
email_verify_code,
email2_verify_code,
email3_verify_code,
datetime_format,
number_format_decimal,
number_format_thousands_sep,
two_factor_auth_secret,
display_on_email_users,
two_factor_auth_twilio_prompt_phone,
two_factor_auth_code_expiration,
api_token,
messaging_email_preference,
messaging_email_urgent_all,
messaging_email_ts)
VALUES (3,'alice','alice.manager@projectredcap.org','','',NULL,NULL,'Alice','Manager','',0,1,'2017-02-02 14:21:22','2017-02-02 14:26:49','2017-02-02 14:26:40','2017-02-02 14:26:49','2017-02-02 14:26:40',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','64E2ESJTNTFAUYS4',1,1,2,NULL,'NONE',1,NULL);

REPLACE INTO `redcap_user_information`
(ui_id,
username,
user_email,
user_email2,
user_email3,
user_phone,
user_phone_sms,
user_firstname,
user_lastname,
user_inst_id,
super_user,
account_manager,
user_creation,
user_firstvisit,
user_firstactivity,
user_lastactivity,
user_lastlogin,
user_suspended_time,
user_expiration,
user_access_dashboard_view,
user_access_dashboard_email_queued,
user_sponsor,
user_comments,
allow_create_db,
email_verify_code,
email2_verify_code,
email3_verify_code,
datetime_format,
number_format_decimal,
number_format_thousands_sep,
two_factor_auth_secret,
display_on_email_users,
two_factor_auth_twilio_prompt_phone,
two_factor_auth_code_expiration,
api_token,
messaging_email_preference,
messaging_email_urgent_all,
messaging_email_ts)
VALUES (4,'bob','bob.user@projectredcap.org','','',NULL,NULL,'Bob','User','',0,0,'2017-02-02 14:20:20','2017-02-02 14:28:33','2017-02-02 14:28:24','2017-02-02 14:28:33','2017-02-02 14:28:24',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','5OMDTXHZYMX62IQJ',1,1,2,NULL,'NONE',1,NULL);

REPLACE INTO `redcap_user_information`
(ui_id,username,user_email,user_email2,user_email3,user_phone,user_phone_sms,user_firstname,user_lastname,user_inst_id,super_user,account_manager,user_creation,user_firstvisit,user_firstactivity,user_lastactivity,user_lastlogin,user_suspended_time,user_expiration,user_access_dashboard_view,user_access_dashboard_email_queued,user_sponsor,user_comments,allow_create_db,email_verify_code,email2_verify_code,email3_verify_code,datetime_format,number_format_decimal,number_format_thousands_sep,two_factor_auth_secret,display_on_email_users,two_factor_auth_twilio_prompt_phone,two_factor_auth_code_expiration,api_token,messaging_email_preference,messaging_email_urgent_all,messaging_email_ts)
VALUES (5,'carol','carol.user@projectredcap.org','','',NULL,NULL,'Carol','User','',0,0,'2017-02-02 14:20:20','2017-02-02 14:28:33','2017-02-02 14:28:24','2017-02-02 14:28:33','2017-02-02 14:28:24',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','5OMDTXHZYMX62IQJ',1,1,2,NULL,'NONE',1,NULL);

REPLACE INTO `redcap_user_information`
(ui_id,username,user_email,user_email2,user_email3,user_phone,user_phone_sms,user_firstname,user_lastname,user_inst_id,super_user,account_manager,user_creation,user_firstvisit,user_firstactivity,user_lastactivity,user_lastlogin,user_suspended_time,user_expiration,user_access_dashboard_view,user_access_dashboard_email_queued,user_sponsor,user_comments,allow_create_db,email_verify_code,email2_verify_code,email3_verify_code,datetime_format,number_format_decimal,number_format_thousands_sep,two_factor_auth_secret,display_on_email_users,two_factor_auth_twilio_prompt_phone,two_factor_auth_code_expiration,api_token,messaging_email_preference,messaging_email_urgent_all,messaging_email_ts)
VALUES (6,'dan','dan.user@projectredcap.org','','',NULL,NULL,'Dan','User','',0,0,'2017-02-02 14:20:20','2017-02-02 14:28:33','2017-02-02 14:28:24','2017-02-02 14:28:33','2017-02-02 14:28:24',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','5OMDTXHZYMX62IQJ',1,1,2,NULL,'NONE',1,NULL);
