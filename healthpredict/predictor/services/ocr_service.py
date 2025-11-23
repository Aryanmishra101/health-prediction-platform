"""
Medical Report OCR Extraction Service
Extracts medical data from PDF and image files using OCR
"""

import re
import os
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    import PyPDF2
except ImportError as e:
    logging.error(f"Required OCR libraries not installed: {e}")

logger = logging.getLogger(__name__)


class MedicalReportExtractor:
    """Extract medical data from reports using OCR and text parsing"""
    
    # Regex patterns for medical values
    PATTERNS = {
        # Blood Pressure: 120/80, 120 / 80 mmHg, BP: 120/80
        'blood_pressure': r'(?:BP|Blood\s+Pressure)[:\s]*(\d{2,3})\s*/\s*(\d{2,3})',
        'systolic_bp': r'(?:Systolic|SBP)[:\s]*(\d{2,3})',
        'diastolic_bp': r'(?:Diastolic|DBP)[:\s]*(\d{2,3})',
        
        # Glucose: 100 mg/dL, Glucose: 100, FBS: 100
        'glucose': r'(?:Glucose|FBS|Fasting\s+Blood\s+Sugar)[:\s]*(\d{2,3})',
        
        # HbA1c: 5.6%, A1C: 5.6, HbA1c: 5.6
        'hba1c': r'(?:HbA1c|A1C|Hemoglobin\s+A1C)[:\s]*(\d+\.?\d*)',
        
        # Cholesterol: Total: 200, HDL: 50, LDL: 130
        'total_cholesterol': r'(?:Total\s+Cholesterol|TC)[:\s]*(\d{2,3})',
        'hdl_cholesterol': r'(?:HDL|HDL-C)[:\s]*(\d{2,3})',
        'ldl_cholesterol': r'(?:LDL|LDL-C)[:\s]*(\d{2,3})',
        'triglycerides': r'(?:Triglycerides|TG)[:\s]*(\d{2,4})',
        
        # Heart Rate: 72 bpm, HR: 72, Pulse: 72
        'heart_rate': r'(?:Heart\s+Rate|HR|Pulse)[:\s]*(\d{2,3})',
        
        # Temperature: 98.6°F, Temp: 37°C
        'temperature': r'(?:Temperature|Temp)[:\s]*(\d{2,3}\.?\d*)',
        
        # Creatinine: 1.0 mg/dL
        'creatinine': r'(?:Creatinine|Cr)[:\s]*(\d+\.?\d*)',
        
        # Hemoglobin: 15.2 g/dL
        'hemoglobin': r'(?:Hemoglobin|Hb|Hgb)[:\s]*(\d{1,2}\.?\d*)',
        
        # Dates: DD/MM/YYYY, MM-DD-YYYY, DD-MM-YYYY
        'date': r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
    }
    
    def __init__(self):
        """Initialize the extractor"""
        self.confidence_threshold = 0.5
    
    def extract_from_pdf(self, file_path: str) -> Tuple[str, float]:
        """
        Extract text from PDF using PyPDF2 and pdf2image
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            # First try PyPDF2 for text-based PDFs
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # If we got substantial text, return it
                if len(text.strip()) > 100:
                    logger.info(f"Extracted {len(text)} characters from PDF using PyPDF2")
                    return text, 0.9
            
            # If PyPDF2 didn't work well, use OCR on images
            logger.info("PDF appears to be image-based, using OCR...")
            images = convert_from_path(file_path)
            text = ""
            
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
                logger.info(f"Extracted {len(page_text)} characters from page {i+1}")
            
            confidence = 0.7 if len(text.strip()) > 50 else 0.3
            return text, confidence
            
        except Exception as e:
            logger.error(f"Error extracting from PDF: {e}")
            return "", 0.0
    
    def extract_from_image(self, file_path: str) -> Tuple[str, float]:
        """
        Extract text from image using pytesseract
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            # Calculate confidence based on text length and quality
            confidence = 0.8 if len(text.strip()) > 100 else 0.5
            
            logger.info(f"Extracted {len(text)} characters from image")
            return text, confidence
            
        except Exception as e:
            logger.error(f"Error extracting from image: {e}")
            return "", 0.0
    
    def get_units(self, field_name: str) -> str:
        """Get standard units for a field"""
        units = {
            'systolic_bp': 'mmHg',
            'diastolic_bp': 'mmHg',
            'fasting_glucose': 'mg/dL',
            'hba1c': '%',
            'total_cholesterol': 'mg/dL',
            'hdl_cholesterol': 'mg/dL',
            'ldl_cholesterol': 'mg/dL',
            'triglycerides': 'mg/dL',
            'heart_rate': 'bpm',
            'temperature': '°C',
            'creatinine': 'mg/dL',
            'hemoglobin': 'g/dL',
        }
        return units.get(field_name, '')

    def parse_medical_data(self, text: str) -> Dict:
        """
        Parse extracted text to identify medical values with context
        
        Args:
            text: Extracted text from OCR
            
        Returns:
            Dictionary of parsed medical values with metadata
        """
        data = {}
        lines = text.split('\n')
        
        # Helper to process value based on field type
        def process_value(field, val_str):
            try:
                if field in ['hba1c', 'temperature', 'creatinine', 'hemoglobin']:
                    return float(val_str)
                return int(val_str)
            except ValueError:
                return None

        # Iterate through all patterns
        for field, pattern in self.PATTERNS.items():
            # Skip composite patterns like 'blood_pressure' for direct assignment
            if field == 'blood_pressure':
                continue
                
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    val_str = match.group(1)
                    value = process_value(field, val_str)
                    
                    if value is not None:
                        # Special handling for temperature conversion
                        if field == 'temperature' and value > 50:
                            value = round((value - 32) * 5/9, 1)
                        
                        # Special handling for HbA1c percentage
                        if field == 'hba1c' and value > 15:
                            value = value / 10

                        # Map 'glucose' to 'fasting_glucose'
                        field_name = 'fasting_glucose' if field == 'glucose' else field

                        data[field_name] = {
                            "value": value,
                            "units": self.get_units(field_name),
                            "confidence": 0.9, # High confidence for regex match
                            "raw_line": line.strip()
                        }
                        break # Stop after first match for this field
        
        # Handle composite Blood Pressure if individual not found
        if 'systolic_bp' not in data or 'diastolic_bp' not in data:
            for line in lines:
                match = re.search(self.PATTERNS['blood_pressure'], line, re.IGNORECASE)
                if match:
                    systolic = int(match.group(1))
                    diastolic = int(match.group(2))
                    
                    if 'systolic_bp' not in data:
                        data['systolic_bp'] = {
                            "value": systolic,
                            "units": "mmHg",
                            "confidence": 0.9,
                            "raw_line": line.strip()
                        }
                    
                    if 'diastolic_bp' not in data:
                        data['diastolic_bp'] = {
                            "value": diastolic,
                            "units": "mmHg",
                            "confidence": 0.9,
                            "raw_line": line.strip()
                        }
                    break

        logger.info(f"Parsed {len(data)} medical values from text")
        return data
    
    def validate_medical_values(self, data: Dict) -> Dict:
        """
        Validate extracted medical values are within reasonable ranges
        
        Args:
            data: Dictionary of extracted values (rich format)
            
        Returns:
            Dictionary with only valid values (rich format)
        """
        valid_data = {}
        
        # Define valid ranges
        ranges = {
            'systolic_bp': (70, 250),
            'diastolic_bp': (40, 150),
            'fasting_glucose': (70, 500),
            'hba1c': (4.0, 15.0),
            'total_cholesterol': (100, 400),
            'hdl_cholesterol': (20, 100),
            'ldl_cholesterol': (50, 300),
            'triglycerides': (50, 1000),
            'heart_rate': (40, 200),
            'temperature': (30, 45),
            'creatinine': (0.3, 5.0),
            'hemoglobin': (8.0, 20.0),
        }
        
        for key, item in data.items():
            value = item['value']
            if key in ranges:
                min_val, max_val = ranges[key]
                if min_val <= value <= max_val:
                    valid_data[key] = item
                else:
                    logger.warning(f"Value {key}={value} outside valid range [{min_val}, {max_val}]")
                    # Optionally keep it but lower confidence? 
                    # For now, strictly filter as per original logic, or maybe keep with low confidence?
                    # Let's keep it but mark confidence low
                    item['confidence'] = 0.3
                    item['notes'] = f"Value outside normal range ({min_val}-{max_val})"
                    valid_data[key] = item
            else:
                valid_data[key] = item
        
        return valid_data
    
    def map_to_form_fields(self, parsed_data: Dict) -> Dict:
        """
        Map extracted data to HealthAssessmentForm fields
        
        Args:
            parsed_data: Dictionary of parsed medical values (rich format)
            
        Returns:
            Dictionary ready for form population (rich format preserved)
        """
        # Validate first
        valid_data = self.validate_medical_values(parsed_data)
        
        # Add default values for required fields if missing
        # Note: We wrap defaults in rich structure too for consistency in frontend
        defaults = {
            'stress_level': 5,
            'sleep_hours': 7.0,
        }
        
        for key, value in defaults.items():
            if key not in valid_data:
                valid_data[key] = {
                    "value": value,
                    "units": "",
                    "confidence": 1.0,
                    "raw_line": "Default value"
                }
        
        return valid_data
    
    def extract_and_parse(self, file_path: str, file_type: str) -> Tuple[Dict, float]:
        """
        Main method to extract and parse medical report
        
        Args:
            file_path: Path to the file
            file_type: Type of file (pdf, jpg, png)
            
        Returns:
            Tuple of (extracted_data_dict, confidence_score)
        """
        # Extract text based on file type
        if file_type.lower() == 'pdf':
            text, confidence = self.extract_from_pdf(file_path)
        else:
            text, confidence = self.extract_from_image(file_path)
        
        if not text:
            return {}, 0.0
        
        # Parse medical data
        parsed_data = self.parse_medical_data(text)
        
        # Map to form fields (validates and adds defaults)
        final_data = self.map_to_form_fields(parsed_data)
        
        # Calculate overall extraction confidence
        # Average of individual field confidences weighted by number of fields found
        if not final_data:
            overall_confidence = 0.0
        else:
            # Base confidence from OCR quality
            overall_confidence = confidence
            
            # Adjust based on fields found vs expected
            expected_fields = 12 # approx number of key vitals
            fields_found = len([k for k in final_data.keys() if k not in ['stress_level', 'sleep_hours']])
            
            completeness_score = min(fields_found / expected_fields, 1.0)
            overall_confidence = (overall_confidence * 0.4) + (completeness_score * 0.6)
            
        return final_data, round(overall_confidence, 2)
