# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""A module containing the tasks for purging expired records.."""

from .ext import InvenioPurgeExpired

__version__ = "0.2.6"

__all__ = ("__version__", "InvenioPurgeExpired")
