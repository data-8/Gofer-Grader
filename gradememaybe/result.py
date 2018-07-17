import html

class TestResult:
    """
    The result of running a test against an environment.

    A Test can only result in a pass or fail. If it failed, it
    can produce a 'hint' that can be shown to the user.
    """
    def __init__(self, passed, hint=None):
        """
        Result of running a Test of some kind.

        passed - True if this test passed, false otherwise
        hint - Possible hint to be shown the user. Plain text.
        """
        self.passed = passed
        self.hint = hint

    def _repr_html_(self):
        """
        Return HTML representation of this Test Result.

        Used by IPython to display pretty results
        """
        return '<pre>' + html.escape(self.hint) + '</pre>'

    def __eq__(self, other):
        if not isinstance(other, TestResult):
            raise ValueError('Can not compare TestResult object with object of type {}'.format(type(other)))

        return other.passed == self.passed and other.hint == self.hint
