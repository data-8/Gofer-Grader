import os
import json
import pytest
from glob import glob
from okgrade.ok import parse_ok_test
from okgrade.suite import TestSuite
from okgrade.notebook import execute_notebook, _global_anywhere, grade_notebook

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

def test_okgrade_magic():
    """
    Test we can execute notebooks with injected global variables
    """
    with open(os.path.join(here, 'notebooks/injected-magic.ipynb')) as f:
        nb = json.load(f)

    return_env = execute_notebook(nb, {'__OKGRADE__': True})

    assert return_env['ok_grade_present'] == True

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

    l1_code = """from okgrade.notebook import _global_anywhere
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
    test_paths = glob(os.path.join(here, 'notebooks/grading/tests/q*.py'))

    test_suite = TestSuite([parse_ok_test(p) for p in test_paths], TestSuite.PROPORTIONAL)
    full_grade_notebook = os.path.join(here, 'notebooks/grading/full-grade.ipynb')
    assert grade_notebook(full_grade_notebook, test_suite).grade == 1

    half_grade_notebook = os.path.join(here, 'notebooks/grading/half-grade.ipynb')
    assert grade_notebook(half_grade_notebook, test_suite).grade == 0.5

    zero_grade_notebook = os.path.join(here, 'notebooks/grading/zero-grade.ipynb')
    assert grade_notebook(zero_grade_notebook, test_suite).grade == 0

