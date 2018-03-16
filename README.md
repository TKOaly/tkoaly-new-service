Tekis Association Management System
===================================

Public-facing content management system for the purposes of a student
organization. Integrates with existing account management.

Uses Django 1.10.

**Disclaimer**: This software is currently built with a branded theme
  for TKO-äly ry. No permission to impersonate the association is
  implied. Please replace the branding and contact information with
  your own if you wish to publish this application.

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

Using Docker
-------
1. `docker-compose build` to build the image (The image will have Ubuntu 16.04 and Python 2.7 installed). 
2. Use `docker ps` to find your container id. You will need it in the next step.
3. `docker exec -it <CONTAINER ID> python manage.py compilemessages` to compile messages
4. `docker exec -it <CONTAINER ID> python manage.py migrate` to migrate database
5. `docker-compose up -d` to start the server. The server defaults to port 8000. This can be changed in the Dockerfile.
6. To stop the container, use `docker-compose down`.