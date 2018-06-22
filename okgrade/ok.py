import doctest
import inspect
import io
from contextlib import redirect_stderr, redirect_stdout
from textwrap import dedent

from okgrade.suite import TestSuite
from okgrade.result import TestResult
from okgrade.utils import hide_outputs
from vdom.helpers import pre, strong, div

class OKDocTest:
    """
    A single DocTest defined by OKPy.

    Instances of this class are callable. When called, it takes
    a global_environment dict, and returns a TestResult object.

    We only take a global_environment, *not* a local_environment.
    This makes tests not useful inside functions, methods or
    other scopes with local variables. This is a limitation of
    doctest, so we roll with it.
    """
    def __init__(self, name, doctest_string):
        self.name = name
        self.doctest_string = doctest_string
        self.examples = doctest.DocTestParser().parse(
            doctest_string,
            name
        )

    PLAIN_TEXT_HINT_TEMPLATE = dedent(r"""
    Test code:
    {doctest_string}
    Test result:
    {runresults}
    """).strip()

    def __call__(self, global_environment):
        """
        Run test with given global_environment.
        """
        test = doctest.DocTest(
            [e for e in self.examples if isinstance(e, doctest.Example)],
            global_environment,
            self.name,
            None,
            None,
            self.doctest_string
        )

        doctestrunner = doctest.DocTestRunner(verbose=False)

        runresults = io.StringIO()
        with redirect_stdout(runresults), redirect_stderr(runresults), hide_outputs():
            doctestrunner.run(test, clear_globs=False)
        with open('/dev/null', 'w') as f, redirect_stderr(f), redirect_stdout(f):
            result = doctestrunner.summarize(verbose=True)
        # An individual test can only pass or fail
        if result.failed == 0:
            passed = True
        else:
            passed = False
        hint = {}
        if not passed:

            hint = self.PLAIN_TEXT_HINT_TEMPLATE.format(
                name=self.name,
                doctest_string=dedent(self.doctest_string),
                runresults=runresults.getvalue()
            )
        return TestResult(self, passed, hint)

def parse_ok_test(path):
    """
    Parse a ok test file & return a TestSuite
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
        tests.append(OKDocTest(
            test_spec['name'] + ' ' + str(i + 1),
            test_case['code']
        ))

    return TestSuite(path, tests, TestSuite.MUST_PASS)


def check(test_file_path, global_env=None):
    """
    check global_env against given test_file in oktest format

    If global_env is none, the global environment of the calling
    function is used. The following two calls are equivalent:

    check('tests/q1.py')

    check('tests/q1.py', globals())

    Returns a TestResult object.
    """
    test_suite = parse_ok_test(test_file_path)
    if global_env is None:
        # Get the global env of our callers - one level below us in the stack
        # The grade method should only be called directly from user / notebook
        # code. If some other method is calling it, it should also use the
        # inspect trick to pass in its parents' global env.
        global_env = inspect.currentframe().f_back.f_globals
    return test_suite.run(global_env)