from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    so_barcode_checkout_enabled = fields.Boolean(
        string='Self-Order: Barcode Checkout',
        help='Enable barcode-based customer identification in Self-Order checkout.'
    )
    so_barcode_match_field = fields.Selection(
        [
            ('selforder_barcode', 'Partner Barcode'),
            ('barcode', 'Partner Barcode (legacy/custom field)'),
            ('vat', 'Tax ID (VAT)'),
            ('ref', 'Internal Reference'),
            ('phone', 'Phone'),
            ('mobile', 'Mobile'),
            ('email', 'Email'),
        ],
        string='Self-Order: Match Field',
        default='selforder_barcode',
        help='Select which partner field is matched against the scanned barcode.'
    )
    so_barcode_auto_bind = fields.Boolean(
        string='Auto-Bind Customer',
        default=True,
        help='Automatically set the detected customer on the order after successful scan.'
    )

    # Delivery zone settings
    so_enable_delivery = fields.Boolean(
        string='Self-Order: Delivery Options',
        help='Enable delivery/collection options with zones & fees.'
    )
    so_delivery_zone_ids = fields.One2many(
        'pos.selforder.delivery.zone', 'pos_config_id', string='Delivery Zones'
    )
    so_delivery_fee_product_id = fields.Many2one(
        'product.product', string='Delivery Fee Product',
        domain=[('type', '=', 'service')],
        help='Product used to add delivery fee to orders.'
    )
