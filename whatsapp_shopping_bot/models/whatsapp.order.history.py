from odoo import api, fields, models

class WhatsappOrderHistory(models.Model):
    _name = 'whatsapp.order.history'
    _description = 'WhatsApp Order History'
    _order = 'sent_date desc'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Customer", related='sale_order_id.partner_id', store=True, readonly=True)
    whatsapp_number = fields.Char(string="WhatsApp Number", related='partner_id.mobile', store=True, readonly=True)
    message_body = fields.Text(string="Message Body", readonly=True)
    sent_date = fields.Datetime(string="Sent Date", default=fields.Datetime.now, readonly=True)
    status = fields.Selection([
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ], string="Status", default='sent', readonly=True)
    error_message = fields.Text(string="Error Message", readonly=True)

    @api.model
    def create_history(self, sale_order, message_body, status='sent', error_message=None):
        vals = {
            'sale_order_id': sale_order.id,
            'message_body': message_body,
            'status': status,
            'error_message': error_message,
        }
        return self.create(vals)