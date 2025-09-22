from odoo import http
from odoo.http import request

class SelfOrderBarcodeController(http.Controller):

    @http.route(['/pos/self_order/barcode/search'], type='json', auth='public', website=True, csrf=False)
    def self_order_barcode_search(self, barcode=None, config_id=None, **kwargs):
        if not barcode or not config_id:
            return {'ok': False, 'error': 'missing_parameters'}

        config = request.env['pos.config'].sudo().browse(int(config_id))
        if not config.exists():
            return {'ok': False, 'error': 'config_not_found'}
        if not config.so_barcode_checkout_enabled:
            return {'ok': False, 'error': 'feature_disabled'}

        field_name = config.so_barcode_match_field or 'selforder_barcode'
        Partner = request.env['res.partner'].sudo()
        partner = Partner.search([(field_name, '=', barcode)], limit=1)
        if not partner:
            partner = Partner.search([(field_name, '=ilike', barcode)], limit=1)

        if not partner:
            return {'ok': True, 'found': False}

        return {
            'ok': True,
            'found': True,
            'partner': {
                'id': partner.id,
                'name': partner.name,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'email': partner.email,
                'barcode': getattr(partner, field_name, False),
                'street': partner.street,
                'city': partner.city,
                'zip': partner.zip,
            }
        }

    @http.route(['/pos/self_order/delivery/quote'], type='json', auth='public', website=True, csrf=False)
    def self_order_delivery_quote(self, config_id=None, city=None, zip_code=None, amount_total=0.0, **kw):
        if not config_id:
            return {'ok': False, 'error': 'missing_parameters'}
        config = request.env['pos.config'].sudo().browse(int(config_id))
        if not config.exists() or not config.so_enable_delivery:
            return {'ok': False, 'error': 'delivery_not_enabled'}

        zones = config.so_delivery_zone_ids
        best = None
        for z in zones:
            if z.match_address(city, zip_code):
                best = z
                break
        if not best:
            return {'ok': True, 'matched': False}

        fee = 0.0
        if amount_total < (best.free_delivery_threshold or 0.0):
            fee = float(best.delivery_fee or 0.0)

        meets_min = amount_total >= float(best.min_order_amount or 0.0)
        return {
            'ok': True,
            'matched': True,
            'zone': {
                'id': best.id,
                'name': best.name,
                'eta_min': best.eta_min,
                'eta_max': best.eta_max,
                'min_order_amount': best.min_order_amount,
                'free_delivery_threshold': best.free_delivery_threshold,
                'delivery_fee': best.delivery_fee,
            },
            'meets_minimum': meets_min,
            'delivery_fee': fee,
        }
