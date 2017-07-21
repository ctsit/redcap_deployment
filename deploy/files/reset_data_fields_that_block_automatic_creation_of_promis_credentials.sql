-- Reset data fields that block automatic creation of PROMIS credentials

-- These values need to be very plain. A URL in the homepage_contact_email field can easily cause trouble.
update redcap_config set value = "" where field_name = 'homepage_contact';
update redcap_config set value = "" where field_name = 'homepage_contact_email';

-- This citation line is used at the University of Florida. Use whatever is appropriate at your site.
update redcap_config set value = 'NCATS grant UL1 TR000064' where field_name = 'homepage_grant_cite';

-- Now erase the credentials so REDCap will try to regenerate them.
update redcap_config set value = "" where field_name = 'promis_token';
update redcap_config set value = "" where field_name = 'promis_registration_id';
