{
  "name": "POS Self-Order: Barcode Checkout, Custom UI & Delivery Zones (Odoo 18)",
  "summary": "Self-order checkout with barcode-based customer detection, modern UI, and delivery zones with fees & ETAs.",
  "version": "18.0.1.0.0",
  "author": "Your Company",
  "website": "https://example.com",
  "license": "LGPL-3",
  "category": "Point of Sale",
  "depends": ["point_of_sale", "website", "pos_self_order"],
  "assets": {
    "pos_self_order.assets_mobile_menu": [
      "pos_selforder_barcode_checkout/static/src/js/selforder_barcode.js",
      "pos_selforder_barcode_checkout/static/src/js/selforder_delivery.js",
      "pos_selforder_barcode_checkout/static/src/css/selforder.css"
    ],
    "web.assets_qweb": [
      "pos_selforder_barcode_checkout/static/src/xml/selforder_templates.xml"
    ]
  },
  "data": [
    "security/ir.model.access.csv",
    "views/res_partner_views.xml",
    "views/pos_config_views.xml",
    "views/delivery_zone_views.xml"
  ],
  "installable": true
}
