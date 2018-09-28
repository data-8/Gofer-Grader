# Design

When designing `Gofer` and adding features, the developers are influenced by three
primary use cases.

1. An instructor **authors tests** to distribute with an assignment.
2. A student **interactively checks** their code as they are working on an assignment.
3. A completed assignment is **graded** to produce a grade.


This document contains a non-exhaustive list of design principles to consult when making
technical decisions.

## Don't be Notebook specific

`Gofer` should support but not depend on the assignments being Jupyter Notebooks - it
should support plain `.py` files for all core functionality. This means we can not rely on
metadata stored in Jupyter Notebook cells, which is a pretty big constraint. This constraint is
worth it for a few reasons:

1. None of the Jupyter Notebook frontends are currently accessible. If courses want to be
   available to students with accessibility needs (as they should be!), they need to support
   accepting plain `.py` files.
2. Relying on notebook metadata for critical functions forces instructors to use a specific
   UI often implemented as an extension to a specific notebook frontend. This adds to instructor training
   cost, ties them to specific notebook interfaces & can often be avoided.

Python is an extremely dynamic language with cool introspection capabilities, so we should use
them wherever possible. Jupyter Frontend extensions often *can* provide a better user experience
for users and should be built wherever possible - just not **required** to use `Gofer`.

## Prioritize Tradeoffs

Design decisions are always tradeoffs. Good projects make these tradeoffs fairly consistently
throughout their lifetime.

Future design decisions for `Gofer` should prioritize in the following order:

1. *Smooth* student experience (they are least experienced)
2. *Efficient* instructor experience (they don't have much time!)
3. *Clear* contributor experience (confusing other contributors kills projects)

This is merely a prioritization guideline - context matters much more than general rules. Do
not use this as an excuse for anything :)

## Easily integratable

`Gofer` is most likely used along with a suite of tools as part of a distribution
of some sort. It should be easy to integrate the python API or the commandline interface
with other tools. They should be generally backwards compatible & accomodating of integrators'
requests.

## Be explainable

Getting a grade that seems wrong/unfair to you & unexplainable by your instructor is a deeply
frustrating experience, and one we should avoid at all costs. It is the worst failure mode
for `Gofer`, and related bugs should be considered critical.

## Be as 'secure' as possible

Any distribution that uses `Gofer` for grading should have multiple layers of context-specific
security as needed. `Gofer` itself should be considered **untrusted**, since it is executing
arbitrary user code in-process written in a very dynamic language. This is inherent to the problem
of grading, however - the only way to be more secure is to rely exclusively on `stdin` and `stdout`
of the executed program & parse those. This is the approach taken by most programming 'contest' sites
like [TopCoder](https://www.topcoder.com/competitive-programming/), and trades off student/instructor friendliness for security.


However, we can still try to make it harder for students & instructors to *accidentally* screw up
their grading. Distributions should build enough layers of security to make it *impossible* for students to
tamper with *other* students' grades, and `Gofer` should build in enough security to make it
*hard* for students to tamper with their own grades.
