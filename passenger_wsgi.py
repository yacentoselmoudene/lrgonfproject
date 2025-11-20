import os
import sys


import os
import sys

# 1) Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, "/home/lrsmfma/lrgonfproject")

# 2) Indiquer le module settings de ton projet Django
# 👉 remplace "lrgonfproject" ci-dessous par le nom réel défini dans manage.py
#    regarde dans manage.py la ligne :
#    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XXXX.settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lrgonfproject.settings")

# 3) Importer l'application WSGI Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
