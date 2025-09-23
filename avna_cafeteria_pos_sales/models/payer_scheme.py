from odoo import models, fields
class AvnaPayerScheme(models.Model):
    _name='avna.payer.scheme'
    name=fields.Char()
    subsidy_code=fields.Char()
    product_id=fields.Many2one('product.product')
    category_id=fields.Many2one('avna.category')
    payer=fields.Selection([('ASEAVNA','ASEAVNA'),('AVNA','AVNA'),('COLAB','Colaborador')])
    amount_mode=fields.Selection([('fixed','Fijo'),('percent','%')])
    amount_value=fields.Float()
