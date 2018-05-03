import os
from textwrap import dedent
from okgrade.doctest import SingleDocTest
from okgrade.result import TestResult

def test_make_test_pass():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = SingleDocTest("test", docstring)
    assert test({'g': "Hello"}) == TestResult(
        1,
        "Test test passed!"
    )

def test_make_test_fail():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = SingleDocTest("test", docstring)
    # FIXME: There is a path here that will vary across installs.
    assert test({'h': "Hello"}) == TestResult(
        0,
        r"""Test test failed!

Test code:

>>> g == "Hello"
True


Test result:
Trying:
    g == "Hello"
Expecting:
    True
**********************************************************************
Line 2, in test
Failed example:
    g == "Hello"
Exception raised:
    Traceback (most recent call last):
      File "/usr/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
      File "<doctest test[0]>", line 1, in <module>
        g == "Hello"
    NameError: name 'g' is not defined
"""
    )