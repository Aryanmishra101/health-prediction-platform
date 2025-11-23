"""
Views for the accounts app
User authentication and profile management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from predictor.forms import PatientProfileForm
from predictor.models import PatientProfile

class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('predictor:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('predictor:home')

class UserRegistrationView(CreateView):
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:profile_setup')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Authenticate and login the user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Registration successful! Please complete your profile.')
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

@login_required
def profile_setup_view(request):
    """Patient profile setup view"""
    
    try:
        patient_profile = request.user.patientprofile
        messages.info(request, 'Update your profile information.')
    except PatientProfile.DoesNotExist:
        patient_profile = None
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            
            # Generate medical ID if not exists
            if not profile.medical_id:
                import uuid
                profile.medical_id = f"HP{str(uuid.uuid4())[:8].upper()}"
            
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('predictor:health_assessment')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientProfileForm(instance=patient_profile)
    
    context = {
        'form': form,
        'title': 'Complete Your Profile',
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/profile_setup.html', context)

@login_required
def profile_view(request):
    """View user profile"""
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup.')
        return redirect('accounts:profile_setup')
    
    context = {
        'patient_profile': patient_profile,
        'title': 'My Profile',
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def dashboard_view(request):
    """User dashboard view"""
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup.')
        return redirect('accounts:profile_setup')
    
    # Get recent assessments
    recent_assessments = patient_profile.healthassessment_set.order_by('-assessment_date')[:5]
    
    # Get latest prediction if available
    latest_prediction = None
    if recent_assessments:
        try:
            latest_prediction = recent_assessments[0].predictionresult
        except:
            pass
    
    context = {
        'patient_profile': patient_profile,
        'recent_assessments': recent_assessments,
        'latest_prediction': latest_prediction,
        'title': 'My Dashboard',
    }
    return render(request, 'accounts/dashboard.html', context)

def demo_login(request):
    """One-click demo login - automatically logs in the demo user"""
    # Authenticate demo user
    user = authenticate(username='demo', password='demo123')
    
    if user is not None:
        login(request, user)
        messages.success(request, '🎉 Welcome to the demo! You are now logged in as a demo user.')
        messages.info(request, 'Explore the health prediction features with pre-configured demo data.')
        return redirect('predictor:home')
    else:
        messages.error(request, 'Demo user not found. Please contact the administrator.')
        return redirect('accounts:login')