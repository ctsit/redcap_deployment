# Hook Activation and Development

This guide will describes the fabric commands available to activate and test REDCap hooks.

---

## Prerequisites

These commands assume you have a REDCap instance that was deployed via these tools and at least one hook to be activated or tested.  As the test_hook task only works against a REDCap instance in a local development virtual machine (VM), that also requires that you create the local VM according to the instructions in the README.md

The hook and indeed *every* hook in this environment must be *anonymous* PHP function.  This is required to when using the extensible-redcap-hooks framework. This allows you to define multiple anonymous functions that can each be called by the same REDCap hook function.  Each hook is isolated from the other even though they are hooking the same REDCap page. See [https://github.com/ctsit/extensible-redcap-hooks](https://github.com/ctsit/extensible-redcap-hooks) for more details.


## Activating a Deployed Hook

If you have deployed a hook with your REDCap package, you can use the activate_hook task to activate it either globally or on a specific project.  A global activation on the local vagrant instance might look like this:

    fab vagrant activate_hook:redcap_data_entry_form,cap_locs

or

    fab vagrant activate_hook:redcap_data_entry_form,cap_locs.php

You must name the hook_function and the filename of the hook.  The .php extension is optional.


## Developing and Testing Hooks

If you are developing a hook you can easily test it within a local REDCap instance by using the test\_hook task. It's not strictly required, but strongly recommended that the hook be placed in a new subdirectory of this redcap\_deployment repository. This makes it easier to version control the hook separately from the redcap\_deployment repo.

This series of commands will get you started on a new hook.

    mkdir myhook
    cd myhook
    git init
    cat >>END < myhook.php
    <?php // redcap_data_entry_form.php
    return function ($project_id, $record, $instrument, $event_id, $group_id) {
        print '<script>alert("REDCap Hook Alert!");</script>'
    };
    END

Note the use of the *anonymous* PHP function.  This is required to when using the extensible-redcap-hooks framework. The advantage is you can define multiple anonymous functions that can each be called by the same redcap hook function.  Each hook is isolated from the other even though they are hooking the same REDCap page. See [https://github.com/ctsit/extensible-redcap-hooks](https://github.com/ctsit/extensible-redcap-hooks) for more details.

Then activate the hook for a test with this command

    fab vagrant test_hook:redcap_data_entry_form,myhook/myhook.php

This activates the hook globally to make it easy to test in a development environment.
