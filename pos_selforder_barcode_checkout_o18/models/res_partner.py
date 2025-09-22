from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    selforder_barcode = fields.Char(
        string='Self-Order Barcode',
        index=True,
        help='Barcode used to auto-identify the customer in Self-Order checkout.'
    )
