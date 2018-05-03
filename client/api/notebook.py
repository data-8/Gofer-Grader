"""
Backwards compatibility shim for old okpy API
"""
import os
import inspect
from okgrade.doctest import SingleDocTest

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
    assert test_spec['points'] == 1

    test_suite = test_spec['suites'][0]

    # Only support doctest. I am unsure if other tests are implemented
    assert test_suite['type'] == 'doctest'

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

class Notebook:
    def __init__(self, okfile):
        """
        okfile is path to .ok file.

        This implementation does not read the .ok files.
        However, their path is used as basedir when looking
        for tests.
        """
        self.basedir = os.path.dirname(os.path.abspath(okfile))

    def _display(self, *objs):
        """
        Display *objs if running in IPython
        """
        try:
            __IPYTHON__
            # We are in a Notebook / IPython! Let's display output
            from IPython.display import display
            display(*objs)
        except NameError:
            pass

    def auth(self, inline=False):
        """
        Legacy interface for authenticating to an okpy server.

        Not supported, so we ignore for now.
        """
        # FIXME: A warning here?
        pass

    def submit(self):
        """
        Legacy interface for submitting a notebook to okpy server.

        Not supported, so we ignore for now.
        """
        # FIXME: A warning here?
        pass

    def grade(self, question, global_env=None):
        path = os.path.join(self.basedir, "tests", "{}.py".format(question))
        tests = parse_ok_test(path)
        if global_env is None:
            # Get the global env of our callers - one level below us in the stack
            # The grade method should only be called directly from user / notebook
            # code. If some other method is calling it, it should also use the
            # inspect trick to pass in its parents' global env.
            global_env = inspect.stack()[1][0].f_globals
        for test in tests:
            resp = test(global_env)
            if resp.grade == 0:
                self._display(resp)
                break
        else:
            self._display('Tests passed!')
