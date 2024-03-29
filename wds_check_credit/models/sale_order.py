# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv import osv



class sale_order(models.Model):
    _inherit = "sale.order"

    def check_credit(self):
        enc_crd = self.partner_id.credit
        limite = self.partner_id.credit_limit
        cette_cmd = self.amount_total
        tot_encours= self.partner_id.credit + self.amount_total

        # if self.partner_id.credit > self.partner_id.credit_limit:
        if self.partner_id.credit_limit > 0 and tot_encours > self.partner_id.credit_limit:
            enc_crd = str(enc_crd)+' '+self.company_id.currency_id.symbol
            limite = str(limite)+' '+self.company_id.currency_id.symbol
            raise osv.except_osv(_('Erreur'),_('The ongoing credit(%s) and the amount of the order exceeds the credit limit(%s) for that customer.')%(enc_crd,limite))
        return True
