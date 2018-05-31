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

def test_make_test_partial():
    """
    If there are two tests, and one fails, they all fail
    """
    docstring = r"""
    >>> g == "Hello"
    True
    >>> g == "Not Hello"
    """
    test = SingleDocTest("test", docstring)
    result = test({'g': "Hello"})
    assert result.grade == 0

def test_make_test_fail():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = SingleDocTest("test", docstring)
    tr = test({'h': "Hello"})
    assert tr.grade == 0
    assert "NameError: name 'g' is not defined" in tr.get_summary('text/plain')