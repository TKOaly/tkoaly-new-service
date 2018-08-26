#!/bin/sh
docker run -p 8080:5000 --env-file=.env -v db.sqlite3:/db.sqlite3 -v members.sqlite3:/members.sqlite3 -v public:/public --name tkoaly-new-service-container tkoaly-new-service