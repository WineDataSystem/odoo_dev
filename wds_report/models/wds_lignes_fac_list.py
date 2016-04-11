# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools
import openerp.addons.decimal_precision as dp
from datetime import timedelta
from openerp.osv import fields,osv

class wds_lignes_fac_list(osv.osv):
    _name = "wds.lignes.fac.list"
    _description = "Lignes factures"
    _auto = False
    _rec_name = 'id'

    def _compute_amounts_in_user_currency(self, cr, uid, ids, field_names, args, context=None):
        """Compute the amounts in the currency of the user
        """
        if context is None:
            context={}
        currency_obj = self.pool.get('res.currency')
        currency_rate_obj = self.pool.get('res.currency.rate')
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        user_currency_id = user.company_id.currency_id.id
        currency_rate_id = currency_rate_obj.search(
            cr, uid, [
                ('rate', '=', 1),
                '|',
                    ('currency_id.company_id', '=', user.company_id.id),
                    ('currency_id.company_id', '=', False)
                ], limit=1, context=context)[0]
        base_currency_id = currency_rate_obj.browse(cr, uid, currency_rate_id, context=context).currency_id.id
        res = {}
        ctx = context.copy()
        for item in self.browse(cr, uid, ids, context=context):
            ctx['date'] = item.date
            price_total = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_total, context=ctx)
            price_average = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_average, context=ctx)
            residual = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.residual, context=ctx)
            res[item.id] = {
                'user_currency_price_total': price_total,
                'user_currency_price_average': price_average,
                'user_currency_residual': residual,
            }
        return res

    _columns = {
        # 'date': fields.date('Date', readonly=True),
        'id': fields.integer('Id', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Partenaire', readonly=True),
        'date': fields.date('Date', readonly=True),
        'number': fields.char('Reference Facture', size=128, readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'quantity': fields.float('Product Quantity', readonly=True),
        'uom_name': fields.char('Reference Unit of Measure', size=128, readonly=True),
        'currency_id': fields.many2one('res.currency', 'Monnaie', readonly=True),
        'period_id': fields.many2one('account.period', 'Force Period', domain=[('state', '<>', 'done')], readonly=True),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position', readonly=True),
        'categ_id': fields.many2one('product.category', 'Category of Product', readonly=True),
        'price_subtotal': fields.float('Total Without Tax', readonly=True),
        'sequence': fields.integer('Sequence'),
        'type': fields.selection([
            ('out_invoice', 'Customer Invoice'),
            ('in_refund', 'Supplier Refund'),
        ], 'Type', readonly=True),
        'state': fields.selection([
            ('open', 'Open'),
            ('paid', 'Done')
        ], 'Invoice Status', readonly=True),
            }
    _order = 'partner_id, categ_id, product_id'

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term',
            'period_id', 'residual', 'state', 'type', 'user_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uos_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (select ail.id ,ai.partner_id ,date_invoice date,number ,product_id ,
        quantity ,uom.name uom_name, currency_id, period_id,fiscal_position, categ_id, price_subtotal, ai.type, ai.state
 from account_invoice_line ail JOIN account_invoice ai ON ai.id = ail.invoice_id
JOIN res_partner partner ON ai.commercial_partner_id = partner.id
                LEFT JOIN product_product pr ON pr.id = ail.product_id
                left JOIN product_template pt ON pt.id = pr.product_tmpl_id
                LEFT JOIN product_uom u ON u.id = ail.uos_id
                LEFT JOIN product_uom uom ON uom.id = pt.uom_id
  WHERE ((EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE)  or
                EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE) -1) and ai.type in ('out_invoice','out_refund'))
                and ai.state in ('paid','open')
 order by partner_id, categ_id, number, ail.id )""" % (self._table))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: