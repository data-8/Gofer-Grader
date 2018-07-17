import os

from client.api.notebook import Notebook
from gradememaybe.ok import parse_ok_test, OKDocTest

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
    test_suite = parse_ok_test(os.path.join(here, 'oktests/tests/simple_valid.py'))
    global_env = {}

    resp = test_suite.run(global_env)
    # All tests should fail now
    assert resp.grade == 0

    global_env['defined_variable'] = None

    # First test should pass now, but second should fail
    resp = test_suite.run(global_env)
    assert resp.grade == 0
    assert resp.results[0].passed
    assert not resp.results[1].passed

    # Both tests should pass now
    global_env['seconds_in_a_minute'] = 60
    resp = test_suite.run(global_env)
    assert resp.grade == 1
    assert resp.results[0].passed
    assert resp.results[1].passed


def test_make_test_pass():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = OKDocTest("test", docstring)
    result = test({'g': "Hello"})
    assert result.passed

def test_make_test_partial():
    """
    If there are two tests, and one fails, they all fail
    """
    docstring = r"""
    >>> g == "Hello"
    True
    >>> g == "Not Hello"
    """
    test = OKDocTest("test", docstring)
    result = test({'g': "Hello"})
    assert result.passed == False

def test_make_test_fail():
    """
    Test passing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = OKDocTest("test", docstring)
    tr = test({'h': "Hello"})
    assert tr.passed == False
    assert "NameError: name 'g' is not defined" in tr.hint
