# PythonAnywhere Quick Reference

Quick commands and paths for deploying on PythonAnywhere.

## Initial Setup Commands

```bash
# Clone repository
git clone https://github.com/Aryanmishra101/health-prediction-platform.git
cd health-prediction-platform

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 healthpredict-venv

# Install dependencies
pip install -r requirements.txt

# Setup database
cd healthpredict
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Important Paths (Replace 'yourusername')

| Item | Path |
|------|------|
| Virtual Environment | `/home/yourusername/.virtualenvs/healthpredict-venv` |
| Project Directory | `/home/yourusername/health-prediction-platform/healthpredict` |
| Static Files | `/home/yourusername/health-prediction-platform/healthpredict/staticfiles` |
| Media Files | `/home/yourusername/health-prediction-platform/healthpredict/media` |
| WSGI File | `/var/www/yourusername_pythonanywhere_com_wsgi.py` |

## Static Files Configuration

In Web tab → Static files section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/health-prediction-platform/healthpredict/staticfiles` |
| `/media/` | `/home/yourusername/health-prediction-platform/healthpredict/media` |

## Update Workflow

```bash
# Pull latest changes
cd ~/health-prediction-platform
git pull origin main

# Run migrations (if models changed)
cd healthpredict
python manage.py migrate

# Collect static files (if CSS/JS changed)
python manage.py collectstatic --noinput

# Reload web app
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

## Environment Variables (.env file)

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=sqlite:///db.sqlite3
```

## Common Issues

| Problem | Solution |
|---------|----------|
| 500 Error | Check error log in Web tab |
| Static files not loading | Verify paths in Web tab, run collectstatic |
| Import errors | Activate virtualenv, install missing packages |
| Database errors | Run migrations, check permissions |

## Useful Commands

```bash
# Activate virtual environment
workon healthpredict-venv

# Check Django version
python -c "import django; print(django.get_version())"

# Test database connection
python manage.py dbshell

# Create new migrations
python manage.py makemigrations

# View logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Web App Configuration Checklist

- [ ] Virtual environment path set
- [ ] WSGI file configured with correct username
- [ ] Static files mapping added (`/static/`)
- [ ] Media files mapping added (`/media/`)
- [ ] ALLOWED_HOSTS updated in settings.py
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] Web app reloaded

## Your Application URLs

- **Main Site**: `https://yourusername.pythonanywhere.com`
- **Admin Panel**: `https://yourusername.pythonanywhere.com/admin`
- **Health Assessment**: `https://yourusername.pythonanywhere.com/predictor/assessment`

---

For detailed instructions, see [PYTHONANYWHERE_DEPLOYMENT.md](./PYTHONANYWHERE_DEPLOYMENT.md)
