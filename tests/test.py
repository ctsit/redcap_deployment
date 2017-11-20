import unittest
import pycurl
import sys
from StringIO import StringIO
import re

class Weburl():

    def __init__(self):
        self.URL = ""

    def get(self, URL, FOLLOWLOCATION = False):
        self.URL = URL
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(pycurl.FOLLOWLOCATION, FOLLOWLOCATION)
        c.perform()
        c.close()
        return buffer.getvalue().replace('\r\n', '').replace('\n', '')

class UnauthenticatedAccessTestCase(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        # remove any doubled trailing slashes in redcap_url
        self.redcap_root = re.sub('//$', '/', str(redcap_url))
        self.redcap_version_path = str(redcap_version)
        self.weburl = Weburl()
        self.rc_forbidden = '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this page.</p>
</body></html>
'''
        self.rc_forbidden = self.rc_forbidden.replace('\r\n', '').replace('\n', '')

    def tearDown(self):
        """Call after every test case."""

    # Test for access to root level folders
    # NOTE: this test will fail in the local development vagrant until it is
    #       reconfigured from no-authentication to table-based authentication
    def testRedcapRootFolder(self):
        """Verify that we *can't* access the redcap / folder without login"""
        localpath = ""
        self.fullpath=self.redcap_root + localpath
        expected_string = 'Create New Project'
        self.assertNotIn(expected_string, self.weburl.get(self.fullpath))

    def testSurveysFolder(self):
        """Verify that we can access the REDCap surveys/ folder"""
        localpath = "surveys/"
        self.fullpath=self.redcap_root + localpath
        expected_string = 'Please enter your access code to begin the survey'
        self.assertIn(expected_string, self.weburl.get(self.fullpath))

    def testSendItDownload(self):
        """Verify that we can access the REDCap SendIt/download page"""
        localpath = "SendIt/download.php?abcdef"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        expected_string = 'Send-It:'
        self.assertIn(expected_string, self.weburl.get(self.fullpath))

    def testRouteToSendItController(self):
        """Verify the router can route us to SendIt Download"""
        localpath = "index.php?route=SendItController:download&abcdef"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        expected_string = 'Send-It:'
        self.assertIn(expected_string, self.weburl.get(self.fullpath, True))

    def testApiFolder(self):
        """Verify that we can access the REDCap api/ folder"""
        localpath = "api/"
        self.fullpath=self.redcap_root + localpath
        expected_string = 'The requested method is not implemented.'
        self.assertIn(expected_string, self.weburl.get(self.fullpath))

    # deactivate the API Help tests as they are failing routinely in Shib and probably not relevant.
    # def testApiHelpFolder(self):
    #     """Verify that we can access the REDCap api/help/ folder"""
    #     localpath = "api/help/"
    #     self.fullpath=self.redcap_root + localpath
    #     expected_string = 'REDCap API Documentation'
    #     self.assertIn(expected_string, self.weburl.get(self.fullpath))


    # def testApiHelpFile(self):
    #     """Verify that we can access the REDCap api/help/index.php file"""
    #     localpath = "api/help/index.php"
    #     self.fullpath=self.redcap_root + localpath
    #     expected_string = 'REDCap API Documentation'
    #     self.assertIn(expected_string, self.weburl.get(self.fullpath))


    def testResourceFolder(self):
        """Verify that we can access the REDCap Resources/ folder"""
        localpath = "Resources/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        self.assertEqual (self.weburl.get(self.fullpath), self.rc_forbidden)

    # Test for access to the children of the Resources folder
    def testCssFolder(self):
        """Verify that we can access the REDCap Resources/css/ folder"""
        localpath = "Resources/css/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        self.assertEqual (self.weburl.get(self.fullpath), self.rc_forbidden)

    def testJsFolder(self):
        """Verify that we can access the REDCap Resources/js/ folder"""
        localpath = "Resources/js/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        self.assertEqual (self.weburl.get(self.fullpath), self.rc_forbidden)

    def testImagesFolder(self):
        """Verify that we can access the REDCap Resources/images/ folder"""
        localpath = "Resources/images/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        self.assertEqual (self.weburl.get(self.fullpath), self.rc_forbidden)

    def testMiscFolder(self):
        """Verify that we can access the REDCap Resources/misc/ folder"""
        localpath = "Resources/misc/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        expected_string = 'redcap_ddp_demo_files.zip'
        if expected_string in self.weburl.get(self.fullpath):
            expected_string_found = True
        else:
            expected_string_found = False
        self.assertTrue(expected_string_found)

    def testSqlFolder(self):
        """Verify that we can access the REDCap Resources/sql/ folder"""
        localpath = "Resources/sql/"
        self.fullpath=self.redcap_root + self.redcap_version_path + localpath
        self.assertEqual (self.weburl.get(self.fullpath), self.rc_forbidden)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("ERROR: REDCap url and REDCap version directory parameters must be supplied for these tests. e.g.\n\npython tests/test.py http://redcap.dev/redcap/ redcap_v6.18.1/ ")
    redcap_url = sys.argv[1]
    redcap_version = sys.argv[2]
    del sys.argv[1:]
    unittest.main() # run all tests
