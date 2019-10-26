import os
import os.path as op
import json
import pytest
from glob import glob

import nbformat

from gofer.ok import grade_notebook, run_nb_tests
from gofer.notebook import execute_notebook, _global_anywhere

import pytest

here = os.path.dirname(__file__)

def test_simple_execute():
    """
    Test we can execute notebooks & see the resulting environment
    """
    with open(os.path.join(here, 'notebooks/simplest-notebook.ipynb')) as f:
        nb = json.load(f)

    return_env = execute_notebook(nb)
    assert return_env['the_number_1'] == 1
    assert return_env['return_1']() == 1

def test_line_continuation():
    """
    Test line continuations work in notebooks
    """
    with open(os.path.join(here, 'notebooks/line-continuations.ipynb')) as f:
        nb = json.load(f)

    return_env = execute_notebook(nb)
    assert return_env['return_2']() == 2

def test_okgrade_magic():
    """
    Test we can execute notebooks with injected global variables
    """
    with open(os.path.join(here, 'notebooks/injected-magic.ipynb')) as f:
        nb = json.load(f)

    return_env = execute_notebook(nb, initial_env={'__GOFER_GRADER__': True})

    assert return_env['gofer_grader_present'] == True

def test_ignore_error():
    """
    Ignoring errors should work similar to notebooks

    The cell with the error should be executed until the error is
    raised, and then the next cell should be executed.
    """
    with open(os.path.join(here, 'notebooks/partial-error.ipynb')) as f:
        nb = json.load(f)

    return_env = execute_notebook(nb, ignore_errors=True)

    assert return_env['a'] == 5
    assert return_env['b'] == 6
    assert return_env['c'] == 7
    assert 'd' not in return_env
    assert 'e' not in return_env
    assert return_env['f'] == 9

def test_catch_error():
    """
    If code raises an error, we should catch it!

    Raised exceptions also halt execution of all future cells.
    """
    with open(os.path.join(here, 'notebooks/partial-error.ipynb')) as f:
        nb = json.load(f)

    with pytest.raises(NameError):
        execute_notebook(nb, ignore_errors=False)

def test_global_anywhere():
    """
    Test multiple levels of global checking
    """
    globals_l1 = {
        'LEVEL': 1
    }

    l1_code = """from gofer.notebook import _global_anywhere
NEW_LEVEL = _global_anywhere('LEVEL')"""

    # This is 'one' level up
    assert _global_anywhere('_global_anywhere') == _global_anywhere

    # Make sure this works inside exec too!
    exec(l1_code, globals_l1)
    assert globals_l1['NEW_LEVEL'] == 1

def test_grade_notebook():
    """
    Test notebooks that grade at various percentages
    """
    test_paths = os.path.join(here, 'notebooks/grading/tests/q*.py')

    full_grade_notebook = os.path.join(here, 'notebooks/grading/full-grade.ipynb')
    assert grade_notebook(full_grade_notebook, glob(test_paths)) == 1

    half_grade_notebook = os.path.join(here, 'notebooks/grading/half-grade.ipynb')
    assert grade_notebook(half_grade_notebook, glob(test_paths)) == 0.5

    zero_grade_notebook = os.path.join(here, 'notebooks/grading/zero-grade.ipynb')
    assert grade_notebook(zero_grade_notebook, glob(test_paths)) == 0


def test_nb_wd():
    # Test that notebook runs in its own directory.
    # Test will fail, give 0 score if notebook does not run in own directory.
    test_paths = os.path.join(here, 'notebooks', 'pwd', 'tests', 'q*.py')
    pwd_notebook = os.path.join(here, 'notebooks', 'pwd', 'pwd.ipynb')
    assert grade_notebook(pwd_notebook, glob(test_paths)) == 1


def test_run_nb_tests():
    # Test API for run_nb_tests
    # Test will fail, give 0 score, if notebook does not run in own directory.
    pwd_path = op.join(here, 'notebooks', 'pwd')
    test_paths = op.join(pwd_path, 'tests', 'q*.py')
    tests = glob(test_paths)
    pwd_notebook = op.join(pwd_path, 'pwd.ipynb')
    nb = nbformat.read(pwd_notebook, nbformat.NO_CONVERT)
    test_results = run_nb_tests(nb, pwd_path, tests)
    assert len(test_results) == 1
    assert test_results[0].grade == 1
    # When the directory is incorrect, the test fails.
    test_results = run_nb_tests(nb, here, tests)
    assert test_results[0].grade == 0
    # We can add variables to the environment with initial_env
    env_test = op.join(pwd_path, 'extra_tests', 'has_var.py')
    # Fails without initial var.
    test_results = run_nb_tests(nb, pwd_path, [env_test])
    assert test_results[0].grade == 0
    # Passes with.
    test_results = run_nb_tests(nb, pwd_path, [env_test],
                                initial_env={'extra_variable': 1}
                               )
    assert test_results[0].grade == 1
    # The test notebook also has a cell causing an error.
    # By default, testing ignores the error.  With ignore_errors=False, the
    # error falls through to us.
    with pytest.raises(ZeroDivisionError):
        test_results = run_nb_tests(nb, pwd_path, tests, ignore_errors=False)
