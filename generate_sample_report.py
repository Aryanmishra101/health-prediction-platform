"""
Generate sample medical report PDF for testing OCR feature
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

# Create PDF
pdf_path = "sample_medical_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#003366'),
    spaceAfter=30,
    alignment=TA_CENTER
)

header_style = ParagraphStyle(
    'CustomHeader',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#003366'),
    spaceAfter=12
)

# Title
story.append(Paragraph("MEDICAL LABORATORY REPORT", title_style))
story.append(Spacer(1, 0.2*inch))

# Patient Information
patient_data = [
    ['Patient Name:', 'John Doe', 'Medical ID:', 'HP12345'],
    ['Date of Birth:', '15/01/1990', 'Age:', '35 years'],
    ['Gender:', 'Male', 'Date:', datetime.now().strftime('%d/%m/%Y')],
]

patient_table = Table(patient_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
patient_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

story.append(patient_table)
story.append(Spacer(1, 0.3*inch))

# Vital Signs
story.append(Paragraph("VITAL SIGNS", header_style))
vital_data = [
    ['Test', 'Result', 'Normal Range', 'Unit'],
    ['Blood Pressure', '120 / 80', '90-120 / 60-80', 'mmHg'],
    ['Heart Rate', '72', '60-100', 'bpm'],
    ['Temperature', '37.0', '36.1-37.2', '°C'],
]

vital_table = Table(vital_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
vital_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

story.append(vital_table)
story.append(Spacer(1, 0.3*inch))

# Blood Chemistry
story.append(Paragraph("BLOOD CHEMISTRY", header_style))
chemistry_data = [
    ['Test', 'Result', 'Normal Range', 'Unit'],
    ['Fasting Glucose', '95', '70-99', 'mg/dL'],
    ['HbA1c', '5.4', '<5.7', '%'],
    ['Total Cholesterol', '185', '<200', 'mg/dL'],
    ['HDL Cholesterol', '55', '>40 (M), >50 (F)', 'mg/dL'],
    ['LDL Cholesterol', '110', '<100', 'mg/dL'],
    ['Triglycerides', '120', '<150', 'mg/dL'],
    ['Creatinine', '1.0', '0.6-1.2', 'mg/dL'],
    ['Hemoglobin', '15.2', '14-18 (M)', 'g/dL'],
]

chemistry_table = Table(chemistry_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
chemistry_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

story.append(chemistry_table)
story.append(Spacer(1, 0.3*inch))

# Notes
story.append(Paragraph("CLINICAL NOTES", header_style))
notes_text = """
All test results are within normal ranges. Patient shows good metabolic health with 
optimal glucose control and healthy lipid profile. Blood pressure is well-controlled. 
Continue current lifestyle and medication regimen. Follow-up recommended in 6 months.
"""
story.append(Paragraph(notes_text, styles['Normal']))
story.append(Spacer(1, 0.3*inch))

# Footer
footer_data = [
    ['Laboratory:', 'HealthPredict Medical Center'],
    ['Physician:', 'Dr. Sarah Johnson, MD'],
    ['Lab Technician:', 'Michael Chen, MLT'],
]

footer_table = Table(footer_data, colWidths=[2*inch, 5*inch])
footer_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
]))

story.append(footer_table)

# Build PDF
doc.build(story)

print(f"✅ Sample medical report generated: {pdf_path}")
print(f"📄 File contains realistic medical data for OCR testing")
print(f"🔍 Values included: BP, Heart Rate, Glucose, HbA1c, Cholesterol, etc.")
