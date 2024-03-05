from fabric.api import *

def check_host_accessibility():
    """Check accessibility of defined hosts."""
    hosts = [
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
    
    for host in hosts:
        with settings(user=env.deploy_user):
            result = run(f"curl -s -o /dev/null -w '%{{http_code}}' {host}", hide='both')
            http_code = result.stdout.strip()
            if http_code == "200":
                print(f"Success: {host} is accessible.")
            else:
                print(f"Failure: {host} is not accessible. HTTP Status: {http_code}")

