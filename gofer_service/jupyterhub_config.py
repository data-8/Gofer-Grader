c.JupyterHub.services = [
    {
        'name': 'gofer_nb',
        'url': 'http://127.0.0.1:10101',
        'command': ['python', 'gofer_nb.py'],
    }
]
