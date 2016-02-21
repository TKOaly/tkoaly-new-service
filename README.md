Tekis Association Management System
===================================

Public-facing content management system for the purposes of a student
organization. Integrates with existing account management.

Uses Django 1.9.

Members app
-----------

Legacy members database integration.

The bundled "members.sqlite3" includes a database that looks like the
real thing, but with fake data. It is configured to be used by
default. It includes three users, `kayttaja` (user), `virkailija`
(officer) and `yllapitaja` (administrator) who all have the password
`abcabc`.

Flatpages app
-------------

Not to be confused with the Django bundled flatpages app, the
`tekis.flatpages` app provides internationalized flatpages that
organize into a preconfigured, two-level menu hierarchy.

Board app
---------

Structured storage, management and display of association board
members and officers.

Install
-------

1. Install project requirements with `pip install -U -r requirements.txt`
2. Migrate database with `python manage.py migrate`
3. Compile translations with `python manage.py compilemessages`
4. Finally, run the project with `python manage.py runserver`

Repeat these steps every time you update for smooth sailing. For
production deployment, also run `python manage.py collectstatic`.