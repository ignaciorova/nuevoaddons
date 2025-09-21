# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.

{
    'name': 'Ecommerce WhatsApp Checkout',
    'version': '18.0.1.0.1',
    'summary': 'Ecommerce checkout through WhatsApp',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt.Ltd.',
    'description': """
This module enables a WhatsApp checkout feature for the website sales process. 
It allows users to send their selected products to the website shop via WhatsApp message for checkout.
""",
    'category': 'Ecommerce',
    'website': 'http://www.technaureus.com',
    'depends': ['website_sale'],
    'license': 'Other proprietary',
    'price': 35,
    'currency': 'EUR',
    'data': [
        'views/navigation_buttons.xml',
        'views/res_config_settings_views.xml',
        'views/website_views.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'assets': {
        'web.assets_frontend': [
            'tis_ecommerce_whatsapp_checkout/static/src/js/website_clear_cart.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
