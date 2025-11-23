"""
WSGI Configuration for PythonAnywhere Deployment

IMPORTANT: This file should be copied to your PythonAnywhere WSGI configuration file.
Do NOT replace your project's healthpredict/wsgi.py file with this.

Instructions:
1. On PythonAnywhere, go to the Web tab
2. Click on the WSGI configuration file link
3. Replace the contents with this file
4. Update the paths below with your PythonAnywhere username
"""

import os
import sys

# +++++++++++ CONFIGURATION +++++++++++
# Replace 'yourusername' with your actual PythonAnywhere username
username = 'yourusername'

# Path to your project directory (where manage.py is located)
project_home = f'/home/{username}/OKComputer_Django ML Health App Setup/healthpredict'

# Path to your virtual environment
virtualenv_path = f'/home/{username}/.virtualenvs/healthpredict-venv'

# +++++++++++ END CONFIGURATION +++++++++++

# Add your project directory to the sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add your project's parent directory to sys.path
project_parent = os.path.dirname(project_home)
if project_parent not in sys.path:
    sys.path.insert(0, project_parent)

# Activate your virtual environment
activate_this = os.path.join(virtualenv_path, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

# Set environment variable for Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'healthpredict.settings'

# Set environment variables (you can also set these in .env file)
# os.environ['SECRET_KEY'] = 'your-secret-key-here'
# os.environ['DEBUG'] = 'False'

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
