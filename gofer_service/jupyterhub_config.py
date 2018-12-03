c.JupyterHub.services = [
    {
        'name': 'gofer_nb',
        'url': 'http://127.0.0.1:10101',
        'command': ['flask', 'run', '--port=10101'],
        'environment': {
            'FLASK_APP': 'gofer_nb.py',
        }
    }
]
