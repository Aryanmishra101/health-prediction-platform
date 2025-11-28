from decouple import config

database_url = config('DATABASE_URL', default=None)
print(f"DATABASE_URL from .env: {database_url}")
print(f"Has brackets: {'[' in database_url if database_url else 'N/A'}")
