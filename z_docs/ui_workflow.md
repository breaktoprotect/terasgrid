# Default page to display

Dashboard showing basic stats and radar and heatmap.

# Workflow 0: Setup DB of initial/existing configuration settings

Tab name should be like "Setup"
User clicks on the setup, a simple interface to allow loading of existing/initial configuration settings e.g. data.csv
Once uploaded, it should provide simple stats like:

- How many records ingested?
- Any errors?

# Workflow 1: Data Viewer - Navigate multiple tables

There will be a few tables to allow User to navigate through.

User can click on a inner navigation bar/sidebar or tabs to choose the table to view.

All columns will be retrieved via FastAPI but not all table columns will be shown.

The core table that will be displayed is:

- unique_id_mandatory
- status_mandatory
- name_mandatory
- description_mandatory
- os_version_optional
- role_applicable_optional

CIS table:

- number (is actually the id for CIS)
- reviewed
- title
- profile_applicability
- description

First and foremost will be post-setup, the existing configuration settings (e.g. data.csv) ingested earlier.
Subsequently a baseline is uploaded, it should eventually show up here.

# Workflow 2: Upload and perform Baseline Hardening

User upload e.g. CIS Windows 2025 pdf then it automatically gets converted then ingested into local_temp.db

- UI: Must show progression of the conversion as it takes 10-15s
  Showing up a new tab for browsing data (i.e. local_temp.db's table) apart from existing ingested core config records.
- UI: Must show selectable tabs or navigation capability to see table of data

User clicks on a button to start performing CIS baseline hardening
Backend in a loop:

- Retrieves unreviewed CIS recommendation or rec
- Performing semantic search to retrieve top k records
- Call LLM model to ask if record already exist
- Call LLM model to analyze if this baseline is security-related (i.e. impactful to security) or purely comestic or good to have
- Get two sets of JSON to make determination if CIS recommendation will turn into a new "Pending" config in the core
- Repeat if local_temp.db the cis win 2025 table still have unreviewed items

UI: Must show progression (e.g. 2/463 records with a bar or something)
