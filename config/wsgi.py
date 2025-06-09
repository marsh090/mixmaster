"""
WSGI config for mixmaster project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings for Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Create the WSGI application
application = get_wsgi_application()

# Vercel needs the variable to be named 'app'
app = application 