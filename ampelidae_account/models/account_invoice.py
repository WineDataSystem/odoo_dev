# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class account_invoice(models.Model):

    _inherit = 'account.invoice'

    # @api.onchange('date_invoice')
    # def onchange_date_invoice(self):
    #     period = self.env['account.period'].find(self.env.cr, self.env.uid, self.date_invoice)
    #     self.period_id = period

    @api.multi
    def onchange_payment_term_date_invoice(self, payment_term_id, date_invoice):
        res = super(account_invoice, self).onchange_payment_term_date_invoice(payment_term_id,date_invoice)
        period = self.env['account.period'].find(date_invoice)
        if period:
            res['value'].update({
                'period_id': period.id
            })
        return res
