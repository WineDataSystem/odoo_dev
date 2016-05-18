# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv import osv



class sale_order(models.Model):
    _inherit = "sale.order"

    def check_credit(self):
        if self.partner_id.credit > self.partner_id.credit_limit:
            raise osv.except_osv(_('Erreur'),_('Encours Client dépassé!') )
        return True