from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMultiAlternatives
from sendgrid.helpers.mail import (
    Mail,
    Content,
    From,
    To,
    Email,
    PlainTextContent,
    HtmlContent,
    TemplateId,
)
from sendgrid import SendGridAPIClient
import os
from django.conf import settings
import json

class SendGridDjangoEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently
        self.sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

    def open(self):
        print("Open connection??")
        """
        Open a network connection.

        This method can be overwritten by backend implementations to
        open a network connection.

        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.

        This method can be called by applications to force a single
        network connection to be used when sending mails. See the
        send_messages() method of the SMTP backend for a reference
        implementation.

        The default implementation does nothing.
        """
        pass

    def close(self):
        print("Close connection??")
        """Close a network connection."""
        pass

    def __enter__(self):
        try:
            self.open()
        except Exception:
            self.close()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def send_messages(self, email_messages: list):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """

        total_send = []
        for m in email_messages:
            total_send.append(self.send_message(m))

        return total_send.count(True)

    def send_message(self, message: EmailMultiAlternatives):
        text_body = message.body
        html_body = message.body

        if message.alternatives.__len__():
            msg = message.alternatives[0]
            html_body = msg[0]

        email = Mail(
            from_email=Email(f"{settings.DEFAULT_FROM_EMAIL}"),
            to_emails=message.to,
        )
        email.template_id = "d-fe78993596fd4bbcb7716fc89e924af1"

        email.dynamic_template_data = {
            "titulo_da_mensagem": message.subject,
            "corpo_da_mensagem": html_body,
        }
        try:
            print("d-fe78993596fd4bbcb7716fc89e924af1")
            print("d-3028a99ca80348f295374393a06015d0")
            response = self.sg.send(email)
        except Exception as e:
            print(e.__repr__())
            print(dir(e))
            print("erro ao requisitar")
            return False
        else:
            return True
