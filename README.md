# okgrade

A subset of [okpy](http://okpy.org/) that only does grading.

## What?

This library can be used to **autograde** Jupyter Notebooks and
Python files.

Instructors can write tests in a subset of the [okpy test format](docs/ok-test-format.md)
(other formats coming soon), and students can dynamically check if their
code is correct or not. These notebooks / .py files can later
be collected and a grade assigned to them automatically.

## Why?

[okpy](http://okpy.org/) is used at Berkeley for a number of large
classes (CS61A, data8, etc). It has a lot of features for student
management, office hours, providing feedback, autograding, etc.
These are great for large classes, but come with an added complexity
that makes it harder to use for smaller classes. It's featureset
overlaps a lot other student management systems (such as EdX, Canvas,
etc) - this makes it complex to use okpy with other systems.

This project aims to re-implement a small and specific subset of
okpy that does autograding only.