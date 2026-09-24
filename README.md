# 🔍 Domain Intel Scout Skill

> **Autonomous Passive Reconnaissance & Attack Surface Discovery Skill for Sovereign AI Agents**  
> *Structured first-pass domain intelligence using DNS enumeration, WHOIS ownership inspection, and Certificate Transparency logs via crt.sh.*

[![Skill Status](https://img.shields.io/badge/Agent%20Skill-Domain%20Intel%20Scout-00e5ff?style=flat-square)](#overview)
[![Ecosystem](https://img.shields.io/badge/Ecosystem-Nous%20Hermes%20%2F%20Codex-gold?style=flat-square)](#compatibility)
[![Zero Active Scanning](https://img.shields.io/badge/Passive-Zero%20Port%20Scan-brightgreen?style=flat-square)](#safety--ethics)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](#license)

---

## ✦ Overview

**Domain Intel Scout** is an autonomous skill module designed for agentic workflows (compatible with Nous Research Hermes Agent, Codex CLI, and Google AGY SDK). It equips agents with an automated, non-invasive reconnaissance workflow to map an organization's digital footprint without human micro-management.

Unlike noisy active vulnerability scanners, Domain Intel Scout operates entirely passively, extracting intelligence from public authoritative nameservers, registrar records, and cryptographic Certificate Transparency (CT) logs.

---

## ✦ Capabilities & Procedures

```mermaid
flowchart TD
    A[Target Domain Input] --> B(1. DNS Resolution)
    A --> C(2. WHOIS Ownership Audit)
    A --> D(3. Certificate Transparency crt.sh)
    
    B --> E[A/AAAA Records & Mail Servers]
    C --> F[Registrar, Creation & Expiry Dates]
    D --> G[Discovered Subdomains & SAN Wildcards]
    
    E --> H[Consolidated Intelligence Table]
    F --> H
    G --> H
```

### 1. DNS Reconnaissance
Identifies primary IPv4/IPv6 endpoints, mail servers (MX), and cloud hosting providers:
```bash
dig +short A <domain>
dig +short AAAA <domain>
dig +short MX <domain>
dig +short TXT <domain>
```

### 2. Registrar & Ownership Audit
Filters privacy redaction noise to isolate critical dates and authoritative registrars:
```bash
whois <domain> | grep -Ei "Creation Date|Registrar|Registry Expiry"
```

### 3. Passive Subdomain Discovery via CT Logs
Queries the global public Certificate Transparency logs without sending a single packet to the target server:
```bash
curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].common_name' | sort -u
```

---

## ✦ Installation & Compatibility

### For Nous Hermes Agent
Drop into your Hermes skills directory:
```bash
hermes skill install NullAITech/osint-scout-skill
```

### For ZothOS / Local Agent Swarms
Symlink or copy into `~/.hermes/skills/` or `~/.agents/skills/`:
```bash
git clone https://github.com/NullAITech/osint-scout-skill.git ~/.hermes/skills/domain-intel-scout
```

### Required Dependencies
* `dnsutils` (`dig`)
* `whois`
* `curl`
* `jq`

---

## ✦ Safety, Ethics & Rules of Engagement

- **Authorized Auditing**: Intended strictly for security researchers, developers, and red teams auditing infrastructure with appropriate authorization.
- **Zero Port Scanning**: This skill performs **zero** TCP/UDP port scans and sends no intrusive payloads.
- **Zero Exfiltration**: All parsed metadata is presented directly in the operator's terminal context in clean markdown tables.

---

## ✦ License

Part of the **[NullAI Tech](https://github.com/NullAITech)** open security ecosystem. Distributed under the MIT License.
