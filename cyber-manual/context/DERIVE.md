# Derive from a manual: what changed in the Context & Conditions of Use Builder

Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute, 8 November 2026. CC BY 4.0.

## In one paragraph

Until now, a manufacturer who had written a manual in the CRA Manual Builder had to start again in the context builder, ticking by hand every link between functions, components, interfaces, context, conditions of use and risks. Most of those links are already written in the manual, in its tables and its text. The context builder now reads them. Open a manual, and the lists fill in and the links are drawn as a first draft. Each link the tool added is marked as a suggestion until a person accepts or removes it, and anything the manual doesn't say is listed as a gap for a person to fill. The diagrams come out of the same data, so a first set of diagrams appears straight away.

## How to use it

1. In the CRA Manual Builder, use Export JSON to save the manual.
2. In the Context & Conditions of Use Builder (valuechainrisk.org/cyber-manual/context/), press "Derive from a manual" and choose that file. Import JSON accepts it too.
3. Links the tool added have a dashed outline. Hover over one to see which rule added it. Untick it if it's wrong. Ticking or unticking a link removes its mark, and "accept all suggested links" keeps all the remaining ones.
4. At the top of the checks, a "Derived from a manual" group lists what no rule could reach. Fill those in and the list gets shorter.

Nothing is uploaded. As before, all of this happens in the browser.

## What it reads, and how

Twelve rules, each one stated, so anyone can check them:

| Rule | Read from the manual | Becomes |
|---|---|---|
| R1 | the logical interface (protocol) table, 2.1.4 | logical interfaces, and which interfaces each function uses |
| R2 | each function's list of conditions of use, 3.3 | the function's conditions |
| R3 | each condition's "affected" column | what the condition constrains |
| R4 | each security property's component column | where the property sits |
| R5 | what a function's conditions constrain | the context components, persons and zones the function needs |
| R6 | the circumstances leading to risk table | which functions and conditions each circumstance points at |
| R7 | names of elements mentioned in the descriptions | further links, all marked as suggestions |
| R8 | the links above | the function path, in the order persons, context, interfaces, components |
| R9 | a processor or software component | used by every function |
| R10, R12 | a function that has only one interface | its context components and persons are reached through that interface |
| R11 | zones that hold what a function needs | the function's zones |

R1 to R6 copy what the manual's tables already say. R7 to R12 are inferences, and that is why every link is marked until someone decides on it.

## How well it does

We measured it against the working group's own Engineering PC example. None of the rules was tuned to that example; it was held out as the test.

- 76% of the links it suggests match the ones the group drew by hand.
- It finds 67% of the links the group drew.
- Conditions of use and security properties are placed 100% correctly, because the manual's tables state them.

## What it doesn't do, on purpose

Two things can't be derived, and the tool doesn't guess them:

- Zone membership: what sits inside the user's organisation and what sits with the manufacturer or a third party.
- Which components and interfaces each function uses, beyond what the protocol table says.

A manual doesn't state these. They are the manufacturer's assumptions about how the product is used, so the tool leaves them to a person and says where they are missing. A guessed zone would read as a claim the manufacturer never made.

## Why it matters for the group

- Less work: someone with a manual has a context draft and diagrams in minutes instead of an afternoon.
- The manual gets checked: if the derived links look wrong, the manual's tables or descriptions are usually wrong too. On our trial manuals, the chain-integrity checks found real gaps, such as components no function uses and a context component with no condition of use.
- It's open: the rules are listed above and at the top of the derivation code in `index.html`, so anyone can check them against a manual.

## Compatibility

Context files saved earlier load exactly as before. A derived file carries one extra field listing the links still marked as suggestions; older versions of the tool ignore it. The feature arrived in commit 40a1bf0.
