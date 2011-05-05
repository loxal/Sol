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

import os

sol = {
        'USER_NAME' : 'alexander.orlov@loxal.net',
        'PATH_APP'  : '/my/dev/prj/loxal/trunk/sol',
}

bm_supplier_com = {
        'USER_NAME' : 'alexander.orlov@bm-supplier.com',
        'PATH_APP'  : '/my/dev/prj/com/bm-supplier.com',
}

app = sol
#app = bm_supplier_com

#USER_NAME = 'alexander.orlov@loxal.net'
#USER_NAME = 'alexander.orlov@bm-supplier.com'
USER_NAME = app['USER_NAME']

PATH_HOME = os.getenv('HOME')
PATH_PRJ = PATH_HOME + app['PATH_APP']
#PATH_PRJ = PATH_HOME + '/my/dev/prj/loxal/trunk/sol'
#PATH_PRJ = PATH_HOME + '/my/dev/prj/loxal/com/bm-supplier.com'
PATH_PRJ_BUILD = PATH_PRJ + '/src'
PATH_PRJ_SRC = PATH_PRJ + '/src'
PATH_PRJ_LIB = PATH_PRJ + '/lib'

PATH_DEV_ENV = PATH_HOME + '/my/dev/sdk'
PATH_SELENIUM_SERVER = PATH_PRJ_LIB + '/selenium/selenium-server/selenium-server.jar'
PATH_GAE = PATH_DEV_ENV + '/appengine.py'
PATH_GAE_DEV_APPSERVER = PATH_GAE + '/dev_appserver.py'
PATH_DEV_TOOL = PATH_HOME + '/my/dev/tool'
PATH_DJANGO_ADMIN_SCRIPT = PATH_DEV_TOOL + '/django-admin.py'

PWD_DIR = PATH_HOME + '/my/etc'