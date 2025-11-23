# PythonAnywhere Deployment Guide

Complete guide to deploy the Django ML Health Prediction Platform on PythonAnywhere.

## Prerequisites

- A PythonAnywhere account (free tier is sufficient)
- Your project code pushed to GitHub
- Basic familiarity with command line

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account

1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Verify your email address

### 2. Clone Your Repository

1. On PythonAnywhere, click on **"Consoles"** tab
2. Start a new **Bash console**
3. Clone your repository:

```bash
git clone https://github.com/Aryanmishra101/health-prediction-platform.git
cd health-prediction-platform
```

> [!NOTE]
> If your repository is private, you'll need to set up SSH keys or use a personal access token.

### 3. Create Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 healthpredict-venv

# The virtual environment will be automatically activated
# You should see (healthpredict-venv) in your prompt
```

### 4. Install Dependencies

```bash
# Navigate to the project directory if not already there
cd ~/health-prediction-platform

# Install all required packages
pip install -r requirements.txt
```

> [!IMPORTANT]
> This may take several minutes. Some packages like numpy, pandas, and scikit-learn are large.

### 5. Set Up Environment Variables

Create a `.env` file in the healthpredict directory:

```bash
cd healthpredict
nano .env
```

Add the following (replace with your actual values):

```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=sqlite:///db.sqlite3
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

> [!TIP]
> Generate a secure SECRET_KEY using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 6. Run Database Migrations

```bash
# Make sure you're in the healthpredict directory (where manage.py is)
cd ~/health-prediction-platform/healthpredict

# Run migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Collect Static Files

```bash
# Still in the healthpredict directory
python manage.py collectstatic --noinput
```

This collects all static files (CSS, JavaScript, images) into the `staticfiles` directory.

### 8. Configure Web App

1. Go to the **"Web"** tab on PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Click **"Next"** (for the domain name)
4. Select **"Manual configuration"** (NOT "Django")
5. Choose **Python 3.10**
6. Click **"Next"**

### 9. Configure Virtual Environment

On the Web app configuration page:

1. Scroll to the **"Virtualenv"** section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/healthpredict-venv
   ```
   (Replace `yourusername` with your actual PythonAnywhere username)
3. Click the checkmark to save

### 10. Configure WSGI File

1. On the Web app configuration page, find the **"Code"** section
2. Click on the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all the existing content**
4. Copy the contents from `pythonanywhere_wsgi.py` in your project
5. **Update the username** in the file:
   - Replace `'yourusername'` with your actual PythonAnywhere username
6. Click **"Save"** (top right)

The WSGI file should look like this (with your username):

```python
import os
import sys

# Replace 'yourusername' with your actual PythonAnywhere username
username = 'yourusername'

# Path to your project directory (where manage.py is located)
project_home = f'/home/{username}/health-prediction-platform/healthpredict'

# Path to your virtual environment
virtualenv_path = f'/home/{username}/.virtualenvs/healthpredict-venv'

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

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 11. Configure Static Files

On the Web app configuration page, scroll to the **"Static files"** section:

1. Click **"Enter URL"** and add:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/health-prediction-platform/healthpredict/staticfiles`
   
2. Click the checkmark to save

3. Add another entry for media files:
   - **URL:** `/media/`
   - **Directory:** `/home/yourusername/health-prediction-platform/healthpredict/media`

> [!IMPORTANT]
> Replace `yourusername` with your actual PythonAnywhere username in both paths.

### 12. Update ALLOWED_HOSTS

1. Go back to your Bash console
2. Edit settings.py:

```bash
cd ~/health-prediction-platform/healthpredict/healthpredict
nano settings.py
```

3. Find the `ALLOWED_HOSTS` line and update it:

```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
```

4. Save the file (`Ctrl+X`, `Y`, `Enter`)

### 13. Reload Your Web App

1. Go back to the **"Web"** tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button
3. Wait a few seconds for the reload to complete

### 14. Test Your Application

1. Click on the link at the top of the Web tab: `https://yourusername.pythonanywhere.com`
2. Your Django application should now be live! 🎉

## Troubleshooting

### Application Not Loading

1. Check the **Error log** on the Web tab
2. Check the **Server log** on the Web tab
3. Common issues:
   - Wrong paths in WSGI file
   - Virtual environment not activated
   - Missing dependencies

### Static Files Not Loading

1. Verify the static files paths in the Web tab
2. Run `python manage.py collectstatic` again
3. Check that `STATIC_ROOT` in settings.py matches the path in Web tab

### Database Errors

1. Make sure migrations were run: `python manage.py migrate`
2. Check that the database file has correct permissions
3. For SQLite, ensure the directory is writable

### Import Errors

1. Activate your virtual environment: `workon healthpredict-venv`
2. Install missing packages: `pip install package-name`
3. Reload the web app

## Updating Your Application

When you make changes to your code:

```bash
# In your Bash console
cd ~/health-prediction-platform
git pull origin main

# If you changed models
cd healthpredict
python manage.py migrate

# If you changed static files
python manage.py collectstatic --noinput

# Reload the web app (or use the Web tab button)
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

## Free Tier Limitations

PythonAnywhere's free tier includes:

- ✅ One web app at your-username.pythonanywhere.com
- ✅ 512MB disk space
- ✅ Limited CPU time per day
- ✅ SQLite database (MySQL available on paid plans)
- ❌ No HTTPS for custom domains (available on paid plans)
- ❌ No outbound internet access from web app (available on paid plans)

> [!NOTE]
> The free tier is perfect for development, testing, and small projects. For production use with custom domains and more resources, consider upgrading to a paid plan ($5/month).

## Next Steps

1. **Access Admin Panel**: Visit `https://yourusername.pythonanywhere.com/admin` and log in with your superuser credentials
2. **Test ML Models**: Try the health prediction features
3. **Monitor Logs**: Check the error and server logs regularly
4. **Set Up Backups**: Regularly backup your database and media files

## Support

- PythonAnywhere Help: [https://help.pythonanywhere.com](https://help.pythonanywhere.com)
- PythonAnywhere Forums: [https://www.pythonanywhere.com/forums](https://www.pythonanywhere.com/forums)
- Django Documentation: [https://docs.djangoproject.com](https://docs.djangoproject.com)

---

**Congratulations!** Your Django ML Health Prediction Platform is now deployed on PythonAnywhere! 🚀
