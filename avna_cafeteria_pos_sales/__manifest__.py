# -*- coding: utf-8 -*-
{
    "name": "AVNA Cafetería – POS & Ventas (Subsidios, Auditoría, Liquidaciones)",
    "version": "18.0.1.0",
    "category": "Sales/Point of Sale/Accounting",
    "summary": "Subsidios ASEAVNA/AVNA, 1 almuerzo/día, conveniencia, timebands, combos, auditoría, liquidaciones, bot, barcode",
    "license": "OEEL-1",
    "depends": ["base","mail","web","account","sale_management","point_of_sale"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/settings_views.xml",
        "views/category_views.xml",
        "views/payer_scheme_views.xml",
        "views/policy_views.xml",
        "views/timeband_views.xml",
        "views/combo_views.xml",
        "views/audit_views.xml",
        "views/data_quality_views.xml",
        "views/pos_sale_views.xml",
        "views/wizard_views.xml",
        "data/cron.xml",
        "data/demo_defaults.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "avna_cafeteria_pos_sales/static/src/js/pos_override_popup.js",
            "avna_cafeteria_pos_sales/static/src/xml/pos_override_popup.xml"
        ]
    },
    "application": True,
    "installable": True
}
