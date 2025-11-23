"""
Test OCR extraction on sample medical report
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/Users/theogengineer/Downloads/OKComputer_Django ML Health App Setup/healthpredict')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

from predictor.services.ocr_service import MedicalReportExtractor

# Test file
test_file = '/Users/theogengineer/Downloads/OKComputer_Django ML Health App Setup/sample_medical_report.pdf'

print(f"Testing OCR extraction on: {test_file}")
print(f"File exists: {os.path.exists(test_file)}")

try:
    extractor = MedicalReportExtractor()
    print("✓ Extractor initialized")
    
    extracted_data, confidence = extractor.extract_and_parse(test_file, 'pdf')
    
    print(f"\n✅ SUCCESS!")
    print(f"Confidence: {confidence:.2%}")
    print(f"Fields extracted: {len(extracted_data)}")
    print(f"\nExtracted data:")
    for key, value in extracted_data.items():
        print(f"  {key}: {value}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
