# File formats of the CRA tools

Version 1.0, 9 November 2026. Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute.

Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Anyone may implement, copy or adapt this specification, in any tool under any licence, provided they give credit. Suggested credit: "File formats by Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute (CC BY 4.0)."

This document describes the files the three tools in this repository read and write, so other tools can read and write them too. It was prompted by TARAflow (Jürgen Messerer, bbv), which may implement an importer and an export to the manual. Any tool is welcome to do the same.

There are three formats:

| Format | Written by | Read by | Version field |
|---|---|---|---|
| `vcri.tara/v1`: a threat analysis and risk assessment | TARA Builder (File, Save to a file) | TARA Builder | `schema` |
| `vcri.tara-to-manual/v1`: a TARA's results in the manual's shape | TARA Builder (Connect, Save for the Manual Builder) | CRA Manual Builder | `schema` |
| The manual file (`*.cybermanual.json`) | CRA Manual Builder (File, Save to a file) | All three tools | `tpl` |

Machine-readable schemas (JSON Schema 2020-12) are next to this file, and there are real sample files in [examples/](./examples/).

## Rules for all three formats

1. Version. Each file names its format and version. `vcri.tara/v1` means format `vcri.tara`, major version 1.
2. Compatibility. Adding an optional field does not change the major version. Removing or renaming a field, or changing what a field means, does. Readers must ignore fields they don't know.
3. IDs. Where a format has IDs (sections 1 and 2), they are given once and never reused within a file, even after the item is deleted. A tool that imports a file may keep these IDs to refer back to the source.
4. Text is UTF-8. Free-text fields may be empty strings; tools must not treat an empty string as an error.
5. Nothing in these files is uploaded anywhere by the tools. They live in the user's browser and in files the user saves.

## 1. `vcri.tara/v1`: the TARA file

Schema: [vcri.tara.v1.schema.json](./vcri.tara.v1.schema.json). Sample: [examples/flowsense.tara.json](./examples/flowsense.tara.json).

```
{
  "schema":    "vcri.tara/v1",
  "spec":      "https://github.com/value-chain-risk-institute/cra-manual-tools/tree/main/spec",
  "rubric":    "tara-rubric/0.1",
  "generated": "2026-11-09T10:00:00.000Z",
  "data": { ... }
}
```

`rubric` names the scales the ratings use (section 1.5). `data` holds:

### 1.1 Product

`data.product`: `name`, `ver` (type, model, version) and `purpose` (intended purpose and environment), all text.

### 1.2 Interfaces

- `data.interfaces`: the names of the interfaces in scope, for example `"USB"`.
- `data.custIf`: names the user added beyond the built-in list (a subset of the names used anywhere in the file).
- `data.ifIds`: a map from interface name to its stable ID, for example `{"USB": "IF02"}`. Every name in `interfaces`, and every interface a scenario names, has an ID. An interface taken out of scope keeps its ID.

### 1.3 Assets

`data.assets[]`: `id` (`A01`, `A02`, ...), `name`, and `damage`, the damage if the asset is harmed. In this version a scenario does not name the asset it harms; see Known gaps.

### 1.4 Threat scenarios

`data.scenarios[]`, one per candidate threat:

| Field | Meaning |
|---|---|
| `id` | Stable ID, `TS01`, `TS02`, ... |
| `legacyId` | Optional. The random ID a `vcri.tara/v0` file gave this scenario before it was upgraded. |
| `key` | `"<class>|<interface name>"`. The tool makes at most one candidate per key. |
| `cls`, `clsName` | The assumption class: `AUTH`, `INTEG`, `CONF`, `AVAIL`, `AUTHZ`, `FRESH`, `PROV` or `PHYS`, and its name. |
| `iface`, `ifaceId` | The interface's name and its ID from `ifIds`. |
| `text` | The scenario, as edited by the user. |
| `accepted` | `true` if the user accepted it as applying. Only accepted scenarios are rated, treated and exported to the manual. |
| `feas` | Feasibility ratings: `time`, `expertise`, `knowledge`, `window`, `equipment`, each 0 to 4 (section 1.5). |
| `imp` | Impact ratings: `safety`, `operational`, `financial`, `privacy`, each 0 to 3 (section 1.5). |
| `treatment` | `""`, `"Reduce (add control)"`, `"Retain (accept residual)"`, `"Avoid (remove function)"` or `"Transfer (contract/insurance)"`. |
| `bearer` | Who carries the treatment: `""`, `"Manufacturer → security property"` or `"User → condition of use"`. |
| `annex` | The CRA Annex I Part I point the scenario justifies, `"2b"` to `"2m"`, or `""`. |
| `fc` | The function in the manual it affects, as `"FC01 Program a PLC"`, or `""`. |
| `cu` | The condition of use it violates, as `"CU01 Restrict physical access"`, or `""`. |
| `damage` | The potential risk from the user's point of view: the last column of the manual's CR table. |

Treatment and bearer are the decisions the team has made, so an importer should carry them over even where it re-derives everything else.

### 1.5 Ratings (`tara-rubric/0.1`)

Feasibility is a barrier total: the five factors are added (0 to 20), and a lower total means an easier attack. Bands: 0 to 5 High, 6 to 10 Medium, 11 to 14 Low, 15 to 20 Very Low.

| Factor | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| time | < 1 day | < 1 week | < 1 month | < 6 months | > 6 months |
| expertise | Layperson | Some skill | Proficient | Expert | Multiple experts |
| knowledge | Public | Restricted | Sensitive | Confidential | Critical/secret |
| window | Unlimited/remote | Easy | Moderate | Difficult | Rare/none |
| equipment | Standard | Specialized | Bespoke | Multiple bespoke | Lab-grade |

Impact is the worst single domain: 0 Negligible, 1 Moderate, 2 Major, 3 Severe.

Risk = matrix[feasibility][impact]:

| Feasibility \ Impact | Negligible | Moderate | Major | Severe |
|---|---|---|---|---|
| High | Medium | High | Critical | Critical |
| Medium | Low | Medium | High | Critical |
| Low | Low | Low | Medium | High |
| Very Low | Low | Low | Low | Medium |

Feasibility level, impact level and risk are computed, not stored. These scales are VCRI's own. They are close to, but not the same as, the scales other TARA tools use. A tool with different scales should not treat these numbers as its own; bringing the scenarios in as a reference list is the safer use.

### 1.6 Bookkeeping

- `data.nextId`: the next number for each ID kind, for example `{"A": 3, "IF": 5, "TS": 33}`. A tool that adds items to the file must take IDs from here and advance it.
- `data.cm`: if the assessment was started from a manual, the parts of it kept for reference (functions, conditions of use, security properties, template version); otherwise `null`.

### 1.7 Upgrading `vcri.tara/v0`

v0 files had no stable IDs. The TARA Builder upgrades them when they are opened: interfaces in scope, then assets, then scenarios, each numbered in file order. A scenario's old random ID is kept as `legacyId`.

## 2. `vcri.tara-to-manual/v1`: TARA results in the manual's shape

Schema: [vcri.tara-to-manual.v1.schema.json](./vcri.tara-to-manual.v1.schema.json). Sample: [examples/flowsense.tara-to-manual.json](./examples/flowsense.tara-to-manual.json).

This is the file another TARA tool should write if it wants its results merged into a manual. The CRA Manual Builder reads it through File, Open from a file. It adds the rows to the manual already open and replaces nothing.

```
{
  "schema":    "vcri.tara-to-manual/v1",
  "tpl":       "0.39",
  "generated": "...",
  "product":   "FlowSense PLC Gateway 200",
  "ri": [ ... ],
  "cu": [ ... ],
  "sp": [ ... ]
}
```

- `tpl` is the Cyber Manual Movement template version the rows are written for.
- `ri[]` are circumstances leading to significant cybersecurity risk, for chapter 3.3 of the template (3.4.1 for the update function): `title`, `desc`, `fc` (the function's ID, for example `"FC01"`, or several separated by commas, or `""`), `cu` (the violated condition of use, as text), and `risk` (the potential risk from the user's point of view).
- `cu[]` are condition-of-use candidates, from treatments the user carries: `title`, `desc`, `affected` (the context component, person or zone, or `""`), `refs` (Annex I point), and `fc`.
- `sp[]` are security-property candidates, from treatments the manufacturer carries: `comp` (the affected component or interface), `title`, `desc` and `refs` (Annex I point).
- Every row may carry `ts`, the ID of the scenario it came from in the source tool. It's optional, and was added on 9 November 2026 without changing the version. A tool other than the TARA Builder can put its own scenario or claim ID here.

The Manual Builder gives the rows their CRxx, CUxx and SPxx IDs when it merges them. Titles are drafts, for the user to edit there.

## 3. The manual file: the parts the other tools read

The CRA Manual Builder saves the whole manual as `<name>.cybermanual.json`. It follows the Cyber Manual Movement template, so its version field is `tpl`, the template version (currently `"0.39"`). Real examples: [../examples/](../examples/).

The TARA Builder reads these parts:

| Path | Meaning |
|---|---|
| `tpl` | Template version. Files without it are from an old builder and must be re-saved in the current one first. |
| `product.name`, `product.tmv`, `product.additional` | Name; type, model and version; additional information. |
| `pc[].title` | Product components. |
| `pi[].title` | Physical interfaces. |
| `pp[].proto`, `pp[].pi` | Protocols and services, and the physical interface each one uses. |
| `sp[].title` | Security properties. |
| `cc[].title`, `cz[].title` | Context components and zones. |
| `fc[].title`, `fc[].cus` | Functions, and the conditions of use each function lists. |
| `cu[].title`, `cu[].affected` | Conditions of use, and what each one constrains. |

IDs in the manual file are positional: `PC01` is the first entry in `pc`, `FC03` the third in `fc`, and so on. They match the IDs printed in the manual, but they shift if the user reorders or deletes rows. This is the main known gap (below).

## Known gaps, for the next version

- The manual file has no stored IDs. A later version should give `pc`, `pi`, `pp`, `fc`, `cu`, `sp` and `ri` entries an `id` field that does not shift, the way the TARA file now does.
- A TARA scenario does not yet name the asset it harms. Adding an optional `assets` list of asset IDs to each scenario is the obvious next step.
- `vcri.tara-to-manual` rows do not carry a rating. A tool that wants the manual to show its own risk level could add an optional `level` field; the Manual Builder would ignore it today.

Comments and corrections are welcome as issues on this repository.
