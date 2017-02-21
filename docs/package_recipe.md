# Creating a REDCap package for deployment

This guide will provide the sequence of commands needed to package a version of REDCap software for deployment. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

### Prerequisites  
This workflow assumes you have a REDCap zip file as downloaded from the REDCap Consortium. The version of REDCap is up to you, but the zip file needs to be named in the format of redcap#.#.#.zip (standalone package) OR redcap#.#.#_upgrade.zip (upgrade package). There can be a number of digits between each decimal as long as there is at least one. For example, the format redcap6.11.123 is acceptable but the format redcap.0.123 is not. The zip file needs to be in the same directory as the fabfile (should be the same directory as this markdown file). The fabric commands will be entered into the command line from this directory.

## Fabric Command Sequence  
The packaging sequence is relatively simple. While you're in the directory that contains both the fabfile and the desired redcap zip file, execute the command `$ fab package(redcap_zip)`. The redcap_zip is your redcap zip file or it will default to the most recent redcap zip in the directory. This will remove any existing build directories (builddirs) and create a new one for the build. The new builddir is populated with the extracted contents of the zip file found/specified. This will also transfer any existing hooks or plugins within the existing deploy/hooks or deploy/plugins directories to the builddir. The command also applies patches and the upgrade script to the redcap/redcap_v#.#.# directory. Once complete, the builddir should contain a redcap directory with a redcap_v#.#.# file inside.

