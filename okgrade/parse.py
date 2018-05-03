"""
Parse a subset of okpy test files.
"""
import io
import json
import argparse
from glob import glob
import os
import doctest
import copy
from contextlib import redirect_stdout, redirect_stderr

def make_test(name, doctest_string):
    """
    Return a callable for running the given test.

    Returned callable takes a global_environment dict,
    and returns a dict with the following keys:

    1. 'grade' - a float between 0 and 1
    2. 'summary' - text output to show users

    We only take a global_environment, *not* a local_environment.
    This makes tests not useful inside functions, methods or
    other scopes with local variables. This is a limitation of
    doctest, so we roll with it.
    """
    def _test(global_environment):
        """
        Run a doctest in a global_environment & return grade.
        """
        examples = doctest.DocTestParser().parse(
            doctest_string,
            name
        )

        test = doctest.DocTest(
            [e for e in examples if type(e) is doctest.Example],
            global_environment,
            name,
            None,
            None,
            doctest_string
        )

        doctestrunner = doctest.DocTestRunner(verbose=True)
        runresults = io.StringIO()
        with redirect_stdout(runresults), redirect_stderr(runresults):
            doctestrunner.run(test, clear_globs=False)
        with open('/dev/null', 'w') as f, redirect_stderr(f), redirect_stdout(f):
            result = doctestrunner.summarize(verbose=True)
        grade = 1 - (result.failed / result.attempted)
        return {
            'grade': grade,
            'name': name,
            'summary': runresults.getvalue()
        }

    return _test
    
def parse_ok_test(path):
    """
    Parse a ok test file & return list of tests.

    Returned tests can be called with a global environment
    dict to run them.
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
    assert test_spec['points'] == 1

    test_suite = test_spec['suites'][0]

    # Only support doctest. I am unsure if other tests are implemented
    assert test_suite['type'] == 'doctest'

    # Not setup and teardown supported
    assert not bool(test_suite.get('setup'))
    assert not bool(test_suite.get('teardown'))

    tests = []

    for i, test_case in enumerate(test_spec['suites'][0]['cases']):
        tests.append(make_test(
            test_spec['name'] + ' ' + str(i),
            test_case['code']
        ))

    return tests