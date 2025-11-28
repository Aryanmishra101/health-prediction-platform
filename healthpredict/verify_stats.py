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
    print(f"Total Assessments: {context.get('total_assessments')}")
    print(f"Active Users: {context.get('active_users')}")
    print(f"Prediction Accuracy: {context.get('prediction_accuracy')}")
    
    assert 'total_assessments' in context
    assert 'active_users' in context
    assert 'prediction_accuracy' in context
    
    print("\nVerification successful!")

if __name__ == "__main__":
    verify_stats()
