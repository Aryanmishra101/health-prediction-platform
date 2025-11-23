"""
Views for the dashboard app
Analytics and reporting views
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
import json
import logging

from predictor.models import HealthAssessment, PredictionResult, PatientProfile

logger = logging.getLogger(__name__)

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Main analytics dashboard"""
    template_name = 'dashboard/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date range (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Basic statistics
        total_assessments = HealthAssessment.objects.count()
        recent_assessments = HealthAssessment.objects.filter(assessment_date__gte=start_date).count()
        total_patients = PatientProfile.objects.count()
        
        # Risk distribution
        risk_stats = self._get_risk_statistics()
        
        # Recent activity
        recent_activity = HealthAssessment.objects.select_related('patient', 'patient__user').order_by('-assessment_date')[:10]
        
        context.update({
            'title': 'Analytics Dashboard',
            'total_assessments': total_assessments,
            'recent_assessments': recent_assessments,
            'total_patients': total_patients,
            'risk_stats': risk_stats,
            'recent_activity': recent_activity,
        })
        
        return context
    
    def _get_risk_statistics(self):
        """Get risk statistics across all assessments"""
        
        # Get all prediction results
        predictions = PredictionResult.objects.all()
        
        if not predictions.exists():
            return {
                'heart_disease': {'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0},
                'diabetes': {'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0},
                'cancer': {'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0},
                'stroke': {'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0},
            }
        
        # Count risk categories
        heart_disease_stats = predictions.values('heart_disease_category').annotate(count=Count('heart_disease_category'))
        diabetes_stats = predictions.values('diabetes_category').annotate(count=Count('diabetes_category'))
        cancer_stats = predictions.values('cancer_category').annotate(count=Count('cancer_category'))
        stroke_stats = predictions.values('stroke_category').annotate(count=Count('stroke_category'))
        
        def format_stats(stats):
            result = {'low': 0, 'moderate': 0, 'high': 0, 'very_high': 0}
            for stat in stats:
                category = stat['heart_disease_category'] if 'heart_disease_category' in stat else \
                          stat['diabetes_category'] if 'diabetes_category' in stat else \
                          stat['cancer_category'] if 'cancer_category' in stat else \
                          stat['stroke_category']
                result[category] = stat['count']
            return result
        
        return {
            'heart_disease': format_stats(heart_disease_stats),
            'diabetes': format_stats(diabetes_stats),
            'cancer': format_stats(cancer_stats),
            'stroke': format_stats(stroke_stats),
        }

@staff_member_required
def analytics_data_view(request):
    """API endpoint for analytics data"""
    
    try:
        # Get time range parameter
        days = int(request.GET.get('days', 30))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Assessment trends
        assessments_by_day = HealthAssessment.objects.filter(
            assessment_date__gte=start_date
        ).extra(
            select={'day': 'date(assessment_date)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        # Risk distribution over time
        predictions = PredictionResult.objects.filter(
            prediction_date__gte=start_date
        )
        
        # Average risk scores
        avg_risks = predictions.aggregate(
            heart_disease=Avg('heart_disease_risk'),
            diabetes=Avg('diabetes_risk'),
            cancer=Avg('cancer_risk'),
            stroke=Avg('stroke_risk')
        )
        
        # Age group distribution
        age_groups = PatientProfile.objects.raw("""
            SELECT 
                CASE 
                    WHEN age < 30 THEN '18-29'
                    WHEN age < 40 THEN '30-39'
                    WHEN age < 50 THEN '40-49'
                    WHEN age < 60 THEN '50-59'
                    WHEN age < 70 THEN '60-69'
                    ELSE '70+'
                END as age_group,
                COUNT(*) as count
            FROM (
                SELECT 
                    id,
                    EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) as age
                FROM predictor_patientprofile
            ) as ages
            GROUP BY age_group
            ORDER BY age_group
        """)
        
        age_distribution = {group.age_group: group.count for group in age_groups}
        
        data = {
            'assessment_trends': list(assessments_by_day),
            'average_risks': avg_risks,
            'age_distribution': age_distribution,
            'total_assessments': HealthAssessment.objects.count(),
            'total_patients': PatientProfile.objects.count(),
            'high_risk_patients': PredictionResult.objects.filter(
                Q(heart_disease_risk__gte=75) |
                Q(diabetes_risk__gte=75) |
                Q(cancer_risk__gte=75) |
                Q(stroke_risk__gte=75)
            ).count()
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"Analytics data error: {e}")
        return JsonResponse({'error': 'Failed to fetch analytics data'}, status=500)

@staff_member_required
def risk_distribution_view(request):
    """Get risk distribution data"""
    
    try:
        condition = request.GET.get('condition', 'heart_disease')
        
        if condition not in ['heart_disease', 'diabetes', 'cancer', 'stroke']:
            return JsonResponse({'error': 'Invalid condition'}, status=400)
        
        # Get risk score ranges
        field_name = f'{condition}_risk'
        category_field = f'{condition}_category'
        
        predictions = PredictionResult.objects.all()
        
        # Risk score distribution
        risk_ranges = {
            '0-19': predictions.filter(**{field_name + '__lt': 20}).count(),
            '20-39': predictions.filter(**{field_name + '__gte': 20, field_name + '__lt': 40}).count(),
            '40-59': predictions.filter(**{field_name + '__gte': 40, field_name + '__lt': 60}).count(),
            '60-79': predictions.filter(**{field_name + '__gte': 60, field_name + '__lt': 80}).count(),
            '80-100': predictions.filter(**{field_name + '__gte': 80}).count(),
        }
        
        # Risk category distribution
        category_stats = predictions.values(category_field).annotate(count=Count(category_field))
        
        categories = {}
        for stat in category_stats:
            category = stat[category_field]
            if category:
                categories[category] = stat['count']
        
        data = {
            'risk_ranges': risk_ranges,
            'categories': categories,
            'condition': condition
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"Risk distribution error: {e}")
        return JsonResponse({'error': 'Failed to fetch risk distribution'}, status=500)

class ReportsView(LoginRequiredMixin, TemplateView):
    """Reports and insights view"""
    template_name = 'dashboard/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get patient-specific reports if not staff
        if not self.request.user.is_staff:
            try:
                patient_profile = self.request.user.patientprofile
                assessments = HealthAssessment.objects.filter(patient=patient_profile)
                
                # Risk progression over time
                risk_progression = []
                for assessment in assessments.order_by('assessment_date'):
                    try:
                        prediction = assessment.predictionresult
                        risk_progression.append({
                            'date': assessment.assessment_date.strftime('%Y-%m-%d'),
                            'heart_disease': prediction.heart_disease_risk,
                            'diabetes': prediction.diabetes_risk,
                            'cancer': prediction.cancer_risk,
                            'stroke': prediction.stroke_risk,
                        })
                    except:
                        continue
                
                context.update({
                    'risk_progression': risk_progression,
                    'total_assessments': assessments.count(),
                })
                
            except PatientProfile.DoesNotExist:
                pass
        
        context['title'] = 'Health Reports'
        return context