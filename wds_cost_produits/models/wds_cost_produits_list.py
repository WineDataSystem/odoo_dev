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

class wds_cost_produits_list(osv.osv):
    _name = "wds.cost.produits.list"
    _description = "Liste des produits avec leur cout de revient"
    _auto = False
    _rec_name = 'id'

    _columns = {
        # 'date': fields.date('Date', readonly=True),

        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_template_id': fields.many2one('product.template', 'Product templ', readonly=True),
        'date': fields.date('Date', readonly=True),
        'cost': fields.float('Prix de revient', readonly=True),
        }
    _order = 'product_id'

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
        'product_price_history': ['producte_template_id'],
    }

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (select pp.id,ptmp_id, cost, maxdate from product_product pp join (select a.ptmp_id, cost, maxdate from
(select product_template_id ptmp_id , max(datetime) maxdate from product_price_history pph group by product_template_id) a join
product_price_history b on ptmp_id = product_template_id and maxdate=datetime) c on pp.product_tmpl_id=ptmp_id )""" % (self._table))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: