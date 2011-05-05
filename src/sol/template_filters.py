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
from google.appengine.api import users

def contains(super_string, sub_string):
    """ True if sub_string is in super_string """
    import string
    if string.count(super_string, sub_string) is 0:
        return False
    return True

def create_url_auth(req_url):
    """ Creates the Google Account authentication URL """
    url_auth = users.create_login_url(req_url)
    if users.get_current_user():
      url_auth = users.create_logout_url(req_url)
    return url_auth

register = webapp.template.create_template_register()
register.filter(contains)
register.filter(create_url_auth)
webapp.template.register_template_library('sol.template_filters')
