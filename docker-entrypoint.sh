#!/bin/sh

# Create db
python3 -c "from tldrhn import db; db.create_all()"

# Initial cache
python3 -c "from tldrhn import summarize; summarize.main()"

# Start server
uwsgi --ini tldrhn/uwsgi.ini
