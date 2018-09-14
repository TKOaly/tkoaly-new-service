#!/bin/sh
docker run --rm -i -d -p 8080:5000 --env-file=.env -v tekis-website-db:/db.sqlite3 -v tekis-website-public:/public --name tkoaly-new-service-container tkoaly-new-service