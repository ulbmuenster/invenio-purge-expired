..
    Copyright (C) 2024-2026 University of Münster.

    invenio-purge-expired is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version 0.2.6 (released 2025-08-15)

- Fix additional check to permit a purge date of less than 10 years for migrated records

Version 0.2.5 (released 2025-08-14)

- add additional check to permit a purge date of less than 10 years for migrated records

Version 0.2.4 (released 2025-05-15)

- add additional checks for custom planned purge dates set via API

Version 0.2.3 (released 2025-01-07)

- fixed dependencies to work with `uv` tooling and Flask3 in the future

Version 0.2.2 (released 2024-12-18)

- reimplement the check of planned_purge_date to better handle migrated records

Version 0.2.1 (released 2024-12-16)

- add check for missing custom field and add it correct

Version 0.2.0 (released 2024-12-12)

- new component added to guarantee correct setting of planned_purge_date

Version 0.1.4

- add meaningful return values to jobs

Version 0.1.0 (released TBD)

- Initial public release.
