# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test the functions in utils.py."""

import arrow

from invenio_purge_expired.utils import calculate_purge_date


def test_calculate_purge_date():
    """Test calculation of purge date."""
    base_date = arrow.get("2024-01-01 12:00:00", "YYYY-MM-DD HH:mm:ss")
    six_months_date, six_months_text = calculate_purge_date(182, base_date)
    assert six_months_date.format("YYYY-MM-DD") == "2024-07-01"
    assert six_months_text == "in 6 months"

    four_weeks_date, four_weeks_text = calculate_purge_date(28, base_date)
    assert four_weeks_date.format("YYYY-MM-DD") == "2024-01-29"
    assert four_weeks_text == "in 4 weeks"
