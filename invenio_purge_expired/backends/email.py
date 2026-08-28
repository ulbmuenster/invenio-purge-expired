# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""E-mail notification backend."""

from base64 import b64encode

from flask import current_app
from invenio_mail.tasks import send_email
from invenio_notifications.backends.base import NotificationBackend
from marshmallow_utils.html import strip_html

from .utils import JinjaTemplateLoaderMixin


class EmailNotificationBackend(NotificationBackend, JinjaTemplateLoaderMixin):
    """E-mail with pdf-attachment specific notification backend."""

    id = "email_with_pdf"

    def send(self, notification, recipient, cc=None):
        """Mail sending implementation."""
        content = self.render_template(notification, recipient)

        message = {
            "subject": content["subject"],
            #                "html": content["html_body"],
            "body": strip_html(content["plain_body"]),
            "recipients": [
                recipient.data.get("email") or recipient.data.get("email_hidden")
            ],
            "sender": current_app.config["MAIL_DEFAULT_SENDER"],
            "reply_to": current_app.config["MAIL_DEFAULT_REPLY_TO"],
        }
        if cc:
            message["cc"] = cc
        resp = send_email(message)
        return resp
