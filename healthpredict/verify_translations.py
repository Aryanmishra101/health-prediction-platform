import os
import django
from django.utils import translation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

def verify_translations():
    print("Verifying translations...")
    
    # Test strings
    test_strings = [
        "Home",
        "About",
        "Health Prediction Platform",
        "Heart Disease"
    ]
    
    languages = {
        'hi': "Hindi",
        'ja': "Japanese",
        'zh-hans': "Simplified Chinese",
        'ur': "Urdu"
    }
    
    for lang_code, lang_name in languages.items():
        print(f"\nTesting {lang_name} ({lang_code})...")
        translation.activate(lang_code)
        
        for s in test_strings:
            translated = translation.gettext(s)
            print(f"  '{s}' -> '{translated}'")
            
            # Check if translation is different from source (basic check)
            # Note: If translation is missing, it returns source
            if translated == s:
                print(f"  [WARNING] Translation missing for '{s}' in {lang_name}")
            else:
                print(f"  [OK] Translation found")
                
    translation.deactivate()

if __name__ == "__main__":
    verify_translations()
