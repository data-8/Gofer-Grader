# Simple, valid okpy test file
test = {
  'name': 'test_valid',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 'defined_variable' in vars()
          True

          Looks like you did not define the variable 'defined_variable'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> seconds_in_a_minute == 60
          True

          You should set up the variable seconds_in_a_minute to be number of seconds
          per minute
          """,
          'hidden': False,
          'locked': False
        },
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
