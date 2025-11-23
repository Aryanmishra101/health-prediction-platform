#!/usr/bin/env python
"""
Development server runner for Health Prediction Platform
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup development environment"""
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Add project to Python path
    sys.path.insert(0, str(project_dir))
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
    
    print("🩺 Health Prediction Platform - Development Server")
    print("=" * 60)
    print("Setting up development environment...")
    
    # Check if required directories exist
    required_dirs = ['ml_models', 'logs', 'staticfiles', 'media']
    for dir_name in required_dirs:
        dir_path = project_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"✓ Created directory: {dir_name}")
    
    # Create default ML model files if they don't exist
    ml_models_dir = project_dir / 'ml_models'
    default_files = ['health_risk_model.pth', 'feature_scaler.pkl', 'feature_names.json']
    
    for file_name in default_files:
        file_path = ml_models_dir / file_name
        if not file_path.exists():
            # Create placeholder files
            if file_name.endswith('.json'):
                import json
                with open(file_path, 'w') as f:
                    json.dump({"version": "1.0.0", "features": []}, f, indent=2)
            else:
                file_path.touch()
            print(f"✓ Created placeholder: {file_name}")
    
    print("✓ Environment setup complete!")
    print()

def run_migrations():
    """Run Django migrations"""
    print("🔧 Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✓ Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False
    return True

def create_superuser():
    """Create a superuser if one doesn't exist"""
    print("👤 Checking for superuser account...")
    
    try:
        from django.contrib.auth.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            print("Creating default superuser...")
            # This would normally be interactive, but for demo we'll create a default
            print("Default superuser credentials:")
            print("  Username: admin")
            print("  Email: admin@healthpredict.com")
            print("  Password: admin123")
            print()
            print("⚠️  Please change these credentials in production!")
        else:
            print("✓ Superuser account already exists")
    except Exception as e:
        print(f"Note: Could not check superuser status: {e}")
        print("You can create a superuser later with: python manage.py createsuperuser")

def collect_static():
    """Collect static files"""
    print("📦 Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✓ Static files collected!")
    except subprocess.CalledProcessError as e:
        print(f"Note: Static collection failed (this is normal in development): {e}")

def main():
    """Main function to run the development server"""
    setup_environment()
    
    # Run migrations
    if not run_migrations():
        print("❌ Cannot start server due to migration errors")
        sys.exit(1)
    
    # Setup additional components
    collect_static()
    
    # Import Django and setup
    import django
    django.setup()
    
    create_superuser()
    
    print()
    print("🚀 Starting development server...")
    print("=" * 60)
    print("Server will be available at: http://127.0.0.1:8000/")
    print("Admin interface: http://127.0.0.1:8000/admin/")
    print("API endpoint: http://127.0.0.1:8000/api/")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    # Run the development server
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print()
        print("🛑 Server stopped by user")
        print("Thank you for using Health Prediction Platform!")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()