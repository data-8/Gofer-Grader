import html

class TestResult:
    """
    The result of running a test against an environment.

    Contains a grade (float) and a dictionary of 'summaries'
    that can be displayed to the user, in various mime types.
    """
    def __init__(self, grade, summary_mimebundle):
        """
        Result of running a Test of some kind.

        grade - float, the grade this test produced.
        summary_mimebundle - dict | string, mapping mimetypes to summaries.
                             If string is passed in, assume it is for mimetype 
                             text/plain.
        """
        self.grade = grade
        if isinstance(summary_mimebundle, str):
            self.summary_mimebundle = {'text/plain': summary_mimebundle}
        else:
            if 'text/plain' not in summary_mimebundle:
                raise ValueError('summary_mimebundle must contain text/plain')
            self.summary_mimebundle = summary_mimebundle

    def get_summary(self, mimetype='text/plain'):
        """
        Return summary for this TestResult.

        If mimetype is not passed in, 'text/plain' is assumed
        """
        return self.summary_mimebundle[mimetype]

    def _repr_html_(self):
        """
        Return HTML representation of this Test Result.

        Used by IPython to display pretty results
        """
        if 'text/html' in self.summary_mimebundle:
            return self.get_summary('text/html')
        else:
            return '<pre>' + html.escape(self.get_summary('text/plain')) + '</pre>'

    def __eq__(self, other):
        if not isinstance(other, TestResult):
            raise ValueError('Can not compare TestResult object with object of type {}'.format(type(other)))

        return other.grade == self.grade and other.summary_mimebundle == self.summary_mimebundle