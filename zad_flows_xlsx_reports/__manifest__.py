# -*- coding: utf-8 -*-
{
    'name': 'Zad Flows - XLSX Report Generator',
    'summary': 'Generate Excel (XLSX) reports from Jinja-powered templates stored in Odoo.',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'author': 'Zad Flows',
    'website': 'https://zadflows.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/xlsx_template_views.xml',
        'views/actions.xml',
        'wizard/xlsx_export_wizard_views.xml',
    ],
    'external_dependencies': {
        'python': ['openpyxl', 'jinja2', 'Pillow', 'num2words']
    },
    'images': ['static/description/thumb.png', 'static/description/icon.png'],
    'application': False,
}
