import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

from django.test import RequestFactory
from predictor.views import HomeView

def verify_stats():
    factory = RequestFactory()
    request = factory.get('/')
    view = HomeView()
    view.setup(request)
    
    context = view.get_context_data()
    
    print("Verifying HomeView context statistics:")
    print(f"Prediction Accuracy: {context.get('prediction_accuracy')}")
    
    assert context.get('prediction_accuracy') == 91
    
    print("\nVerification successful! Accuracy is updated to 91%.")

if __name__ == "__main__":
    verify_stats()
