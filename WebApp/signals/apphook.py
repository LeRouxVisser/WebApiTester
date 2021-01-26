import sys
from django.urls import clear_url_caches

def debug_server_restart(**kwargs):
    if 'runserver' in sys.argv or 'server' in sys.argv:
        clear_url_caches()