from contextlib import redirect_stderr, redirect_stdout
import json
import inspect
from okgrade.grader import grade
from okgrade.result import TestResult

try:
    from IPython.core.inputsplitter import IPythonInputSplitter
except ImportError:
    raise ImportError('IPython needs to be installed for notebook grading')

def execute_notebook(nb, initial_env=None, ignore_errors=False):
    """
    Execute notebook & return the global environment that results from execution.

    If ignore_errors is True, exceptions are swallowed.

    nb is passed in as a dictionary that's a parsed ipynb file
    """
    if initial_env:
        global_env = initial_env.copy()
    else:
        global_env = {}
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # transform the input to executable Python
            # FIXME: use appropriate IPython functions here
            isp = IPythonInputSplitter(line_input_checker=False)
            source = isp.transform_cell('\n'.join(cell['source']))
            try:
                with open('/dev/null', 'w') as f, redirect_stdout(f), redirect_stderr(f):
                    exec(source, global_env)
            except:
                if not ignore_errors:
                    raise
    return global_env

def _global_anywhere(varname):
    """
    Return global with given name in any frame in the call stack

    Throws NameError if no such global exists anywhere in the call stack
    """
    # This should not be a recursive function, since that modifies the stack!
    cur_frame = inspect.currentframe().f_back
    while cur_frame is not None:
        if varname in cur_frame.f_globals:
            return cur_frame.f_globals[varname]
        cur_frame = cur_frame.f_back
    raise NameError(f'{varname} not found in any globals in the stack')


def grade_notebook(notebook_path, test_files):
    """
    Grade a notebook file & return grade
    """
    try:
        # Lots of notebooks call grade_notebook in them. These notebooks are then
        # executed by okgrade - which will in-turn execute grade_notebook again!
        # This puts us in an infinite loop.
        # We use this sentinel to detect and break out of that loop.
        _global_anywhere('__OKGRADE__')
        # FIXME: Do something else here?
        return None
    except NameError:
        pass

    with open(notebook_path) as f:
        nb = json.load(f)

    initial_env = {
        # Set this to prevent recursive executions!
        '__OKGRADE__': True
    }

    global_env = execute_notebook(nb, initial_env, ignore_errors=True)

    # FIXME: This needs to be more general
    results = [grade(tf, global_env) for tf in test_files]
    
    test_grade = sum([r.grade for r in results]) / len(results)
    if test_grade == 1:
        return TestResult(1.0, 'Grade is: 100%')
    else:
        # FIXME: This is terrible!
        grade_pct = test_grade * 100
        summary = f"Grade is: {grade_pct}%\n"
        summary += "\n".join([r.get_summary() for r in results])
        return TestResult(test_grade, summary)
