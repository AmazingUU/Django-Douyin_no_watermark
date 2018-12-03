"""
WSGI config for download_no_watermark project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

#import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "download_no_watermark.settings")

#path = '/var/www/html/download_no_watermark'
#if path not in sys.path:
#    sys.path.append(path)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'download_no_watermark.settings'

application = get_wsgi_application()
