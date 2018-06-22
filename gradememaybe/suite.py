from .result import TestResult
from vdom.helpers import div, pre, strong

class TestSuiteResult:
    """
    Results from running a Test Suite
    """
    def __init__(self, test_suite, grade, results):
        self.test_suite = test_suite
        self.results = results
        for r in results:
            r.parent = self
        self.grade = grade

    def _repr_vdom_(self):
        """
        Return HTML representation of this test result
        """
        style = {
            'margin-left': '12px',
            'border-left': '1px solid',
            'border-top': '1px solid',
            'padding-left': '4px',
            'padding-top': '4px'
        }
        items = [div('Grade for ', strong(self.test_suite.name), ': {}%'.format(self.grade * 100))]
        if self.grade != 1:
            for r in self.results:
                items.append(div(r._repr_vdom_(), style=style))
        return div(*items)

    def _repr_html_(self):
        return self._repr_vdom_().to_html()


class TestSuite:
    """
    Represents a collection of Tests.

    These are run against the same enviornment, and produce
    a TestSuiteResult object. Multiple grading strategies may be
    used to determine the final grade!

    Responsible for running tests, calculating grades & returning
    results.
    """
    MUST_PASS = 1
    PROPORTIONAL = 2

    def __init__(self, name, tests, scoring_strategy=MUST_PASS):
        # Tests can be Test or TestSuite objects
        self.name = name
        self.tests = tests
        self.scoring_strategy = scoring_strategy

    def run(self, global_environment):
        results = []
        for test in self.tests:
            if isinstance(test, TestSuite):
                # This is a test suite, with its own scoring_strategy
                # So we just ask it to run itself, and give back a score
                cur_result = test.run(global_environment)
                results.append(cur_result)
                if self.scoring_strategy == TestSuite.MUST_PASS and cur_result.grade != 1:
                    # We count anything not 1 as a failure
                    break
            else:
                # This is a test instance, so no scoring strategy.
                # We count a success as 1, failure as 0
                result = test(global_environment)
                results.append(result)
                if not result.passed and self.scoring_strategy == TestSuite.MUST_PASS:
                    # All tests must pass to get a non-zero score, and one has failed!
                    # We set grade to 0, and return hint from failed test
                    break

        # If our strategy was must pass & any test has failed, by this time we would
        # have returned early. Since we have not, we either completely succeeded, or
        # are proportional.
        grades = []
        for r in results:
            if isinstance(r, TestSuiteResult):
                grades.append(r.grade)
            else:
                # This must be a TestResult object
                grades.append(1 if r.passed else 0)
        if self.scoring_strategy == TestSuite.MUST_PASS:
            grade = 1 if all([g != 0 for g in grades]) else 0
        else:
            grade = sum(grades) / len(self.tests)
        return TestSuiteResult(self, grade, results)