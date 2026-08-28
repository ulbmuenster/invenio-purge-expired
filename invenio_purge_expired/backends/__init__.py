# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Notifications base backend module."""

from .email import EmailNotificationBackend

__all__ = ("EmailNotificationBackend",)
