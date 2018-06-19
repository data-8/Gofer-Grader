# okgrade

`okgrade` is a small library for autograding Jupyter notebooks & python files.
It is not dependent on any other grading packages and tools (such as `okpy` or
`nbgrader`), though it may be used *alongside* them in order to facilitate the
grading process. It performs all computation/grading on the computer that
runs the `okgrade` code, and does not distribute notebooks or run them on a
remote server.

## Overview

`okgrade` allows you to combine two kinds of files:

1. Jupyter Notebooks in which students have done their work.
2. Formatted "test" files that define tests to run after all cells in a
   student's notebook have been executed.

`okgrade` provides lightweight functionality to run an arbitrary test suite
against the environment present in a notebook after all cells have been run.
This is primarily useful for two things:

* **interactive feedback**: `okgrade` test files can be distributed with
  Jupyter notebooks, and written to provide helpful error messages that guide
  students toward the right answer.
* **autograding**: `okgrade` test files can also be kept secret by an
  instructor, who collects student notebooks and runs each of them against
  the `okgrade` test suite in order to return a "grade" for notebooks.

## Examples

See the [examples folder](https://github.com/grading/okgrade/examples)
on GitHub for sample notebooks and `okgrade` test files that demonstrate the
functionality of this package. For an interactive version of these examples,
click on the Binder badge below.

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/grading/okgrade/master?filepath=examples)

## What is autograding?

**Autograding** runs a series of **tests** against student submitted code,
producing a **grade**. No humans are in the loop in determining the
correctness / grade of student submission.

It is unit testing with weighted grades and feedback for students when
tests fail.

## Why autograding?

Grading takes up a large chunk of teaching time for many **instructors**.
While not everything can be automatically graded, many exercises can be.
This saves the instructor a lot of time & tedious effort, regardless
of the size of the class.

Autograding provides near-instant feedback to **students** on how well
they are doing. This allows them to correct course immediately,
without having to wait for an instructor to grade & provide feedback.

## Scope of this project

This project is tightly-scoped to provide only the following:

1. Write grading tests in multiple formats
2. Run grading tests (interactively or in batch) against a Jupyter Notebook or
   Python file.
3. Provide multiple strategies for determining overall grade from pass / fail
   results of single tests.

Everything else is out of scope, and should be implemented elsewhere. Examples
of features that are **out of scope** are:

1. Distributing notebooks / lab materials to users
2. Collecting notebooks / lab materials from users
3. Running grading at scale
4. Highly secure execution (only relying on stdout / stderr for validation)
5. Tools to help build student notebooks (without solutions & hidden tests)
   from instructor notebooks
6. Ponies

This list is not exhaustive :)
