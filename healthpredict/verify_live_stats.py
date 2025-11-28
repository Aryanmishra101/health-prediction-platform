import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

def verify_live_stats():
    client = Client()
    
    # 1. Get initial stats
    print("Fetching initial stats...")
    response = client.get('/api/stats/')
    assert response.status_code == 200
    initial_data = response.json()
    initial_users = initial_data['active_users']
    print(f"Initial active users: {initial_users}")
    
    # 2. Create a new user
    print("Creating a new user...")
    new_user = User.objects.create_user(username='test_live_stats_user', password='password123')
    
    # 3. Get stats again
    print("Fetching updated stats...")
    response = client.get('/api/stats/')
    assert response.status_code == 200
    updated_data = response.json()
    updated_users = updated_data['active_users']
    print(f"Updated active users: {updated_users}")
    
    # 4. Verify increase
    assert updated_users == initial_users + 1
    print("Verification successful! User count increased.")
    
    # Cleanup
    new_user.delete()

if __name__ == "__main__":
    verify_live_stats()
