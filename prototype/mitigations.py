"""
Standard mitigation playbooks per threat type.

Each entry contains:
  - name        — human label
  - summary     — one-line description of the threat class
  - steps       — curated defensive playbook (NIST / MITRE / CIS-aligned)
  - references  — authoritative public sources

The data is purposefully kept inside Python (not on the blockchain) so it can
be updated as new defensive practices emerge without rewriting history.
Submitter-provided mitigation always appears *first* and is signed by the
submitter; this catalog is presented alongside it as supplementary guidance.
"""

from __future__ import annotations


MITIGATIONS: dict[str, dict] = {

    "malware": {
        "name": "Malware",
        "summary": "Malicious software (trojans, droppers, RATs, info-stealers, worms).",
        "steps": [
            "Deploy modern EDR with behavioural detection on every endpoint and server; verify daily reporting.",
            "Enforce application allow-listing (Windows Defender Application Control, AppLocker) on critical systems.",
            "Patch operating systems and third-party software within the SLA (Critical: 7 d, High: 14 d).",
            "Disable Office macros by default for documents from the internet (Group Policy: Block macros from Internet).",
            "Hunt for the listed IOCs across the EDR fleet using YARA / Sigma rules.",
            "Network-segment user workstations from servers; restrict lateral SMB and RDP.",
            "Block listed C2 IPs and domains at the perimeter firewall and DNS resolver.",
            "Confirm logs (Sysmon, EDR, DNS, proxy) are forwarded to SIEM for retroactive search.",
        ],
        "references": [
            {"name": "NIST SP 800-83 r1 — Guide to Malware Incident Prevention",
             "url": "https://csrc.nist.gov/pubs/sp/800/83/r1/final"},
            {"name": "MITRE ATT&CK — Defensive Mitigations",
             "url": "https://attack.mitre.org/mitigations/enterprise/"},
            {"name": "CISA — Malicious Code Mitigation Strategies",
             "url": "https://www.cisa.gov/topics/cyber-threats-and-advisories/malware-phishing-and-ransomware"},
        ],
        "detection_models": [
            {"name": "Yara-Rules / rules",
             "url": "https://github.com/Yara-Rules/rules",
             "description": "Community-maintained YARA rule collection (8k+ stars) covering malware families, packers, and exploits."},
            {"name": "SigmaHQ / sigma",
             "url": "https://github.com/SigmaHQ/sigma",
             "description": "Generic detection-rule format usable across SIEMs; thousands of vetted rules for malware behaviour."},
            {"name": "Neo23x0 / signature-base",
             "url": "https://github.com/Neo23x0/signature-base",
             "description": "Florian Roth's curated YARA + IOC signature base used by the Loki scanner."},
            {"name": "mandiant / capa",
             "url": "https://github.com/mandiant/capa",
             "description": "Mandiant's tool that identifies capabilities in executables — useful for triaging unknown samples."},
        ],
    },

    "phishing": {
        "name": "Phishing",
        "summary": "Social-engineering attempts to harvest credentials or deliver payloads via email/SMS/web.",
        "steps": [
            "Deploy SPF, DKIM, and DMARC (p=reject) for all sending domains; monitor reports.",
            "Use a mail gateway with sandbox detonation and URL rewriting (Proofpoint, Mimecast, Defender for Office 365).",
            "Enable MFA on all accounts — prioritise email, VPN, and any admin console; prefer phishing-resistant methods (WebAuthn, FIDO2).",
            "Run quarterly anti-phishing training and simulated phishing exercises; track click rate trend.",
            "Add a one-click 'Report Phishing' button to the corporate mail client.",
            "Block typosquatted and look-alike domains via DNS filtering (Cisco Umbrella, Cloudflare Gateway).",
            "Force password resets and revoke active sessions for any user who interacted with the listed URLs.",
            "Hunt mail logs for inbound messages matching the listed sender/subject/URL patterns.",
        ],
        "references": [
            {"name": "CISA — Avoiding Social Engineering & Phishing Attacks",
             "url": "https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks"},
            {"name": "NIST SP 800-177 r1 — Trustworthy Email (DMARC/DKIM/SPF)",
             "url": "https://csrc.nist.gov/pubs/sp/800/177/r1/final"},
            {"name": "MITRE ATT&CK — Phishing (T1566)",
             "url": "https://attack.mitre.org/techniques/T1566/"},
        ],
        "detection_models": [
            {"name": "mitchellkrogza / Phishing.Database",
             "url": "https://github.com/mitchellkrogza/Phishing.Database",
             "description": "Daily-updated list of active phishing domains and URLs (millions of entries) suitable for DNS/proxy blocking."},
            {"name": "openphish / public_feed",
             "url": "https://openphish.com/feed.txt",
             "description": "OpenPhish public phishing URL feed, refreshed every 12 hours."},
            {"name": "phishfort / phishfort-lists",
             "url": "https://github.com/phishfort/phishfort-lists",
             "description": "Phishing block-list domains aggregated and curated by PhishFort."},
            {"name": "JPCERTCC / phishurl-list",
             "url": "https://github.com/JPCERTCC/phishurl-list",
             "description": "JPCERT/CC-maintained list of phishing URLs targeting Japanese and global brands."},
        ],
    },

    "ransomware": {
        "name": "Ransomware",
        "summary": "Encryption-based extortion that locks file systems and demands payment.",
        "steps": [
            "Maintain a 3-2-1 backup strategy with at least one offline / immutable copy; test restore quarterly.",
            "Use EDR with rollback capability (e.g. CrowdStrike Falcon, SentinelOne, Defender for Endpoint).",
            "Aggressively segment the network — workstations cannot reach file shares they don't need.",
            "Disable SMBv1, enforce SMB signing, and block outbound SMB from user subnets.",
            "Patch externally-facing services (VPN, Exchange, Citrix) within 48 h of advisory.",
            "Pre-stage an incident response runbook and a no-pay decision tree approved by legal/exec.",
            "Block known ransomware C2 IPs and Tor exit nodes at the perimeter.",
            "Practice tabletop recovery drills at least every six months.",
        ],
        "references": [
            {"name": "CISA #StopRansomware Guide",
             "url": "https://www.cisa.gov/stopransomware/ransomware-guide"},
            {"name": "NIST SP 1800-26 — Data Integrity: Detecting & Responding to Ransomware",
             "url": "https://csrc.nist.gov/pubs/sp/1800/26/final"},
            {"name": "MITRE ATT&CK — Data Encrypted for Impact (T1486)",
             "url": "https://attack.mitre.org/techniques/T1486/"},
        ],
        "detection_models": [
            {"name": "Neo23x0 / signature-base — ransomware YARA rules",
             "url": "https://github.com/Neo23x0/signature-base/tree/master/yara",
             "description": "YARA rules covering Ryuk, Conti, LockBit, REvil, BlackCat and many other ransomware families."},
            {"name": "Cyb3rWard0g / ThreatHunter-Playbook",
             "url": "https://github.com/Cyb3rWard0g/ThreatHunter-Playbook",
             "description": "Hunting analytics mapped to MITRE ATT&CK — the 'Impact' tactic covers ransomware behaviours."},
            {"name": "redcanaryco / atomic-red-team",
             "url": "https://github.com/redcanaryco/atomic-red-team",
             "description": "Pre-built test scripts you can run safely to validate your EDR catches ransomware techniques."},
            {"name": "elastic / protections-artifacts",
             "url": "https://github.com/elastic/protections-artifacts",
             "description": "Elastic Security's open detection rules — includes ransomware-specific behavioural rules."},
        ],
    },

    "c2": {
        "name": "Command & Control (C2)",
        "summary": "Attacker-controlled channels for tasking compromised hosts (beacons, RATs, tunnels).",
        "steps": [
            "Enforce egress filtering — block outbound traffic to TOR exit nodes and the listed C2 IPs.",
            "Sinkhole known malicious domains via internal DNS (Pi-hole, Quad9, Umbrella).",
            "Apply TLS inspection on outbound corporate traffic where legally permitted.",
            "Hunt for low-and-slow beaconing patterns in proxy / NetFlow data (regular interval connections to rare destinations).",
            "Scan for default Cobalt Strike artefacts: malleable C2 profiles, named pipes (\\\\.\\pipe\\msagent_*), default certificates.",
            "Block PowerShell network calls from non-admin user contexts (Constrained Language Mode).",
            "Add IDS/IPS signatures for Cobalt Strike, Sliver, Mythic, Brute Ratel, and Empire traffic patterns.",
            "Isolate any host with outbound traffic matching the listed IOCs and start IR investigation.",
        ],
        "references": [
            {"name": "MITRE ATT&CK — Command and Control (TA0011)",
             "url": "https://attack.mitre.org/tactics/TA0011/"},
            {"name": "SANS — Detecting Cobalt Strike",
             "url": "https://www.sans.org/blog/detecting-cobalt-strike-cmd-process-and-network-artifacts/"},
            {"name": "CISA — Manage and Configure DNS Filtering",
             "url": "https://www.cisa.gov/news-events/cybersecurity-advisories"},
        ],
        "detection_models": [
            {"name": "montysecurity / C2-Tracker",
             "url": "https://github.com/montysecurity/C2-Tracker",
             "description": "Daily-updated list of live C2 server IPs across Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel and more."},
            {"name": "stamparm / maltrail",
             "url": "https://github.com/stamparm/maltrail",
             "description": "Malicious-traffic detection system with 100+ public C2/IOC trail feeds built in."},
            {"name": "eset / malware-ioc",
             "url": "https://github.com/eset/malware-ioc",
             "description": "ESET's published IOCs (IPs, domains, hashes) for APT and crimeware campaigns."},
            {"name": "Neo23x0 / sigma — Network category rules",
             "url": "https://github.com/SigmaHQ/sigma/tree/master/rules/network",
             "description": "Sigma rules for detecting beaconing, suspicious DNS, and C2 tunnelling."},
        ],
    },

    "vulnerability": {
        "name": "Vulnerability / CVE",
        "summary": "A specific software flaw — patched, mitigated, or compensated for.",
        "steps": [
            "Cross-reference the CVE against the CISA Known Exploited Vulnerabilities (KEV) catalog and treat as critical if listed.",
            "Apply vendor patches within the SLA: Critical = 7 d, High = 14 d, Medium = 30 d.",
            "Run authenticated vulnerability scans weekly (Nessus, Qualys, Tenable.io) to confirm coverage.",
            "Identify all affected assets via CMDB; any asset unaccounted for is an immediate ticket.",
            "Deploy compensating controls (WAF rules, IPS signatures, network ACLs) where patching must be delayed.",
            "Disable the vulnerable service or feature if it is not business-critical.",
            "Subscribe to the vendor's security advisory mailing list to be alerted at release time.",
            "Document the residual risk and approval chain if the patch is intentionally deferred.",
        ],
        "references": [
            {"name": "CISA Known Exploited Vulnerabilities (KEV) catalog",
             "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"},
            {"name": "NIST National Vulnerability Database",
             "url": "https://nvd.nist.gov/"},
            {"name": "CIS Controls v8 — Continuous Vulnerability Management",
             "url": "https://www.cisecurity.org/controls/continuous-vulnerability-management"},
        ],
        "detection_models": [
            {"name": "aquasecurity / trivy",
             "url": "https://github.com/aquasecurity/trivy",
             "description": "Comprehensive open-source vulnerability scanner for containers, file-systems, and code repositories."},
            {"name": "CVEProject / cvelistV5",
             "url": "https://github.com/CVEProject/cvelistV5",
             "description": "Official MITRE CVE record source-of-truth in JSON 5.0 schema — machine-parseable advisory feed."},
            {"name": "OWASP / Dependency-Check",
             "url": "https://github.com/jeremylong/DependencyCheck",
             "description": "OWASP tool that identifies project dependencies with known public vulnerabilities."},
            {"name": "cisagov / kev (Known Exploited Vulnerabilities)",
             "url": "https://github.com/cisagov/kev-data",
             "description": "Public mirror of the CISA KEV catalog — vulns currently exploited in the wild."},
        ],
    },

    "ddos": {
        "name": "DDoS",
        "summary": "Distributed denial-of-service against public-facing services.",
        "steps": [
            "Front public services with a cloud-based DDoS mitigation provider (Cloudflare, AWS Shield, Azure DDoS Protection).",
            "Use Anycast DNS hosting to distribute load across many edges (Route 53, Cloudflare, Akamai).",
            "Configure rate-limits on every web server, API gateway, and authentication endpoint.",
            "Pre-arrange BGP blackholing with your upstream ISP for emergency null-routing.",
            "Maintain an IR runbook listing provider on-call contacts and escalation steps.",
            "Apply geo-blocking for source regions you do not serve.",
            "Plan capacity for 3–5× peak traffic to absorb application-layer floods.",
            "Cache aggressively at the edge so the origin is hit only for non-cacheable requests.",
        ],
        "references": [
            {"name": "CISA — Understanding and Responding to Distributed Denial-of-Service Attacks",
             "url": "https://www.cisa.gov/news-events/news/understanding-and-responding-distributed-denial-service-attacks"},
            {"name": "NIST SP 800-189 — Resilient Interdomain Traffic Exchange (BGP)",
             "url": "https://csrc.nist.gov/pubs/sp/800/189/final"},
            {"name": "Cloudflare — DDoS Mitigation Best Practices",
             "url": "https://developers.cloudflare.com/ddos-protection/best-practices/"},
        ],
        "detection_models": [
            {"name": "firehol / blocklist-ipsets",
             "url": "https://github.com/firehol/blocklist-ipsets",
             "description": "Aggregated IP block-lists (botnet, attack, brute-force, spam) refreshed every few minutes — ready for iptables/ipset."},
            {"name": "stamparm / ipsum",
             "url": "https://github.com/stamparm/ipsum",
             "description": "Daily-updated feed of suspicious / malicious IPs cross-correlated across 30+ public block-lists."},
            {"name": "kdkanishka / DDoS-Attack-Detection",
             "url": "https://github.com/kdkanishka/DDoS-Attack-Detection",
             "description": "Open-source ML classifier for detecting DDoS attack patterns in NetFlow / traffic features."},
            {"name": "ANTLab-USP / FastNetMon",
             "url": "https://github.com/pavel-odintsov/fastnetmon",
             "description": "Production-grade DDoS detection tool used by ISPs and large enterprises (sFlow / NetFlow / mirror)."},
        ],
    },

    "other": {
        "name": "Other / Custom",
        "summary": "Generic baseline controls; tailor to the specific threat reported.",
        "steps": [
            "Validate the report's IOCs against your environment using SIEM, EDR, proxy, and DNS logs.",
            "Block the listed IPs, domains, hashes, and URLs at every choke-point you control.",
            "Identify affected assets and isolate them from the network pending investigation.",
            "Apply least-privilege and MFA on any account potentially exposed.",
            "Engage the relevant business owner; communicate impact and recovery ETA.",
            "Document the incident in your tracking system and capture forensic artefacts.",
            "Brief the SOC on detection rules / signatures derived from this incident.",
            "Schedule a post-incident review within two weeks to harden controls.",
        ],
        "references": [
            {"name": "NIST SP 800-61 r2 — Computer Security Incident Handling Guide",
             "url": "https://csrc.nist.gov/pubs/sp/800/61/r2/final"},
            {"name": "MITRE ATT&CK — Defensive Mitigations index",
             "url": "https://attack.mitre.org/mitigations/enterprise/"},
            {"name": "SANS Incident Handler's Handbook",
             "url": "https://www.sans.org/white-papers/33901/"},
        ],
        "detection_models": [
            {"name": "MISP / misp-warninglists",
             "url": "https://github.com/MISP/misp-warninglists",
             "description": "Curated IOC warning-lists (known-good IPs, hosting providers, false-positive filters) maintained by the MISP community."},
            {"name": "MISP / MISP",
             "url": "https://github.com/MISP/MISP",
             "description": "Reference open-source threat-intel platform — supports STIX/TAXII import & cross-org sharing."},
            {"name": "Cyb3rWard0g / HELK",
             "url": "https://github.com/Cyb3rWard0g/HELK",
             "description": "Hunting ELK — Elastic-based threat-hunting platform with bundled detection analytics."},
            {"name": "SigmaHQ / sigma",
             "url": "https://github.com/SigmaHQ/sigma",
             "description": "Generic rule-based detection format; convert one rule into Splunk, Elastic, Sentinel, Crowdstrike etc."},
        ],
    },
}


def get_playbook(threat_type: str) -> dict:
    """Return the playbook for a known type, or the 'other' fallback."""
    return MITIGATIONS.get((threat_type or "").lower(), MITIGATIONS["other"])
