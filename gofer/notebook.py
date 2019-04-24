from contextlib import redirect_stderr, redirect_stdout
import inspect
from .utils import hide_outputs
import ast

try:
    from IPython.core.inputsplitter import IPythonInputSplitter
except ImportError:
    raise ImportError('IPython needs to be installed for notebook grading')


def find_check_definition(tree):
    """Given an AST for a source, check for definitions of `check` function

    Returns True if such a definition is found, False otherwise."""
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.FunctionDef):
            continue
        if stmt.name == 'check':
            return True
    return False


def find_check_assignment(tree):
    """Given an AST for a source, check for variable redefinition of `check`

    Returns True if such a definition is found, False otherwise."""
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.Assign):
            continue
        # check id for tuple target
        target_names = []
        for target in stmt.targets:
            if isinstance(target, tuple):
                target_names += [t.id for t in target]
            elif isinstance(target, ast.Tuple) or isinstance(target, ast.List):
                target_names += [t.id for t in target.elts]
            elif isinstance(target, ast.Subscript):
                target_names.append(target.value.id)
            else:
                target_names.append(target.id)
        if 'check' in target_names:
            return True
    return False


class CheckCallWrapper(ast.NodeTransformer):
    """NodeTransformer visits and replaces nodes in place.
    CheckCallWrapper finds nodes with check(..) and replaces it with
    check_results_<secret>(check(...))"""

    def __init__(self, secret):
        self.secret = secret

    def node_constructor(self, expression):
        """Creates node that wraps expression in a list (check_results_XX) append call"""
        args = [expression]
        func = ast.Attribute(attr='append',
                             value=ast.Name(id='check_results_{}'.format(self.secret),
                                            ctx=ast.Load()),
                             ctx=ast.Load(),
                             keywords=[])
        return ast.Call(func=func, args=args, keywords=[])

    def visit_Call(self, node):
        """Function that handles whether a given function call is a 'check' call
        and transforms the node accordingly."""
        # test case is if check is .check
        if isinstance(node.func, ast.Attribute):
            return node
        elif isinstance(node.func, ast.Name):
            if node.func.id == 'check':
                return self.node_constructor(node)
            else:
                return node
        else:
            return node


def execute_notebook(nb, secret='secret', initial_env=None, ignore_errors=False):
    """
    Execute notebook & return the global environment that results from execution.

    TODO: write a note about the injection of check_results

    If ignore_errors is True, exceptions are swallowed.

    secret contains random digits so check_results and check are not easily modifiable

    nb is passed in as a dictionary that's a parsed ipynb file
    """
    with hide_outputs():
        if initial_env:
            global_env = initial_env.copy()
        else:
            global_env = {}
        source = ""

        # Before rewriting AST, find cells of code that generate errors.
        # One round of execution is done beforehand to mimic the Jupyter notebook style of running
        # (e.g. code runs up to the point of execution).
        # The reason this is workaround is introduced is because once the
        # source code is parsed into an AST, there is no sense of local cells

        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                # transform the input to executable Python
                # FIXME: use appropriate IPython functions here
                isp = IPythonInputSplitter(line_input_checker=False)
                try:
                    code_lines = ['import warnings\n', 'warnings.filterwarnings("ignore")\n']
                    cell_source_lines = cell['source']
                    source_is_str_bool = False
                    if isinstance(cell_source_lines, str):
                        source_is_str_bool = True
                        cell_source_lines = cell_source_lines.split('\n')

                    for line in cell_source_lines:
                        # Filter out ipython magic commands
                        # Filter out interact widget
                        if not line.startswith('%'):
                            if "interact(" not in line:
                                code_lines.append(line)
                                if source_is_str_bool:
                                    code_lines.append('\n')
                    cell_source = isp.transform_cell(''.join(code_lines))
                    exec(cell_source, global_env)
                    source += cell_source
                except:
                    if not ignore_errors:
                        raise

        tree = ast.parse(source)
        if find_check_assignment(tree) or find_check_definition(tree):
            # an empty global_env will fail all the tests
            return global_env

        # wrap check(..) calls into a check_results_X.append(check(..))
        transformer = CheckCallWrapper(secret)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        cleaned_source = compile(tree, filename="nb-ast", mode="exec")
        try:
            with open('/dev/null', 'w') as f, redirect_stdout(f), redirect_stderr(f):
                exec(cleaned_source, global_env)
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
