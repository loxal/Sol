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

from google.appengine.api import mail
from sol import properties

class SendMail:
    """ responsible for mail communication """
    @staticmethod
    def send(page):
        """ send mail via main site contact form """
        ENCODING = 'utf-8'
        emailMessage = mail.EmailMessage()
        emailMessage.to = properties.MAIL_RECEIVER
        emailMessage.subject = properties.MAIL_RECEIVER
        sender = '"' + page.request.get('name').encode(ENCODING) + '" <' + page.request.get('sender').encode(ENCODING) + '>'
        emailMessage.sender = properties.MAIL_GAE_ACCOUNT
        emailMessage.body = page.request.get('body').encode(ENCODING) + '\n' + sender.encode(ENCODING)
        emailMessage.send()
