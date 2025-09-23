# -*- coding: utf-8 -*-
#################################################################################
# Author      : ABL Solutions.
# Copyright(c): 2017-Present ABL Solutions.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################
{
    'name': 'TILOPAY PAYMENT GATEWAY',
    'version': '18.0.0.1',
    'summary': "Tilopay's payment gateway for Odoo.",
    'description': 'This module integrates the Tilopay SDK with Odoo working with Credit Card and Debid Card.',
    'category': 'Payment',
    'author': 'ABL Solutions',
    'license': 'Other proprietary',
    'price':45.0,
    'currency':'USD',
    'support':'infoablsolutions24@gmail.com',
    'depends': ['payment','website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_provider_views.xml',
        'views/payment_tilopay_templates.xml',
        'views/payment_template.xml',
        'views/templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_tilopay/static/src/js/payment_form.js',
        ],
        #'web.assets_backend': [
        #    'payment_tilopay/static/src/js/form_view.js',
        #],
    },
    'images':['static/description/Banner.png'],
}