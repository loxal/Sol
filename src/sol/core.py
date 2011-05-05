# -*- coding: utf-8 -*-

# Copyright 2010 Alexander Orlov <alexander.orlov@loxal.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

import os
from sol import properties
class WebCmd(db.Model):
    webCmdId = db.IntegerProperty()
    shortcut = db.StringProperty()
    uri = db.LinkProperty()

class Main(webapp.RequestHandler):
    def displayTemplate(self, req):

        urlAuth = users.create_login_url(self.request.uri)
        if users.get_current_user():
          urlAuth = users.create_logout_url(self.request.uri)
          
        webCmds_query = db.Query(WebCmd)
        webCmds = webCmds_query.fetch(10)

        from datetime import datetime
        tplProperties = {
            'webCmds'           : webCmds,

            'resDir'            : properties.RES_DIR,
            'tplMain'           : properties.TPL_MAIN,
            'tplMainForService' : properties.TPL_MAIN_FOR_SERVICE,
            'author'            : properties.AUTHOR,
            'title'             : properties.TITLE,
            'titleDesc'         : properties.TITLE_DESC,

            'reqUrl'            : req.request.url,
            'urlAuth'           : urlAuth,
            'reqIp'             : req.request.remote_addr,
            'reqUserAgent'      : req.request.headers.get('User-Agent'),
            'dateNowYear'       : datetime.utcnow().year,
            'user'              : users.get_current_user(),
          }
        reqPath = req.request.path
        templatePath = properties.TPL_DIR + reqPath
        # handling: "Error: 404 Not Found"
        if not os.path.isfile(templatePath):
            templatePath = properties.TPL_DIR + properties.TPL_404_NOT_FOUND

        path = os.path.join(os.path.dirname(__file__), templatePath)
        req.response.out.write(template.render(path, tplProperties))

if __name__ == "__main__":
    print "Hello"

