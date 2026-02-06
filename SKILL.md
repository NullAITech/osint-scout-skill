---
name: domain-intel-scout
description: Performs initial OSINT recon on a domain using whois, dig, and certificate transparency checks.
dependencies: whois, dnsutils, curl
---

## Overview
This skill enables the agent to perform a structured "first-pass" recon on a target domain. It is designed for security researchers and web developers auditing their own infrastructure.

## Procedures

### 1. DNS Reconnaissance
Run `dig +short A <domain>` and `dig +short MX <domain>` to identify hosting and mail providers.

### 2. Ownership Information
Execute `whois <domain>` to find registrar data and registration dates. 
**Note:** Filter out the privacy-protected fluff; focus on the "Creation Date" and "Registrar."

### 3. Subdomain Discovery (Passive)
Use the crt.sh API to find subdomains via certificates:
`curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].common_name' | sort -u`

## Safety & Ethics
- ONLY use this on domains you own or have explicit permission to test.
- This skill does NOT perform active port scanning (nmap).
- Do not exfiltrate this data; present it to the user in a table format.
