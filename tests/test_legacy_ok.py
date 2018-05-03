import os

from client.api.notebook import Notebook, parse_ok_test

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
    tests = parse_ok_test(os.path.join(here, 'oktests/tests/simple_valid.py'))
    global_env = {}

    responses = [test(global_env) for test in tests]
    # All tests should fail now
    assert all([resp.grade == 0 for resp in responses])

    global_env['defined_variable'] = None

    # First test should pass now, but second should fail
    responses = [test(global_env) for test in tests]
    assert responses[0].grade == 1
    assert responses[1].grade == 0

    # Both tests should pass now
    global_env['seconds_in_a_minute'] = 60
    responses = [test(global_env) for test in tests]
    assert responses[0].grade == 1
    assert responses[1].grade == 1