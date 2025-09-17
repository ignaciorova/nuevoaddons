from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    twilio_account_sid = fields.Char(string="Twilio Account SID", config_parameter='whatsapp_shopping_bot.twilio_account_sid')
    twilio_account_token = fields.Char(string="Twilio Account Auth Token", config_parameter='whatsapp_shopping_bot.twilio_account_token')
    use_twilio_rtc_servers = fields.Boolean(string="Use Twilio ICE Servers", config_parameter='whatsapp_shopping_bot.use_twilio_rtc_servers', help="If you want to use Twilio as TURN/STUN server provider")