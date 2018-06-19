test = {
  'name': 'Second question',
  'suites': [
    {
    'cases': [
        {
          'code': r"""
          >>> # This is the second test, only one notebook should pass it
          >>> myvariable2 == 20
          True
          """
        }
      ]
    }
  ]
}
