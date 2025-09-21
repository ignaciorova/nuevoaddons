# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.

import re
from odoo import fields, models
from odoo.exceptions import ValidationError


class Website(models.Model):
    """Inherit website to add fields"""
    _inherit = 'website'

    whatsapp_number = fields.Char(string="WhatsApp Number", help="WhatsApp Number")
    whatsapp_check_out = fields.Boolean(string="WhatsApp Checkout", help="Enable if WhatsApp checkout is needed")
    whatsapp_checkout = fields.Selection(
        selection=[
            ('public_users', 'Public Users'),
            ('login_users', 'Login Users'),
        ],
        default='public_users', help="WhatsApp checkout button visibility")

    def write(self, vals):
        """Override write to check valid WhatsApp number is provided"""
        res = super(Website, self).write(vals)
        if self.whatsapp_number:
            pattern = re.compile(r'^\d{10}$')
            if not pattern.match(self.whatsapp_number):
                raise ValidationError(
                    "The phone number '%s' is not valid. It should be exactly 10 digits long and contain only numeric characters." % self.whatsapp_number)
        return res