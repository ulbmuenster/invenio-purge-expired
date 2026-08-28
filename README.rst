..
    Copyright (C) 2024-2026 University of Münster.

    invenio-purge-expired is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

=======================
 invenio-purge-expired
=======================

A module containing the tasks for purging expired records.

Module will check on each publish of a record (no matter if via API or web) if the planned purge date set by the user
is within the allowed range from the guaranteed minimum to the allowed maximum storage period (by default 10 to 15
years from creation date of the earliest version) and corrects it if it isn't. Celery tasks notify record owners
before the planned purge date and purge expired records.

Configuration
-------------

The module can be configured via the following variables in ``invenio.cfg``:

- ``PURGE_EXPIRED_CUSTOM_FIELD``: custom field key that holds the planned
  purge date (default: ``planned_purge_date``).
- ``PURGE_EXPIRED_MIN_YEARS`` / ``PURGE_EXPIRED_MAX_YEARS``: guaranteed
  minimum and allowed maximum storage period in years (defaults: ``10`` / ``15``).
- ``PURGE_EXPIRED_MIGRATED_IDENTIFIER_PREFIXES``: identifier prefixes marking
  a record as migrated from another system. Such records may keep a planned
  purge date shorter than the guaranteed minimum period (default: empty).

Authors
-------

- University of Münster <forschungsdaten@uni-muenster.de>

Disclaimer
----------

This project is not an official Invenio module. It is neither maintained by nor
affiliated with CERN or the Invenio collaboration.

The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.
