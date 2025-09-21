# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    message = fields.Text(string='WhatsApp Inquiry Message', default='Hello, I am interested in this product.')