# -*- coding: utf-8 -*-

from openerp import fields, models, _, api
from openerp.osv import osv

class sale_force_credit_limit(models.TransientModel):
    _name = 'sale.force.credit.limit'

    @api.model
    def _get_result(self):
        active_id = self.env.context.get('active_id',False)
        sale = self.env['sale.order'].browse(active_id)
        credit = str((sale.partner_id.credit + sale.amount_total))+' '+sale.company_id.currency_id.symbol
        credit_limit = str(sale.partner_id.credit_limit)+' '+sale.company_id.currency_id.symbol
        result = _("""The ongoing credit(%s) and the amount of the order exceeds the credit limit(%s) for that customer.\n\nYou can force this credit limit by clicking the button "Force".""")%(credit,credit_limit)
        return result

    name = fields.Text('Result', required=True, readonly=1, default=_get_result)

    def force_credit_limit(self):
        ids = [self.env.context['active_id']] if self.env.context.get('active_id',False) else []
        self.env['sale.order'].signal_workflow(self.env.cr, self.env.uid, [self.id], 'order_right_confirm')
        return {}
