# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Setting the planned purge date."""

import sys

from arrow import get, now
from flask import current_app
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import RecordCommitOp

from ..utils import calculate_planned_purge_date


class PlannedPurgeComponent(ServiceComponent):
    """Service component to set the planned purge date properly."""

    def publish(self, identity, draft=None, record=None):
        """Set the planned purge date properly."""
        custom_field = current_app.config["PURGE_EXPIRED_CUSTOM_FIELD"]
        min_years = current_app.config["PURGE_EXPIRED_MIN_YEARS"]
        max_years = current_app.config["PURGE_EXPIRED_MAX_YEARS"]
        migrated_prefixes = current_app.config[
            "PURGE_EXPIRED_MIGRATED_IDENTIFIER_PREFIXES"
        ]

        # Get the record service to access version information
        rdm_record_service = current_service_registry.get("records")

        # Search for all versions of the current record
        versions = rdm_record_service.search_versions(
            identity, str(record.pid.pid_value)
        )

        # Initialize variables for tracking the earliest version
        min_index = sys.maxsize
        base_date = now()  # Default to the current date if no versions found

        # Iterate over all versions to find the earliest created date
        for hit in versions.hits:
            index = hit["versions"]["index"]  # Get version index
            if index < min_index:
                min_index = index
                base_date = get(
                    hit["created"]
                )  # Set base_date to earliest created date

        # base_date is either today's date or the earliest created date if more than one version exists

        # Calculate the allowed purge date limits from the base date
        min_purge_date = calculate_planned_purge_date(min_years, base_date)
        max_purge_date = calculate_planned_purge_date(max_years, base_date)
        today = now()

        # Check if the record already has a planned purge date set
        if (
            record.custom_fields is not None
            and custom_field in record.custom_fields
            and record.custom_fields[custom_field] is not None
        ):
            # Retrieve the current planned purge date from custom fields
            planned_purge_date = get(record.custom_fields[custom_field])

            # If the current purge date is later than the allowed maximum, set it to the maximum
            if planned_purge_date > max_purge_date:
                record.custom_fields[custom_field] = max_purge_date.format(
                    "YYYY-MM-DD"
                )

            # Records migrated from another system (identifier matching one of
            # the configured prefixes) may keep a purge date earlier than the
            # guaranteed minimum period
            is_migrated = False
            try:
                identifier = record.metadata["identifiers"][0]["identifier"]
                is_migrated = any(
                    identifier.startswith(prefix) for prefix in migrated_prefixes
                )
            except (IndexError, KeyError):
                pass

            # If the current purge date is earlier than the guaranteed minimum
            # period, set it to the minimum period
            if planned_purge_date < min_purge_date and not is_migrated:
                record.custom_fields[custom_field] = min_purge_date.format(
                    "YYYY-MM-DD"
                )

            # If the current purge date is in the past, reset it to the minimum period
            if planned_purge_date <= today:
                record.custom_fields[custom_field] = min_purge_date.format(
                    "YYYY-MM-DD"
                )

        else:
            # If no planned purge date exists, set it to the guaranteed minimum
            # period or, if this is already in the past, to the maximum period
            if min_purge_date > today:
                record.custom_fields = {
                    custom_field: min_purge_date.format("YYYY-MM-DD"),
                }
            else:
                record.custom_fields = {
                    custom_field: max_purge_date.format("YYYY-MM-DD"),
                }

        # Register the record for commit operation to save changes
        self.uow.register(RecordCommitOp(record))
