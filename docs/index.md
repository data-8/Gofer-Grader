# okgrade

`okgrade` is a small library for autograding Jupyter notebooks & python files.

## What is autograding?

**Autograding** runs a series of **tests** against student submitted code,
producing a **grade**. No humans are in the loop in determining the
correctness / grade of student submission.

It is unit testing with weighted grades and feedback for students when
tests fail.

## Why autograding?

Grading takes up a large chunk of teaching time for many **instructors**.
While not everything can be automatically graded, many excercises can be.
This saves the instructor a lot of time & tedious effort, regardless
of the size of the class.

Autograding provides near-instant feedback to **students** on how well
they are doing. This allows them to correct course immediately,
without having to wait for an instructor to grade & provide feedback.

## Scope of this project

This project is tightly scoped to provide only the following:

1. Write grading tests in multiple formats
2. Run grading tests (interactively or in batch) against a Jupyter Notebook or
   Python file.
3. Provide multiple strategies for determining overall grade from pass / fail
   results of single tests.

Everything else is out of scope, and should be implemented elsewhere. Examples
of features that are out of scope are:

1. Distributing notebooks / lab materials to users
2. Collecting notebooks / lab materials from users
3. Running grading at scale
4. Highly secure execution (only relying on stdout / stderr for validation)
5. Tools to help build student notebooks (without solutions & hidden tests)
   from instructor notebooks
6. Ponies

This list is not exhaustive :)
