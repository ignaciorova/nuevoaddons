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
from odoo import api, fields, models

class TilopayPaymentsAvailable(models.Model):
    _name="tilopay.payments.availables"
    _description = "Tilopay Payment Availables"
    _order = "sequence ASC"

    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)
    sequence = fields.Integer("Sequence",default=1)
    acquirer_id = fields.Many2one('payment.provider','Provider',required=True)