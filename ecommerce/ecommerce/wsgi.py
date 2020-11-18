"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
=======
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
