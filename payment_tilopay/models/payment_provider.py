# -*- coding: utf-8 -*-
#################################################################################
# Author      : ABL Solutions.
# Copyright(c): 2017-Present ABL Solutions.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################

import json
import logging
import pprint
import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('tilopay', 'Tilopay')], ondelete={'tilopay': 'set default'})
    tilopay_api_key = fields.Char("TiloPay API Key", help="The Api Key of tilopay account",required_if_provider='tilopay')
    tilopay_api_user = fields.Char("Tilopay API User", required_if_provider='tilopay', groups='base.group_system')
    tilopay_api_password = fields.Char("Tilopay API Password", required_if_provider='tilopay', groups='base.group_system')
    tilopay_payment_ids = fields.One2many('tilopay.payments.availables', 'acquirer_id', 'Tilopay Payments Type')

    def _tilopay_get_inline_form_values(self):
        """ Return a serialized JSON of the required values to render the inline form.

        Note: `self.ensure_one()`

        :return: The JSON serial of the required values to render the inline form. Generate Values
        :rtype: str
        """
        self.ensure_one()
        #Get Acces token of TiloPay
        payload = {
            "apiuser":self.tilopay_api_user,
            "password":self.tilopay_api_password,
            "key":self.tilopay_api_key,
        }

        headers = {
            'Content-Type':'application/json',
        }
        url= "https://app.tilopay.com/api/v1/loginSdk"

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()

        order_id = self.env['sale.order'].browse(request.session.get('sale_order_id'))
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        inline_form_values = {
            "token": response['access_token'] if 'access_token' in response else None,
            "currency":order_id.currency_id.name,
            "language":"es",
            "amount":order_id.amount_total,
            "billToFirstName":order_id.partner_id.first_name,
            "billToLastName":order_id.partner_id.last_name,
            "billToAddress":order_id.partner_id.street,
            "billToCountry":order_id.partner_id.country_id.code,
            "billToEmail": order_id.partner_id.email,
            "orderNumber": order_id.name,
            "capture":1,
            "redirect":base_url+"/payment/tilopay",
            "subscription":0,
            "hashVersion":"V2",
        }
        return json.dumps(inline_form_values)

    def action_tilopay_fetch_methods(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'tilopay_fetch_methods',
            'target': 'current',
        }

