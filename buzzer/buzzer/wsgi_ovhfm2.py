"""
WSGI config for buzzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os,sys,site


sys.path.append('/var/www/buzzer/buzzer')
sys.path.append('/var/www/buzzer/env_buzzer/lib/python3.5/site-packages')

from django.core.wsgi import get_wsgi_application
#from whitenoise import 	WhiteNoise
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buzzer.settings_ovhfm2")

application = get_wsgi_application()
#application = DjangoWhiteNoise(application)
#application = WhiteNoise(application, root='/var/www/snapnews/appcomm/static/')
