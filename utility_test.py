from fabric.api import *
import unittest

class CheckHostAccessibility(unittest.TestCase):
    def setUp(self):
        self.hosts = [
            "https://api.reporter.nih.gov",
            "https://eutils.ncbi.nlm.nih.gov",
            "https://www.ncbi.nlm.nih.gov",
            "https://icite.od.nih.gov",
            "https://pub.orcid.org",
            "https://redcap.vanderbilt.edu",
            "https://api.altmetric.com",
            "https://api.patentsview.org",
            "https://api.nsf.gov",
            "https://api.ies.ed.gov",
            "https://ies.ed.gov",
            "https://taggs.hhs.gov",
            "https://api.elsevier.com",
            "https://dev.elsevier.com",
            "https://ws.isiknowledge.com"
        ]
        self.failed_hosts = []

    def check_host_accessibility(self, host):
        with settings(warn_only=True, user=env.deploy_user):
            result = run(f"curl -s -o /dev/null -w '%{{http_code}}' -L {host}")
            http_code = result.stdout.strip()
            return http_code

    def test_hosts(self):
        for host in self.hosts:
            http_code = self.check_host_accessibility(host)
            if http_code != "200":
                # Collect details about failed hosts for assertion later
                self.failed_hosts.append(f"{host} - HTTP Status: {http_code}")
        self.assertTrue(len(self.failed_hosts) == 0, "Some hosts were not accessible:\n" + "\n".join(self.failed_hosts))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CheckHostAccessibility())
    return suite

def main():
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)

