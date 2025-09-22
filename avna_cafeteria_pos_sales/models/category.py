from odoo import models, fields
class AvnaCategory(models.Model):
    _name='avna.category'
    name=fields.Char()
    code=fields.Char()
class AvnaCategorySynonym(models.Model):
    _name='avna.category.synonym'
    category_id=fields.Many2one('avna.category')
    token=fields.Char()
