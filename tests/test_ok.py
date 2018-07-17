import os

from client.api.notebook import Notebook
from gradememaybe.ok import OKTests, run_doctest

defined_variable = None
seconds_in_a_minute = 60

def test_nb_grade_simple_valid():
    """
    Test parsing & running a simple oktest file.
    """
    here = os.path.dirname(__file__)

    nb = Notebook(os.path.join(here, 'oktests/simple.ok'))

    nb.grade('simple_valid')


def test_ok_parse_simple_valid():
    """
    Test parsing & running a simple oktest file.
    """
    here = os.path.dirname(__file__)

    # This should not raise any AssertionErrors
    test_suite = OKTests([os.path.join(here, 'oktests/tests/simple_valid.py')])
    global_env = {}

    resp = test_suite.run(global_env)
    # All tests should fail now
    assert resp.grade == 0

    global_env['defined_variable'] = None

    # First test should pass now, but second should fail
    # This should cause the whole thing to fail
    resp = test_suite.run(global_env)
    assert resp.grade == 0
    assert len(resp.passed_tests) == 0
    assert len(resp.failed_tests) == 1
    assert "NameError: name 'seconds_in_a_minute' is not defined" in resp.failed_tests[0][1]

    # Both tests should pass now
    global_env['seconds_in_a_minute'] = 60
    resp = test_suite.run(global_env)
    assert resp.grade == 1
    assert len(resp.passed_tests) == 1
    assert len(resp.failed_tests) == 0


def test_make_test_pass():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    passed, _ = run_doctest('test', docstring, {'g': "Hello"})
    assert passed

def test_make_test_partial():
    """
    If there are two tests, and one fails, they all fail
    """
    docstring = r"""
    >>> g == "Hello"
    True
    >>> g == "Not Hello"
    True
    """
    passed, _ = run_doctest('test', docstring, {'g': 'hello'})
    assert not passed

def test_make_test_fail():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    passed, hint = run_doctest('test', docstring, {'h': "hello"})
    assert not passed
    assert "NameError: name 'g' is not defined" in hint
