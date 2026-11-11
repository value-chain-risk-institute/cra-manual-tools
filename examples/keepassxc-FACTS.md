# KeePassXC: fact sheet for a CMM example manual

Cairn Viktor, 8 November 2026. Sources read 8 November 2026. Facts not found are marked NOT FOUND and are not invented in the example.

## Product
- Latest release 2.8.0, published 2026-10-21 (GitHub releases API; keepassxc.org/download).
- Desktop password manager for Windows 10/11 (x64, ARM64), macOS 12+ (Apple Silicon, Intel), Linux. No official mobile app (keepassxc.org/docs FAQ). Licence GPL v3 (user guide).
- Tagline on the download page: "Keep your passwords safe on the computer you trust. No clouds. No 3rd parties."
- Distribution: keepassxc.org downloads (.dmg, .msi, portable .zip, .AppImage, source .tar.xz), Microsoft Store, winget, Chocolatey, Homebrew Cask, Flatpak on Flathub ("recommended... with automatic updates"), Snap, distro packages (keepassxc.org/download).
- Database: KDBX file stored wherever the user chooses, "fully encrypted at all times" (user guide). AES-256 or Twofish (docs FAQ). KDF: Argon2 recommended (KDBX 4); AES-KDF for KDBX 3.1 (user guide).
- Additional factors: key file; hardware key challenge-response (YubiKey, OnlyKey) (user guide).
- Quick Unlock: enabled by default on Windows (Windows Hello) and macOS (Touch ID / Apple Watch), can be disabled in Application Settings > Security (user guide).
- Optional integrations: Browser Integration via KeePassXC-Browser extension and native messaging (off until "Enable browser integration" is ticked), passkeys through the browser extension, Auto-Type (global and entry level; Wayland limits), Secret Service provider over DBus (Linux), SSH Agent integration (OpenSSH agent, Pageant), KeeShare (shared groups), remote database sync, CLI tool (keepassxc-cli), Windows Group Policy enforcement of settings (user guide).
- Network: opt-in, used for favicon downloads; a build without networking is possible with -DWITH_XC_NETWORKING=OFF (docs FAQ).

## Integrity of releases (keepassxc.org/verifying-signatures)
- Every package has a .sig (PGP) and .DIGEST (SHA-256) sidecar.
- Windows MSI: Authenticode, verified publisher "DroidMonkey Apps, LLC".
- macOS: signed with the project's Apple Developer ID, checked by the OS at launch.
- "If you downloaded KeePassXC directly from our website, there is no need for further verification."

## Vulnerability handling (SECURITY.md, develop branch)
- Report via GitHub Security Advisory ("Report a Vulnerability"), private Matrix messages to named team members, or team@keepassxc.org (encrypt if possible). No public channels for initial reports.
- Team replies with next steps and keeps the reporter informed until fix and announcement.
- CVE policy: do not go to a CNA before the team confirms; restriction lapses if no response within 30 days.
- Third-party module vulnerabilities go to those maintainers.

## Assurance (keepassxc.org/audits)
- ANSSI Security Visa ANSSI-CSPN-2025/16, 17 Nov 2025, valid until 17 Nov 2028, KeePassXC 2.7.9 on Windows 10; certification report, certificate, security target, full technical report published.
- Application security review by Zaur Molotnikov, 19 Jan 2023, version 2.7.4 (source).

## CRA framing (for the group, not asserted)
- Developed by a volunteer team; the Windows binaries are published by DroidMonkey Apps, LLC. Whether any party is a CRA "manufacturer" (commercial activity) or the project falls under the open-source steward or non-commercial provisions is a question for the group. Password managers are listed in Annex III Class I.

## Answered by the KeePassXC Team (email to Joshua Marpet, 8 November 2026, in reply to our note of the same day)
- Support: "We generally support the latest release."
- "The default lock timeout is 900 seconds." (Not stated: whether locking after inactivity is switched on by default, and the clipboard-clear default.)
- SBOM: "We do not release an SBOM at the moment, but you can find our dependencies on GitHub in the vcpkg.json manifest file and the wiki."

## NOT FOUND
- A dated support period or end-of-support date per version (the team supports the latest release; see above).
- An in-app update check or automatic update mechanism (only Flatpak and store channels update automatically).
- Default clipboard-clear timeout, and whether auto-lock is on by default (lock timeout itself answered above).
- EU Declaration of Conformity. Postal address.
