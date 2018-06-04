import html

class TestResult:
    """
    The result of running a test against an environment.

    A Test can only result in a pass or fail. If it failed, it
    can produce a 'hint' that can be shown to the user.
    """
    def __init__(self, passed, hint_bundle=None):
        """
        Result of running a Test of some kind.

        passed - True if this test passed, false otherwise
        hint_bundle -   dict | string, mapping mimetypes to hints.
                        If string is passed in, assume it is for mimetype
                        text/plain.
        """
        self.passed = passed
        if isinstance(hint_bundle, str):
            self.hint_bundle = {'text/plain': hint_bundle}
        else:
            self.hint_bundle = hint_bundle

    def get_hint(self, mimetype='text/plain'):
        """
        Return hint for this TestResult.

        If mimetype is not passed in, 'text/plain' is assumed
        """
        return self.hint_bundle[mimetype]

    def _repr_html_(self):
        """
        Return HTML representation of this Test Result.

        Used by IPython to display pretty results
        """
        if 'text/html' in self.hint_bundle:
            return self.get_hint('text/html')
        else:
            return '<pre>' + html.escape(self.get_hint('text/plain')) + '</pre>'

    def __eq__(self, other):
        if not isinstance(other, TestResult):
            raise ValueError('Can not compare TestResult object with object of type {}'.format(type(other)))

        return other.passed == self.passed and other.hint_bundle == self.hint_bundle