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

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from django.conf import settings
#settings.LANGUAGE_CODE = self.request.headers.get('Accept-Language')
#settings.LANGUAGE_CODE = 'ru'
#settings._target = None
#settings.configure('ru')

import os
from sol import properties
from sol import settings # : where to place? to place where it is needed exclusively [l/l/l]
from sol import sendmail
class Default(webapp.RequestHandler):
    # : extract this and all related parts as an extra service l/n-8
    def post(self):
        if self.request.get('body'):
            sendmail.SendMail().send(self)
        Default.get(self)

    def get(self):
        import sol.template_filters
        from datetime import datetime
        template_properties = {
            'properties'                : properties.template,
            
            'req_url'                   : self.request.url,
            'user'                      : users.get_current_user(),
            
            'ip'                        : self.request.remote_addr,
            'user_agent'                : self.request.headers.get('User-Agent'),
            'browser_accept_language'   : self.request.headers.get('Accept-Language'),

            # : extract this and all related parts as an extra service l/n-8
            'send_mail'                 : self.request.get('send'),
            'mail_sender'               : self.request.get('sender'),
            'mail_name'                 : self.request.get('name'),
            'mail_body'                 : self.request.get('body'),
          }

        req_path = self.request.path
        # handling: entry page "exclusion"
        if self.request.path is '/':
            req_path = '/home.html'

        templatePath = properties.TPL_DIR + req_path
        # handling: "Error: 404 Not Found"
        if not os.path.isfile(templatePath):
            templatePath = properties.TPL_DIR + properties.TPL_404_NOT_FOUND

        path = os.path.join(os.path.dirname(__file__), templatePath)
        self.response.out.write(template.render(path, template_properties))

def main():
#    app = django.core.handlers.wsgi.WSGIHandler([
    app = webapp.WSGIApplication([
                                  ('.*', Default),
                              ], debug = settings.DEBUG)
    # : check which app call is faster l/l-4 > via GAE Web Admin Console
#    run_wsgi_app(app)
#    wsgiref.handlers.CGIHandler().run(app)
    util.run_wsgi_app(app)

if __name__ == '__main__':
  main()