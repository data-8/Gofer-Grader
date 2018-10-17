"""
Backwards compatibility shim for old okpy API
"""
import os
import inspect
from gofer.ok import check

class Notebook:
    """
    Legacy class representing a notebook + associated tests.

    Provided for drop-in compatibility with projects that
    use a small subset of okpy's features.
    """
    def __init__(self, okfile):
        """
        okfile is path to .ok file.

        This implementation does not read the .ok files.
        However, their path is used as basedir when looking
        for tests.
        """
        self.basedir = os.path.dirname(os.path.abspath(okfile))

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
        """
        Legacy interface for grading a question in an environment.

        Acts similar to gradememaybe.ok.check, but displays the response
        directly if running in a Jupyter Notebook / IPython terminal.
        This keeps it compatible with okpy's interface.
        """
        path = os.path.join(self.basedir, "tests", "{}.py".format(question))
        if global_env is None:
            # Get the global env of our callers - one level below us in the stack
            # The grade method should only be called directly from user / notebook
            # code. If some other method is calling it, it should also use the
            # inspect trick to pass in its parents' global env.
            global_env = inspect.currentframe().f_back.f_globals
        result = check(path, global_env)
        # We display the output if we're in IPython.
        # This keeps backwards compatibility with okpy's grade method
        # which dumped into into stdout.
        try:
            __IPYTHON__
            # We are in a Notebook / IPython! Let's display output
            from IPython.display import display
            display(result)
        except NameError:
            pass
        return result
