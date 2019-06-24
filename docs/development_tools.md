# Development tools

## Tracking mysql changes

To help you track changes to the MySQL database, two BASH aliases have been defined for the root and vagrant users:

- `dump_schema` will dump the entire schema of the redcap database to ./schema.sql
- `dump_data` will dump the redcap database to ./data.sql

If you commit an initial state of your redcap database to a temporary git repo, it is easy to track changes during upgrades, redcap activity and module development.
