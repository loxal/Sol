#!/usr/bin/env python
#
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

# Google Code zip-build upload n/l/l/4
import os
import sys

class _Options:
  help = False

def _ParseArguments(args):
  cmd = None
  opt = _Options()
  arg = []

  for i in xrange(0, len(args)):
    a = args[i]
    if a == '-h' or a == '--help':
      opt.help = True

    elif not a.startswith('-'):
      cmd = a
      arg = args[i + 1:]
      break
  return cmd, opt, arg


def _Usage():
    print >>sys.stderr,\
        """usage: repo COMMAND [ARGS]

        repo is not yet installed.  Use "repo init" to install it here.

        The most commonly used repo commands are:

        init      Install repo in the current working directory
        help      Display detailed help on a command

        For access to the full online help, install repo ("repo init").
        """
    sys.exit(1)

def _Help(args):
  if args:
    if args[0] == 'init':
      init_optparse.print_help()
    else:
      print >>sys.stderr,\
      "error: '%s' is not a bootstrap command.\n"\
      '        For access to online help, install repo ("repo init").'\
      % args[0]
  else:
    _Usage()
  sys.exit(1)

def _NoCommands(cmd):
  print >>sys.stderr,\
"""error: command '%s' requires repo to be installed first.
       Use "repo init" to install it here.""" % cmd
  sys.exit(1)

import dev_admin_settings

#PATH_HOME = dev_admin_settings.PATH_HOME
#USER_NAME = dev_admin_settings.USER_NAME
#PATH_PRJ = dev_admin_settings.PATH_PRJ
#PATH_PRJ_BUILD = dev_admin_settings.PATH_PRJ_BUILD
#PATH_PRJ_SRC = dev_admin_settings.PATH_PRJ_SRC
#PATH_GAE = dev_admin_settings.PATH_GAE
#
#PATH_DEV_TOOL = dev_admin_settings.PATH_DEV_TOOL
#PATH_DJANGO_ADMIN_SCRIPT = dev_admin_settings.PATH_DJANGO_ADMIN_SCRIPT
#
#PWD_DIR = dev_admin_settings.PWD_DIR


class GAEext:

    @staticmethod
    def critical_operation_prompt():
        """ prevent the accidentally execution of critical operations """
        decision = raw_input('Precede operation (y/n): ')
        if not decision == 'y':
            print('Operation Aborted')
            sys.exit(0)

    @staticmethod
    def switch_debug_mode():
        """ to supress debug information """
        DEBUG_TRUE_MODE = 'DEBUG = True'
        DEBUG_FALSE_MODE = 'DEBUG = False'
        
        import re
        debugVar = re.compile(DEBUG_TRUE_MODE)
        
        releaseSensitiveFilePath = PATH_PRJ_SRC + '/sol/settings.py'
        releaseSensitiveFile = open(releaseSensitiveFilePath)
        releaseSensitiveFileContent = releaseSensitiveFile.read()
        
        if debugVar.match(releaseSensitiveFileContent):
            oldDebugMode = DEBUG_TRUE_MODE
            newDebugMode = DEBUG_FALSE_MODE
        else:
            oldDebugMode = DEBUG_FALSE_MODE
            newDebugMode = DEBUG_TRUE_MODE

        releaseSensitiveFileContentReplaced = re.sub(oldDebugMode, newDebugMode, releaseSensitiveFileContent)
        
        releaseSensitiveFile = open(releaseSensitiveFilePath, 'w')
        releaseSensitiveFile.write(releaseSensitiveFileContentReplaced)
        releaseSensitiveFile.close()

import subprocess

class GAEAdmin:
    """ GAE development related tasks """

    @staticmethod
    def selenium_run_tests():
        """ start Selenium Server for Unit Testing """

        args = (
                '-jar ',
                dev_admin_settings.PATH_SELENIUM_SERVER,
                )
        subprocess.call(['java', args], shell = True)

    @staticmethod
    def selenium_server_start():
        """ start Selenium Server for Unit Testing """

        args = (
                '-jar ',
                dev_admin_settings.PATH_SELENIUM_SERVER,
                )
        subprocess.call(['java', args], shell = True)

    @staticmethod
    def gae_run():
        """ start GAE dev_appserver """

        args = (
                ' --enable_sendmail ',
                ' --require_indexes ',
                dev_admin_settings.PATH_PRJ_SRC,
                )
        proc_return_value = subprocess.call([dev_admin_settings.PATH_GAE_DEV_APPSERVER, args], shell = True)
        return proc_return_value

    @staticmethod
    def gae_update():
        """ update the GAE app """
        
        GAEext().critical_operation_prompt()
        
        # switch DEBUG to False
        #GAEext().switch_debug_mode()
        
        password_file_descriptor = open('%s/loxal.key.txt' % dev_admin_settings.PWD_DIR)
        
#        args = (
#                ' --email=%s ' % dev_admin_settings.USER_NAME,
#                ' --no_cookies ',
#                '--passin ', # "passin" is necessary to supply the password via the "input" file
#                ' update ',
#                dev_admin_settings.PATH_PRJ_BUILD,
#                )
        os.system('%s/appcfg.py --email=%s --no_cookies update %s' % (dev_admin_settings.PATH_GAE, dev_admin_settings.USER_NAME, dev_admin_settings.PATH_PRJ_BUILD))
#        proc_return_value = subprocess.call(['%s/appcfg.py' % dev_admin_settings.PATH_GAE, args], shell = True, stdin = password_file_descriptor)
#        return proc_return_value
        
        #GAEext().switch_debug_mode() # switch DEBUG back to True

    # obsolete method
    @staticmethod
    def build():
        """
            create build
        """
        print os.getcwd()
        gae_admin().clean()
    
        os.mkdir(PATH_PRJ_BUILD)
        essentialElements = (
                         '/main.py', 
                         '/app.yaml', 
                         '/index.yaml',

                         '/canvas.html',
                         '/rpc_relay.html',
                         
                         '/locale', 
                         '/service', 
                         '/static', 
                         '/sol', 
                         '/templates', 
                        )
        for essentialElement in essentialElements:
            # symlink does not work on Windows
            os.symlink(PATH_PRJ_SRC + essentialElement, PATH_PRJ_BUILD + essentialElement)

    @staticmethod
    def clean():
      """
        clean the build destination
      """
      import shutil
      if os.path.exists(PATH_PRJ_BUILD):
          shutil.rmtree(PATH_PRJ_BUILD)

#    def zip_build(self):
#        taskForExternScriptWithParam = 'ant zip-build'
#        status = os.system(taskForExternScriptWithParam)

    @staticmethod
    def zip_build():
        import zipfile
#        solBuild = zipfile.ZipFile(PATH_HOME + 'konto-depot-uebertrag.pdf.zip', 'w')
#        solBuild.write(PATH_PRJ_BUILD + '/app.yaml')
#        solBuild.close()
        
        print PATH_HOME
        print PATH_PRJ_BUILD
        pass
        raw_input("ddte")

    @staticmethod
    def django_make_messages():
        # get generic translation keys
        CMD_DJANGO_DOMAIN = '%s makemessages -a' % PATH_DJANGO_ADMIN_SCRIPT
        # get translation keys from JavaScript files
        CMD_DJANGOJS_DOMAIN = '%s makemessages --domain=djangojs -a' % PATH_DJANGO_ADMIN_SCRIPT
                
        os.chdir(PATH_PRJ_SRC)
        os.system(CMD_DJANGO_DOMAIN)
        os.system(CMD_DJANGOJS_DOMAIN)
        
    @staticmethod
    def django_compile_messages():
        gae_admin().django_make_messages()
        
        os.chdir(PATH_PRJ_SRC)
        CMD = '%s compilemessages' % PATH_DJANGO_ADMIN_SCRIPT
        os.system(CMD)

    @staticmethod
    def zip_upload():
        # create a ZIPped build before uploading it
#        zip_build()

        gae_admin().critical_operation_prompt()
        
        PATH_DEV_TOOL_GOOGLECODE_UPLOAD = PATH_DEV_TOOL + '/support/scripts/googlecode_upload.py'
        ZIP_PATH_PRJ_BUILD = PATH_HOME + '/my/dev/prj/loxal/trunk/*.zip'
        
#        CMD = PATH_DEV_TOOL_GOOGLECODE_UPLOAD \
#            + ' --project=loxal --labels=Featured,GAE-ready --summary="sol build: GAE deployment ready" --user=' \
#            + USER_NAME \
#            + ' ' \
#            + ZIP_PATH_PRJ_BUILD
            
#        does this work? h/l-1
        CMD = '%s --project="loxal" --labels="Featured,GAE-ready" --summary="sol build: GAE deployment ready" --user=%s %s' \
            % (PATH_DEV_TOOL_GOOGLECODE_UPLOAD, USER_NAME, ZIP_PATH_PRJ_BUILD)
            
        # upload the ZIPped build
        os.system(CMD)
        
        # move this to zip_build() l/l-1
        # remove the old ZIPped build
#        os.system('rm ' + ZIP_PATH_PRJ_BUILD)

    @staticmethod
    def test():
        if os.getenv('SERVER_SOFTWARE'):
            DEBUG = True
        else:
            DEBUG = False
        print DEBUG
        print os.getenv('SERVER_SOFTWARE')
#        GAEext().critical_operation_prompt()
        print dev_admin_settings.PATH_PRJ
        print dev_admin_settings.app['PATH_APP']
        
def gae_admin(args):
    GAE_ADMIN_CLASS = 'GAEAdmin().'
    
    # mapping dict for faster task access
    shortcutMap = {
                   'b'      : 'build()',
                   'c'      : 'clean()',    
                   'dcm'    : 'django_compile_messages()',
                   'dmm'    : 'django_make_messages()',
                   'gr'     : 'gae_run()',
                   'sss'     : 'selenium_server_start()',
                   'gu'     : 'gae_update()',
                   'zb'     : 'zip_build()',
                   'zu'     : 'zip_upload()',
                   't'      : 'test()',
                   }
    
    taskName = args[0]
    
#    if shortcutMap.has_key(taskName):
    if taskName in shortcutMap:
        taskName = shortcutMap.get(taskName)
        task = GAE_ADMIN_CLASS + taskName
        eval(task)
        
def main(orig_args):
    cmd, opt, args = _ParseArguments(orig_args)
    gae_admin(orig_args)

if __name__ == '__main__':
    main(sys.argv[1:])
