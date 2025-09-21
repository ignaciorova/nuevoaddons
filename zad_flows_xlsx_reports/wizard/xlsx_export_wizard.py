# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64

class ZadXlsxExportWizard(models.TransientModel):
    _name = 'zad.xlsx.export.wizard'
    _description = 'Export XLSX (Zad Flows)'

    template_id = fields.Many2one('zad.xlsx.template', required=True)
    res_model = fields.Char(default=lambda self: self.env.context.get('active_model'))
    res_id = fields.Integer(default=lambda self: self.env.context.get('active_id'))
    file_name = fields.Char(string='Filename', default='report.xlsx')
    file_data = fields.Binary(string='File', readonly=True)

    def action_generate(self):
        self.ensure_one()
        if not self.res_model or not self.res_id:
            raise UserError(_('No active record found in context.'))
        record = self.env[self.res_model].browse(self.res_id)
        if record._name != self.template_id.model_id.model:
            raise UserError(_('Template model (%s) does not match active record model (%s).') % (self.template_id.model_id.model, record._name))
        content = self.template_id.generate_xlsx_bytes(record)
        self.file_data = base64.b64encode(content)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'zad.xlsx.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
