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

def getBrowserDetails(userAgent):
   result = {}
   # Regexp for most used "User-Agent"s built using "http://www.useragentstring.com/"
   browsersRegexps = [
                      ['Internet Explorer', 'MSIE (\S+)'],
                      ['Opera', 'Opera[ /](\S+)'],
                      ['Konqueror', 'KHTML/(\S+)'],
                      ['Firefox', 'Gecko/\S+ Firefox/(\S+)'],
                      ['Chrome','AppleWebKit/\S+ (KHTML, like Gecko) Chrome/(\S+) Safari/\S+'],
                      ['Safari', 'Version/\S+ Safari/(\S+)'],
                      ['Mozilla', 'Gecko/(\S+)'],
                      ['WebKit', 'AppleWebKit/(\S+)']
                     ]

   # Search for the Browser that matches, if any
   for browser in browsersRegexps:
      compiledRegexp = re.compile( browser[1] )
      searchResult = compiledRegexp.search( userAgent )

      if (searchResult):
         result['browser_name'] = browser[0]
         result['browser_version'] = searchResult.group(1)
         return result

   # If nothing matches, return "unknown"
   result['browser_name'] = "unknown"
   result['browser_version'] = "unknown"
   return result

from hashlib import sha1
class Etc:
    def fetchContent(self, url):
        try:
            fetchResult = urlfetch.fetch(url)
        except:
            return 'Exception: Not an URL'
        if fetchResult.status_code == 200:
            encTypeRaw = fetchResult.headers['content-type']
            encStartIdx = encTypeRaw.find('=')
            encType = encTypeRaw[encStartIdx + 1:]
            fetchResultContent = fetchResult.content
            return fetchResultContent.decode(encType)
        return 'Warning: URL could not be retrieved successfully'
    
    def getChkSum(self, url):
        try:
            fetchResult = urlfetch.fetch(url)
        except:
            return 'Exception: Not an URL'
        if fetchResult.status_code == 200:
          chkSum = sha1()
          chkSum.update(fetchResult.content)
          return chkSum.hexdigest()
        return 'Warning: URL could not be retrieved successfully'
