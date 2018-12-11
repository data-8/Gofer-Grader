import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import tornado.options
import os
import json
import asyncio
from grade_lab import grade_lab
from gofer.ok import grade_notebook, id_generator

from jupyterhub.services.auth import HubAuthenticated

test_dirs = {'test': '/Users/vipasu/Dropbox/Berkeley/Y2Fall/gradememaybe/tests/notebooks/grading'}
prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')


class GoferHandler(HubAuthenticated, tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write("This is a post only page. You probably shouldn't be here!")
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        """For grading submission, accept json notebook of submission"""
        if not self.current_user:
            self.get_current_user()
        req_data = tornado.escape.json_decode(self.request.body)
        # in the future, assignment should be metadata in notebook
        assignment, notebook = req_data['assignment'], req_data['nb']
        # change directory
        test_dir = test_dirs[assignment]
        os.chdir(test_dir)
        # save notebook to this dir
        fname = 'tmp.' + id_generator() + '.ipynb'
        while os.path.isfile(fname):
            # Generate new name is file exists
            fname = 'tmp.' + id_generator() + '.ipynb'
        with open(fname, 'w') as outfile:
            json.dump(notebook, outfile)
        # execute notebook from this directory
        grade = grade_notebook(fname)
        # remove file
        os.remove(fname)
        # return grade
        print(grade)
        self.write(str(grade))
        self.finish()


if __name__=='__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([(prefix, GoferHandler)])

    app.listen(10101)

    tornado.ioloop.IOLoop.current().start()
