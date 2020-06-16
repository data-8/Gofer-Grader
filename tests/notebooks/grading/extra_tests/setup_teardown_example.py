test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> np.sqrt(1)
          1.0
          """,
          'hidden': False,
          'locked': False
        },
      ],
      'scored': True,
      'setup': r"""
      >>> import numpy as np
      """,
      'teardown': r"""
      >>> assert False
      """,
      'type': 'doctest'
    }
  ]
}
