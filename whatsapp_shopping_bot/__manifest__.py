{
    'name': "WhatsApp Shopping Bot & Order Notifications",
    'summary': "Integrate WhatsApp shopping bot with Twilio for order notifications and checkout.",
    'description': """
        This module allows users to purchase via WhatsApp, configure Twilio integration,
        send order notifications, and track WhatsApp message history.
    """,
    'author': "Your Company",
    'website': "https://yourcompany.com",
    'category': 'Website/eCommerce',
    'version': '18.0.1.0.0',
    'depends': ['website', 'website_sale', 'sale_management', 'account', 'mail', 'queue_job'],
    'data': [
        'security/ir.model.access.xml',
        'views/wk_twilio_whatsapp_views.xml',
        'views/whatsapp_shopping_bot_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'whatsapp_shopping_bot/static/src/js/whatsapp_cart.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}