from odoo import models, fields
class ResConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    avna_partner_cc_field=fields.Char()
    avna_partner_subsidy_field=fields.Char()
