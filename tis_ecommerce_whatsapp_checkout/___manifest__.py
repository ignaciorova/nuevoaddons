# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.

{
    'name': 'Ecommerce WhatsApp Checkout and Inquiry',
    'version': '18.0.1.0.1',
    'summary': 'Ecommerce checkout and product inquiry through WhatsApp',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'description': """
This module enables WhatsApp checkout and product inquiry features for the website sales process.
It allows users to send their cart or product inquiries via WhatsApp message.
""",
    'category': 'Ecommerce',
    'website': 'http://www.technaureus.com',
    'depends': ['website_sale', 'base'],
    'license': 'Other proprietary',
    'price': 35,
    'currency': 'EUR',
    'data': [
        'views/navigation_buttons.xml',
        'views/res_config_settings_views.xml',
        'views/website_views.xml',
        'views/product_template.xml',
        'views/res_company_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tis_ecommerce_whatsapp_checkout/static/src/js/website_clear_cart.js',
            'tis_ecommerce_whatsapp_checkout/static/src/js/website_sale_address.js',
            'tis_ecommerce_whatsapp_checkout/static/src/css/address_management.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}