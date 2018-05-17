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
classes (CS61A, data8, etc). It has a lot of features that are
very useful for large and diverse classes, such as:

1. Office Hours management
2. Student assignment statistics
3. Plagiarism detection
4. Personalized feedback
5. Backups of student submissions
6. Support for Python, Scheme and other languages
7. Hiding / locking tests when students are running them locally
8. Mass automatic grading

And many more.

However, this comes with a complexity cost for instructors who only
need a subset of these features and sysadmins operating an okpy server
installation.

This project is tightly scoped to only do automatic grading, and nothing
else.

## Credit

Lots of credit to the amazing teams that have worked on okpy over the
years.

1. [Academic Publications](https://okpy.org/about/publications/)
2. [GitHub Organizatio](https://github.com/okpy)
3. [ok-client GitHub repository](https://github.com/Cal-CS-61A-Staff/ok-client)
