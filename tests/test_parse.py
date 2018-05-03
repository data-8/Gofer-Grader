import os
from textwrap import dedent
from okgrade.parse import make_test, parse_ok_test

def test_make_test():
    """
    Test passing & failing test runs with tests from make_test
    """
    docstring = r"""
    >>> g == "Hello"
    True
    """
    test = make_test("test", docstring)
    assert test({'g': "Hello"}) == {
        'grade': 1,
        'summary': dedent(r"""
        Trying:
            g == "Hello"
        Expecting:
            True
        ok
        """).lstrip()
    }
    # FIXME: There is a path here that will vary across installs. 
    assert test({'h': "Hello"})  == {
        'grade': 0,
        'summary': dedent(r"""
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
        """).lstrip()
        }

def test_ok_parse_simple_valid():
    """
    Test parsing & running a simple oktest file.
    """
    here = os.path.dirname(__file__)

    # This should not raise any AssertionErrors
    tests = parse_ok_test(os.path.join(here, 'oktests/simple_valid.py'))
    global_env = {}

    responses = [test(global_env) for test in tests]
    # All tests should fail now
    assert all([resp['grade'] == 0 for resp in responses])

    global_env['defined_variable'] = None

    # First test should pass now, but second should fail
    responses = [test(global_env) for test in tests]
    assert responses[0]['grade'] == 1
    assert responses[1]['grade'] == 0

    # Both tests should pass now
    global_env['seconds_in_a_minute'] = 60
    responses = [test(global_env) for test in tests]
    assert responses[0]['grade'] == 1
    assert responses[1]['grade'] == 1