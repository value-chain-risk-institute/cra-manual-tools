# Three real-product example manuals for the Cyber Manual Movement

Cairn Viktor for the Value Chain Risk Institute, 8 November 2026. Offered to the Cyber Manual Movement working group for discussion.

## What this is

Three illustrative Cybersecurity Manuals (template v0.39), built with the VCRI CRA Manual Builder from public documentation only, read on 8 November 2026. Each picks a real product whose documentation is public enough to fill the template, and each fills a slot in the exemplar coverage matrix (valuechainrisk.org/cra-manual-builder/exemplars/).

| Product | Matrix slot | Why it teaches something |
|---|---|---|
| OpenWrt One (router) | SOHO router, Important I, HW + firmware, radio | Hardware maker (Banana Pi) and software steward (OpenWrt project) are different parties. Ships with an empty root password, and the security page says so. |
| KeePassXC (password manager) | Password manager, Important I, pure software | Strong security documentation (ANSSI CSPN, signed releases, SECURITY.md) but no support period. It's a volunteer project, which tests the CRA's non-commercial and steward boundary. |
| Home Assistant Green (smart home hub) | Not in the matrix yet: local-first hub, wired-only (no onboard radio), sold by a company | The only one with an EU Declaration of Conformity (RoHS, EMC, LVD, ErP; no CRA yet). Physical console access resets the owner password. No support period is published. |

## Rules followed

- Every statement comes from the fact sheet beside it (`*-FACTS.md`), which names its source.
- Gaps are written as NOT FOUND, never filled with a plausible guess. The gaps are part of the lesson: none of the three publishes an SBOM, and none publishes a dated support period.
- Each manual says on its first page that it is an illustrative example, not the manufacturer's manual, and makes no claim about CRA conformity.
- CRA role allocation (who is the manufacturer, who is a steward) is left to the group.

## What the builder flagged

Annex I Part I rows with no Security Property or Condition of Use mapped:
- OpenWrt One: 2i (minimisation of negative impact on other services).
- KeePassXC: 2k (impact reduction), 2l (recording and monitoring).
- Home Assistant Green: 2e (confidentiality), 2i, 2l.

These are honest gaps in the public documentation, and they're good discussion material.

## Source conflicts to raise

- OpenWrt One flash sizes: the wiki says 256 MiB NAND and 16 MiB NOR; Software Freedom Conservancy says 128 MiB NAND and 4 MiB NOR. The manual uses the wiki figures.
- Home Assistant Green model number: datasheet v2.0 says NC-GREEN-9703 (changed 5 Aug 2025); the EU DoC of 3 Jul 2026 still names NC-GREEN-1175.

## Files

- `openwrt-one.cybermanual.json`, `keepassxc.cybermanual.json`, `home-assistant-green.cybermanual.json`: open in the builder with Import JSON.
- `*-example-manual-DRAFT.pdf`: the rendered manuals.
- `*-FACTS.md`: the sourced fact sheets.
- `build-examples.py`: regenerates the JSON from one place. `build-context.py` and `attach-and-print.py` draw the diagrams, embed them and print the PDFs.
- `derive_links.py`, `score_links.py`, `heldout-engineering-pc.*`: the link deriver and its held-out test on the working group's Engineering PC example (the group's own manual and hand links).

## Diagrams (added 8 Nov)

Each manual now carries every diagram the template has a slot for: the product diagram, the security property diagram, the context diagram, and one secure-use diagram per function. That's 26 in all, drawn by our Context & Conditions of Use builder from `*.context.json` and embedded in the manual JSON as SVG. Loose SVGs are in `diagrams/`.

The context builder's chain-integrity checker also flagged real modelling gaps. For example, the RAM, the M.2 slot and JTAG are used by no function, and a hardware key carries no condition of use. Each one is either a missing function or a row that doesn't belong, and that's worth putting to the group.

## Automating the links

`derive_links.py` reads a manual and derives the context links with twelve stated rules (R1 to R12, listed at the top of the file). Anything it can't derive is listed as a gap for a person. `score_links.py` measures it:

- On the working group's Engineering PC example, a held-out test with the group's own hand links that nothing was tuned to: 76% of the links it proposes are right, and it finds 67% of the hand links. Conditions of use and security properties come out at 100%.
- On these three products: 81% right, 57% found. These scores are weaker evidence, because I wrote both the hand links and the rules.
- What it can't do is zone membership (who sits inside the user's organisation and who sits with the manufacturer) and which components each function uses. Nothing in the manual states those. They are the manufacturer's assumptions, so they stay a short to-do list for a person, not a guess.

Built into the context builder on 8 November, after Joshua's go-ahead. There's a "Derive from a manual" button, and Import JSON also accepts a manual. Either one takes a file saved from the CRA Manual Builder, fills the lists, and derives the links with the same twelve rules. Each derived link gets a dashed outline until a person ticks or unticks it, or presses "accept all suggested links". A "Derived from a manual" group at the top of the checks lists what no rule reaches, and it shrinks as the gaps are filled. The JavaScript gives the same result as `derive_links.py` on all four manuals: 403 links, no differences.

## Corrections from the projects (11 November 2026)

We wrote to all three projects on 8 November and asked them to correct us. Two have answered, and their examples are now version 0.2. Each fact sheet quotes the reply it used.

- OpenWrt One: Luka Perkov replied on the openwrt-adm list on 10 November. The example no longer suggests the OpenWrt project could be an open-source software steward, because a steward is a legal person and the project is not one. The support section now says the release policy covers OpenWrt software releases and that the project declares no support period for hardware it does not sell.
- KeePassXC: the KeePassXC Team replied by email on 8 November. The team generally supports the latest release, and no SBOM is published at the moment (dependencies are in the vcpkg.json manifest and the wiki). Both were NOT FOUND before.
- Home Assistant Green: no reply yet. Unchanged at version 0.1.
