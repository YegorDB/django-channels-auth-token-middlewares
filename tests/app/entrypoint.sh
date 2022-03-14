#!/bin/bash

# while true; do
#     sleep 60
# done

pip install -e /new_app/

python manage.py test
