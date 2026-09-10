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

## Extension, 10 September 2026: the audience is derived too

A recurring question is whether a product needs a second, non-technical
diagram, and for whom. The answer follows from the same chain.

Every condition of use is somebody's job. The template already gives each
context person a skill level: ordinary, instructed, skilled. So the audience
is not a property of the product. It is read off the persons responsible for
the conditions of use.

- If every condition is the responsibility of a skilled or instructed person,
  the technical diagram is the diagram. There is no second audience.
- If any condition is the responsibility of an ordinary person, that condition
  must reach them in a form they can act on. The CRA does not require a
  picture; it requires the information to be clear, understandable,
  intelligible and legible to the user. A picture is often the cheapest way
  to meet that requirement for an ordinary person, which is the honest case
  for a non-technical diagram: not mandated, but frequently the easiest route
  to compliance.

This needs one field the template does not yet carry on a condition of use:
who is responsible for satisfying it. A condition assigned to nobody is a
condition nobody meets, so the field earns its place independently of the
diagram question.

**Translating the technical diagram for an ordinary person** is a filter and
a relabel, from the same data. Keep only the nodes that person can see, touch,
or decide about. Delete every internal component, protocol label and path
step they never encounter. Relabel what remains in their vocabulary: not "PI03
USB (CDC, MSC)" but "the USB port on the side." Show each of their conditions
as an instruction and each risk as its consequence, in outcomes they
recognise: the machine stops, the batch is ruined, someone is hurt. The risk
diagram's numbered steps become a short story with the middle collapsed.

**What matters to that reader, and nothing else:** what I must do or not do;
what happens if I do not; how I recognise the thing you mean; and when, in the
product's life, this applies.

**Sub-assemblies.** A component manufacturer's context persons are integrators,
all skilled, so by the rule its own manual needs no non-technical rendering.
Its obligation is different: to mark which conditions of use survive
integration and must be carried into the next manufacturer's manual, where
they may meet an ordinary person. That gives the integration-guidance chapter
a precise job.

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
