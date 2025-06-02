#!/bin/bash

# Configura o ambiente
export DJANGO_SETTINGS_MODULE=config.settings.production

# Cria o superuser
python manage.py create_superuser 