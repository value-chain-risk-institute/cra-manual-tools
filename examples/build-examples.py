#!/usr/bin/env python3
"""Write the three illustrative CMM example manuals as CRA Manual Builder JSON (template v0.39).
Every statement comes from the *-FACTS.md sheet beside this script; gaps say NOT FOUND instead of guessing.
Cairn Viktor for the Value Chain Risk Institute, 2026-11-08."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
NF = "NOT FOUND in the public documentation read on 8 November 2026."
DISC = ("Illustrative example for the Cyber Manual Movement, built by the Value Chain Risk Institute with the CRA Manual Builder "
        "from public documentation read on 8 November 2026. It is NOT the manufacturer's manual and makes no claim about CRA conformity. "
        "Gaps are marked NOT FOUND rather than filled in.")

def base(name, tmv, additional, refs):
    return {"tpl": "0.39",
            "meta": {"version": "0.1", "date": "2026-11-08", "author": "Cairn Viktor for the Value Chain Risk Institute (illustrative example, not the manufacturer's manual)"},
            "references": refs, "product": {"name": name, "tmv": tmv, "idguide": "", "additional": DISC + "\n" + additional, "family": ""},
            "dia": {"product": "", "sp": "", "context": "", "cu": "", "ri": ""},
            "opts": {"definitions": True}, "er1": {}, "er2": {}}

def T(*titles): return [{"title": t} for t in titles]
def TD(*pairs): return [{"title": a, "desc": b} for a, b in pairs]

# ---------------------------------------------------------------- OpenWrt One
o = base("OpenWrt One", "OpenWrt One (FCC ID 2BLLI-HW24) running OpenWrt 25.12.6",
    "Hardware manufactured by Banana Pi in collaboration with the OpenWrt project; the firmware is the OpenWrt project's. Which party is the CRA manufacturer, and whether the OpenWrt project acts as an open-source software steward, is left to the working group.\n"
    "Flash sizes conflict between sources: the OpenWrt wiki (edited 23 Oct 2026) says 256 MiB NAND and 16 MiB NOR; the Software Freedom Conservancy page says 128 MiB NAND and 4 MiB NOR. This example uses the wiki figures.",
    "openwrt.org/toh/openwrt/one (last modified 2026-10-23)\nopenwrt.org/docs/guide-developer/security (last modified 2026-10-22)\nsfconservancy.org/activities/openwrt-one.html\none.openwrt.org/hardware/ (schematics and datasheets)")
o["pc"] = T("MediaTek MT7981BA SoC (Filogic 820, 2 cores, 1.3 GHz)", "MediaTek MT7976CN Wi-Fi 6 radio", "1 GB DDR4 RAM",
            "256 MiB SPI NAND (normal boot: bootloader, kernel, root file system)", "16 MiB SPI NOR (recovery system, write-protect jumper)",
            "OpenWrt firmware with the LuCI web interface")
o["pi"] = T("2.5 Gbit Ethernet (WAN by default; PoE powered device, 802.3af/at)", "1 Gbit Ethernet (LAN by default)", "Wi-Fi 2.4 GHz and 5 GHz",
            "USB 2.0 Type-A host", "USB-C serial console", "USB-C power (PD, 15 V 2 A)", "M.2 2242/2230 slot (NVMe, PCIe gen 2 x1)",
            "NAND/NOR boot switch", "Front button and rear Reset button", "JTAG", "mikroBUS expansion header")
o["pp"] = [
 {"proto": "HTTP / TCP (LuCI web interface)", "pi": "PI02 1 Gbit Ethernet (LAN)", "port": "80", "fc": "FC03 Administer the router", "enabled": "yes"},
 {"proto": "SSH / TCP", "pi": "PI02 1 Gbit Ethernet (LAN)", "port": "22", "fc": "FC03 Administer the router", "enabled": "yes"},
 {"proto": "Wi-Fi (WPA2 or WPA3)", "pi": "PI03 Wi-Fi", "port": "/", "fc": "FC02 Provide Wi-Fi access", "enabled": "after configuration"},
 {"proto": "Serial console, 115200 8N1", "pi": "PI05 USB-C serial console", "port": "/", "fc": "FC04 Recover the firmware", "enabled": "yes"},
 {"proto": "USB mass storage (FAT32) read by the bootloader", "pi": "PI04 USB 2.0 Type-A", "port": "/", "fc": "FC04 Recover the firmware; FC05 Install security updates", "enabled": "on button press at power-on"},
 {"proto": "TFTP client (recovery, router at 192.168.11.11)", "pi": "PI02 1 Gbit Ethernet (LAN)", "port": "69", "fc": "FC04 Recover the firmware", "enabled": "boot menu only"},
 {"proto": "Request to the Attended Sysupgrade server", "pi": "PI01 2.5 Gbit Ethernet (WAN)", "port": "/", "fc": "FC05 Install security updates", "enabled": "user-initiated"}]
o["sp"] = [
 {"comp": "PC05 SPI NOR", "title": "Write-protected recovery system", "desc": "A stripped-down recovery system lives in SPI NOR, protected by the NOR WP jumper in its factory default position. With the boot switch on NOR, it re-flashes the whole NAND from a USB drive, even if the NAND bootloader or Trusted Firmware-A is broken.", "refs": "2f,2h,2k"},
 {"comp": "Product: OpenWrt One", "title": "Security fixes backported to supported releases", "desc": "The OpenWrt project backports security fixes for its core components to supported releases. Package fixes reach users in about two days through the build bots; kernel and kernel-module fixes need a new minor release.", "refs": "2c"},
 {"comp": "PC06 OpenWrt firmware", "title": "Compiler hardening by default", "desc": "Packages are built with format-security checks, stack protector (regular), FORTIFY_SOURCE=1, full RELRO and PIE for network-exposed binaries; the kernel has seccomp enabled. SELinux is not enabled.", "refs": "2j,2k"},
 {"comp": "PC06 OpenWrt firmware", "title": "Open source with reproducibility checks", "desc": "The firmware source is public and copyleft-compliant from the start. The reproducible-builds project checks that OpenWrt master builds reproducibly.", "refs": "2f"}]
o["er1"] = {"2b": "NOT MET BY DEFAULT: after a fresh installation or upgrade no root password is set (OpenWrt security page). The owner must set one before use; see chapter 3.2.",
            "2g": "The product only processes the following data:\nNetwork traffic routed between WAN, LAN and Wi-Fi\nConfiguration, including Wi-Fi keys and the root password",
            "2l": NF}
o["er2"] = {"v-test": "The OpenWrt project runs uscan weekly (package versions against upstream, and CVEs by CPE) and Coverity Scan weekly on OpenWrt-developed components.",
            "v-sbom": NF,
            "v-pub": "Advisories are published at openwrt.org/docs/guide-developer/security. They cover OpenWrt-maintained components only, not upstream components such as the Linux kernel or OpenSSL.",
            "v-cvd": "Report confidentially to contact@openwrt.org. The mailbox is not always monitored; if there is no answer, send a brief note without exploit details to openwrt-adm@lists.openwrt.org.",
            "v-contact": "contact@openwrt.org"}
o["cc"] = TD(("Upstream network", "The modem or ISP network connected to the 2.5 Gbit WAN port."),
             ("Wired LAN devices", "Computers and devices connected to the 1 Gbit LAN port or a switch behind it."),
             ("Wi-Fi clients", "Devices connecting over Wi-Fi."),
             ("Administration computer", "A computer with a browser (LuCI) or SSH client used to configure the router."),
             ("OpenWrt download and build servers", "Release download pages, the Firmware Selector and the Attended Sysupgrade server."),
             ("USB drive", "A FAT32 drive holding a sysupgrade or recovery image."),
             ("Recovery host", "A computer with a serial terminal and, for NOR re-flashing, a TFTP server at 192.168.11.23."))
o["cp"] = [{"title": "Owner / administrator", "desc": "The person who sets up and maintains the router.", "skill": "instructed"},
           {"title": "Network users", "desc": "People whose devices use the network.", "skill": "ordinary"},
           {"title": "Recovery technician", "desc": "A person re-flashing NAND or NOR using the recovery procedures.", "skill": "skilled"}]
o["cz"] = [{"title": "Home network", "desc": "LAN and Wi-Fi under the owner's control", "type": "communication", "access": "controlled"},
           {"title": "Internet", "desc": "Everything on the WAN side", "type": "communication", "access": "public"},
           {"title": "Physical location", "desc": "The room where the router is installed", "type": "physical", "access": "controlled"}]
o["fc"] = [
 {"title": "Route and filter traffic", "desc": "Forward traffic between the WAN port, the LAN port and Wi-Fi.", "rfu": "Use with the LAN and WAN ports swapped; one user reported this out of the box.", "kind": "core", "cus": "CU02, CU03"},
 {"title": "Provide Wi-Fi access", "desc": "Dual-band Wi-Fi 6 access point.", "rfu": "Operation without setting the country code.", "kind": "core", "cus": "CU04"},
 {"title": "Administer the router", "desc": "Configuration through LuCI at http://192.168.1.1 or SSH as root.", "rfu": "Administration from outside the home network.", "kind": "ancillary", "cus": "CU01, CU05, CU06"},
 {"title": "Recover the firmware", "desc": "NAND initramfs recovery (front button), NOR full recovery (boot switch on NOR, USB drive), and NOR re-flashing over UART and TFTP.", "rfu": "", "kind": "ancillary", "cus": "CU07, CU09"},
 {"title": "Install security updates", "desc": "User-initiated upgrade through LuCI Attended Sysupgrade, owut on the command line, the web Firmware Selector, or a USB drive read by the bootloader.", "rfu": "Installing SNAPSHOT builds instead of a release.", "kind": "ancillary", "cus": "CU03, CU08"}]
o["cu"] = [
 {"affected": "CP01 Owner / administrator", "title": "Set a strong root password before use", "desc": "Set it in LuCI (System > Administration > Router Password) or with passwd, before connecting other devices or enabling Wi-Fi.", "refs": "2b,2d"},
 {"affected": "CC01 Upstream network", "title": "Confirm the WAN and LAN ports", "desc": "Connect the upstream network to the 2.5 Gbit port and check in LuCI that it is the WAN interface before going online.", "refs": "2d,2j"},
 {"affected": "Product boundary OpenWrt One", "title": "Run a supported release", "desc": "Use a release with Supported or Security Maintenance status (25.12 as of 8 November 2026) and upgrade before it reaches End of Life.", "refs": "2c"},
 {"affected": "CC03 Wi-Fi clients", "title": "Set the country code and use WPA2 or WPA3", "desc": "Set the Wi-Fi country code first, then protect every SSID with WPA2 or WPA3.", "refs": "2d,2e"},
 {"affected": "CZ02 Internet", "title": "No administration from the internet", "desc": "Keep LuCI and SSH reachable from the home network only.", "refs": "2d,2j"},
 {"affected": "CZ01 Home network", "title": "Limit password guessing", "desc": "LuCI has no built-in brute-force protection. Restrict who can reach it, or install a tool such as fail2ban.", "refs": "2d"},
 {"affected": "CZ03 Physical location", "title": "Control physical access", "desc": "The serial console has no password prompt unless one is enabled, and the buttons and boot switch allow re-flashing. Keep the device where only trusted people can reach it.", "refs": "2d,2f"},
 {"affected": "CC05 OpenWrt download and build servers", "title": "Use only official images", "desc": "Obtain images only from the OpenWrt download pages, the Firmware Selector or Attended Sysupgrade.", "refs": "2c,2f"},
 {"affected": "PC05 SPI NOR", "title": "Keep the NOR write protection", "desc": "Leave the NOR WP jumper in its factory position; when re-flashing NOR, unlock it from the boot menu, then lock it again (menu item 7) and remove the jumper.", "refs": "2f,2k"}]
o["ri"] = [
 {"title": "No root password", "desc": "The owner never sets a root password.", "fc": "FC03", "cu": "CU01", "risk": "Anyone on the LAN or Wi-Fi can log in as root through LuCI or SSH and take full control."},
 {"title": "Ports swapped", "desc": "The upstream network is plugged into the LAN port.", "fc": "FC01", "cu": "CU02", "risk": "The administration interfaces face the upstream network."},
 {"title": "End-of-life release", "desc": "The router stays on a release past End of Life (24.10 reached it in September 2026).", "fc": "FC01, FC05", "cu": "CU03", "risk": "New vulnerabilities, even severe ones, are no longer fixed."},
 {"title": "Open or misconfigured Wi-Fi", "desc": "An SSID runs without WPA2 or WPA3, or without the correct country code.", "fc": "FC02", "cu": "CU04", "risk": "Strangers can join the network; operation may break radio rules."},
 {"title": "Administration exposed to the internet", "desc": "LuCI or SSH is opened to the WAN side.", "fc": "FC03", "cu": "CU05", "risk": "Attackers on the internet can attempt to log in or exploit the interface."},
 {"title": "Password guessing", "desc": "LuCI is reachable by many devices and nothing limits login attempts.", "fc": "FC03", "cu": "CU06", "risk": "A weak password can be guessed."},
 {"title": "Unattended physical access", "desc": "Untrusted people can reach the device.", "fc": "FC04", "cu": "CU07", "risk": "Console access or re-flashing gives full control."},
 {"title": "Image from an unofficial source", "desc": "A firmware image is taken from a forum, a mirror or a seller.", "fc": "FC05", "cu": "CU08", "risk": "Malicious firmware is installed."},
 {"title": "NOR left unlocked", "desc": "NOR is not locked again after re-flashing.", "fc": "FC04", "cu": "CU09", "risk": "The recovery system can be overwritten, so the failsafe no longer protects the device."}]
o["commissioning"] = ("Set the NAND/NOR switch to NAND (up).\nConnect a computer to the 1 Gbit port (LAN by default) and power the device by USB-C or PoE on the 2.5 Gbit port.\n"
    "Open http://192.168.1.1 and log in as root with an empty password, then set a strong root password immediately.\n"
    "Set the Wi-Fi country code before enabling Wi-Fi.\nCheck that a supported release is installed and upgrade if not.")
o["updates"] = {"note": "Updates are user-initiated: LuCI System > Attended Sysupgrade, owut upgrade on the command line, the web Firmware Selector, or a USB drive read by the bootloader (hold Reset at power-on). Package fixes can arrive in about two days; kernel fixes need a new minor release image.",
    "disableAuto": "The product does not install updates automatically.",
    "end": "Per OpenWrt release, not per device: 25.12 is Supported with end of life to be announced. A release reaches End of Life one year after its initial release or six months after the next major release, whichever is later. No hardware support period is published."}
o["decommission"] = "Use NOR recovery to factory re-flash the entire NAND, which removes the configuration, Wi-Fi keys and passwords.\nRemove any USB drive or NVMe SSD; they keep their data."
o["mfr"] = {"name": "Banana Pi (hardware), with the OpenWrt project (firmware). CRA role allocation is for the working group.", "address": NF, "email": "contact@openwrt.org (OpenWrt project)",
            "website": "openwrt.org/toh/openwrt/one", "updatesUrl": "firmware-selector.openwrt.org", "advisoriesUrl": "openwrt.org/docs/guide-developer/security"}
o["vuln"] = {"contact": "contact@openwrt.org (confidential); fallback openwrt-adm@lists.openwrt.org without exploit details", "policy": "openwrt.org/docs/guide-developer/security"}
o["doc"] = {"link": "NOT FOUND: no EU Declaration of Conformity located on 8 November 2026."}
o["sbom"] = {"access": NF, "format": ""}

# ---------------------------------------------------------------- KeePassXC
k = base("KeePassXC", "KeePassXC 2.8.0 (released 21 October 2026)",
    "Desktop password manager for Windows, macOS and Linux, licensed GPL v3. Password managers are listed in CRA Annex III, Class I. KeePassXC is developed by a volunteer team, and its Windows installer names DroidMonkey Apps, LLC as publisher. Whether anyone is a CRA manufacturer here, or the non-commercial and open-source steward provisions apply, is left to the working group.",
    "keepassxc.org/download\nkeepassxc.org/verifying-signatures\nkeepassxc.org/audits\nkeepassxc.org/docs (FAQ) and keepassxc.org/docs/KeePassXC_UserGuide\ngithub.com/keepassxreboot/keepassxc/blob/develop/SECURITY.md")
k["pc"] = T("KeePassXC desktop application", "keepassxc-cli command-line tool", "Browser integration (native messaging host)")
k["pi"] = T("Keyboard, display and clipboard (through the host operating system)", "File system (database, key files, attachments)", "USB (hardware keys, through the host operating system)")
k["pp"] = [
 {"proto": "Native messaging with the KeePassXC-Browser extension (local)", "pi": "PI01 Keyboard, display and clipboard", "port": "/", "fc": "FC02 Fill credentials in the browser", "enabled": "no (off until enabled)"},
 {"proto": "Synthetic keystrokes (Auto-Type)", "pi": "PI01 Keyboard, display and clipboard", "port": "/", "fc": "FC03 Auto-Type into other applications", "enabled": "on user action"},
 {"proto": "Secret Service over D-Bus (Linux)", "pi": "/", "port": "/", "fc": "FC01 Store and retrieve credentials", "enabled": "no (off until enabled)"},
 {"proto": "SSH agent (OpenSSH agent, Pageant)", "pi": "/", "port": "/", "fc": "FC01 Store and retrieve credentials", "enabled": "no (setup required)"},
 {"proto": "HTTPS favicon download", "pi": "/", "port": "443", "fc": "FC01 Store and retrieve credentials", "enabled": "opt-in"},
 {"proto": "Hardware key challenge-response (YubiKey, OnlyKey)", "pi": "PI03 USB", "port": "/", "fc": "FC01 Store and retrieve credentials; FC04 Unlock the database", "enabled": "if configured"}]
k["sp"] = [
 {"comp": "Product: KeePassXC", "title": "Database encryption", "desc": "The database is encrypted with AES-256 or Twofish and is encrypted at all times on disk.", "refs": "2e,2f"},
 {"comp": "Product: KeePassXC", "title": "Key derivation against guessing", "desc": "With KDBX 4, the Argon2 key derivation function (recommended) transforms the composite master key, making dictionary attacks slower.", "refs": "2d,2e"},
 {"comp": "Product: KeePassXC", "title": "Additional unlock factors", "desc": "A key file and hardware-key challenge-response (YubiKey, OnlyKey) can be added to the master password.", "refs": "2d"},
 {"comp": "Product: KeePassXC", "title": "Protected attributes", "desc": "Attributes marked Protect are hidden by default and shown only on Reveal.", "refs": "2e"},
 {"comp": "Product: KeePassXC", "title": "No network access by default", "desc": "Network access is opt-in (favicon downloads); a build without networking code is possible.", "refs": "2j"},
 {"comp": "Product: KeePassXC", "title": "Signed releases", "desc": "Every package ships with a PGP signature and a SHA-256 digest. The Windows MSI carries an Authenticode signature (DroidMonkey Apps, LLC); macOS builds are signed with the project's Apple Developer ID and checked at launch.", "refs": "2c,2f"}]
k["er1"] = {"2b": "Browser integration, Secret Service, SSH agent and network features are off until the user enables them. Quick Unlock (Windows Hello, Touch ID) is ON by default on Windows and macOS and can be disabled under Application Settings > Security.",
            "2g": "The product only processes the following data:\nCredentials, notes and attachments the user stores\nFavicons, only if the user enables downloading them"}
k["er2"] = {"v-test": "Independent reviews: ANSSI Security Visa ANSSI-CSPN-2025/16 (17 November 2025, valid to 17 November 2028, version 2.7.9 on Windows 10) and an application security review by Zaur Molotnikov (19 January 2023, version 2.7.4). Reports are published at keepassxc.org/audits.",
            "v-sbom": NF, "v-pub": NF,
            "v-cvd": "SECURITY.md: report privately through a GitHub Security Advisory, private Matrix messages to named team members, or email. No public channels for first reports. Reporters should not go to a CVE Numbering Authority before the team confirms, unless the team has not responded within 30 days.",
            "v-contact": "team@keepassxc.org (encryption recommended)",
            "v-dist": "Packages are signed and published with SHA-256 digests; see chapter 3.4."}
k["cc"] = TD(("Host computer and operating system", "The Windows, macOS or Linux computer KeePassXC runs on."),
             ("Database storage location", "Local disk, a synced folder or a remote location holding the database file."),
             ("Web browser with KeePassXC-Browser", "A browser with the extension installed from its official store."),
             ("Hardware key", "A YubiKey or OnlyKey configured for challenge-response."),
             ("Distribution channels", "keepassxc.org, Microsoft Store, winget, Chocolatey, Homebrew, Flathub, Snap and distribution packages."),
             ("Other applications", "Programs that receive Auto-Type keystrokes or Secret Service and SSH agent requests."))
k["cp"] = [{"title": "User", "desc": "The person who keeps passwords in the database.", "skill": "ordinary"},
           {"title": "Administrator", "desc": "A person enforcing settings through Windows Group Policy.", "skill": "skilled"}]
k["cz"] = [{"title": "User's computer", "desc": "The host computer and its user account", "type": "physical + communication", "access": "controlled"},
           {"title": "Storage and sync services", "desc": "Places outside the computer where the database is stored or synced", "type": "communication", "access": "limited"}]
k["fc"] = [
 {"title": "Store and retrieve credentials", "desc": "Create, edit, search and copy entries in an encrypted KDBX database.", "rfu": "Keeping the only copy of the database on one device.", "kind": "core", "cus": "CU01, CU02, CU03"},
 {"title": "Fill credentials in the browser", "desc": "Browser integration with KeePassXC-Browser, including passkeys.", "rfu": "", "kind": "ancillary", "cus": "CU04"},
 {"title": "Auto-Type into other applications", "desc": "Type the username and password into the previously selected window.", "rfu": "Auto-Type into the wrong window.", "kind": "ancillary", "cus": "CU05"},
 {"title": "Unlock the database", "desc": "Unlock with the master password and optional key file or hardware key, or with Quick Unlock (biometrics).", "rfu": "Quick Unlock on a computer account other people use.", "kind": "core", "cus": "CU01, CU06"},
 {"title": "Share and sync databases", "desc": "KeeShare shared groups and remote database synchronisation.", "rfu": "", "kind": "ancillary", "cus": "CU02, CU07"},
 {"title": "Install security updates", "desc": "Install the newest signed release from the channel used for installation.", "rfu": "", "kind": "ancillary", "cus": "CU08"}]
k["cu"] = [
 {"affected": "CP01 User", "title": "Strong master password", "desc": "Use a strong master password; add a key file or hardware key for more protection.", "refs": "2d"},
 {"affected": "CC02 Database storage location", "title": "Keep backups", "desc": "Back up the database, key files and hardware-key secrets (the user guide explains creating a YubiKey backup).", "refs": "2h"},
 {"affected": "CC01 Host computer and operating system", "title": "Use a computer you trust", "desc": "Run KeePassXC only on a computer that is kept updated and free of malware.", "refs": "2d,2e,2i"},
 {"affected": "CC03 Web browser with KeePassXC-Browser", "title": "Official extension only", "desc": "Install KeePassXC-Browser only from the official browser stores and connect only your own browsers.", "refs": "2d,2j"},
 {"affected": "CP01 User", "title": "Check the target window", "desc": "Before Auto-Type, make sure the intended window has focus.", "refs": "2e"},
 {"affected": "CZ01 User's computer", "title": "Quick Unlock only on a personal account", "desc": "Disable Quick Unlock if other people can use the same computer account or biometrics.", "refs": "2d"},
 {"affected": "CZ02 Storage and sync services", "title": "Trusted storage and sharing", "desc": "Store or sync the database only in locations you control or trust, and share groups only with intended people.", "refs": "2e,2f"},
 {"affected": "CC05 Distribution channels", "title": "Official, verified downloads", "desc": "Install from keepassxc.org or an official channel. On Windows, check that the verified publisher is DroidMonkey Apps, LLC; for other sources, verify the PGP signature.", "refs": "2c,2f"}]
k["ri"] = [
 {"title": "Weak master password", "desc": "A short or reused master password without another factor.", "fc": "FC01, FC04", "cu": "CU01", "risk": "Anyone who obtains the database file can guess the password offline."},
 {"title": "No backup", "desc": "The only copy of the database, key file or hardware-key secret is lost.", "fc": "FC01, FC05", "cu": "CU02", "risk": "All stored credentials become unrecoverable."},
 {"title": "Compromised computer", "desc": "Malware runs on the host computer.", "fc": "FC01", "cu": "CU03", "risk": "Credentials can be captured while the database is unlocked."},
 {"title": "Unofficial browser extension", "desc": "An extension from another source is connected.", "fc": "FC02", "cu": "CU04", "risk": "Credentials are handed to an attacker-controlled extension."},
 {"title": "Auto-Type into the wrong window", "desc": "The focused window is not the intended one.", "fc": "FC03", "cu": "CU05", "risk": "The password is typed into a chat, a document or a hostile page."},
 {"title": "Quick Unlock on a shared account", "desc": "Quick Unlock stays enabled on a computer account others use.", "fc": "FC04", "cu": "CU06", "risk": "Another person can unlock the database."},
 {"title": "Untrusted storage or sharing", "desc": "The database is kept or shared in a location others control.", "fc": "FC05", "cu": "CU07", "risk": "The encrypted file is exposed to offline attack or tampering."},
 {"title": "Tampered installer", "desc": "KeePassXC is installed from an unofficial source without verification.", "fc": "FC06", "cu": "CU08", "risk": "A modified program can steal every credential."}]
k["commissioning"] = ("Download from keepassxc.org or an official channel and verify it (chapter 3.4).\nCreate a database in KDBX 4 format with Argon2.\n"
    "Set a strong master password; optionally add a key file or hardware key.\nDecide whether Quick Unlock should stay enabled.\nSet up a backup of the database.")
k["updates"] = {"note": "Install new releases from the channel used for installation. Flatpak (recommended on Linux) and store channels can update automatically; website downloads are replaced with the new signed package. Verify signatures as described at keepassxc.org/verifying-signatures.",
    "disableAuto": "No in-app update mechanism was found in the documentation read; automatic updating depends on the distribution channel.",
    "end": "NOT FOUND: no support period is published."}
k["decommission"] = "Delete the database files, key files and backups from every location they were stored.\nRemove the browser extension, then uninstall KeePassXC."
k["mfr"] = {"name": "KeePassXC Team (volunteer project); Windows binaries published by DroidMonkey Apps, LLC. CRA role allocation is for the working group.",
            "address": NF, "email": "team@keepassxc.org", "website": "keepassxc.org", "updatesUrl": "keepassxc.org/download", "advisoriesUrl": NF}
k["vuln"] = {"contact": "GitHub Security Advisory on keepassxreboot/keepassxc, or team@keepassxc.org (encrypt if possible)", "policy": "github.com/keepassxreboot/keepassxc/blob/develop/SECURITY.md"}
k["doc"] = {"link": "NOT FOUND: no EU Declaration of Conformity located on 8 November 2026."}
k["sbom"] = {"access": NF, "format": ""}

# ---------------------------------------------------------------- Home Assistant Green
h = base("Home Assistant Green", "NC-GREEN-9703 (datasheet v2.0); the EU Declaration of Conformity names NC-GREEN-1175",
    "Smart home hub running Home Assistant Operating System, manufactured by Nabu Casa, Inc. It has no onboard radios; Zigbee, Thread and Z-Wave need USB adapters. The datasheet changed the SKU from NC-GREEN-1175 to NC-GREEN-9703 on 5 August 2025, while the EU DoC of 3 July 2026 still names NC-GREEN-1175.",
    "Datasheet v2.0 (4 Aug 2025) and EU DoC (3 Jul 2026), github.com/NabuCasa/support\nsupport.nabucasa.com Home Assistant Green articles (updated 2026)\nhome-assistant.io/security\nhome-assistant.io/getting-started/onboarding\nhome-assistant.io/common-tasks/os")
h["pc"] = T("Rockchip RK3566 SoC (quad-core Cortex-A55, 1.8 GHz)", "4 GB LPDDR4X RAM", "32 GB eMMC", "Home Assistant Operating System (Home Assistant Core and Supervisor)", "Optional CR2032 battery (not included)")
h["pi"] = T("Gigabit Ethernet", "2x USB 2.0 Type-A", "HDMI (diagnostics only)", "microSD slot (recovery and diagnostics)", "DC power, 12 V 1 A", "3 status LEDs")
h["pp"] = [
 {"proto": "HTTP / TCP (web interface)", "pi": "PI01 Gigabit Ethernet", "port": "8123 or 80", "fc": "FC01 Run the smart home; FC02 Administer Home Assistant", "enabled": "yes"},
 {"proto": "Local console (HDMI monitor and USB keyboard)", "pi": "PI03 HDMI; PI02 USB", "port": "/", "fc": "FC04 Recover access", "enabled": "yes, opens automatically"},
 {"proto": "Zigbee, Thread or Z-Wave through USB adapters", "pi": "PI02 USB", "port": "/", "fc": "FC01 Run the smart home", "enabled": "no (adapter needed)"},
 {"proto": "Outbound connection to update servers", "pi": "PI01 Gigabit Ethernet", "port": "/", "fc": "FC05 Install security updates; FC06 Factory reset", "enabled": "yes"}]
h["sp"] = [
 {"comp": "PC04 Home Assistant Operating System", "title": "No default account", "desc": "The owner account and password are created during onboarding; there is no default password.", "refs": "2b,2d"},
 {"comp": "Product: Home Assistant Green", "title": "No onboard radios", "desc": "The device has no Wi-Fi, Bluetooth, Zigbee or Thread radio; radio interfaces exist only if the user adds adapters.", "refs": "2j"},
 {"comp": "PC04 Home Assistant Operating System", "title": "Backup before update", "desc": "Updates offer an automatic or manual backup before they are installed.", "refs": "2h,2k"},
 {"comp": "PC03 32 GB eMMC", "title": "Factory reset clears the data partition", "desc": "The reset removes all user data as well as Home Assistant Core, the Supervisor and installed apps.", "refs": "2m"}]
h["er1"] = {"2b": "No default password; the owner account is created at first setup.",
            "2g": "The product only processes the following data:\nUser accounts and credentials\nSmart home device states, automations and configuration\nData from integrations the user installs",
            "2h": "Backups, stored off the device, and the backup-before-update option support recovery."}
h["er2"] = {"v-cvd": "Report through a GitHub Security Advisory; no public issues. Nabu Casa asks for at least 90 days before disclosure and aims to respond within 7 days, noting reliance on volunteers.",
            "v-pub": "Past security issues are listed at home-assistant.io/security.",
            "v-contact": "GitHub Security Advisory (home-assistant.io/security)", "v-sbom": NF}
h["cc"] = TD(("Home router and network", "The wired network the device connects to by Ethernet."),
             ("Smart home devices", "Devices controlled through integrations or USB radio adapters."),
             ("USB radio adapters", "For example Home Assistant Connect ZBT-1 (Zigbee or Thread) or ZWA-2 (Z-Wave)."),
             ("Administration device", "A browser or phone used to open the web interface."),
             ("Update servers", "Servers delivering Home Assistant versions during onboarding and updates."),
             ("Off-device backup location", "Home Assistant Cloud or another location outside the device."),
             ("Monitor and keyboard", "Used for the local console during recovery."))
h["cp"] = [{"title": "Owner", "desc": "The person who sets up the hub and holds the owner account.", "skill": "instructed"},
           {"title": "Household users", "desc": "People with their own Home Assistant accounts.", "skill": "ordinary"}]
h["cz"] = [{"title": "Home network", "desc": "The owner's local network", "type": "communication", "access": "controlled"},
           {"title": "Internet", "desc": "Everything outside the home network", "type": "communication", "access": "public"},
           {"title": "Physical location", "desc": "Where the hub is installed (indoors, 0 to 40 C)", "type": "physical", "access": "controlled"}]
h["fc"] = [
 {"title": "Run the smart home", "desc": "Run Home Assistant integrations and automations for connected devices.", "rfu": "Installing third-party integrations or apps.", "kind": "core", "cus": "CU02, CU03, CU04"},
 {"title": "Administer Home Assistant", "desc": "Configure the system and accounts in the web interface.", "rfu": "Giving accounts to people who should not have full trust.", "kind": "core", "cus": "CU01, CU02"},
 {"title": "Back up and restore", "desc": "Create backups and restore or migrate from them.", "rfu": "", "kind": "ancillary", "cus": "CU05"},
 {"title": "Recover access", "desc": "Reset the owner password from the local console with an HDMI monitor and USB keyboard.", "rfu": "", "kind": "ancillary", "cus": "CU06"},
 {"title": "Install security updates", "desc": "Install Home Assistant OS updates from Settings, or ha os update on the command line.", "rfu": "", "kind": "ancillary", "cus": "CU05, CU07"},
 {"title": "Factory reset", "desc": "Clear the data partition and reinstall (HA OS 13.1 or later, or with an SD card).", "rfu": "", "kind": "ancillary", "cus": "CU05, CU08"}]
h["cu"] = [
 {"affected": "CP01 Owner", "title": "Strong passwords, trusted users only", "desc": "Use a strong owner password and create accounts only for people you trust fully: Home Assistant assumes every user is trusted.", "refs": "2d"},
 {"affected": "CC01 Home router and network", "title": "Wired, local, not exposed", "desc": "Connect by Ethernet to a network you control and do not expose the web interface (port 8123) directly to the internet.", "refs": "2d,2j"},
 {"affected": "CP01 Owner", "title": "Trusted integrations and apps only", "desc": "Install only integrations, apps and plugins from sources you trust; malicious third-party additions are outside Home Assistant's security scope.", "refs": "2d,2f"},
 {"affected": "CC03 USB radio adapters", "title": "Known adapters", "desc": "Use radio adapters from known sources.", "refs": "2f"},
 {"affected": "CC06 Off-device backup location", "title": "Backups off the device", "desc": "Store backups outside the device, for example in Home Assistant Cloud or another location.", "refs": "2h"},
 {"affected": "CZ03 Physical location", "title": "Control physical access", "desc": "Anyone with a monitor and keyboard can reset the owner password from the console. Keep the hub where only trusted people can reach it.", "refs": "2d,2f"},
 {"affected": "PC04 Home Assistant Operating System", "title": "Install updates and check afterwards", "desc": "Install Home Assistant OS updates when offered, then check Settings > System > Repairs and Logs.", "refs": "2c"},
 {"affected": "CC05 Update servers", "title": "Internet during reset", "desc": "Make sure the hub has a working internet connection before a factory reset; otherwise the reset fails.", "refs": "2h"}]
h["ri"] = [
 {"title": "Untrusted account holder", "desc": "An account is given to someone who should not have full control.", "fc": "FC02", "cu": "CU01", "risk": "Any logged-in user can change the system; privilege escalation by users is out of scope."},
 {"title": "Web interface exposed to the internet", "desc": "Port 8123 is forwarded from the internet.", "fc": "FC01, FC02", "cu": "CU02", "risk": "Attackers can attempt to log in or exploit the interface."},
 {"title": "Malicious integration", "desc": "A third-party integration, app or plugin is installed from an untrusted source.", "fc": "FC01", "cu": "CU03", "risk": "The smart home and its data are controlled by the attacker."},
 {"title": "No off-device backup", "desc": "Backups are kept only on the hub.", "fc": "FC03, FC05, FC06", "cu": "CU05", "risk": "A failed update, reset or device loss destroys the configuration."},
 {"title": "Unattended physical access", "desc": "Untrusted people can reach the hub.", "fc": "FC04", "cu": "CU06", "risk": "The owner password can be reset and the system taken over."},
 {"title": "Updates not installed", "desc": "Offered updates are ignored.", "fc": "FC05", "cu": "CU07", "risk": "Known vulnerabilities stay unfixed."},
 {"title": "Reset without internet", "desc": "A factory reset is started without internet.", "fc": "FC06", "cu": "CU08", "risk": "The reset fails and leaves the device unusable until recovered."}]
h["commissioning"] = ("Connect power and Ethernet.\nOpen http://homeassistant.local (or :8123) and wait while Home Assistant downloads its latest version; this needs internet and can take 20 minutes or more.\n"
    "Create the owner account with a strong password, or restore from a backup.\nSet up backups to a location outside the device.")
h["updates"] = {"note": "Settings shows available Home Assistant OS updates (or Settings > System > Updates; Check for updates in the menu). Turn on the backup-before-update option, select Update, then check Repairs and Logs. Command line: ha os update.",
    "disableAuto": "Updates are installed when the user selects Update; no automatic installation is described.",
    "end": "NOT FOUND: Nabu Casa publishes no end date for security updates."}
h["decommission"] = "Create a backup if you want to keep the configuration, then factory reset the device; this clears the data partition (user data, Core, Supervisor and apps) and needs internet.\nRemove any microSD card and USB storage."
h["mfr"] = {"name": "Nabu Casa, Inc.", "address": "15 Hubble Suite 200, Irvine, CA 92618, USA", "email": "green@nabucasa.com",
            "website": "home-assistant.io/green", "updatesUrl": "home-assistant.io/common-tasks/os", "advisoriesUrl": "home-assistant.io/security"}
h["vuln"] = {"contact": "GitHub Security Advisory (see home-assistant.io/security)", "policy": "home-assistant.io/security"}
h["doc"] = {"link": "raw.githubusercontent.com/NabuCasa/support/refs/heads/main/static/docs/green/Green_DoC_EU.pdf (RoHS, EMC, LVD, ErP; no CRA, which does not yet apply)"}
h["sbom"] = {"access": NF, "format": ""}

for slug, m in (("openwrt-one", o), ("keepassxc", k), ("home-assistant-green", h)):
    for key in ("pc","pi","pp","sp","cc","cp","cz","fc","cu","ri"):
        m.setdefault(key, [])
    m.setdefault("commissioning", ""); m.setdefault("decommission", "")
    m["product"]["idguide"] = m["product"]["idguide"] or NF
    if not m["sbom"].get("format"): m["sbom"]["format"] = "NOT FOUND"
    if not m["mfr"].get("email"): m["mfr"]["email"] = NF
    for f in m["fc"]:  # the template's own wording when nothing extra is foreseeable (security-update functions excepted, as in the EXAMPLE)
        if not f["rfu"] and "security update" not in f["title"].lower(): f["rfu"] = "None beyond the function description."
    p = os.path.join(HERE, f"{slug}.cybermanual.json")
    json.dump(m, open(p, "w"), indent=2, ensure_ascii=False)
    print(p, len(m["fc"]), "functions", len(m["cu"]), "CUs", len(m["ri"]), "CRs")
