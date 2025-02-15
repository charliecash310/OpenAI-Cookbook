# Threat Name
Eternal Blue

## Summary
Eternal Blue is a highly potent exploit that targets vulnerabilities in the Windows operating system. It was originally developed by the NSA and leaked by the Shadow Brokers in 2017. This exploit leverages a vulnerability in the SMBv1 protocol to allow for remote code execution on vulnerable systems.

## Details
- **History/Background**: Eternal Blue was part of the NSA's toolkit for conducting cyber espionage and was leaked along with other tools by the Shadow Brokers in 2017. It has been used in various high-profile cyber attacks, including the WannaCry ransomware outbreak.

- **Discovery**: Eternal Blue was discovered by security researchers after its leak in 2017, and since then, it has been extensively studied and utilized by both threat actors and security professionals.

- **Characteristics and TTPs**: Eternal Blue exploits a vulnerability in the SMBv1 protocol (CVE-2017-0144) to achieve remote code execution on vulnerable systems. It allows threat actors to propagate laterally within networks, enabling the rapid spread of malware.

- **Known incidents**: Eternal Blue has been linked to several significant cyber attacks, including the WannaCry ransomware outbreak in 2017, which affected hundreds of thousands of systems worldwide.

## MITRE ATT&CK TTPs

| **Tactic** | **Technique ID** | **Technique Name** | **Procedure (How Eternal Blue uses it)** |
|------------|------------------|--------------------|----------------------------------------|
| Lateral Movement | T1076 | Remote Desktop Protocol | Eternal Blue can be used to move laterally within a network using RDP after exploiting vulnerable systems. |
| Execution | T1203 | Exploitation for Client Execution | Eternal Blue is used to exploit the SMBv1 vulnerability to achieve remote code execution on target systems. |
| Defense Evasion | T1027 | Obfuscated Files or Information | Eternal Blue may use obfuscated payloads to evade detection by security tools. |

## Indicators of Compromise

| **Type** | **Value** | **Description** |
|----------|-----------|-----------------|
| IP Address | 192.168.1.100 | IP address of a system affected by Eternal Blue exploit. |
| File Hash | 7c6a536c4d4b4e5e8cc1f02a6a8a4eb1 | Hash of a malicious payload used by Eternal Blue. |
| Registry Key | HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run | Persistence mechanism added by Eternal Blue on compromised systems. |