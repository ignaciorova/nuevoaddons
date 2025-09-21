# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.
import werkzeug
from urllib.parse import quote_plus
from odoo import fields, http, _
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    """Extension of the WebsiteSale model to integrate WhatsApp Checkout and Inquiry functionality."""

    def _get_checkout_data(self):
        """Get the checkout data including the WhatsApp number and the message string."""
        order = request.website.sale_get_order()
        whatsapp_number = request.website.whatsapp_number
        if not whatsapp_number:
            return request.redirect('/shop/cart')
        message_string = 'Hi, I would like to buy the following products.\n\n'
        for order_line in order.order_line:
            message_string += f"{order_line.product_uom_qty} x {order_line.product_id.display_name}\n"
        message_string += f"\nOrder Total: {order.currency_id.symbol} {order.amount_total}\n\nThank You\n"
        encoded_message = quote_plus(message_string)
        return whatsapp_number, encoded_message

    @http.route(['/whatsapp/inquiry/<int:product>'], type='http', auth="public", website=True)
    def whatsapp_product_inquiry(self, product, **kw):
        """Redirect to WhatsApp web page for product inquiry."""
        company = request.website.get_current_website().company_id
        product_obj = request.env['product.product'].browse(product)
        message = (company.message or "Hello, I am interested in this product.") + '\nProduct Url: ' + \
                  request.website.get_base_url() + product_obj.website_url
        encoded_message = quote_plus(message)
        return werkzeug.utils.redirect(f"https://wa.me/{company.whatsapp_number}?text={encoded_message}")

    @http.route(['/shop/whatsapp_checkout'], type='http', auth="public", website=True, sitemap=False)
    def whatsapp_checkout(self, **post):
        """Redirect the user to WhatsApp web for checkout with pre-filled message."""
        mobile_num, message_string = self._get_checkout_data()
        order = request.website.sale_get_order()
        for line in order.order_line:
            line.unlink()
        request.session['website_sale_cart_quantity'] = order.cart_quantity
        url = f"https://wa.me/{mobile_num}?text={message_string}"
        return werkzeug.utils.redirect(url)

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """Main cart management + abandoned cart revival."""
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        order = request.website.sale_get_order()
        if order and order.carrier_id:
            order._remove_delivery_line()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        request.session['website_sale_cart_quantity'] = order.cart_quantity if order else 0

        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:
                raise werkzeug.exceptions.NotFound()
            if abandoned_order.state != 'draft':
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get('sale_order_id')):
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get('sale_order_id'):
                values.update({'access_token': abandoned_order.access_token})

        if order:
            order.order_line.filtered(lambda sol: sol.product_id and not sol.product_id.active).unlink()
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: from_currency._convert(
                price, to_currency, request.env.user.company_id, fields.Date.today())
        else:
            compute_currency = lambda price: price

        whatsapp_checkout_user = request.website.whatsapp_checkout
        mobile_num = request.env['ir.config_parameter'].sudo().get_param(
            'tis_ecommerce_whatsapp_checkout.whatsapp_number')
        message = _("WhatsApp number not configured! Please set it in Website Settings.") if not mobile_num else ''
        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories() if order else [],
            'compute_currency': compute_currency,
            'error': message,
            'whatsapp_checkout_user': whatsapp_checkout_user
        })

        values.update(self._get_express_shop_payment_values(order) if order else {})
        values.update(self._cart_values(**post))
        return request.render("website_sale.cart", values)