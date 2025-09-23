from odoo import models, fields
class AvnaTimebandRule(models.Model):
    _name='avna.timeband.rule'
    name=fields.Char()
    start_time=fields.Float()
    end_time=fields.Float()
