#!/bin/bash

# while true; do
#     sleep 60
# done

pip install -e /new_app/ --root-user-action ignore --use-pep517

python manage.py test
