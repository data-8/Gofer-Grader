# Using Gofer Grader

1. Write your tests in [ok test format](ok-test-format.md),
   and distribute them the same way you distribute lab notebooks
   to students.
2. In the lab notebooks distributed to your students, import
   the `check` function on top:

   ```python
   from gofer.ok import check
   ```

3. At various points, insert `check cells`, like:

   ```python
   check('tests/q1.py')
   ```

   This will run the tests in `q1.py` with the student's
   current environment, and provide interactive results.

# Usage Demo
To test out Gofer Grader, we've provided a sample Docker image with a demo notebook and test file. Make sure Docker is installed and running on your computer.  
In your terminal, run  
```docker run -p 8888:8888 gavrilm/gofer-grader-demo```  
This will download the demo image and start it in a new container, exposing port 8888 as the notebook server. Then, go to your browser and paste in the URL printed in the terminal to access the demo. It should be in the format `http://<ip address here>:8888?token=<token number here>`.  
\*Note: the IP address printed in the terminal may not be correct. Run `docker-machine ip` in the terminal for the correct one.\*.

## Drop-in replacement for okpy

If you are currently using okpy in notebooks, you will
import it like:

```python
from client.api.notebook import Notebook
ok = Notebook('test1.ok')
ok.auth()
```

And then your grading cells will look like:

```python
_ = ok.grade('q1.py')
```

A small shim is provided so this interface will continue
to not error!

`ok.auth` and `ok.submit` are empty methods that do
nothing. `ok.grade` does the same thing as `gofer.ok.check`,
but also displays the output if run inside an IPython
environment, to mimic okpy's behavior.
