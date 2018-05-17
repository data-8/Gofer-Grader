import doctest
import io
from contextlib import redirect_stderr, redirect_stdout
from textwrap import dedent

from okgrade.result import TestResult

class SingleDocTest:
    """
    A single DocTest.

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

    PLAIN_TEXT_SUMMARY_TEMPLATE = dedent(r"""
    Test {name} failed!

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

        doctestrunner = doctest.DocTestRunner(verbose=True)

        runresults = io.StringIO()
        with redirect_stdout(runresults), redirect_stderr(runresults):
            doctestrunner.run(test, clear_globs=False)
        with open('/dev/null', 'w') as f, redirect_stderr(f), redirect_stdout(f):
            result = doctestrunner.summarize(verbose=True)
        grade = 1.0 - (result.failed / result.attempted)
        if grade == 1.0:
            summary = 'Test {} passed!'.format(self.name)
        else:
            summary = self.PLAIN_TEXT_SUMMARY_TEMPLATE.format(
                name=self.name,
                doctest_string=dedent(self.doctest_string),
                runresults=runresults.getvalue()
            )
        return TestResult(grade, summary)