from contextlib import redirect_stderr, redirect_stdout
import json
from glob import glob
from okgrade.grader import grade
from okgrade.result import TestResult

def code_from_ipynb(nb, ignore_errors=False):
    """
    Get the code for a given notebook

    If ignore_errors is True, exceptions are swallowed.

    nb is passed in as a dictionary that's a parsed ipynb file
    """
    global_env = {
        # Set this to prevent recursive executions!
        'OKGRADE_EXEC': True
    }
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # transform the input to executable Python
            # FIXME: use appropriate IPython functions here
            source = '\n'.join(cell['source']).replace('%matplotlib inline', '')
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
    try:
        OKGRADE_EXEC
        return
    except NameError:
        pass

    with open(notebook_path) as f:
        nb = json.load(f)

    global_env = code_from_ipynb(nb, ignore_errors=True)

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
