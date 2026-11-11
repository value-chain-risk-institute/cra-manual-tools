# Home Assistant Green: fact sheet for a CMM example manual

Cairn Viktor, 8 November 2026. Sources read 8 November 2026 (Claude in Chrome for the support portal, then its public Zendesk article API; Nabu Casa's own PDFs from github.com/NabuCasa/support). Facts not found are marked NOT FOUND and are not invented in the example.

## Manufacturer and conformity
- Manufacturer: Nabu Casa, Inc., 15 Hubble Suite 200, Irvine, CA 92618; green@nabucasa.com (datasheets v1.1 and v2.0; the EU DoC prints the postal address but no email).
- CONTACT ADDRESS DOES NOT WORK (checked 11 Nov 2026): our note of 8 November to green@nabucasa.com was rejected with "The email account that you tried to reach does not exist" (status 5.1.3). The address is still printed on both datasheets in github.com/NabuCasa/support (static/docs/green/). The example keeps it, because it is what the manufacturer's documentation states, and flags it here.
- nabucasa.com (read 11 Nov 2026) gives a different postal address: 1500 Valley House Drive Suite 210, Rohnert Park, CA 94928, USA. The datasheets and the DoC say Irvine. Flag for the group.
- EU DoC (issued 3 Jul 2026, signed Paulus Schoutsen), model NC-GREEN-1175: RoHS 2011/65/EU, EMC 2014/30/EU, LVD 2014/35/EU, ErP 2009/125/EC. Standards: EN IEC 63000:2018; EN 62368-1:2014 + A11:2017; EN IEC 55014-1/-2:2021, EN 55032:2015+A11:2020, EN IEC 61000-3-2:2019+A1:2021, EN 61000-3-3:2013+A2:2021, EN 55035:2017+A11:2020; EN 50563:2011/A1:2013. No RED (no radio). No CRA (not yet applicable).
- Datasheet v2.0 lists model NC-GREEN-9703 (SKU changed from NC-GREEN-1175 on 5 Aug 2025); the DoC still names NC-GREEN-1175. Flag for the group.
- Conformity marks: CE, FCC. Made in PRC.

## Product (datasheet; support articles updated 2026-01-16)
- Rockchip RK3566, quad-core Cortex-A55 at 1.8 GHz; 4 GB LPDDR4X; 32 GB eMMC.
- Gigabit Ethernet; 2x USB 2.0 Type-A host (5 V, 2 A combined); HDMI "for diagnostic purposes only"; microSD slot (recovery and diagnostics); 12 V DC 1 A barrel (5.5 x 2.1 mm, centre-positive), no PoE; optional CR2032 (not included); 3 status LEDs (white power, green activity, yellow system health heartbeat).
- No onboard radios: no Zigbee, Thread, Wi-Fi or Bluetooth. Radios only via USB dongles (Home Assistant Connect ZBT-1 for Zigbee/Thread, ZWA-2 for Z-Wave). Wi-Fi dongle not recommended.
- Indoor use only, 0 to 40 C, non-condensing.
- Preinstalled Home Assistant Operating System (HA OS includes Home Assistant Core and the Supervisor, which "keeps it up to date").

## Use and access
- Web UI at http://homeassistant.local or http://homeassistant.local:8123 (plain HTTP on the LAN) (support article updated 2026-08-18; onboarding docs).
- Onboarding: on first open, "Preparing Home Assistant" downloads the latest version (needs internet, 20+ minutes), then the user creates the owner account or restores a backup (home-assistant.io/getting-started/onboarding). No default password.
- Owner password reset: connect HDMI monitor + USB keyboard; the console opens automatically; "auth reset" sets a new password with no prior authentication (support articles). Physical access therefore equals account takeover.
- Factory reset (HA OS 13.1+, or SD card for older): wipes the data partition, "removes all user data as well as Home Assistant Core, Supervisor, and any ins[talled apps]"; requires a working internet connection, otherwise the reset fails.
- Backups: Nabu Casa advises storing backups off the device (Home Assistant Cloud or another location).

## Updates (home-assistant.io/common-tasks/os)
- HA OS updates appear under Settings (or Settings > System > Updates; "Check for updates" in the menu); the user selects Update; optional "Automatic backup before update". CLI: ha os update. User-initiated; no automatic installation described.

## Vulnerability handling (home-assistant.io/security)
- Report via GitHub Security Advisory; no public issues. Asks for 90 days before disclosure; aims to respond within 7 days; relies heavily on volunteers.
- Non-qualifying: scanner reports, theoretical attacks, third-party library issues, social engineering, attacks needing host access or physical access, malicious third-party integrations/apps, privilege escalation by logged-in users. "Home Assistant assumes every user is trusted."
- Past advisories are listed on the same page.

## NOT FOUND
- A stated support period for the hardware or end date for security updates.
- SBOM publication.
- Update signing and verification details (not on the pages read).
- Whether remote access (Home Assistant Cloud) is part of the product or a separate service; treated here as a context component.
