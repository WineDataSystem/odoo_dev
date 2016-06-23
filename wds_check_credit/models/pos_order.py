# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv import osv

import logging
_logger = logging.getLogger(__name__)

class pos_order(osv.osv):
    _inherit = "pos.order"

    def check_credit(self):
        # _logger.info(self.uid)
        enc_crd = self.partner_id.credit
        limite = self.partner_id.credit_limit
        cette_cmd = self.amount_total
        tot_encours= self.partner_id.credit + self.amount_total

        if self.partner_id.credit_limit > 0 and tot_encours > self.partner_id.credit_limit:
            enc_crd = str(enc_crd)+' '+self.company_id.currency_id.symbol
            limite = str(limite)+' '+self.company_id.currency_id.symbol
            raise osv.except_osv(_('Erreur'),_('The ongoing credit(%s) and the amount of the order exceeds the credit limit(%s) for that customer.')%(enc_crd,limite))
        return True

    def check_credit_from_ui(self, cr, uid, partner_id, amount_total):
        partner = self.pool.get('res.partner').browse(cr,uid,partner_id)
        total_in_progress = partner.credit + amount_total

        if partner.credit > 0 and total_in_progress > partner.credit_limit:
            return False, partner.credit
        return True
