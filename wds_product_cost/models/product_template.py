# -*- coding: utf-8 -*-

from openerp import fields, models, _
import time

class product_template(models.Model):
    _inherit = 'product.template'

    def get_history_price(self, cr, uid, product_tmpl, company_id, date=None, context=None):
        if context is None:
            context = {}
        if date is None:
            date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        price_history_obj = self.pool.get('product.price.history')
        history_ids = price_history_obj.search(cr, uid, [('company_id', '=', company_id), ('product_template_id', '=', product_tmpl), ('datetime', '<=', date)], limit=1)
        if history_ids:
            return price_history_obj.read(cr, uid, history_ids[0], ['cost','datetime'], context=context)['cost','datetime']
        return 0.0
    #
    # _columns = {
    #     'datetime': fields.datetime('Date Cout'),
    # }
