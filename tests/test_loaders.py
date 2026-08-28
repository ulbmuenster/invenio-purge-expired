# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test utility functions for Jinja templates."""

import arrow

from invenio_purge_expired.backends.utils.loaders import (
    datetime_delta,
    datetime_format,
    unit_calculator,
)


def test_datetime_delta_format():
    """Test datetime delta function."""
    base_date = arrow.get("2024-01-01 12:00:00", "YYYY-MM-DD HH:mm:ss").datetime
    result = datetime_delta(base_date, 1, 1, 1)
    assert result == "2025-02-02"

    result = datetime_delta(base_date, 1, 1, 1, format="%d.%m.%Y")
    assert result == "02.02.2025"


def test_datetime_format():
    """Test datetime format function."""
    base_date = arrow.get("2024-01-01 12:00:00", "YYYY-MM-DD HH:mm:ss").datetime
    result = datetime_format(base_date)
    assert result == "2024-01-01"

    result = datetime_format(base_date, format="%d.%m.%Y")
    assert result == "01.01.2024"


def test_unit_calculator():
    """Test unit_calculator function."""
    assert unit_calculator(950) == "950 Bytes"
    assert unit_calculator(1012) == "1.012 Kb"
    assert unit_calculator(5321003) == "5.321003 Mb"
    assert unit_calculator(5321003000) == "5.321003 Gb"
    assert unit_calculator(7321003000000) == "7.321003 Tb"
    assert unit_calculator(9300865421003000) == "9.300865421003 Pb"
    assert unit_calculator(11321003000000000000) == "11.321003 Eb"
    assert unit_calculator(501321003000000000000000) == "501.321003 Zb"
    assert unit_calculator(501321003000000000000000000) == "501321003000000000000000000"
