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
        if tot_encours > self.partner_id.credit_limit:
            raise osv.except_osv(_('Erreur'),_('Encours client (%s €) + commande (%s €) dépasse crédit autorisé (%s €)!')%(enc_crd,cette_cmd,limite))
        return True