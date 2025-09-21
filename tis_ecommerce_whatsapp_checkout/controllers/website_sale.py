# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.
import werkzeug
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.http import request, route

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleWhatsapp(WebsiteSale):
    """Extension of the WebsiteSale model to integrate WhatsApp Checkout functionality."""

    def _get_checkout_data(self):
        """Get the checkout data including the WhatsApp number and the message string."""
        order = request.website.sale_get_order()
        whatsapp_number = request.website.whatsapp_number
        if not whatsapp_number:
            return request.redirect('/shop/cart')
        message_string = 'Hi, I would like to buy the following products.%0a%0a'
        for order_line in order.order_line:
            message_string = message_string + '%20' + str(order_line.product_uom_qty) + '%20X%20' + str(
                order_line.product_id.display_name) + '%0a'
        message_string = message_string + '%0aOrder Total : ' + str(order.currency_id.symbol) + '%20' + \
                         str(order.amount_total) + '%0a%0a _Thank You_%20%0a%20'
        return whatsapp_number, message_string

    @http.route(['/shop/whatsapp_checkout'], type='http', auth="public", website=True, sitemap=False)
    def whatsapp_checkout(self, **post):
        """Redirect the user to WhatsApp web for checkout with pre-filled message."""
        mobile_num, message_string = self._get_checkout_data()
        order = request.website.sale_get_order()
        for line in order.order_line:
            line.unlink()
        request.session['website_sale_cart_quantity'] = order.cart_quantity
        url = "https://web.whatsapp.com/send?phone=" + mobile_num + "&text=" + message_string
        return werkzeug.utils.redirect(url)

    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'"""
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        order = request.website.sale_get_order()
        if order and order.carrier_id:
            # Express checkout is based on the amout of the sale order. If there is already a
            # delivery line, Express Checkout form will display and compute the price of the
            # delivery two times (One already computed in the total amount of the SO and one added
            # in the form while selecting the delivery carrier)
            order._remove_delivery_line()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        request.session['website_sale_cart_quantity'] = order.cart_quantity

        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)],
                                                                      limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get(
                    'sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get(
                    'sale_order_id'):  # abandoned cart found, user have to choose what to do
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
        message = _("WhatsApp number not configured!") if not mobile_num else ''
        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
            'compute_currency': compute_currency,
            'error': message,
            'whatsapp_checkout_user': whatsapp_checkout_user
        })

        if order:
            order.order_line.filtered(lambda sol: sol.product_id and not sol.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        values.update(self._cart_values(**post))
        return request.render("website_sale.cart", values)
