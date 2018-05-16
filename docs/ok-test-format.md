# Writing OK Tests

We implement a specific subset of OK Tests that instructors
can write. It doesn't have all the features that okpy has, but
tries to be compatible wherever possible. 

An OK Test should be a valid python file that assigns a dictionary
to a global variable named `test`. Let's explore this more with an
example.

## Example

```python
test = {
  'name': '2.2',
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # It looks like you didn't give anything the name
          >>> # seconds_in_a_decade.  Maybe there's a typo, or maybe you
          >>> # just need to run the cell below Question 3.2 where you defined
          >>> # seconds_in_a_decade.  (Click that cell and then click the "run
          >>> # cell" button in the menu bar above.)
          >>> 'seconds_in_a_decade' in vars()
          True
          """
        },
        {
          'code': r"""
          >>> # It looks like you didn't change the cell to define
          >>> # seconds_in_a_decade appropriately.  It should be a number,
          >>> # computed using Python's arithmetic.  For example, here's
          >>> # a statement that changes seconds_in_a_decade to 100:
          >>> #   seconds_in_a_decade = 10*10
          >>> seconds_in_a_decade != ...
          True
          """
        },
        {
          'code': r"""
          >>> # The number of seconds you computed is too low by at least
          >>> # a factor of 5.
          >>> # There are 10 years, some number of days in a year, some 
          >>> # number of hours per day, minutes per hour, and seconds
          >>> # per minute. For example, this is almost right:
          >>> #   seconds_in_a_decade = 10*365*24*60*60
          >>> seconds_in_a_decade > 60000000
          True
          """
        },
        {
          'code': r"""
          >>> # The number of seconds you computed is too high by at least
          >>> # a factor of 5.
          >>> # There are 10 years, some number of days in a year, some 
          >>> # number of hours per day, minutes per hour, and seconds
          >>> # per minute. For example, this is almost right:
          >>> #   seconds_in_a_decade = 10*365*24*60*60
          >>> seconds_in_a_decade < 1600000000
          True
          """
        },
        {
          'code': r"""
          >>> # You're close! Perhaps you didn't account for leap years correctly.
          >>> # There were 2 leap years and 8 non-leap years in this period.
          >>> # Leap years have 366 days instead of 365.
          >>> 315360000 < seconds_in_a_decade < 331344000
          True
          """
        },
        {
          'code': r"""
          >>> seconds_in_a_decade == 315532800
          True
          """
        }
      ]
    }
  ]
}
```

## Name

Name of this series of tests that is shown to students when it passes.

## Suites

This should always be a list with a single item. The single item must
be a dictionary with the single key `cases` where the value is a list of
**test cases**.

Each **test case** is a dictionary, with one key `code`, and the value is
a test in [doctest](https://docs.python.org/3.6/library/doctest.html) format.
There can be any number of test cases - these will be run sequentially until
one of them fails.