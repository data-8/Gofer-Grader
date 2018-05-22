from contextlib import redirect_stderr, redirect_stdout
import json
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

def grade_notebook(notebook_path, test_files):
    """
    Grade a notebook file & return grade
    """
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
