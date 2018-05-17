# Using okgrade

1. Write your tests in [ok test format](ok-test-format.md),
   and distribute them the same way you distribute lab notebooks
   to students.
2. In the lab notebooks distributed to your students, import
   the `grade` function on top:

   ```python
   from okgrade import grade
   ```
3. At various points, insert `grading cells`, like:

   ```python
   grade('tests/q1.py')
   ```

   This will run the tests in `q1.py` with the student's
   current environment, and provide interactive results.

## Drop-in replacement for okpy

If you are currently using okpy in notebooks, you will
import it like:

```python
from client.api.notebook import Notebook
ok = Notebook('test1.ok')
ok.auth() # Pops open an OAuth authentication link
```

And then your grading cells will look like:

```python
_ = ok.grade('q1.py')
```

A small shim is provided so this interface will continue
to not error!

`ok.auth` and `ok.submit` are empty methods that do
nothing. `ok.grade` does the same thing as `grade`,
but also displays the output if run inside an IPython
environment, to mimic okpy's behavior.