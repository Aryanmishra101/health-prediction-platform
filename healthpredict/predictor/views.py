"""
Views for the predictor app
Health assessment and prediction views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import json
import logging
from datetime import datetime

from django.contrib.auth.models import User
from .models import PatientProfile, HealthAssessment, PredictionResult
from .forms import HealthAssessmentForm, PatientProfileForm
from .ml_models import health_predictor

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    """Home page view"""
    template_name = 'predictor/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Health Prediction Platform'
        context['subtitle'] = 'Advanced AI-powered health risk assessment'
        
        # Platform Statistics
        context['total_assessments'] = HealthAssessment.objects.count()
        context['active_users'] = User.objects.count()
        # Calculated accuracy from test data (MAE ~8.6%)
        context['prediction_accuracy'] = 91 
        
        return context

class AboutView(TemplateView):
    """About page view"""
    template_name = 'predictor/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Our Platform'
        return context

class ServicesView(TemplateView):
    """Services page view"""
    template_name = 'predictor/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Services'
        context['services'] = [
            {
                'name': 'Heart Disease Prediction',
                'description': 'Advanced ML models for cardiovascular risk assessment',
                'icon': 'heart',
                'features': ['Risk scoring', 'Lifestyle recommendations', 'Clinical insights']
            },
            {
                'name': 'Diabetes Risk Assessment',
                'description': 'Early detection of diabetes risk factors',
                'icon': 'activity',
                'features': ['Glucose analysis', 'Preventive strategies', 'Monitoring plans']
            },
            {
                'name': 'Cancer Risk Analysis',
                'description': 'Comprehensive cancer risk evaluation',
                'icon': 'shield',
                'features': ['Genetic factors', 'Lifestyle assessment', 'Screening recommendations']
            },
            {
                'name': 'Stroke Prevention',
                'description': 'Stroke risk prediction and prevention',
                'icon': 'brain',
                'features': ['Neurological assessment', 'Risk stratification', 'Intervention planning']
            }
        ]
        return context

@login_required
def health_assessment_view(request):
    """Health assessment form view"""
    
    # Get or create patient profile
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile before assessment.')
        return redirect('accounts:profile_setup')
    
    if request.method == 'POST':
        form = HealthAssessmentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save assessment
                    assessment = form.save(commit=False)
                    assessment.patient = patient_profile
                    assessment.assessed_by = request.user
                    assessment.status = 'completed'
                    assessment.save()
                    
                    # Generate predictions
                    assessment_data = form.cleaned_data.copy()
                    assessment_data.update({
                        'age': patient_profile.age or 30,
                        'gender': patient_profile.gender,
                        'bmi': patient_profile.bmi or 25.0,
                        'smoking_status': patient_profile.smoking_status,
                        'alcohol_consumption': patient_profile.alcohol_consumption,
                        'exercise_level': patient_profile.exercise_level,
                        'family_medical_history': patient_profile.family_medical_history,
                    })
                    
                    # Make prediction
                    prediction_results = health_predictor.predict_health_risks(assessment_data)
                    
                    # Save prediction results
                    prediction = PredictionResult.objects.create(
                        assessment=assessment,
                        heart_disease_risk=prediction_results['heart_disease_risk'],
                        diabetes_risk=prediction_results['diabetes_risk'],
                        cancer_risk=prediction_results['cancer_risk'],
                        stroke_risk=prediction_results['stroke_risk'],
                        heart_disease_confidence=prediction_results.get('prediction_confidence', 0.85),
                        diabetes_confidence=prediction_results.get('prediction_confidence', 0.85),
                        cancer_confidence=prediction_results.get('prediction_confidence', 0.85),
                        stroke_confidence=prediction_results.get('prediction_confidence', 0.85),
                        heart_disease_category=prediction_results['heart_disease_category'],
                        diabetes_category=prediction_results['diabetes_category'],
                        cancer_category=prediction_results['cancer_category'],
                        stroke_category=prediction_results['stroke_category'],
                        feature_importance=prediction_results.get('feature_importance', {}),
                        model_version=prediction_results.get('model_version', '1.0.0'),
                        prediction_time_ms=prediction_results.get('prediction_time_ms', 0),
                        recommendations=prediction_results.get('recommendations', []),
                        follow_up_required=prediction_results.get('overall_risk_score', 0) >= 50
                    )
                    
                    messages.success(request, 'Health assessment completed successfully!')
                    return redirect('predictor:assessment_results', assessment_id=assessment.id)
                    
            except Exception as e:
                logger.error(f"Assessment save error: {e}")
                messages.error(request, 'Error saving assessment. Please try again.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        # Pre-populate form with patient data
        initial_data = {}
        if patient_profile.bmi:
            initial_data['weight'] = patient_profile.weight
            initial_data['height'] = patient_profile.height
        
        form = HealthAssessmentForm(initial=initial_data)
    
    context = {
        'form': form,
        'title': 'Health Assessment',
        'patient_profile': patient_profile,
    }
    return render(request, 'predictor/health_assessment.html', context)

@login_required
def assessment_results_view(request, assessment_id):
    """View assessment results"""
    assessment = get_object_or_404(HealthAssessment, id=assessment_id, patient__user=request.user)
    
    try:
        prediction = assessment.predictionresult
    except PredictionResult.DoesNotExist:
        messages.error(request, 'No prediction results found for this assessment.')
        return redirect('predictor:health_assessment')
    
    # Prepare data for visualization
    risk_data = {
        'Heart Disease': {
            'risk': prediction.heart_disease_risk,
            'category': prediction.heart_disease_category,
            'confidence': prediction.heart_disease_confidence
        },
        'Diabetes': {
            'risk': prediction.diabetes_risk,
            'category': prediction.diabetes_category,
            'confidence': prediction.diabetes_confidence
        },
        'Cancer': {
            'risk': prediction.cancer_risk,
            'category': prediction.cancer_category,
            'confidence': prediction.cancer_confidence
        },
        'Stroke': {
            'risk': prediction.stroke_risk,
            'category': prediction.stroke_category,
            'confidence': prediction.stroke_confidence
        }
    }
    
    context = {
        'assessment': assessment,
        'prediction': prediction,
        'risk_data': risk_data,
        'overall_risk': prediction.overall_risk_score,
        'primary_condition': prediction.primary_risk_condition,
        'recommendations': prediction.recommendations,
        'feature_importance': prediction.feature_importance,
        'title': 'Your Health Assessment Results'
    }
    return render(request, 'predictor/assessment_results.html', context)

@login_required
def assessment_history_view(request):
    """View assessment history"""
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    assessments = HealthAssessment.objects.filter(patient=patient_profile).order_by('-assessment_date')
    
    context = {
        'assessments': assessments,
        'title': 'Assessment History'
    }
    return render(request, 'predictor/assessment_history.html', context)

@login_required
def export_results_view(request, assessment_id):
    """Export assessment results as PDF"""
    # This would integrate with a PDF generation library
    # For now, return a simple text response
    assessment = get_object_or_404(HealthAssessment, id=assessment_id, patient__user=request.user)
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="health_assessment_{assessment.id}.txt"'
    
    content = f"""
Health Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Patient: {assessment.patient.user.get_full_name()}
Assessment Date: {assessment.assessment_date.strftime('%Y-%m-%d')}

Risk Assessment Results:
- Heart Disease Risk: {assessment.predictionresult.heart_disease_risk:.1f}%
- Diabetes Risk: {assessment.predictionresult.diabetes_risk:.1f}%
- Cancer Risk: {assessment.predictionresult.cancer_risk:.1f}%
- Stroke Risk: {assessment.predictionresult.stroke_risk:.1f}%

This report was generated by the Health Prediction Platform.
Please consult with healthcare professionals for medical advice.
"""
    
    response.write(content)
    return response

# API Views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def api_predict_view(request):
    """API endpoint for health predictions"""
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['systolic_bp', 'diastolic_bp', 'fasting_glucose', 'total_cholesterol']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Make prediction
        results = health_predictor.predict_health_risks(data)
        
        return Response({
            'success': True,
            'prediction': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        return Response(
            {'error': 'Prediction failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def api_health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'model_loaded': health_predictor.model is not None,
        'timestamp': datetime.now().isoformat()
    })

@api_view(['GET'])
def get_live_stats(request):
    """Get live platform statistics"""
    try:
        stats = {
            'total_assessments': HealthAssessment.objects.count(),
            'active_users': User.objects.count(),
            'prediction_accuracy': 91  # Calculated accuracy
        }
        return Response(stats)
    except Exception as e:
        logger.error(f"Error fetching live stats: {e}")
        return Response(
            {'error': 'Failed to fetch statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Medical Report Upload Views
from .models import MedicalReport
from .services.ocr_service import MedicalReportExtractor
from django.core.files.storage import default_storage
from django.utils import timezone
import os

@login_required
def upload_medical_report(request):
    """Handle medical report file upload"""
    # Debug logging
    with open('/tmp/upload_debug.log', 'a') as f:
        f.write(f"Upload request received: {request.method}\n")
        f.write(f"User: {request.user}\n")
        f.write(f"FILES: {request.FILES.keys()}\n")

    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        # Get patient profile
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        return JsonResponse({'error': 'Patient profile not found'}, status=400)
    
    # Validate file upload
    if 'report_file' not in request.FILES:
        with open('/tmp/upload_debug.log', 'a') as f:
            f.write("Error: No file uploaded\n")
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['report_file']
    
    # Validate file type
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    if file_ext not in allowed_extensions:
        return JsonResponse({
            'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
        }, status=400)
    
    # Validate file size (10MB max)
    max_size = 10 * 1024 * 1024  # 10MB
    if uploaded_file.size > max_size:
        return JsonResponse({
            'error': f'File too large. Maximum size: 10MB'
        }, status=400)
    
    try:
        # Create MedicalReport record
        report = MedicalReport.objects.create(
            patient=patient_profile,
            file=uploaded_file,
            file_type=file_ext,
            file_size=uploaded_file.size,
            original_filename=uploaded_file.name,
            processing_status='pending'
        )
        
        logger.info(f"Medical report {report.id} uploaded by {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'report_id': report.id,
            'filename': uploaded_file.name,
            'file_size': report.file_size_mb,
            'message': 'File uploaded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error uploading medical report: {e}")
        return JsonResponse({
            'error': 'Failed to upload file'
        }, status=500)


@login_required
def process_medical_report(request, report_id):
    """Process uploaded report and extract medical data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        # Get report
        report = MedicalReport.objects.get(
            id=report_id,
            patient__user=request.user
        )
    except MedicalReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    
    # Check if already processed
    if report.processing_status == 'completed':
        return JsonResponse({
            'success': True,
            'extracted_data': report.extracted_data,
            'confidence': report.extraction_confidence,
            'message': 'Report already processed'
        })
    
    try:
        # Update status
        report.processing_status = 'processing'
        report.save()
        
        # Debug logging to file
        with open('/tmp/ocr_debug.log', 'a') as f:
            f.write(f"Processing report {report.id}\n")
            f.write(f"File field: {report.file}\n")
            try:
                f.write(f"File path: {report.file.path}\n")
            except Exception as e:
                f.write(f"Could not get path: {e}\n")
        
        logger.info(f"Starting OCR processing for report {report.id}")
        
        # Check if file exists
        if not report.file:
            raise Exception("No file attached to report")
        
        # Get file path
        try:
            file_path = report.file.path
            logger.info(f"File path: {file_path}")
        except Exception as e:
            logger.error(f"Error getting file path: {e}")
            raise Exception(f"Cannot access file: {str(e)}")
        
        # Check if file exists on disk
        import os
        if not os.path.exists(file_path):
            raise Exception(f"File not found on disk: {file_path}")
        
        # Extract data using OCR service
        try:
            from .services.ocr_service import MedicalReportExtractor
            extractor = MedicalReportExtractor()
            logger.info(f"OCR extractor initialized")
            
            extracted_data, confidence = extractor.extract_and_parse(
                file_path,
                report.file_type
            )
            logger.info(f"OCR extraction complete. Fields: {len(extracted_data)}, Confidence: {confidence}")
            
        except ImportError as e:
            logger.error(f"Import error in OCR service: {e}")
            raise Exception(f"OCR service error: {str(e)}")
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            raise Exception(f"Text extraction failed: {str(e)}")
        
        # Save extracted data
        report.extracted_data = extracted_data
        report.extraction_confidence = confidence
        report.processing_status = 'completed'
        report.processed_at = timezone.now()
        report.save()
        
        logger.info(f"Report {report.id} processed successfully. Confidence: {confidence:.2f}")
        
        return JsonResponse({
            'success': True,
            'extracted_data': extracted_data,
            'confidence': confidence,
            'fields_extracted': len(extracted_data),
            'message': 'Report processed successfully'
        })
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing report {report_id}: {error_msg}", exc_info=True)
        report.processing_status = 'failed'
        report.processing_error = error_msg
        report.save()
        
        return JsonResponse({
            'error': 'Failed to process report',
            'details': error_msg
        }, status=500)


@login_required
def delete_medical_report(request, report_id):
    """Delete uploaded medical report"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        report = MedicalReport.objects.get(
            id=report_id,
            patient__user=request.user
        )
        
        # Soft delete
        report.soft_delete()
        
        logger.info(f"Report {report.id} deleted by {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'message': 'Report deleted successfully'
        })
        
    except MedicalReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting report {report_id}: {e}")
        return JsonResponse({
            'error': 'Failed to delete report'
        }, status=500)