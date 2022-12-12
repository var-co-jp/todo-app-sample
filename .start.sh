#!/bin/sh

export FLASK_APP=app.py
python -m flask db init
python -m flask db stamp head
python -m flask db migrate -m 'db start'
python -m flask db upgrade

python app.py
