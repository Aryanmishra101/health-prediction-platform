# Install dependencies
pip install -r requirements.txt

# Run migrations (ensure DATABASE_URL is set in Vercel)
python3.9 healthpredict/manage.py migrate --noinput

# Collect static files
python3.9 healthpredict/manage.py collectstatic --noinput
