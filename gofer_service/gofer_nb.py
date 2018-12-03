#!/usr/bin/env python3
"""
whoami service authentication with the Hub
"""

from functools import wraps
import json
import os
from urllib.parse import quote

from flask import Flask, redirect, request, Response

from jupyterhub.services.auth import HubAuth

from gofer.ok import grade_notebook, id_generator

from flask_cors import CORS

prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')

auth = HubAuth(
    api_token=os.environ['JUPYTERHUB_API_TOKEN'],
    cache_max_age=60,
)

app = Flask(__name__)
CORS(app)


def authenticated(f):
    """Decorator for authenticating with the Hub"""
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.get_json())
        cookie = request.cookies.get(auth.cookie_name)
        token = request.headers.get(auth.auth_header_name)
        if cookie:
            user = auth.user_for_cookie(cookie)
        elif token:
            user = auth.user_for_token(token)
        else:
            user = None
        if user:
            return f(user, *args, **kwargs)
        else:
            # redirect to login url on failed auth
            return redirect(auth.login_url + '?next=%s' % quote(request.path))
    return decorated

test_dirs = {'test': '/Users/vipasu/Dropbox/Berkeley/Y2Fall/gradememaybe/tests/notebooks/grading'}

@app.route(prefix, methods=['POST'])
@authenticated
def grade_submission(user):
    print(user['name']+ ' has just submitted an assignment')
    req_data = request.get_json(force=True)
    # in the future, assignment should be metadata in notebook
    assignment, notebook = req_data['assignment'], req_data['nb']
    # change directory
    test_dir = test_dirs[assignment]
    os.chdir(test_dir)
    # save notebook to this dir
    # careful not to overwrite
    fname = 'tmp.' + id_generator() + '.ipynb'
    while os.path.isfile(fname):
        fname = id_generator() + '.ipynb'
    with open(fname, 'w') as outfile:
        json.dump(notebook, outfile)
    # execute notebook from this directory
    grade = grade_notebook(fname)
    # remove file
    os.remove(fname)
    # return grade
    print(grade)
    return str(grade)
