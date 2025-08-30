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

import logging
import pprint

from werkzeug import urls
from odoo import _, http
from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale
from odoo.exceptions import ValidationError
from werkzeug.exceptions import Forbidden
from odoo.http import request

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):
    def __init__(self):
        super(WebsiteSale, self).__init__()
        WebsiteSale.WRITABLE_PARTNER_FIELDS.extend(['first_name','last_name'])

    def _get_mandatory_address_fields(self, country_sudo):
        res = super(WebsiteSale, self)._get_mandatory_address_fields(country_sudo)
        res.update({'first_name', 'last_name', 'surname'})
        return res

    def _parse_form_data(self, form_data):
        res = super(WebsiteSale, self)._parse_form_data(form_data)
        address_values = {}

        authorized_partner_fields = {'first_name', 'last_name', 'surname'}

        ResPartner = request.env['res.partner']
        partner_fields = {
            name: field
            for name, field in ResPartner._fields.items()
            if name in authorized_partner_fields
        }

        for key, value in form_data.items():
            if isinstance(value, str):
                value = value.strip()
                # Always keep field values, even if falsy, as it might be for resetting a field.
                #address_values[key] = value
            if key in partner_fields and key in authorized_partner_fields:
                field = partner_fields[key]
                if field.type == 'many2one' and isinstance(value, str) and value.isdigit():
                    address_values[key] = field.convert_to_cache(int(value), ResPartner)
                else:
                    # Always keep field values, even if falsy, as it might be for resetting a field.
                    address_values[key] = field.convert_to_cache(value, ResPartner)

        res[0].update(address_values)
        return res

    def values_postprocess(self, order, mode, values, errors, error_msg):
        res = super(WebsiteSale, self).values_postprocess(order, mode, values, errors, error_msg)
        res[0].update({k: v for k, v in values.items() if k in ['first_name', 'last_name', 'surname']})
        return res

class TilopayController(http.Controller):

    @http.route('/payment/tilopay', type='http', auth='public',methods=['GET'], csrf=False)
    def tilopay_payment(self, **kwargs):
        """ Make a payment request and handle the response.
        """
        _logger.info("Handling redirection from Tilopay with data:\n%s", pprint.pformat(kwargs))

        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data('tilopay', kwargs)
        try:
            notification_data = self._parse_pdt_validation_response(kwargs, tx_sudo)
        except Forbidden:
            _logger.exception("Could not verify the origin of the PDT; discarding it.")
        else:
            tx_sudo._handle_notification_data('tilopay', notification_data)

        return request.redirect('/payment/status')

    @staticmethod
    def _parse_pdt_validation_response(response,tx_sudo):
        """ Parse the PDT validation request response and return the parsed notification data.

        :param str response_content: The PDT validation request response
        :return: The parsed notification data
        :rtype: dict
        """
        notification_data = {}
        for key,value in response.items():
            notification_data[key] = urls.url_unquote_plus(value)
        return notification_data
