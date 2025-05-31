#!/bin/bash

# while true; do
#     sleep 60
# done

pip install -e /new_app/ --root-user-action ignore

python manage.py test
