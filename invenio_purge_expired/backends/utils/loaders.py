# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Template loaders ."""

from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import current_app
from invenio_i18n import force_locale, get_locale
from invenio_i18n.proxies import current_i18n
from invenio_notifications.backends.utils import (
    JinjaTemplateLoaderMixin as BaseJinjaTemplateLoaderMixin,
)


def datetime_format(value: datetime | str, format: str = "%Y-%m-%d") -> str:
    """Formats date and time according to format string."""
    if type(value) is datetime:
        return value.strftime(format)
    date_value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    return date_value.strftime(format)


def datetime_delta(value, years=0, months=0, days=0, format="%Y-%m-%d"):
    """Calculates new date time and formats it."""
    if type(value) is datetime:
        date_value: datetime = value + relativedelta(
            years=years, months=months, days=days
        )
    else:
        date_value: datetime = datetime.strptime(
            value, "%Y-%m-%dT%H:%M:%S.%f%z"
        ) + relativedelta(years=years, months=months, days=days)
    return date_value.strftime(format)


def unit_calculator(value: int) -> str:
    """Calculates size units."""
    if value < 1000:
        return f"{value} Bytes"
    elif value < 1000 * 1000:
        return f"{value / 1000} Kb"
    elif value < (1000 * 1000 * 1000):
        return f"{value / (1000 * 1000)} Mb"
    elif value < (1000 * 1000 * 1000 * 1000):
        return f"{value / (1000 * 1000 * 1000)} Gb"
    elif value < (1000 * 1000 * 1000 * 1000 * 1000):
        return f"{value / (1000 * 1000 * 1000 * 1000)} Tb"
    elif value < (1000 * 1000 * 1000 * 1000 * 1000 * 1000):
        return f"{value / (1000 * 1000 * 1000 * 1000 * 1000)} Pb"
    elif value < (1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000):
        return f"{value / (1000 * 1000 * 1000 * 1000 * 1000 * 1000)} Eb"
    elif value < (1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000):
        return f"{value / (1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000)} Zb"
    return str(value)


class JinjaTemplateLoaderMixin(BaseJinjaTemplateLoaderMixin):
    """Used only in EmailNotificationBackend."""

    pdf_template_folder = "invenio_purge_expired"

    def render_template(self, notification, recipient):
        """Render template for a notification.

        Fetch the template based on the notification type and return the template blocks.
        More specific templates take precedence over less specific ones.
        Rendered template will also take the locale into account.
        """
        # Take recipient locale into account. Fallback to default locale (set via config variable)
        locale = recipient.data.get("preferences", {}).get("locale")
        if not current_i18n.is_locale_available(locale):
            locale = get_locale()

        current_app.jinja_env.filters["datetime_format"] = datetime_format
        current_app.jinja_env.filters["datetime_delta"] = datetime_delta
        template = current_app.jinja_env.select_template(
            [
                # Backend-specific templates first, e.g notifications/email/comment_edit.jinja
                f"{self.template_folder}/{self.id}/{notification.type}.{locale}.jinja",
                f"{self.template_folder}/{self.id}/{notification.type}.jinja",
                # Default templates, e.g notifications/comment_edit.jinja
                f"{self.template_folder}/{notification.type}.{locale}.jinja",
                f"{self.template_folder}/{notification.type}.jinja",
            ]
        )
        ctx = template.new_context(
            {
                "notification": notification,
                "recipient": recipient,
            },
        )

        # Forcing the locale of the recipient so the correct language is chosen for translatable strings
        with force_locale(locale):
            # "Force" rendering the whole template (including global variables).
            # Since we render block by block afterwards, the context and variables
            # would be lost between blocks.
            list(template.root_render_func(ctx))

            return {
                block: "".join(
                    block_func(ctx)
                )  # have to evaluate, as block_func is a generator
                for block, block_func in template.blocks.items()
            }
