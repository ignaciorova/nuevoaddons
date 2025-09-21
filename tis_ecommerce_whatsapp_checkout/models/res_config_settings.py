# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2024. All rights reserved.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Inherit res config settings to add fields"""
    _inherit = 'res.config.settings'

    whatsapp_number = fields.Char(string='WhatsApp Number', related='website_id.whatsapp_number',
                                  config_parameter='tis_ecommerce_whatsapp_checkout.whatsapp_number',
                                  help="Whatsapp Number")
    whatsapp_checkout = fields.Selection(related='website_id.whatsapp_checkout', readonly=False,
                                         help="Whatsapp checkout button visibility")
