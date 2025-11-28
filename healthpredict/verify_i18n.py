import os
import django
from django.conf import settings
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

def verify_i18n():
    print("Verifying i18n configuration...")
    
    # Check LANGUAGES
    print(f"Languages: {[l[0] for l in settings.LANGUAGES]}")
    assert 'hi' in [l[0] for l in settings.LANGUAGES]
    assert 'ja' in [l[0] for l in settings.LANGUAGES]
    assert 'zh-hans' in [l[0] for l in settings.LANGUAGES]
    assert 'ur' in [l[0] for l in settings.LANGUAGES]
    
    # Check Middleware
    assert 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE
    print("LocaleMiddleware found.")
    
    # Check URL
    try:
        url = reverse('set_language')
        print(f"set_language URL: {url}")
    except Exception as e:
        print(f"Error finding set_language URL: {e}")
        raise
        
    print("\nVerification successful! i18n is configured correctly.")

if __name__ == "__main__":
    verify_i18n()
