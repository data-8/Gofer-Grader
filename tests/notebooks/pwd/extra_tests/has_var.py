test = {
  'name': 'Presence of variable',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 'extra_variable' in vars()
          True
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
