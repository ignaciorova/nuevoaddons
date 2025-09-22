from odoo import api, fields, models

class PosSelfOrderDeliveryZone(models.Model):
    _name = 'pos.selforder.delivery.zone'
    _description = 'Self-Order Delivery Zone'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    pos_config_id = fields.Many2one('pos.config', required=True, ondelete='cascade', index=True)
    city = fields.Char(help='Optional city name; leave empty to allow any.')
    zip_prefix = fields.Char(help='Match ZIP/Postal Code prefix (e.g. 10, 101, 1010).')
    min_order_amount = fields.Monetary(string='Minimum Order', currency_field='currency_id', default=0.0)
    free_delivery_threshold = fields.Monetary(string='Free Delivery From', currency_field='currency_id', default=0.0)
    delivery_fee = fields.Monetary(currency_field='currency_id', default=0.0)
    eta_min = fields.Integer(string='ETA Min (min)', default=20)
    eta_max = fields.Integer(string='ETA Max (min)', default=45)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)

    def match_address(self, city, zip_code):
        self.ensure_one()
        ok_city = (not self.city) or (self.city.strip().lower() == (city or '').strip().lower())
        ok_zip = (not self.zip_prefix) or (zip_code or '').startswith(self.zip_prefix)
        return ok_city and ok_zip
