#!/bin/bash

pip install -U pip
pip install -r ./requirements.txt

export FLASK_APP=setup.py
python -m flask db init
python -m flask db stamp head
python -m flask db migrate -m 'db start'
python -m flask db upgrade

python setup.py
