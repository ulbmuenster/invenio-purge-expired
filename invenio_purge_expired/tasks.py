# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""A module containing the tasks for purging expired records."""

from datetime import date
from typing import Dict

from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_notifications.models import Notification, Recipient
from invenio_records_resources.proxies import current_service_registry
from invenio_users_resources.proxies import current_users_service

from .backends import EmailNotificationBackend
from .utils import calculate_purge_date


@shared_task(ignore_result=True)
def notify_on_expiration() -> Dict[str, str]:
    """Notify users about expiration of records."""
    preliminary_period = current_app.config[
        "PURGE_EXPIRED_PRELIMINARY_INFORMATION_PERIOD"
    ]
    planned_purge_date, purge_date_humanized = calculate_purge_date(preliminary_period)
    custom_field = current_app.config["PURGE_EXPIRED_CUSTOM_FIELD"].replace(":", r"\:")
    record_service = current_service_registry.get("records")
    search_results = record_service.search(
        identity=system_identity,
        q=f"custom_fields.{custom_field}:{planned_purge_date.format('YYYY-MM-DD')}",
    )
    results = {
        "planned_purge_date": planned_purge_date.strftime("%Y-%m-%d"),
        "total_hits": str(len(list(search_results.hits))),
    }
    planned_purge_year = planned_purge_date.year

    users_service = current_users_service
    extended_period = 0
    sent_mails = 0
    informed_owners = []
    for hit in search_results.hits:
        publication_date = hit["metadata"]["publication_date"]
        publication_year = int(publication_date[:4])
        if planned_purge_year - publication_year > 10:
            """The guaranteed period has already been extended once, so do nothing."""
            extended_period = extended_period + 1
        else:
            """Send a notification mail."""
            access = hit["parent"]["access"]
            owner_id = access["owned_by"]["user"]
            user = users_service.read(system_identity, owner_id)
            recipient = Recipient(data=user.data)
            informed_owners.append(user["email"])
            granted_users = []
            if "grants" in access:
                if "grants" in access:
                    for grant in access["grants"]:
                        if grant["subject"]["type"] == "user":
                            granted_user = users_service.read(
                                system_identity, grant["subject"]["id"]
                            )
                            granted_users.append(granted_user["email"])
            context = {
                "request": {
                    "receiver": {
                        "access": {
                            "visibility": "restricted",
                        },
                    },
                    "created_by": user.data,
                    "topic": hit,
                    "planned_period": purge_date_humanized,
                },
            }
            notification = Notification(type="notify-on-expiration", context=context)
            email = EmailNotificationBackend()
            email.send(notification=notification, recipient=recipient, cc=granted_users)
            sent_mails = sent_mails + 1

    results["extended_period"] = str(extended_period)
    results["sent_mails"] = str(sent_mails)
    results["informed_owners"] = ", ".join(informed_owners)
    return results


@shared_task(ignore_result=True)
def purge_expired_records() -> Dict[str, str]:
    """Purge expired records."""
    planned_purge_date = date.today()
    custom_field = current_app.config["PURGE_EXPIRED_CUSTOM_FIELD"].replace(":", r"\:")
    record_service = current_service_registry.get("records")
    search_results = record_service.search(
        identity=system_identity,
        q=f"custom_fields.{custom_field}:{planned_purge_date.strftime('%Y-%m-%d')}",
    )
    results = {"expired_records": str(len(list(search_results.hits)))}

    deleted_records = []
    problems_with_deletion = []
    for hit in search_results.hits:
        record_deleted = record_service.delete(system_identity, hit["id"])
        if record_deleted:
            deleted_records.append(hit["id"])
        else:
            problems_with_deletion.append(hit["id"])

    results["deleted_records"] = ", ".join(deleted_records)
    results["problems_with_deletion"] = ", ".join(problems_with_deletion)
    return results
