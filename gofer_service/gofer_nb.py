import aiohttp
import asyncio
import async_timeout
import base64
import json
import os
import time
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import tornado.options
from tempfile import NamedTemporaryFile
from grade_lab import grade_lab
from hashlib import sha1
from jupyterhub.services.auth import HubAuthenticated
from lxml import etree
from oauthlib.oauth1.rfc5849 import signature, parameters

prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')


class GoferHandler(HubAuthenticated, tornado.web.RequestHandler):

    async def get(self):
        self.write("This is a post only page. You probably shouldn't be here!")
        self.finish()

    async def post(self):
        """Accept notebook submissions, saves, then grades them"""
        user = self.get_current_user()
        req_data = tornado.escape.json_decode(self.request.body)
        # in the future, assignment should be metadata in notebook
        notebook = req_data['nb']
        section = notebook['metadata']['section']
        lab = notebook['metadata']['lab']

        # save notebook submission with user id and time stamp
        submission_file = "{}_{}_{}_{}.ipynb".format(user['name'], section, lab, str(time.time()))
        with open(submission_file, 'w') as outfile:
            json.dump(notebook, outfile)

        # Let user know their submission was received
        self.write("User submission has been received. Grade will be posted to the gradebook once it's finished running!")
        self.finish()

        # Grade lab
        grade = await grade_lab(submission_file, section, lab)

        # post grade to EdX
        with open('x19_config.json', 'r') as fname:
            # Course DEPENDENT configuration file
            # Should contain page for hitting the gradebook (outcomes_url)
            # as well as resource IDs for assignments
            # e.g. sourcedid['3']['lab02'] = c09d043b662b4b4b96fceacb1f4aa1c9
            # Make sure that it's placed in the working directory of the service (pwdx <PID>)
            course_config = json.load(fname)
        await post_grade(user['name'], grade, course_config["sourcedid"][section][lab], course_config["outcomes_url"])


async def post_grade(user_id, grade, sourcedid, outcomes_url):
    # TODO: extract this into a real library with real XML parsing
    # WARNING: You can use this only with data you trust! Beware, etc.
    post_xml = r"""
    <?xml version = "1.0" encoding = "UTF-8"?>
    <imsx_POXEnvelopeRequest xmlns = "http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
      <imsx_POXHeader>
        <imsx_POXRequestHeaderInfo>
          <imsx_version>V1.0</imsx_version>
          <imsx_messageIdentifier>999999123</imsx_messageIdentifier>
        </imsx_POXRequestHeaderInfo>
      </imsx_POXHeader>
      <imsx_POXBody>
        <replaceResultRequest>
          <resultRecord>
            <sourcedGUID>
              <sourcedId>{sourcedid}</sourcedId>
            </sourcedGUID>
            <result>
              <resultScore>
                <language>en</language>
                <textString>{grade}</textString>
              </resultScore>
            </result>
          </resultRecord>
        </replaceResultRequest>
      </imsx_POXBody>
    </imsx_POXEnvelopeRequest>
    """
    # Assumes these are read in from a config file in Jupyterhub
    consumer_key = os.environ['LTI_CONSUMER_KEY']
    consumer_secret = os.environ['LTI_CONSUMER_SECRET']
    sourcedid = "{}:{}".format(sourcedid, user_id)
    post_data = post_xml.format(grade=float(grade), sourcedid=sourcedid)

    # Yes, we do have to use sha1 :(
    body_hash_sha = sha1()
    body_hash_sha.update(post_data.encode('utf-8'))
    body_hash = base64.b64encode(body_hash_sha.digest()).decode('utf-8')
    args = {
        'oauth_body_hash': body_hash,
        'oauth_consumer_key': consumer_key,
        'oauth_timestamp': str(time.time()),
        'oauth_nonce': str(time.time())
    }

    base_string = signature.construct_base_string(
        'POST',
        signature.normalize_base_string_uri(outcomes_url),
        signature.normalize_parameters(
            signature.collect_parameters(body=args, headers={})
        )
    )

    oauth_signature = signature.sign_hmac_sha1(base_string, consumer_secret, None)
    args['oauth_signature'] = oauth_signature

    headers = parameters.prepare_headers(args, headers={
        'Content-Type': 'application/xml'
    })


    async with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.post(outcomes_url, data=post_data, headers=headers) as response:
                resp_text = await response.text()

                if response.status != 200:
                    raise GradePostException(response)

    response_tree = etree.fromstring(resp_text.encode('utf-8'))

    # XML and its namespaces. UBOOF!
    status_tree = response_tree.find('.//{http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0}imsx_statusInfo')
    code_major = status_tree.find('{http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0}imsx_codeMajor').text

    if code_major != 'success':
        raise GradePostException(response)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([(prefix, GoferHandler)])

    app.listen(10101)

    tornado.ioloop.IOLoop.current().start()
