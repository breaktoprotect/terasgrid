# Attachment

`to_add.csv`

# Prompt for multple records:

You are a cybersecurity specialist who is an expert in Windows Server security baseline hardening.

New configuration settings (CSV format):
config_id,config_name,config_desc,config_settings,status,remarks
CAND-1,Enable PUA protection,Block potentially unwanted applications,HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\PUAProtection=1,active,""
CAND-4,Force dark mode UI,Set system and apps to dark theme for user preference,HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize\AppsUseLightTheme=0; SystemUsesLightTheme=0,draft,""
CAND-6,Enable Credential Guard,Use VBS to isolate secrets and protect credentials,HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags=1,active,""

Instructions:

1. Using the semantic search tool, search for existing configuration settings that match the new configuration's config_name and/or config_desc.
2. If a match is found (functionally equivalent setting already exists), do not insert it. Include the matching existing config_id in the decision_reason.
3. Determine if the new configuration is security-related. A security-related setting is one that directly mitigates threats, improves authentication, hardens OS configuration, or prevents exploitation. Cosmetic or user-preference settings are not considered security-related.
4. Insert the new configuration only if:
    - It is security-related, AND
    - No existing equivalent configuration is found in the baseline.
5. Output all records from the input in a single table with the following columns:
    - config_id
    - config_name
    - decision_reason (brief, audit-ready explanation of why it was added or not added)

Output format:
| config_id | config_name | decision_reason |
|-----------|-------------|-----------------|
| CAND-<Number> | <name> | <reason> |

# Prompt for single:

You are a cybersecurity specialist who is an expert in Windows Server security baseline hardening.

New configuration settings (CSV format):
config_id,config_name,config_desc,config_settings,status,remarks
CAND-6,Enable Credential Guard,Use VBS to isolate secrets and protect credentials,HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags=1,active,""

Instructions:

1. Using the semantic search tool, search for existing configuration settings that match the new configuration's config_name and/or config_desc.
2. If a match is found (functionally equivalent setting already exists), do not insert it.
3. Determine if the new configuration is security-related. If it is not security-related, do not insert it.
4. Insert the new configuration only if:
    - It is security-related, AND
    - No existing equivalent configuration is found in the baseline.
5. For each new configuration, explain your decision in a table with the following columns:
    - config_id
    - config_name
    - decision_reason (brief, audit-ready explanation of why it was added or not added)

Output format:
| config_id | config_name | decision_reason |
|-----------|-----------------------|-----------------|
| CAND-<Number> | Enable Credential Guard | <reason> |

# Record choices

CAND-1,Enable PUA protection,Block potentially unwanted applications,HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\PUAProtection=1,active,""

CAND-4,Force dark mode UI,Set system and apps to dark theme for user preference,HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize\AppsUseLightTheme=0; SystemUsesLightTheme=0,draft,""

CAND-6,Enable Credential Guard,Use VBS to isolate secrets and protect credentials,HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags=1,active,""
