# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""A module containing the tasks for purging expired records."""

"""
        To add the tasks to the Celery Beat schedule the following should be added
        to invenio.cfg:

        from celery.schedules import crontab
        from invenio_app_rdm.config import CELERY_BEAT_SCHEDULE

        CELERY_BEAT_SCHEDULE["notify_expiration"] = {
            "task": "invenio_purge_expired.tasks.notify_on_expiration",
            "schedule": crontab(**app.config["PURGE_EXPIRED_CRONTAB_SETTINGS"]),
        }
        CELERY_BEAT_SCHEDULE["purge_expired"] = {
            "task": "invenio_purge_expired.tasks.purge_expired_records",
            "schedule": crontab(**app.config["PURGE_EXPIRED_CRONTAB_SETTINGS"]),
        }
"""

PURGE_EXPIRED_CRONTAB_SETTINGS = {"minute": "1", "hour": "0"}
"""Default crontab settings for schedule beat (every midnight)."""

PURGE_EXPIRED_PRELIMINARY_INFORMATION_PERIOD = 180
"""Default period of days for preliminary information about purging of record."""

PURGE_EXPIRED_CUSTOM_FIELD = "planned_purge_date"
"""Custom field key that holds the planned purge date of a record."""

PURGE_EXPIRED_MIN_YEARS = 10
"""Guaranteed minimum storage period in years."""

PURGE_EXPIRED_MAX_YEARS = 15
"""Allowed maximum storage period in years."""

PURGE_EXPIRED_MIGRATED_IDENTIFIER_PREFIXES = ()
"""Identifier prefixes marking a record as migrated from another system.

Records with an identifier starting with one of these prefixes may keep a
planned purge date shorter than the guaranteed minimum period, e.g. when the
original creation date of the data cannot be determined."""
