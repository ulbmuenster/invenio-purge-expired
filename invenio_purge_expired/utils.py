# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Helper functions."""

from arrow import now
from arrow.arrow import Arrow


def calculate_purge_date(period: int, base_date: Arrow = now()) -> tuple[Arrow, str]:
    """Calculate the expiration date for a given notification period."""
    purge_date = base_date.shift(days=period)
    return purge_date, purge_date.humanize(base_date)


def calculate_planned_purge_date(no_of_years: int, base_date: Arrow = now()) -> Arrow:
    """Calculate the expiration date for a given number of years."""
    planned_purge_date = base_date.shift(years=no_of_years)
    return planned_purge_date
