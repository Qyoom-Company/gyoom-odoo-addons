from odoo import models, fields

class JournalAccount(models.Model):
    _inherit = 'account.journal'

    company_id = fields.Many2one(readonly=False)
    company_partner_id = fields.Many2one(readonly=False)
