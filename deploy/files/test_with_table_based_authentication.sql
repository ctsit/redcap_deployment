-- test_with_table_based_authentication.sql
-- Add three users and activate table based authentication
-- Users:
--   admin - the Admin Account
--   alice - the Account Manager
--   bob - a user with basic permissions
--
-- The password for each user is 'Password1'
-- All email address are fake addresses at projectredcap.org
--
-- Please change passwords and email addresses on any system that is more than a isolated, local test system.
-- Alternatively, just delete these accounts after the roles have been assigned to new accounts.
REPLACE INTO `redcap_auth` VALUES ('admin','f00a29960d1108086c2d86742bfc5a89','6hgNrh8n%A3R4GwIuny@quxwHjVo7yu%B&4U@LmKd~n72UJzJ&xBEN-t4CYzIyxVzucwQm.vLK.N23S.Ltc@ZZq~$jFxhYU~bopz',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('alice','bea198176813848e6167cd43baaf5094','66~xW#mg3n@.jKb94!M..FXDTy&VMDUHmPILK4^GLBQ5mRj3%XW%YUaM8Wpyi7*iBtJvTrUcT8c&qmuyVqe&*ZUfWRae6&2BCY^A',0,0,NULL,NULL,NULL,NULL);
REPLACE INTO `redcap_auth` VALUES ('bob','7fd2b57c81616c7123650eaa7355d9e9','z%QiWLyN@w3y9UQKdB%%GHDtS%@A9cYP*!oPXy4kkZR.&V@hJvpP.^udA5JWCg!mzYA6W.37$8mMWW.j$huhemeKrYFoTj@sSABz',0,0,NULL,NULL,NULL,NULL);

REPLACE INTO `redcap_config` VALUES ('auth_meth_global','table');

REPLACE INTO `redcap_user_information` VALUES (1,'site_admin','joe.user@projectredcap.org',NULL,NULL,NULL,NULL,'Joe','User',NULL,0,0,NULL,'2017-02-02 14:07:08','2017-02-02 14:15:52','2017-02-02 14:22:19','2017-02-02 14:15:15',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','PYCDZD4KK2ST2AYZ',1,1,2,NULL,'X_HOURS',1,NULL);
REPLACE INTO `redcap_user_information` VALUES (2,'admin','joe.admin@projectredcap.org','','',NULL,NULL,'Joe','Admin','',1,0,'2017-02-02 14:15:52','2017-02-02 14:23:03','2017-02-02 14:22:41','2017-02-02 14:23:03','2017-02-02 14:22:42',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','7HXAGUD5HJD7QP3I',1,1,2,NULL,'X_HOURS',1,NULL);
REPLACE INTO `redcap_user_information` VALUES (3,'alice','alice.manager@projectredcap.org','','',NULL,NULL,'Alice','Manager','',0,1,'2017-02-02 14:21:22','2017-02-02 14:26:49','2017-02-02 14:26:40','2017-02-02 14:26:49','2017-02-02 14:26:40',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','64E2ESJTNTFAUYS4',1,1,2,NULL,'X_HOURS',1,NULL);
REPLACE INTO `redcap_user_information` VALUES (4,'bob','bob.user@projectredcap.org','','',NULL,NULL,'Bob','User','',0,0,'2017-02-02 14:20:20','2017-02-02 14:28:33','2017-02-02 14:28:24','2017-02-02 14:28:33','2017-02-02 14:28:24',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'M/D/Y_12','.',',','5OMDTXHZYMX62IQJ',1,1,2,NULL,'X_HOURS',1,NULL);
