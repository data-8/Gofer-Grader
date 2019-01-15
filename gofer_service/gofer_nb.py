import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import tornado.options
import os
import json
import asyncio
from tempfile import NamedTemporaryFile
from grade_lab import grade_lab

from jupyterhub.services.auth import HubAuthenticated

prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')


class GoferHandler(HubAuthenticated, tornado.web.RequestHandler):

    async def get(self):
        self.write("This is a post only page. You probably shouldn't be here!")
        self.finish()

    async def post(self):
        """For grading submission, accept json notebook of submission"""
        if not self.current_user:
            self.get_current_user()
        req_data = tornado.escape.json_decode(self.request.body)
        # in the future, assignment should be metadata in notebook
        notebook = req_data['nb']
        section = notebook['metadata']['section']
        lab = notebook['metadata']['lab']

        # save notebook to temporary file
        tempfile = NamedTemporaryFile('w', delete=False)
        json.dump(notebook, tempfile)
        tempfile.close()

        grade = await grade_lab(tempfile.name, section, lab)

        # remove file
        os.remove(tempfile.name)
        # return grade
        print(section, lab, grade)
        self.write(str(grade))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([(prefix, GoferHandler)])

    app.listen(10101)

    tornado.ioloop.IOLoop.current().start()
