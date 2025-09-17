from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from twilio.rest import Client
from odoo.addons.queue_job.job import job
import logging

_logger = logging.getLogger(__name__)

class TwilioWhatsapp(models.Model):
    _name = 'wk.twilio.whatsapp'
    _description = 'Twilio WhatsApp Integration'
    _rec_name = 'user_mobile_no'

    user_mobile_no = fields.Char(string="User Mobile Number", required=True, help="e.g. +919898989898")
    twilio_whatsapp_number = fields.Char(string="Twilio WhatsApp Phone Number", help="Twilio Phone Number (e.g. +12044993370)")
    account_whatsapp_sid = fields.Char(string="Twilio WhatsApp Account SID", required=True)
    auth_whatsapp_token = fields.Char(string="Twilio WhatsApp Auth Token", required=True, password=True)
    message_template = fields.Text(
        string="WhatsApp Message Template",
        default="Thank you for your order, {name}! Order Reference: {order_ref}",
        help="Template for WhatsApp messages. Use {name} for customer name and {order_ref} for order reference."
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._validate_twilio_credentials()
        return res

    def write(self, vals):
        res = super().write(vals)
        self._validate_twilio_credentials()
        return res

    def _validate_twilio_credentials(self):
        for rec in self:
            if not rec.account_whatsapp_sid or not rec.auth_whatsapp_token:
                raise ValidationError(_("Twilio SID and Token are required."))

    def test_conn_twilio_whatsapp(self):
        self.ensure_one()
        try:
            client = Client(self.account_whatsapp_sid, self.auth_whatsapp_token)
            account = client.api.v2010.accounts(self.account_whatsapp_sid).fetch()
            _logger.info("Twilio connection successful: %s", account.friendly_name)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Twilio WhatsApp connection tested successfully!'),
                    'sticky': False,
                    'type': 'success',
                }
            }
        except Exception as e:
            _logger.error("Twilio connection failed: %s", str(e))
            raise UserError(_("Connection test failed: %s") % str(e))

    @job(default_channel='root.whatsapp')
    def send_whatsapp_message(self, sale_order, whatsapp_number, message_body):
        self.ensure_one()
        try:
            client = Client(self.account_whatsapp_sid, self.auth_whatsapp_token)
            client.messages.create(
                from_='whatsapp:' + self.twilio_whatsapp_number,
                to='whatsapp:' + whatsapp_number,
                body=message_body
            )
            _logger.info("WhatsApp message sent for order %s", sale_order.name)
            self.env['whatsapp.order.history'].sudo().create_history(sale_order, message_body)
        except Exception as e:
            _logger.error("Failed to send WhatsApp message for order %s: %s", sale_order.name, str(e))
            self.env['whatsapp.order.history'].sudo().create_history(sale_order, message_body, status='failed', error_message=str(e))
            raise