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

class ResPartner(models.Model):
    _inherit = "res.partner"

    first_name = fields.Char('First Name', help="First Name of Customer/Supplier")
    last_name = fields.Char('Last Name', help="First Name of Customer/Supplier")
    surname = fields.Char('Surnmae',help="Surname of Customer/Supplier")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' in vals:
                if not vals['name'] or vals['name'] == '*':
                    if "first_name" in vals and vals['first_name']:
                        vals['name'] = "%s%s%s" % (vals['first_name'] + " " or "", vals["last_name"] + " " or "",
                                                   vals["surname"] + " " or "")
        return super(ResPartner, self).create(vals_list)

    def write(self, values):
        if 'name' in values:
            if not values['name'] or values['name'] == '*':
                if "first_name" in values and values['first_name']:
                    values['name'] = "%s %s %s" % (values['first_name'] or "", values["last_name"] or "",
                                                   values["surname"] or "")
        return super(ResPartner, self).write(values)