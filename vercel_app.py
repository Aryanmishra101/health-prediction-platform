import os
import sys

# Add the project directory to the sys.path
# The project structure is:
# root/
#   healthpredict/ (contains manage.py)
#     healthpredict/ (contains settings.py)
#
# We need to add 'healthpredict' (the outer one) to sys.path so that
# 'healthpredict.settings' can be imported.

path = os.path.join(os.path.dirname(__file__), 'healthpredict')
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
