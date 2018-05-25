# Test for 'another_defined_variable'
test = {
  'name': 'test_valid',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 'another_defined_variable' in vars()
          True

          Looks like you did not define the variable 'another_defined_variable'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> another_defined_variable == 200
          True

          You should set another_defined_variable to 200
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