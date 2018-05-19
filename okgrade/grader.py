import inspect
from okgrade.doctest import SingleDocTest
from okgrade.result import TestResult

def parse_ok_test(path):
    """
    Parse a ok test file & return list of SingleDocTests.
    """
    # ok test files are python files, with a global 'test' defined
    test_globals = {}
    with open(path) as f:
        exec(f.read(), test_globals)
    
    test_spec = test_globals['test']

    # We only support a subset of these tests, so let's validate!

    # Make sure there is a name
    assert 'name' in test_spec

    # Do not support multiple suites in the same file
    assert len(test_spec['suites']) == 1

    # Do not support point values other than 1
    assert test_spec.get('points', 1) == 1

    test_suite = test_spec['suites'][0]

    # Only support doctest. I am unsure if other tests are implemented
    assert test_suite.get('type', 'doctest') == 'doctest'

    # Not setup and teardown supported
    assert not bool(test_suite.get('setup'))
    assert not bool(test_suite.get('teardown'))

    tests = []

    for i, test_case in enumerate(test_spec['suites'][0]['cases']):
        tests.append(SingleDocTest(
            test_spec['name'] + ' ' + str(i + 1),
            test_case['code']
        ))

    return tests


def grade(test_file_path, global_env=None):
    """
    Grade global_env against given test_file

    If global_env is none, the global environment of the calling
    function is used. The following two calls are equivalent:

    grade('somefile.ok')

    grade('somefile.ok', globals())

    Returns a TestResult object.
    """
    tests = parse_ok_test(test_file_path)
    if global_env is None:
        # Get the global env of our callers - one level below us in the stack
        # The grade method should only be called directly from user / notebook
        # code. If some other method is calling it, it should also use the
        # inspect trick to pass in its parents' global env.
        global_env = inspect.currentframe().f_back.f_globals
    for test in tests:
        resp = test(global_env)
        if resp.grade == 0:
            return resp
    # All tests passed!
    return TestResult(1, f"{test_file_path}: All tests passed!")