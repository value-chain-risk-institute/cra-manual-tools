# File formats of the CRA tools

Version 1.0, 9 November 2026. Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute.

Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Anyone may implement, copy or adapt this specification, in any tool under any licence, provided they give credit. Suggested credit: "File formats by Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute (CC BY 4.0)."

This document describes the files the three tools in this repository read and write, so other tools can read and write them too. It was prompted by TARAflow (Jürgen Messerer, bbv), which may implement an importer and an export to the manual. Any tool is welcome to do the same. Version 1.0 takes in Jürgen's review of the first draft; what changed is listed at the end.

There are three formats:

| Format | Written by | Read by |
|---|---|---|
| `vcri.tara/v1.0`: a threat analysis and risk assessment | TARA Builder (File, Save to a file) | TARA Builder |
| `vcri.tara-to-manual/v1.0`: a TARA's results in the manual's shape | TARA Builder (Connect, Save for the Manual Builder) | CRA Manual Builder |
| `vcri.cybermanual/v1.0`: the manual (`*.cybermanual.json`) | CRA Manual Builder (File, Save to a file) | All three tools |

Machine-readable schemas (JSON Schema 2020-12) are next to this file, and there are sample files, saved by the tools themselves, in [examples/](./examples/).

## Rules for all three formats

1. Version. Each file names its format and version in `schema`, as `<format>/v<major>.<minor>`, for example `vcri.tara/v1.0`. Readers accept every minor version of a major version they know, and refuse a newer major version with a message.
2. Compatibility. Adding an optional field raises the minor version. Removing or renaming a field, or changing what a field means, raises the major version. Readers must ignore fields they don't know. So a reader can tell "no value" from "written before the field existed": a missing optional field means "no value" only in files whose minor version already has that field.
3. Generator. Each file may carry `generator`: `{tool, version, url}` of the program that wrote it.
4. IDs. Where a format has IDs, they are given once and never reused within a file, even after the item is deleted. IDs are references, not positions: deleting or moving an item never changes another item's ID. A tool that imports a file may keep these IDs to refer back to the source.
5. Codes, not labels. Fixed choices are stored as lower-case codes (for example `reduce`, `user`), so tools in any UI language can read them. The English labels the VCRI tools show are listed here.
6. Text is UTF-8. Free-text fields may be empty strings; tools must not treat an empty string as an error.
7. Nothing in these files is uploaded anywhere by the tools. They live in the user's browser and in files the user saves.

## 1. `vcri.tara/v1.0`: the TARA file

Schema: [vcri.tara.v1.schema.json](./vcri.tara.v1.schema.json). Sample: [examples/flowsense.tara.json](./examples/flowsense.tara.json).

```
{
  "schema":    "vcri.tara/v1.0",
  "spec":      "https://github.com/value-chain-risk-institute/cra-manual-tools/tree/main/spec",
  "generator": {"tool": "VCRI TARA Builder", "version": "2026-11-09", "url": "https://valuechainrisk.org/tara/"},
  "rubric":    "tara-rubric/0.1",
  "generated": "2026-11-09T12:00:00.000Z",
  "data": { ... }
}
```

`rubric` names the scales the ratings use (section 1.5). `data` holds:

### 1.1 Product

`data.product`: `name`, `ver` (type, model, version) and `purpose` (intended purpose and environment), all text.

### 1.2 Interfaces

`data.interfaces[]`, one object per interface the assessment knows: `id` (`IF01`, `IF02`, ...), `name`, `inScope` (true if it is assessed) and `custom` (true if the user added it, rather than taking it from the tool's built-in list). Scenarios point at an interface by `id`, so renaming an interface keeps every link. An interface taken out of scope stays in the list with its ID.

### 1.3 Assets

`data.assets[]`: `id` (`A01`, `A02`, ...), `name`, and `damage`, the damage if the asset is harmed.

### 1.4 Threat scenarios

`data.scenarios[]`, one per candidate threat:

| Field | Meaning |
|---|---|
| `id` | Stable ID, `TS01`, `TS02`, ... |
| `legacyId` | Optional. The ID a file older than v1.0 gave this scenario before it was upgraded. |
| `key` | `"<class>|<interface ID>"`. The tool makes at most one candidate per key. |
| `cls`, `clsName` | The assumption class: `AUTH`, `INTEG`, `CONF`, `AVAIL`, `AUTHZ`, `FRESH`, `PROV` or `PHYS`, and its name. |
| `ifaceId` | The interface's ID. |
| `text` | The scenario, as edited by the user. |
| `accepted` | `true` if the user accepted it as applying. Only accepted scenarios are rated, treated and exported to the manual. |
| `feas` | Feasibility ratings: `time`, `expertise`, `knowledge`, `window`, `equipment`, each 0 to 4 (section 1.5). |
| `imp` | Impact ratings: `safety`, `operational`, `financial`, `privacy`, each 0 to 3 (section 1.5). |
| `treatment` | `""` (not set), `reduce`, `retain`, `avoid` or `transfer`. |
| `bearer` | Who carries the treatment: `""` (not set), `manufacturer` (it becomes a security property) or `user` (it becomes a condition of use). |
| `annex` | The CRA Annex I Part I point the scenario justifies, `"2b"` to `"2m"`, or `""`. |
| `fcIds` | The functions in the manual it affects, as IDs: `["FC01", "FC03"]`. |
| `cuIds` | The conditions of use already in the manual that it violates: `["CU04"]`. A scenario can violate more than one. |
| `assetIds` | Optional. The assets it harms: `["A01"]`. |
| `damage` | The potential risk from the user's point of view: the last column of the manual's CR table. |

Treatment and bearer are the decisions the team has made, so an importer should carry them over even where it re-derives everything else.

The labels the VCRI tools show: treatment `reduce` "Reduce (add control)", `retain` "Retain (accept residual)", `avoid` "Avoid (remove function)", `transfer` "Transfer (contract/insurance)"; bearer `manufacturer` "Manufacturer → security property", `user` "User → condition of use".

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

Feasibility level, impact level and risk are computed, not stored. These scales are VCRI's own. They are close to, but not the same as, the scales other TARA tools use. A tool with different scales should not treat these numbers as its own; bringing the scenarios in as a reference list is the safer use. Ratings never go into the manual (section 2).

### 1.6 Bookkeeping

- `data.nextId`: the next number for each ID kind, for example `{"A": 3, "IF": 5, "TS": 33}`. A tool that adds items to the file must take IDs from here and advance it.
- `data.cm`: if the assessment was started from a manual, the parts of it kept for reference, with the manual's IDs: `fc[]` (`id`, `title`, `cus`), `cu[]` (`id`, `title`, `affected`), `sp[]` (`id`, `title`), `tpl` and `schema`. Otherwise `null`.

### 1.7 Upgrading older files

The TARA Builder upgrades older files when they are opened, and writes v1.0 from then on.

- `vcri.tara/v0` had no stable IDs. Interfaces are numbered first (those in scope, then the rest), then assets, then scenarios, each in file order. A scenario's old random ID is kept as `legacyId`.
- The draft of v1 published on the morning of 9 November 2026 (`"schema": "vcri.tara/v1"`) stored interfaces as names with a name-to-ID map (`ifIds`), treatment and bearer as English labels, and `fc` and `cu` as text. All of these are converted, and its IDs are kept.

## 2. `vcri.tara-to-manual/v1.0`: TARA results in the manual's shape

Schema: [vcri.tara-to-manual.v1.schema.json](./vcri.tara-to-manual.v1.schema.json). Sample: [examples/flowsense.tara-to-manual.json](./examples/flowsense.tara-to-manual.json).

This is the file another TARA tool should write if it wants its results merged into a manual. The CRA Manual Builder reads it through File, Open from a file.

```
{
  "schema":    "vcri.tara-to-manual/v1.0",
  "generator": {"tool": "VCRI TARA Builder", "version": "2026-11-09"},
  "tpl":       "0.39",
  "generated": "...",
  "product":   "FlowSense PLC Gateway 200",
  "ri": [ ... ],
  "cu": [ ... ],
  "sp": [ ... ]
}
```

`tpl` is the Cyber Manual Movement template version the rows are written for. Every row has:

- `ref`: a local reference, unique within the file, so rows can point at each other (for example `"cu-TS16"`).
- `source`: where the row came from, `{"tool": "vcri-tara", "ids": ["TS16"]}`. `tool` says whose IDs they are; another TARA tool puts its own name and its own scenario or claim IDs here. One row may come from several IDs.

### 2.1 What goes in which list

- `ri[]`, circumstances potentially leading to significant cybersecurity risk (chapter 3.3 of the template, 3.4.1 for the update function). This list holds only what the user can influence: a violated condition of use, reasonably foreseeable misuse, or another circumstance the user can influence (GUIDANCE v0.36, chapter "Circumstances potentially leading to significant cybersecurity risk"). It is not the risk register. A risk the manufacturer treats alone does not belong here, and no row carries a likelihood, impact or risk level, because the GUIDANCE says circumstances carry none. Fields: `title`, `desc`, `fcIds` (the functions it belongs to), `cuIds` (conditions of use already in the manual that it violates), `cuRefs` (the `ref`s of condition-of-use candidates in this same file that it violates), and `risk` (the potential risk from the user's point of view).
- `cu[]`, condition-of-use candidates: what the user must do. Fields: `title`, `desc`, `affected` (the context component, person or zone, or `""`), `annex` (Annex I points, `["2j"]`) and `fcIds`.
- `sp[]`, security-property candidates: what the manufacturer does. Fields: `comp` (the affected component or interface), `title`, `desc` and `annex`.

The TARA Builder writes them this way: an accepted scenario with bearer `user` becomes a CR row. If it names no existing condition of use, it also becomes a condition-of-use candidate, and the CR row points at it through `cuRefs`. An accepted scenario with bearer `manufacturer` becomes a security-property candidate only. An accepted scenario with no bearer goes nowhere, and the tool says so.

### 2.2 How the Manual Builder merges it

- Rows are added, and nothing already in the manual is changed. The builder gives each new row its CRxx, CUxx or SPxx ID, attaches each condition-of-use candidate to the functions in its `fcIds`, and fills each CR's violated conditions of use from `cuIds` plus the IDs its `cuRefs` received.
- Each new row keeps its `source`. When the same TARA is merged again, a row whose source is already in the manual is not added a second time, and the manual's row stays as the user edited it.
- Rows in the manual whose source tool is in the file, but whose source IDs no longer appear in it, are listed for the user to check. They are not deleted.

## 3. `vcri.cybermanual/v1.0`: the manual file

Schema: [vcri.cybermanual.v1.schema.json](./vcri.cybermanual.v1.schema.json), covering the parts other tools read and write; the Manual Builder keeps more (prose, contacts, chapter 5). Sample: [examples/engineering-pc.cybermanual.json](./examples/engineering-pc.cybermanual.json).

The file has two version fields, which change independently:

- `schema`, the file format: `"vcri.cybermanual/v1.0"`.
- `tpl`, the Cyber Manual Movement template version the content follows: currently `"0.39"`.

The ten lists `pc`, `pi`, `pp`, `sp`, `cc`, `cp`, `cz`, `fc`, `cu` and `ri` hold one object per row, and every row has a stored `id` with its list's prefix (`PC`, `PI`, `PP`, `SP`, `CC`, `CP`, `CZ`, `FC`, `CU`, and `CR` for `ri`). The ID is the one printed in the manual. It is given once and never reused: deleting CU02 leaves CU01, CU03, and a reference to CU03 elsewhere in the manual still means the same row. `nextId` holds the next number for each prefix, for example `{"CU": 9, "CR": 10}`.

| Path | Meaning |
|---|---|
| `product.name`, `product.tmv`, `product.additional`, `product.family` | Name; type, model and version; additional information; product family members, comma separated. |
| `pc[]`, `pi[]` | Product components and physical interfaces: `id`, `title`. |
| `pp[]` | Protocols and services: `id`, `proto`, `pi` (the PI it uses), `port`, `fc` (FC IDs, comma separated), `enabled`. |
| `sp[]` | Security properties: `id`, `comp`, `title`, `desc`, `refs` (Annex I points, comma separated), optional `source`. |
| `cc[]`, `cp[]`, `cz[]` | Context components, persons and zones: `id`, `title`, `desc` (persons add `skill`, zones `type` and `access`). |
| `fc[]` | Functions: `id`, `title`, `desc`, `rfu` (reasonably foreseeable use), `kind` (`core` or `ancillary`), `cus` (the CU IDs attached to it, comma separated). |
| `cu[]` | Conditions of use: `id`, `affected`, `title`, `desc`, `refs`, optional `source`. |
| `ri[]` | Circumstances leading to risk: `id`, `title`, `desc`, `fc` (FC IDs), `cu` (CU IDs), `risk`, optional `source`. |
| any row | Optional `vars`: the product family members it applies to; empty means all. |

References between rows (`cus`, `fc`, `cu`, `pi`) are ID strings separated by commas, as the manual prints them. Files from the builder before v1.0 have no `schema` and no stored IDs; the tools number their rows by position when they open them, which gives the IDs those files printed with, and save them as v1.0 from then on. The manuals in [../examples/](../examples/) are such files.

## What changed from the draft of 9 November (morning)

Thanks to Jürgen Messerer's review:

1. Treatment and bearer are codes (`reduce`, `user`), with the labels listed here, instead of English labels.
2. Interfaces are objects `{id, name, inScope, custom}` instead of names with a name-to-ID map, so a rename keeps the ID.
3. Scenarios name functions and conditions of use as ID lists (`fcIds`, `cuIds`), and the export uses `fcIds` arrays instead of a comma-separated `fc`.
4. Rows in the export have a local `ref`, and a CR points at condition-of-use candidates in the same file through `cuRefs`.
5. The export's `ri` holds only circumstances the user can influence, as the GUIDANCE defines them, and the TARA Builder now writes it that way.
6. The manual file has its own format version, `schema`, next to the template version `tpl`, and stored IDs on every row.
7. Versions have a minor number (`v1.0`), and every file may name its `generator`.

Also taken in: scenarios may name the assets they harm (`assetIds`); `ts` became `source: {tool, ids}`; merging the same TARA again no longer duplicates rows and flags rows whose source is gone; and no rating field goes into the export.

## Known gaps, for a later version

- The TARA file has no data-flow or trust-boundary model. Tools that have one keep it in their own format; this format carries interfaces and assets only.
- The manual file's references between rows are comma-separated strings, as printed. Arrays would be cleaner; changing them is a major version, so it waits until there is a second reason to make one.
- A product family's `vars` name members by text, not by ID.

Comments and corrections are welcome as issues on this repository.
