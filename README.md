# CRA Manual Tools

Free, browser-based tools for producing the two documentation artifacts the EU
Cyber Resilience Act (CRA) requires of every product with digital elements:

| Tool | CRA artifact | Live | Source |
|---|---|---|---|
| **CRA Manual Builder** | Annex II: Information & instructions to the user | [valuechainrisk.org/cra-manual-builder](https://valuechainrisk.org/cra-manual-builder/) | [`/cra-manual-builder`](./cra-manual-builder) |
| **TARA Builder** | Annex VII: product cybersecurity risk assessment | [valuechainrisk.org/tara](https://valuechainrisk.org/tara/) | [`/tara`](./tara) |
| **Context & Conditions of Use Builder, user-view preview** | The same tool plus a non-technical “user view” layer, in two renderings (A picture, B cards), for the working group to compare. Adds a fictitious consumer example with an ordinary-skill user. | [valuechainrisk.org/cyber-manual/context/next](https://valuechainrisk.org/cyber-manual/context/next/) | [`/cyber-manual/context/next`](./cyber-manual/context/next) |
| **Context & Conditions of Use Builder** | Cyber Manual ch. 2.2–2.5 (functions, context components, conditions of use, risks) + the diagrams | [valuechainrisk.org/cyber-manual/context](https://valuechainrisk.org/cyber-manual/context/) | [`/cyber-manual/context`](./cyber-manual/context) |

Together they cover the pair: the user-facing manual, and the risk assessment
behind it.

The tools work alone or as a chain. Each one can bring in another's work from
the same browser with one button: the Manual Builder brings in the Context
builder's lists and every diagram, or merges the TARA's accepted risks; the
Context builder and the TARA can start from the manual saved in the Manual
Builder. The other page is opened in a hidden frame on the same site and hands
its data back, so nothing is uploaded. The Context builder owns the chain
(components, interfaces, context, functions, conditions of use, circumstances,
diagrams); bringing it into the manual replaces those lists and never the prose.
The Manual Builder saves only when you press Save. Built for the small and mid-size manufacturers who cannot reach for
paywalled standards or a consultant for every product.

## A Cyber Manual Movement contribution

The [Value Chain Risk Institute](https://valuechainrisk.org) is a member of the
**Cyber Manual Movement** working group. These tools are built in the Movement's
established mode: **VCRI provides the engine and drafting aids; the working group
owns the template, the scenario libraries, and the worked examples.**

- The **Manual Builder** populates the Cyber Manual Movement's CRA
  "Information & instructions to the user" template (v0.39, 26 October 2026).
  It shows how full the manual is: a count of empty fields per section and
  overall, which is a mechanical count and not a judgement of what is written. The template and
  boilerplate are the working group's work; this repository does not republish
  them; it links to them and generates against them.
- The **Context & Conditions of Use Builder** (added 2026-09-10) answers the
  working group's hardest question, how much context and how many conditions
  to write, by treating it as a chain rather than a judgment: a context
  component exists only because a function needs it, a condition of use only
  because a context component must satisfy it, a risk only as a condition not
  met. Structure follows the working group's Engineering PC example v0.22
  (9 September 2026): product interfaces with a logical-interface table,
  context as components, persons (with skill) and zones (with type and access),
  conditions of use that can affect any of those or the product itself. Emits
  chapters 1.1.2, 1.1.3, 1.2.1, 2.2.1 to 2.2.3, 2.3.1, 2.4.1 and 2.5.1 in the
  template's chapter order, computes 2.7.2, and draws all six optional diagrams
  (1.1.4, 1.2.3, 2.2.4, 2.3.2, 2.4.2, 2.5.2) as layers over one picture, with
  function and risk paths as numbered steps. Ships with the working group's
  Engineering PC example, seeded faithfully; the level-of-detail checks show
  where that example is still incomplete, which is the point. The concept behind it is written up
  and citable as a method note: [The Derivation Rule for Context and Conditions
  of Use](./cyber-manual/context/METHOD.md) (Marpet & Viktor, VCRI, 2026).
  Since 8 November 2026 the structure follows template v0.39 and the Engineering
  PC example v0.40, and the builder can derive a first draft from a manual:
  "Derive from a manual" (or Import JSON) takes a file saved from the Manual
  Builder, fills the lists, and derives the links by twelve stated rules. Every
  derived link is marked as suggested until a person confirms or removes it, and
  what no rule reaches (zones, which interface a person touches) is listed as a
  gap. On the working group's Engineering PC example, held out, 76% of derived
  links are right and 67% of the hand-drawn links are found.
  How it works and what it leaves to a person: [DERIVE.md](./cyber-manual/context/DERIVE.md).
- The **TARA Builder** is the Annex VII companion VCRI authored to complete the
  pair. Its methodology is informed by ISO/SAE 21434-style TARA practice; all
  rubric anchors are authored originally, with no text reproduced from paywalled
  standards. It makes no conformance determination.

## Design principles

- **Single file, no build, no dependencies.** Each tool is one `index.html`.
  Open it locally, host it anywhere, read every line.
- **All-local. Nothing is transmitted.** State lives in your browser
  (`localStorage`); export/import is a JSON file you control. This matters
  doubly for a TARA, which enumerates a product's actual weaknesses.
- **Deterministic and versioned.** Rubrics are versioned JSON; the same inputs
  always produce the same result. No hidden scoring.
- **Honest by construction.** The TARA Builder labels each risk's evidence and
  makes no conformance claim; the Manual Builder marks what is manufacturer
  responsibility versus user condition-of-use.

## Examples

[`/examples`](./examples) holds three illustrative Cyber Manuals for real products (OpenWrt One, KeePassXC, Home Assistant Green), built from public documentation only, with their fact sheets, diagrams and rendered PDFs. None is the manufacturer's manual, and none claims CRA conformity. It also holds `derive_links.py`, the reference version of the context builder's "Derive from a manual" rules, and the held-out test that measures them.

## Contributing

Issues and pull requests welcome, especially from the working group. Good first
contributions: scenario libraries for the TARA class matrix, worked examples,
sector-specific interface lists, corrections to the Annex I crosswalk, and
translations. Nitpicks are a feature here, not a burden: these are compliance
tools, and precision is the point.

## License

[CC BY 4.0](./LICENSE). Use, adapt, and redistribute with attribution to the
Value Chain Risk Institute and the Cyber Manual Movement. SPDX: `CC-BY-4.0`.

---

*Value Chain Risk Institute · valuechainrisk.org · a member of the Cyber Manual Movement working group*
