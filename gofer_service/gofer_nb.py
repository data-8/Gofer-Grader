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
        notebook = req_data['nb']
        section = notebook['metadata']['section']
        lab = notebook['metadata']['lab']

        # save notebook to temporary file
        fname = 'tmp.' + id_generator() + '.ipynb'
        while os.path.isfile(fname):
            # Generate new name is file exists
            fname = 'tmp.' + id_generator() + '.ipynb'
        with open(fname, 'w') as outfile:
            json.dump(notebook, outfile)

        loop = asyncio.get_event_loop()
        task = loop.create_task(grade_lab(fname, section, lab))
        grade = loop.run_until_complete(task)

        # remove file
        os.remove(fname)
        # return grade
        print(grade)
        self.write(str(grade))
        self.finish()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([(prefix, GoferHandler)])

    app.listen(10101)

    tornado.ioloop.IOLoop.current().start()
