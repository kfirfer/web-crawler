# -*- coding: utf-8 -*-
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from webcrawler.util.util import Singleton


class Mailer(metaclass=Singleton):
    send_grid_client = None

    def __init__(self):
        self.send_grid_client = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    def send(self, from_mail, from_name, to_mail, _subject, mail_content, content_type="text/plain"):
        message = Mail(from_email=from_mail, subject=_subject, to_emails=to_mail, html_content=mail_content)
        response = self.send_grid_client.send(message)
        return response
