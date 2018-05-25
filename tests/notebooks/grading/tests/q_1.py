# Test for 'defined_variable'
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
          >>> defined_variable == 100
          True

          You should define variable defined_variable to the value 100
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
