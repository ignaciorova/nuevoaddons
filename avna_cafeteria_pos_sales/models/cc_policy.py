from odoo import models, fields
class AvnaCCPolicy(models.Model):
    _name='avna.cc.policy'
    analytic_account_id=fields.Many2one('account.analytic.account')
    daily_subsidy_cap=fields.Monetary()
