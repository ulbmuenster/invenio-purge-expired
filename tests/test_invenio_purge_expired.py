# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 University of Münster.
#
# invenio-purge-expired is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_purge_expired import InvenioPurgeExpired


def test_version():
    """Test version import."""
    from invenio_purge_expired import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioPurgeExpired(app)
    assert "invenio-purge-expired" in app.extensions

    app = Flask("testapp")
    ext = InvenioPurgeExpired()
    assert "invenio-purge-expired" not in app.extensions
    ext.init_app(app)
    assert "invenio-purge-expired" in app.extensions
