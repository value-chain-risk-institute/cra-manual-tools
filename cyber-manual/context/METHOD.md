# The Derivation Rule for Context and Conditions of Use

**Joshua Marpet and Cairn Viktor, The Value Chain Risk Institute · 10 September 2026 · CC BY 4.0**

A method note for the Cyber Manual Movement. The tool at
[valuechainrisk.org/cyber-manual/context](https://valuechainrisk.org/cyber-manual/context/)
is one implementation of it; the rule stands on its own and can be applied by
hand, in a spreadsheet, or in any other tool.

## The problem it solves

Manufacturers filling the Cyber Manual template stall on the context chapter
and the conditions-of-use chapter. The recurring question is "how much detail?"
Asked to describe a product's context, an engineer can write three items or
thirty, and nothing on the page says which is correct. The same is true of
conditions of use. Diagrams are wanted and resisted for the same reason:
nobody knows what should be in them.

## The observation

The difficulty is not a level-of-detail judgment. It is that the chapters are
presented as lists, and a list has no stopping rule.

The template's own definitions already contain one. Read as a chain rather
than as separate boxes:

- A **context component** is something outside the product that is *needed to
  describe a product function*.
- A **condition of use** is a security characteristic the context must have,
  and it names the context component(s) it affects.
- A **risk** is a circumstance the user can influence that leads to damage.

Therefore:

1. **Functions produce context.** A context component exists only because a
   function needs it. Walk each function and ask what outside the product it
   depends on. Each answer is a context component. Nothing else is.
2. **Context produces conditions.** A condition of use exists only because a
   context component must satisfy it for a function to be safe. Each answer is
   a condition of use, already attached to the context component the template
   asks for.
3. **Conditions produce risks.** A risk is a condition of use that is not met.
   Ask what happens if this condition is violated. Each answer is a risk with
   its potential damage.

In the current template, context is three lists, components, persons and
zones, and the rule applies to each of them identically: a person or a zone
exists in the manual only because a function needs it.

Product components are the one list that is not derived from anything. They
are what the manufacturer already knows, and every function and security
property points back at them.

## The rule

> Derive, do not brainstorm. The right level of detail for context and
> conditions of use is whatever the chain from the product's functions
> produces, and nothing more.

## The corollary about diagrams

Once context is derived from functions, the diagram is not a separate artifact.
It is the chain drawn: product components inside a boundary, functions on the
boundary because a function is exactly the thing that reaches from inside the
product to outside it, context components outside, each condition of use
hanging off the context component it constrains, each risk hanging off the
condition it breaks.

Three of the template's optional diagrams are therefore one picture: the
context diagram is the whole chain, the conditions-of-use diagram is the same
chain with conditions shown, and a function diagram is the same chain filtered
to a single function.

Nobody draws the diagram. Fix the lists and the picture fixes itself.

## Checks that follow from the rule

Each link in the chain yields a check that can be applied by hand:

- A context component needed by no function is not context.
- A function needing nothing from the context is unusual; confirm it is
  genuinely self-contained.
- A condition of use with no affected context component is a wish, not a
  condition.
- A context component that a function depends on, but that has no condition,
  is an unstated assumption.
- A condition of use with no risk stating what happens if it is not met will
  not be taken seriously by the reader.
- A product component used by no function and holding no security property is
  either a missing function or a row not worth having.

## What is the working group's and what is ours

The definitions of product, context, function, security property, condition of
use and risk are the Cyber Manual Movement's, in its template and guidance.
The Engineering PC example is the working group's. This note claims neither.

What this note contributes is the articulation of those definitions as a
derivation chain with a stopping rule, the corollary that the diagram is the
chain drawn, and the checks that follow. That is the concept we ask to be
attributed.

## How to cite

> Marpet, J. and Viktor, C. (2026). *The Derivation Rule for Context and
> Conditions of Use.* The Value Chain Risk Institute, method note for the
> Cyber Manual Movement, 10 September 2026.
> https://github.com/value-chain-risk-institute/cra-manual-tools/blob/main/cyber-manual/context/METHOD.md

Licensed CC BY 4.0. Use it, adapt it, build on it, and say where it came from.
