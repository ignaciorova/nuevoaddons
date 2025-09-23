from odoo import models, fields
class AvnaCategoryLimit(models.Model):
    _name='avna.category.limit'
    category_id=fields.Many2one('avna.category')
    per_day=fields.Integer(default=1)
