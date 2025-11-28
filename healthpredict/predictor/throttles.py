"""
Custom throttle classes for ML prediction endpoints
"""
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class PredictionRateThrottle(UserRateThrottle):
    """
    Rate limiting specifically for ML prediction endpoints
    Limits authenticated users to 100 predictions per hour
    """
    scope = 'prediction'
    rate = '100/hour'


class AnonPredictionRateThrottle(AnonRateThrottle):
    """
    Rate limiting for anonymous prediction requests
    Limits anonymous users to 20 predictions per hour
    """
    scope = 'anon_prediction'
    rate = '20/hour'
