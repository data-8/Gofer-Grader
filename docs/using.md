# Using okgrade

There are two primary use-cases for `okgrade`: as a lightweight
grading tool for instructors, and as a means of giving interactive
feedback to students doing work within Jupyter notebooks. See below
for information unique to each use-case.


## Prepare your tests

`okgrade` uses structured text files to define the tests that
it runs against your notebooks. Currently, it supports the
[ok test format](ok-test-format.html) to define the test
structure. See the [examples folder](https://github.com/grading/okgrade/examples)
for sample notebooks and okgrade tests.


## Common use-cases

### Interactive feedback

This section covers how to prepare a notebook to give interactive
feedback to students.

1. Write your tests in [ok test format](ok-test-format.html),
   and **distribute them along with your student notebooks**.

2. In the lab notebooks distributed to your students, import
   the `grade` function on top:

   ```python
   from okgrade import grade
   ```

3. At various points in the notebook, insert "grading feedback" cells, like:

   ```python
   grade('tests/q1.py')
   ```

   This will run the tests in `q1.py` with the student's
   current environment, and provide interactive results.
   Note that in this case, **no grading occurs**, this function is used
   solely to give feedback.

For an example notebook that uses this pattern, see
the [interactive example](https://github.com/grading/okgrade/examples/interactive_feedback.ipynb)

### As an auto-grading tool

You can also use `okgrade` to quickly grade the contents of multiple
student notebooks against multiple tests. To do so, take the
following steps:

1. Write your tests in [ok test format](ok-test-format.html). **You
   do not need to distribute these tests to your students**, as they
   will not be running them interactively.

2. After students have finished their work, make sure you have
   access to their notebooks. Each notebook should be able to be run
   successfully without error in order to receive full marks.

3. In a Python script, import the `grade_notebook` function:

   ```python
   from okgrade.notebook impor grade_notebook
   ```

4. Pass the path to a student notebook, as well as a list of paths to tests
   that you wish to run against that notebook.

   ```python
   result = grade_notebook(path_to_student_notebook, list_of_okgrade_tests)
   ```

5. Repeat for all students. `result` is an object that contains the fraction
   of correctly-passed tests for each notebook.

Remember, the tests are run *after all notebook cells have been executed*.

For an example notebook that uses this pattern, see
the [autograding example](https://github.com/grading/okgrade/examples/grade_notebooks.ipynb)

### As a drop-in replacement for okpy

`okpy` is a full-stack course management and grading tool currently being used
at UC Berkeley. It is possible to use `okgrade` to grade `okpy`-compliant notebooks.

If you are currently using okpy in notebooks, import the `okgrade`-compliant
functions like so:

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
