from odoo import models, fields
class CafeteriaAudit(models.Model):
    _name='cafeteria.audit'
    name=fields.Char()
