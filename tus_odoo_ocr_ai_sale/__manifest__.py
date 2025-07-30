# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Odoo OCR Using AI - Sale Order',
    'version': '18.0.2.0.0',
    'summary': 'Transform your sales order processing with the Odoo OCR Using AI app! This powerful tool leverages advanced optical character recognition (OCR) technology and artificial intelligence to streamline the capture and management of sale orders within your Odoo environment.',
    'sequence': 10,
    'description': """ Transform your sales order processing with the Odoo OCR Using AI app! This powerful tool leverages advanced optical character recognition (OCR) technology and artificial intelligence to streamline the capture and management of sale orders within your Odoo environment.
        Odoo OCR AI
        Odoo Optical Character Recognition
        AI-based OCR in Odoo
        Odoo OCR integration
        Odoo AI OCR module
        Automated OCR Odoo
        Odoo OCR document processing
        Odoo AI text recognition
        Odoo OCR invoice scanning
        Odoo OCR AI implementation
        OCR automation with Odoo
        Intelligent OCR Odoo
        Odoo OCR solution
        Odoo AI document scanning
        AI OCR Odoo application
        Odoo machine learning OCR
        Odoo OCR AI technology
        Odoo document AI OCR
        Odoo OCR workflow automation
        Odoo AI OCR customization
        Odoo OCR
        AI Invoice Processing
        Invoice OCR
        Optical Character Recognition
        AI-Powered OCR
        Invoice Automation
        Smart Invoice Scanning
        Odoo Invoice Management
        Automated Invoice Data Extraction
        OCR AI Integration
        Invoice Recognition
        AI Document Processing
        OCR for Accounting
        Intelligent Invoice Processing
        AI-Driven OCR
        Invoice Data Capture
        Odoo AI Module
        OCR Invoice Automation
        Digital Invoice Processing
        Machine Learning OCR """,
    'category': 'tools',
    'website': "https://techultrasolutions.com",
    "author": "TechUltra Solutions Private Limited",
    'live_test_url': 'https://ai.fynix.app/',
    'depends': ["sale", "tus_odoo_ocr_ai_base","account"],
    'data': [
        'data/ocr_model_data.xml',
        'views/ocr_ai_sale_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tus_odoo_ocr_ai_sale/static/src/xml/**/*',
            'tus_odoo_ocr_ai_sale/static/src/js/**/*',
        ],
    },
    "images": ["static/description/main_banner.gif"],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}