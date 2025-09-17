from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import re
import logging

_logger = logging.getLogger(__name__)

class WhatsappCheckout(http.Controller):

    def _validate_e164_phone(self, phone):
        """Validate phone number in E.164 format (e.g., +14155238886)."""
        pattern = r'^\+[1-9]\d{1,14}$'
        if not phone or not re.match(pattern, phone):
            return False
        return phone

    @http.route('/checkout/whatsapp', type='http', auth='public', methods=['GET', 'POST'], csrf=True, website=True)
    def checkout_whatsapp(self, **post):
        if request.httprequest.method == 'GET':
            return request.render('whatsapp_shopping_bot.wk_whtsappPublic_form', {})

        sale_order_id = int(post.get('sale_order_id', 0))
        sale_order = request.env['sale.order'].sudo().browse(sale_order_id) if sale_order_id else False
        if not sale_order:
            return request.redirect('/shop/cart')

        required_fields = ['name', 'phone', 'whatsappnumber', 'street', 'city', 'country_id']
        errors = {}
        for field in required_fields:
            if not post.get(field):
                errors[field] = _(f"{field.capitalize()} is required.")

        # Validate WhatsApp number format
        whatsapp_number = post.get('whatsappnumber')
        if whatsapp_number and not self._validate_e164_phone(whatsapp_number):
            errors['whatsappnumber'] = _("WhatsApp number must be in E.164 format (e.g., +14155238886).")

        if errors:
            values = {
                'error': {'error_message': list(errors.values())},
                'checkout': post,
                'countries': request.env['res.country'].sudo().search([]),
                'sale_order_id': sale_order_id,
                'mode': ['new', 'billing'],
                'zip_city': ['city', 'zip'],
            }
            if post.get('country_id'):
                values['country'] = request.env['res.country'].sudo().browse(int(post['country_id']))
            return request.render('whatsapp_shopping_bot.wk_whtsappPublic_form', values)

        try:
            partner_vals = {
                'name': post['name'],
                'phone': post['phone'],
                'mobile': whatsapp_number,
                'street': post['street'],
                'street2': post.get('street2'),
                'city': post['city'],
                'zip': post.get('zip'),
                'country_id': int(post['country_id']),
                'state_id': int(post.get('state_id', 0)) or False,
                'email': post.get('email'),
                'type': 'delivery',
            }
            partner = request.env['res.partner'].sudo().create(partner_vals)

            sale_order.write({
                'partner_id': partner.id,
                'partner_shipping_id': partner.id,
                'partner_invoice_id': partner.id,
            })
            sale_order.action_confirm()

            twilio_config = request.env['wk.twilio.whatsapp'].sudo().search([], limit=1)
            if not twilio_config:
                raise ValidationError(_("Twilio WhatsApp configuration not found."))

            message_body = twilio_config.message_template.format(
                name=post['name'],
                order_ref=sale_order.name
            )
            twilio_config.with_delay().send_whatsapp_message(sale_order, whatsapp_number, message_body)

            return request.redirect('/shop/confirmation?order_id=%s' % sale_order.id)

        except Exception as e:
            _logger.error("Error during WhatsApp checkout: %s", str(e))
            errors['general'] = _("An error occurred during processing. Please try again.")
            values = {
                'error': {'error_message': [errors['general']]},
                'checkout': post,
                'countries': request.env['res.country'].sudo().search([]),
                'sale_order_id': sale_order_id,
                'mode': ['new', 'billing'],
                'zip_city': ['city', 'zip'],
            }
            if post.get('country_id'):
                values['country'] = request.env['res.country'].sudo().browse(int(post['country_id']))
            return request.render('whatsapp_shopping_bot.wk_whtsappPublic_form', values)