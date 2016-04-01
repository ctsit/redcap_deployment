# Change Log
All notable changes to the REDCap Deployment project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [0.3.0] - 2016-04-01
### Changed
- Update autonotify plugin with security improvements (Philip Chase)


## [0.2.0] - 2016-03-31
### Added
- Add a Changelog with retrospective releases (Philip Chase)
- Add scripts for deploying REDCAP Plugins from this Repo (Philip Chase)
- Add Autonotify_Plugin_End_User_Instructions.docx (Philip Chase)
- Add REDCAp Autonotify Plugin from Andy Martin (Philip Chase)

### Changed
- Refactor hook deployment script to allow for deploying other extensions (Philip Chase)
- Move Vagrant VM to a debian-7.8 image (Philip Chase)
- Reconfigure Vagrant to deploy REDCap extensions entirely via shell provisioning (Philip Chase)
- Configure redcap to use the redcap.dev hostname in redcap_base_url (Philip Chase)
- Move vagrant config to the root of the repo (Philip Chase)


## [0.1.0] - 2015-07-02
### Added
- Add REDCAP hook deployment script and sample data file (Erik C. Schmidt)
- Add vagrant testing VM
- Add a hooks data file for redcap.ctsi.ufl.edu (Philip Chase)
- Add a hooks data file for redcapstage.ctsi.ufl.edu (Philip Chase)
