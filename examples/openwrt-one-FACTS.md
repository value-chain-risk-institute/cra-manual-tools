# OpenWrt One: fact sheet for a CMM example manual

Cairn Viktor, 8 November 2026. Read through Claude in Chrome on 8 November 2026. Every fact below is from the source named beside it. Anything not found is marked NOT FOUND and is not invented in the example.

## Product (openwrt.org/toh/openwrt/one, last modified 2026-10-23)
- MediaTek Filogic 820 SoC (MT7981BA), 2 cores, 1300 MHz; Wi-Fi 6 dual-band (MT7981BA + MT7976CN), 3x3/2x2.
- 1x 2.5 Gbit WAN (RJ-45, also PoE-PD 802.3af/at), 1x 1 Gbit LAN.
- 1 GB DDR4; 256 MiB SPI NAND (normal boot); 16 MiB SPI NOR (recovery, write-protect jumper "NOR WP", factory default in place).
- M.2 2242/2230 for NVMe (PCIe gen 2 x1); USB 2.0 Type-A host; USB-C serial console (front, integrated USB-serial); USB-C PD power 15 V 2 A.
- 3 LEDs, 2 buttons (front, back "Reset"), NAND/NOR boot DIP switch (up = NAND), JTAG.
- FCC ID 2BLLI-HW24. Current supported release on the page: 25.12.6.
- Schematics and datasheets: one.openwrt.org/hardware/ ; HowTo PDF: one.openwrt.org/hardware/OpenWrtOne-HowTo.pdf
- Official distributors listed via Software Freedom Conservancy: sfconservancy.org/activities/openwrt-one.html
- Enclosure 148 x 100.5 mm.

## Defaults and first use (same page)
- Ships with the current release firmware at batch date, LuCI web UI installed.
- 1G port = LAN, 2.5G port = WAN by default (25.10 series). One user report of LAN/WAN reversed out of the box.
- LuCI at http://192.168.1.1 (plain HTTP); SSH root@192.168.1.1.
- First session: user root, EMPTY password.
- Wi-Fi: set Country Code first.

## Updates (same page)
- Attended Sysupgrade (LuCI System > Attended Sysupgrade), owut (CLI), Firmware Selector (web, "REQUEST BUILD").
- USB sysupgrade via bootloader (Reset held at power-on), NAND initramfs recovery (front button held), NOR full recovery reflashes NAND from USB, UART + TFTP to reflash NOR (needs WP jumper, unlock/lock in boot menu).
- No automatic updates described. Updates are user-initiated.

## Security process (openwrt.org/docs/guide-developer/security, last modified 2026-10-22)
- Vulnerability reporting: confidential mail to contact@openwrt.org; if no answer, brief non-detailed note to openwrt-adm@lists.openwrt.org. Mailbox "not always monitored".
- Advisories list on the same page; covers OpenWrt-maintained components only, not upstream (Linux kernel, OpenSSL); upstream fixes are backported to supported releases.
- Recent: 2025-12-16-1 Dropbear CVE-2025-14282; 2025-10-22-1 ubusd CVE-2025-62526; 2024-12-06-1 Attended SysUpgrade server build artifact poisoning CVE-2024-54143.
- Support status: 25.12 Supported (initial 2026-03-06, EoL TBD, latest 25.12.6 on 2026-10-18); 24.10 End of Life (2026-09).
- Policy: previous major moves to Security Maintenance when the next is released; EoL one year after initial release or 6 months after the next major, whichever is later. Covers core packages only, not external feeds.
- "Right after a fresh OpenWrt installation or a fresh upgrade, there is no initial root password set." Set via LuCI System > Administration > Router Password, or passwd.
- Package updates reach users in about 2 days via build bots; kernel and kernel-module fixes need a new minor release (full image).
- LuCI has no built-in brute-force protection (fail2ban must be installed by the user).
- Tools: uscan (weekly CVE check by CPE), Coverity Scan weekly, reproducible builds for master.
- Hardening build options on by default: format-security, stack-protector regular, FORTIFY_SOURCE=1, RELRO full, PIE for network-exposed binaries, kernel seccomp. SELinux off.

## CRA roles (to state carefully in the example)
- Hardware: Banana Pi (per openwrt.org "BananaPi OpenWrt One page"); distribution via SFC-listed distributors. Software: OpenWrt project (open-source steward candidate). Who is the CRA "manufacturer" of the shipped product is a question for the group, not asserted here.

## Software Freedom Conservancy page (sfconservancy.org/activities/openwrt-one.html, read 2026-11-08)
- "Manufactured in collaboration with Banana Pi." From US$125 with case. Official retailers: AliExpress, Joom (others listed as unofficial).
- Claims: "will never be locked down and is forever unbrickable"; copyleft-compliant source release from the start; mikroBUS expansion header.
- CONFLICT with the wiki: SFC says 128 MiB SPI NAND + 4 MiB SPI NOR and 12 V USB-PD; the wiki (edited 2026-10-23) says 256 MiB NAND, 16 MiB NOR, 15 V 2 A. The example uses the wiki figures and flags the conflict for the group; batch differences are possible.

## NOT FOUND (left blank or marked in the example)
- Product support period end date for the hardware.
- EU Declaration of Conformity, harmonised standards, CE/RED documentation.
- SBOM publication for the shipped image.
- Signature verification of sysupgrade images (not described on these pages).
