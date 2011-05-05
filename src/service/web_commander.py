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

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from sol import settings
from google.appengine.api import mail

#from django.conf import settings
##settings.LANGUAGE_CODE = self.request.headers.get('Accept-Language')
#settings._target = None
#settings.LANGUAGE_CODE = 'de'

#from django.conf import settings
#import random
#i = random.choice(['de', 'ru', 'en-us', 'es', 'pt'])
##os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#
#settings.configure(LANGUAGE_CODE = i)

class Caching():
    
    @staticmethod
    def flush_public_web_cmd_cache(cmds):
        DELETE_SUCCESSFUL = 2
        web_cmd_objs_delete_result = memcache.delete_multi(cmds, 0, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_PUBLIC_CMD)
        cmds_delete_result = memcache.delete(WEB_CMDS_MEMCACHE_KEY + IS_PUBLIC_CMD)
        if web_cmd_objs_delete_result and cmds_delete_result is DELETE_SUCCESSFUL:
            return True
        return False

    @staticmethod
    def flush_user_web_cmd_cache(cmds):
        user = users.get_current_user()
        DELETE_SUCCESSFUL = 2
        web_cmd_objs_delete_result = memcache.delete_multi(cmds, 0, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_USER_CMD + str(user) + '_')
        cmds_delete_result = memcache.delete(WEB_CMDS_MEMCACHE_KEY + IS_USER_CMD + str(user) + '_')
        if web_cmd_objs_delete_result and cmds_delete_result is DELETE_SUCCESSFUL:
            return True
        return False
    
    @staticmethod
    def reset_public_web_cmd_cache(web_cmds):
        web_cmd_objs = {}
        cmds = []
        for web_cmd in web_cmds:
            web_cmd_objs[web_cmd.cmd] = web_cmd
            cmds.append(web_cmd.cmd)
        Caching().flush_public_web_cmd_cache(cmds)
        memcache_add_web_cmd_objs_result = memcache.add_multi(web_cmd_objs, 0, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_PUBLIC_CMD)
        memcache_add_web_cmds_result = memcache.add(WEB_CMDS_MEMCACHE_KEY + IS_PUBLIC_CMD, cmds, 0)
        if memcache_add_web_cmds_result and len(memcache_add_web_cmd_objs_result) is 0:
            web_cmd_objs_memcached = memcache.get_multi(cmds, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_PUBLIC_CMD)
            return web_cmd_objs_memcached

    @staticmethod
    def reset_user_web_cmd_cache(web_cmds):
        user = users.get_current_user()
        web_cmd_objs = {}
        cmds = []
        for web_cmd in web_cmds:
            web_cmd_objs[web_cmd.cmd] = web_cmd
            cmds.append(web_cmd.cmd)
        Caching().flush_user_web_cmd_cache(cmds)
        memcache_add_web_cmd_objs_result = memcache.add_multi(web_cmd_objs, 0, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_USER_CMD + str(user) + '_')
        memcache_add_web_cmds_result = memcache.add(WEB_CMDS_MEMCACHE_KEY + IS_USER_CMD + str(user) + '_', cmds, 0)
        if memcache_add_web_cmds_result and len(memcache_add_web_cmd_objs_result) is 0:
            web_cmd_objs_memcached = memcache.get_multi(cmds, WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_USER_CMD + str(user) + '_')
            return web_cmd_objs_memcached

import urllib
class Exec(webapp.RequestHandler):
    
    def get(self):
        DEFAULT_QUERY_URL = 'http://www.google.com/search?q='
        QUERY_DELIMITER = ' '
        # WORKAROUND (API bug): self.request.get(QUERY_DELIMITER) was broken and stripped all special signs in Firefox
        request_query = urllib.unquote_plus(urllib.splitvalue(self.request.query)[1]).split(QUERY_DELIMITER)
        cmd = request_query[0]
        # FIX: if cmd contains special signs, the UnicodeDecodeError exception is issued

        user = users.get_current_user()
        if user is None:
            web_cmd_from_mc = memcache.get(WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_PUBLIC_CMD + cmd)
        else:
            web_cmd_from_mc = memcache.get(WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX + IS_USER_CMD + str(user) + '_' + cmd)

        if web_cmd_from_mc is None:
            # Web Command is not in the cache
            if user is None:
                web_cmd_from_db = WebCmd().get_public_web_cmd(cmd)
            else:
                web_cmd_from_db = WebCmd().get_user_web_cmd(cmd)
                
            if web_cmd_from_db is None:
                # default fallback Web Command
                query_url = DEFAULT_QUERY_URL
                cmd_query = request_query
            else:
                # if Web Command exists but is not in the cache
                if user is None:
                    web_cmds = WebCmd().get_public_web_cmds()
                    Caching().reset_public_web_cmd_cache(web_cmds)
                else:
                    web_cmds = WebCmd().get_user_web_cmds()
                    Caching().reset_user_web_cmd_cache(web_cmds)
                query_url = web_cmd_from_db.url
                cmd_query = request_query[1:]
        else:
            query_url = web_cmd_from_mc.url
            cmd_query = request_query[1:]
#        self.redirect(query_url + str.join(QUERY_DELIMITER, cmd_query))
        self.redirect(query_url + urllib.quote(str.join(QUERY_DELIMITER, cmd_query)))



class WebCmd(db.Model):
    """ definition of the Web Command model """
    name = db.StringProperty()
    cmd = db.StringProperty()
    url = db.LinkProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    updated = db.DateTimeProperty(auto_now = True)
    is_public = db.BooleanProperty(default = users.is_current_user_admin()) # : see also create method (fix DOUBLE check)
    owner = db.UserProperty(auto_current_user_add = True)

    @staticmethod
    def is_key_owner(key):
        ''' check current user the owner of the Web Command '''
        web_cmd = db.get(key)
        if web_cmd.owner == users.get_current_user():
            return True

    @staticmethod
    def get_public_web_cmds():
        ''' get all public web commands '''
        web_cmds = WebCmd.all().filter(IS_PUBLIC, True).order(SERVICE_URL_QUERY).fetch(99)
        return web_cmds

    @staticmethod
    def get_public_web_cmd(cmd):
        ''' get a certain public web command '''
        web_cmd = WebCmd.all().filter(IS_PUBLIC, True).filter(SERVICE_URL_QUERY, cmd).get()
        return web_cmd

    @staticmethod
    def is_public_web_cmd(web_cmd):
        ''' True if a web command is already available to the public '''
        web_cmd_cmd = WebCmd.all().filter(IS_PUBLIC, True).filter(SERVICE_URL_QUERY, web_cmd.cmd).get()
        web_cmd_name = WebCmd.all().filter(IS_PUBLIC, True).filter('name', web_cmd.name).get()
        web_cmd_url = WebCmd.all().filter(IS_PUBLIC, True).filter('url', web_cmd.url).get()
        if web_cmd_cmd is not None or web_cmd_name is not None or web_cmd_url is not None:
            return True
    
    @staticmethod
    def get_user_web_cmds():
        ''' get all web commands of the current user '''
        web_cmds = WebCmd.all().filter('owner', users.get_current_user()).order(SERVICE_URL_QUERY).fetch(99)
        return web_cmds

    @staticmethod
    def get_user_web_cmd(cmd):
        ''' get a certain web command of the current user '''
        web_cmd = WebCmd.all().filter('owner', users.get_current_user()).filter(SERVICE_URL_QUERY, cmd).get()
        return web_cmd
    
    @staticmethod
    def create_initial_user_web_cmd_set():
        ''' copy all public web commands to the initially created user '''
        public_web_cmds = WebCmd.all().filter(IS_PUBLIC, True).fetch(99)
        user_web_cmds = []
        for public_web_cmd in public_web_cmds:
            user_web_cmd = WebCmd()
            user_web_cmd.cmd = public_web_cmd.cmd
            user_web_cmd.name = public_web_cmd.name
            user_web_cmd.url = public_web_cmd.url
            user_web_cmd.is_public = False
            user_web_cmd.owner = users.get_current_user()
            user_web_cmds.append(user_web_cmd)
        db.put(user_web_cmds)

    @staticmethod
    def is_initial_user_login():
        ''' check if there is any web command assigned to the current user '''
        is_any_user_web_cmd = WebCmd.all().filter('owner', users.get_current_user()).get()
        if is_any_user_web_cmd is None:
            return True

class Delete(webapp.RequestHandler):
    
    def get(self):
        key = self.request.get('key')
        if WebCmd().is_key_owner(key):
            cmd = db.get(key).cmd
            self.redirect('?key=%s&cmd=%s&confirm_delete=.' % (key, cmd))
        else:
            self.redirect(SERVICE_PATH)
        
    def post(self):
        is_confirmed = self.request.get('ok')
        key = self.request.get('key')
        if is_confirmed and WebCmd().is_key_owner(key):
            cmd = db.get(key).cmd
            db.delete(key)
            self.redirect('%s?cmd=%s&info_success=.' % (SERVICE_PATH, cmd))
        else:
            self.redirect(SERVICE_PATH)

class Suggest(webapp.RequestHandler):

    def get(self):
        ''' suggest a command to public via email '''
        web_cmd = db.get(self.request.get('key'))
        if WebCmd().is_key_owner(web_cmd.key()) and not WebCmd().is_public_web_cmd(web_cmd):
            Suggest().send_suggestion(web_cmd)
            self.redirect('%s?info_success=.' % SERVICE_PATH)
        else:
            self.redirect('%s?info_warning=.' % SERVICE_PATH)

    @staticmethod
    def send_suggestion(web_cmd):
        ''' send web command suggestion via email '''
        msg = mail.EmailMessage()
        msg.to = properties.MAIL_RECEIVER
        subject = _('sol Notification: Web Commander - Suggestion')
        msg.subject = subject.encode(ENCODING)
        sender = '"' + str(users.get_current_user().nickname()) + '" <' + str(users.get_current_user().email()) + '>'
        msg.sender = properties.MAIL_GAE_ACCOUNT
        body = '''
            user: \t%s\n
            key: \t%s
            cmd: \t%s
            name: \t%s
            url: \t%s
        ''' % (sender, web_cmd.key(), web_cmd.cmd, web_cmd.name, web_cmd.url)
        msg.body = body.encode(ENCODING)
        if msg.is_initialized():
#            send_mail_to_admins(sender, subject, body, **kw)
            msg.send()

class Edit(webapp.RequestHandler):
    @staticmethod
    def edit_cmd(key, name, url):
        web_cmd = db.get(key)
        web_cmd.name = name
        web_cmd.url = url
        db.put(web_cmd)
        
    def post(self):
        is_ok = self.request.get('ok')
        key = self.request.get('key')
        if is_ok and WebCmd().is_key_owner(key):
            Edit().edit_cmd(key, self.request.get('name'), self.request.get('url'))
        self.redirect(SERVICE_PATH)

class Create(webapp.RequestHandler):

    @staticmethod
    def is_user_admin():
        if users.get_current_user().email() == 'alexander.orlov@loxal.net':
            return True
        else:
            return False

    @staticmethod
    def create(cmd, name, url):
        """ create a new web command"""
        web_cmd = WebCmd()
        web_cmd.name = name
        web_cmd.cmd = cmd
        web_cmd.url = url
#        web_cmd.is_public = users.is_current_user_admin()
        web_cmd.is_public = Create().is_user_admin()
        web_cmd.put()

    def post(self):
        cmd = self.request.get('cmd')
        name = self.request.get('name')
        url = self.request.get('url').encode(ENCODING)
        
        is_cmd = WebCmd().get_user_web_cmd(cmd)
        if is_cmd is None:
            Create().create(cmd, name, url)
            self.redirect(SERVICE_PATH)
        else:
            if self.request.get('action.edit'):
                Edit().edit_cmd(is_cmd.key(), name, url)
                self.redirect(SERVICE_PATH)
            else:
                self.redirect(SERVICE_PATH + '?key=%s&cmd=%s&name=%s&url=%s&edit=.' % (is_cmd.key(), cmd, name, url))

import os
from sol import properties
from google.appengine.ext import webapp
class Default(webapp.RequestHandler):
    
    def get(self):
        if users.get_current_user():
            if WebCmd().is_initial_user_login():
                WebCmd().create_initial_user_web_cmd_set()
            web_cmds = WebCmd.get_user_web_cmds()
        else:
            web_cmds = WebCmd.get_public_web_cmds()

        from sol import template_filters
        from datetime import datetime
        template_properties = {
            'properties'        : properties.template,
            
            'web_cmds'          : web_cmds,
            'is_cmd'            : self.request.get('is_cmd'),
            'key'               : self.request.get('key'),
            'cmd'               : self.request.get('cmd').encode(ENCODING),
            'name'              : self.request.get('name'),
            'url'               : self.request.get('url'),
            'confirm_delete'    : self.request.get('confirm_delete'),
            'info_success'      : self.request.get('info_success'),
            'info_warning'      : self.request.get('info_warning'),
            'edit'              : self.request.get('edit'),
            'edit_instant'      : self.request.get('edit_instant'),
            'service_path'      : SERVICE_PATH,
#            'service_url'       : 'http://%s%s%s?%s=' % (self.request.headers.get('Host'), SERVICE_PATH, SERVICE_URL_SUFFIX, SERVICE_URL_QUERY),

            'user_agent'        : self.request.headers.get('User-Agent'),
            'req_url'           : self.request.url,
            'user'              : users.get_current_user(),

            'is_user_admin'     : users.is_current_user_admin(),
          }

        req_path = self.request.path
        # handling: entry page "exclusion"
        if self.request.path.endswith('/'):
            req_path = SERVICE_PATH
        template_path = properties.TPL_DIR + req_path + '.html'
        # handling: "Error: 404 Not Found"
        if not os.path.isfile(template_path):
            template_path = properties.TPL_DIR + properties.TPL_404_NOT_FOUND

        path = os.path.join(os.path.dirname(__file__), template_path)
        self.response.out.write(template.render(path, template_properties))

ENCODING = 'utf-8'
SERVICE_PATH = '/service/web-commander'
SERVICE_URL_SUFFIX = '/exec'
SERVICE_URL_QUERY = 'cmd'

WEB_CMD_OBJS_MEMCACHE_KEY_PREFIX = 'web_cmds_objs_'
WEB_CMDS_MEMCACHE_KEY = 'web_cmds'

IS_PUBLIC_CMD = 'is_public_cmd_'
IS_USER_CMD = 'is_user_cmd_'
IS_PUBLIC = 'is_public'

def main():
    app = webapp.WSGIApplication([
                                    (SERVICE_PATH + '/create', Create),
                                    (SERVICE_PATH + '/delete', Delete),
                                    (SERVICE_PATH + '/edit', Edit),
                                    (SERVICE_PATH + '/suggest', Suggest),
                                    (SERVICE_PATH + SERVICE_URL_SUFFIX, Exec),
                                    ('.*', Default),
                                ], debug = settings.DEBUG)
    util.run_wsgi_app(app)

if __name__ == '__main__':
  main()
