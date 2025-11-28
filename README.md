# Health Prediction Platform

An advanced AI-powered health risk assessment platform that uses machine learning to predict risks for heart disease, diabetes, cancer, and stroke. Built with Django, PyTorch, and modern web technologies.

## 🏥 Features

### Core Functionality
- **Multi-Disease Risk Prediction**: Advanced ML models for heart disease, diabetes, cancer, and stroke
- **Comprehensive Health Assessment**: Medical-grade forms with real-time validation
- **Personalized Recommendations**: AI-generated health improvement suggestions
- **Interactive Dashboards**: Real-time analytics and risk visualization
- **Secure User Management**: Authentication, profiles, and data privacy

### Technical Features
- **Machine Learning Integration**: PyTorch neural networks for risk prediction
- **Modern UI/UX**: Responsive design with medical-grade aesthetics
- **Data Visualization**: Interactive charts using ECharts.js
- **API Endpoints**: RESTful API for third-party integrations
- **Security**: HIPAA-compliant data handling and encryption

## 🛠 Technology Stack

### Backend
- **Django 4.2**: Web framework with security features
- **PyTorch 2.1**: Machine learning models
- **PostgreSQL**: Primary database
- **Django Allauth**: Authentication system
- **Django REST Framework**: API development

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **ECharts.js**: Data visualization
- **Anime.js**: Smooth animations
- **Font Awesome**: Icons and graphics
- **Custom CSS**: Medical-themed design system

### DevOps & Quality Assurance
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline with automated testing
- **pytest**: Comprehensive test suite with 70%+ coverage
- **Sentry**: Real-time error tracking and monitoring
- **drf-spectacular**: Interactive API documentation
- **Django Debug Toolbar**: Development performance profiling
- **Heroku/Railway**: Cloud deployment
- **WhiteNoise**: Static file serving

## 📁 Project Structure

```
healthpredict/
├── healthpredict/          # Django project settings
├── predictor/              # Main prediction app
│   ├── models.py          # Database models
│   ├── views.py           # Views and controllers
│   ├── forms.py           # Forms and validation
│   ├── ml_models.py       # ML model integration
│   ├── throttles.py       # API rate limiting
│   └── urls.py            # URL patterns
├── accounts/               # User management app
├── dashboard/              # Analytics and reporting
├── tests/                  # Comprehensive test suite
│   ├── conftest.py        # Test fixtures
│   ├── factories.py       # Test data factories
│   ├── test_models.py     # Model tests
│   ├── test_api.py        # API endpoint tests
│   └── test_ml_models.py  # ML model tests
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── ml_models/              # Trained ML models
├── requirements.txt        # Python dependencies
├── pytest.ini              # Test configuration
├── run_server.py          # Development server
└── .env                   # Environment variables
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (for frontend dependencies)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/health-prediction-platform.git
   cd health-prediction-platform
   ```

2. **Setup virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python run_server.py
   ```

### Alternative: Quick Start Script
```bash
python run_server.py
```
This script automatically:
- Sets up the environment
- Runs migrations
- Creates default directories
- Starts the development server

## 📊 Data & Models

### Health Assessment Data
The platform uses comprehensive health data including:
- **Vital Signs**: Blood pressure, heart rate, temperature
- **Laboratory Results**: Glucose, cholesterol, HbA1c, creatinine
- **Symptoms**: Chest pain, fatigue, vision problems
- **Lifestyle**: Smoking, exercise, stress levels
- **Demographics**: Age, gender, family history

### Machine Learning Models
- **Neural Networks**: Multi-output classification for disease risks
- **Feature Engineering**: 25+ health indicators
- **Risk Scoring**: 0-100 scale with confidence intervals
- **Model Validation**: Cross-validation and performance metrics

### Sample Data
The platform includes realistic mock datasets:
- 10,000 synthetic patient records
- Balanced risk distributions
- Clinical validation data
- Training and test sets

## 🔐 Security & Privacy

### Data Protection
- **Encryption**: All health data encrypted at rest
- **Access Control**: Role-based permissions
- **Audit Logging**: Complete activity tracking
- **HIPAA Compliance**: Medical data handling standards

### Authentication
- **Secure Login**: Django Allauth integration
- **Password Policies**: Strong password requirements
- **Session Management**: Secure session handling
- **Two-Factor Auth**: Optional 2FA support

## 📈 API Documentation

### Prediction API
```http
POST /api/predict/
Content-Type: application/json

{
  "age": 45,
  "gender": "male",
  "systolic_bp": 140,
  "diastolic_bp": 90,
  "fasting_glucose": 110,
  "total_cholesterol": 220,
  "hdl_cholesterol": 45,
  "ldl_cholesterol": 140,
  "triglycerides": 180,
  "hba1c": 6.2,
  "creatinine": 1.0,
  "hemoglobin": 15.2,
  "smoking_status": "former",
  "family_history": "heart_disease"
}
```

### Response
```json
{
  "success": true,
  "prediction": {
    "heart_disease_risk": 75.5,
    "diabetes_risk": 45.2,
    "cancer_risk": 25.8,
    "stroke_risk": 35.1,
    "prediction_confidence": 0.85,
    "recommendations": [...]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎯 Usage Examples

### Patient Journey
1. **Registration**: Create secure account with medical consent
2. **Profile Setup**: Complete health profile and medical history
3. **Assessment**: Fill comprehensive health assessment form
4. **Results**: View AI-generated risk predictions and recommendations
5. **Monitoring**: Track progress through dashboard and follow-up assessments

### Healthcare Provider Workflow
1. **Patient Management**: View and manage patient assessments
2. **Risk Monitoring**: Monitor population health trends
3. **Clinical Decision Support**: Use predictions for treatment planning
4. **Analytics**: Generate reports and insights

## 🏗 Deployment

### Development
```bash
python run_server.py
```

### Production
```bash
# Using Docker
docker-compose up -d

# Using Heroku
git push heroku main

# Using Railway
railway up
```

### Environment Variables
```env
# Required
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com

# Optional
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
ML_MODEL_PATH=/app/ml_models/
```

## 📱 Mobile Support

The platform is fully responsive and optimized for:
- **Mobile Devices**: Touch-friendly interface
- **Tablets**: Clinical workflow optimization
- **Desktop**: Full-featured experience
- **Progressive Web App**: Installable application

## 🔧 Customization

### Styling
- **CSS Variables**: Easy theme customization
- **Bootstrap Themes**: Compatible with Bootstrap themes
- **Custom Components**: Reusable UI components
- **Responsive Design**: Mobile-first approach

### Models
- **Custom Algorithms**: Integrate your own ML models
- **Feature Engineering**: Add new health indicators
- **Risk Categories**: Customize risk thresholds
- **Recommendations**: Personalized health advice

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests
- Update documentation
- Ensure security compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)

### Community
- [GitHub Issues](https://github.com/yourusername/health-prediction-platform/issues)
- [Discussions](https://github.com/yourusername/health-prediction-platform/discussions)
- [Email Support](support@healthpredict.com)

### Professional Support
- Enterprise deployment
- Custom model development
- Integration services
- Training and consultation

## 🙏 Acknowledgments

- **Medical Advisors**: Dr. Sarah Johnson, Dr. Michael Chen
- **ML Researchers**: Stanford AI Lab, MIT CSAIL
- **Open Source**: Django, PyTorch, Bootstrap communities
- **Beta Testers**: Healthcare professionals and patients

## 📈 Roadmap

### Version 2.0 (Q2 2024)
- [ ] Integration with EMR systems
- [ ] Advanced ML models (CNN, RNN)
- [ ] Telemedicine integration
- [ ] Mobile app development

### Version 3.0 (Q4 2024)
- [ ] Real-time monitoring
- [ ] Wearable device integration
- [ ] Population health analytics
- [ ] AI-powered treatment recommendations

---

**Built with ❤️ for better healthcare outcomes**

*This platform is designed to support healthcare decisions, not replace professional medical advice. Always consult with qualified healthcare providers for medical concerns.*