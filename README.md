# CRA Manual Tools

Free, browser-based tools for producing the two documentation artifacts the EU
Cyber Resilience Act (CRA) requires of every product with digital elements:

| Tool | CRA artifact | Live | Source |
|---|---|---|---|
| **CRA Manual Builder** | Annex II — Information & instructions to the user | [valuechainrisk.org/cra-manual-builder](https://valuechainrisk.org/cra-manual-builder/) | [`/cra-manual-builder`](./cra-manual-builder) |
| **TARA Builder** | Annex VII — product cybersecurity risk assessment | [valuechainrisk.org/tara](https://valuechainrisk.org/tara/) | [`/tara`](./tara) |
| **Context & Conditions of Use Builder** | Cyber Manual ch. 2.2–2.5 (functions, context components, conditions of use, risks) + the diagrams | [valuechainrisk.org/cyber-manual/context](https://valuechainrisk.org/cyber-manual/context/) | [`/cyber-manual/context`](./cyber-manual/context) |

Together they cover the pair: the user-facing manual, and the risk assessment
behind it. Built for the small and mid-size manufacturers who cannot reach for
paywalled standards or a consultant for every product.

## A Cyber Manual Movement contribution

The [Value Chain Risk Institute](https://valuechainrisk.org) is a member of the
**Cyber Manual Movement** working group. These tools are built in the Movement's
established mode: **VCRI provides the engine and drafting aids; the working group
owns the template, the scenario libraries, and the worked examples.**

- The **Manual Builder** populates the Cyber Manual Movement's CRA
  "Information & instructions to the user" template (v0.20). The template and
  boilerplate are the working group's work; this repository does not republish
  them — it links to them and generates against them.
- The **Context & Conditions of Use Builder** (added 2026-09-10) answers the
  working group's hardest question, how much context and how many conditions
  to write, by treating it as a chain rather than a judgment: a context
  component exists only because a function needs it, a condition of use only
  because a context component must satisfy it, a risk only as a condition not
  met. Built to template v0.23; emits chapters 1.2.1, 2.2.1, 2.3.1, 2.4.1 and
  2.5.1 in the template's column order, computes 2.7.2, and draws the optional
  diagrams (2.2.2, 2.3.2, 2.4.2) from the same lists. Ships with the fictitious
  Engineering PC example fully populated.
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

## Contributing

Issues and pull requests welcome — especially from the working group. Good first
contributions: scenario libraries for the TARA class matrix, worked examples,
sector-specific interface lists, corrections to the Annex I crosswalk, and
translations. Nitpicks are a feature here, not a burden: these are compliance
tools, and precision is the point.

## License

[CC BY 4.0](./LICENSE). Use, adapt, and redistribute with attribution to the
Value Chain Risk Institute and the Cyber Manual Movement. SPDX: `CC-BY-4.0`.

---

*Value Chain Risk Institute · valuechainrisk.org · a member of the Cyber Manual Movement working group*
