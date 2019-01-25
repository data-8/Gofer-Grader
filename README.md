# Gofer Grader

[![CircleCI](https://circleci.com/gh/data-8/Gofer-Grader/tree/master.svg?style=shield)](https://circleci.com/gh/data-8/Gofer-Grader/tree/master)
[![codecov](https://codecov.io/gh/data-8/Gofer-Grader/branch/master/graph/badge.svg)](https://codecov.io/gh/data-8/Gofer-Grader)

Simple library for interactive autograding.

Previous names include `gradememaybe` and `okgrade`.

[See the Gofer Grader documentation](http://okgrade.readthedocs.io/en/latest/) for more information.

## What?

This library can be used to **autograde** Jupyter Notebooks and
Python files.

Instructors can write tests in a subset of the [okpy test format](docs/ok-test-format.md)
(other formats coming soon), and students can dynamically check if their
code is correct or not. These notebooks / .py files can later
be collected and a grade assigned to them automatically.

### Integrating Gofer into your course

As an effort to help autograding with Berkeley's offering of Data 8 online,
Gofer also works with two other components that could be useful for other
courses. courses. The primary one, [Gofer service](https://github.com/data-8/gofer_service),
is a tornado service that receives notebook submissions and runs/grades them in
docker containers. The second piece, [Gofer submit](https://github.com/data-8/gofer_submit)
is a Jupyter notebook extension that submits the current notebook to the
service. Though they could be modified to work on your own setup, these are
meant to play particularly nicely with
[Jupyterhub](https://github.com/jupyterhub/jupyterhub).

## Why?

[okpy](http://okpy.org/) is used at Berkeley for a number of large
classes (CS61A, data8, etc). It has a lot of features that are
very useful for large and diverse classes.
However, this comes with a complexity cost for instructors who only
need a subset of these features and sysadmins operating an okpy server
installation.

This project is tightly scoped to only do automatic grading, and nothing
else.

## Caveats

Gofer executes arbitrary user code within the testing environment, rather than
parsing standard out. While there are certain measures implemented to make it
more difficult for users to maliciously modify the tests, it is not 100%
possible to secure against these attacks since Python exposes all the objects.

## Credit

Lots of credit to the amazing teams that have worked on okpy over the
years.

1. [Academic Publications](https://okpy.org/about/publications/)
2. [GitHub Organizatio](https://github.com/okpy)
3. [ok-client GitHub repository](https://github.com/Cal-CS-61A-Staff/ok-client)
