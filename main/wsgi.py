# -*- coding: utf-8 -*-

import os
import sys
import platform

sys.path.insert(0, 'home/root/newsite/public_html/Dir')
sys.path.insert(0, 'home/root/newsite/public_html/Dir/main')
sys.path.insert(0, 'home/root/newsite/venv/lib/python3.8/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


