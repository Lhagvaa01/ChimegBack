"""
WSGI config for ChimegBack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChimegBack.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    with open('/tmp/wsgi_error.log', 'w') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
    raise
