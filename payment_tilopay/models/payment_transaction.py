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
import ast

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from odoo.addons.payment_tilopay.const import PAYMENT_METHODS_MAPPING
from odoo.http import request

_logger = logging.getLogger(__name__)

PAYMENT_STATUS_MAPPING = {
    '1': 'Processed',
    'done': ('Processed', 'Completed'),
    'cancel': ('Voided', 'Expired'),
}

class PaymentTransaction(models.Model):
    _inherit="payment.transaction"

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Tilopay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'tilopay' or len(tx) == 1:
            return tx

        returnData = ast.literal_eval(notification_data.get('returnData'))

        tx = self.search([('reference', '=', returnData['reference']), ('provider_code', '=', 'tilopay')])
        if not tx:
            raise ValidationError(
                "Tilopay: " + _("No transaction found matching reference %s.", returnData['reference'])
            )
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Tilopay data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'tilopay':
            return

        if not notification_data:
            self._set_canceled(_("The customer left the payment page."))
            return
        returnData = ast.literal_eval(notification_data.get('returnData'))
        amount = returnData.get('amount')
        currency_code = returnData.get('currency')
        assert amount and currency_code, 'Tilopay: missing amount or currency'
        currency_code = self.env['res.currency'].browse(int(currency_code))
        assert self.currency_id.compare_amounts(float(amount), self.amount) == 0, 'Tilopay: mismatching amounts'
        assert currency_code.name == self.currency_id.name, 'Tilopay: mismatching currency codes'


        # Update the provider reference.
        txn_id = notification_data.get('tilopay-transaction')
        if not all((txn_id)):
            raise ValidationError(
                "Tilopay: " + _(
                    "Missing value for txn_id (%(txn_id)s).",
                    txn_id=txn_id
                )
            )
        self.provider_reference = txn_id

        # Update the payment state.
        payment_status = notification_data.get('code')
        _logger.info('-----NOTIFICATION DATA------')
        _logger.info(str(notification_data))
        if payment_status == '1':
            self._set_done()
        elif payment_status != '1':
            self._set_canceled(state_message=notification_data.get('description'))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Tilopay: " + _("Received data with invalid payment status: %s", payment_status)
            )