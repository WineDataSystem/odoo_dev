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

class wds_lignes_pos_list(osv.osv):
    _name = "wds.lignes.pos.list"
    _description = "Lignes commandes points de vente"
    _auto = False
    _rec_name = 'id'

    _columns = {
        # 'date': fields.date('Date', readonly=True),
        'id': fields.integer('Id', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Partenaire', readonly=True),
        'date': fields.date('Date', readonly=True),
        'pos_reference': fields.char('Reference Commande', size=128, readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'qty': fields.float('Product Quantity', readonly=True),
        'categ_id': fields.many2one('product.category', 'Category of Product', readonly=True),
        'price_subtotal': fields.float('Total Without Tax', readonly=True),
        'state': fields.char('Order Status',size=64, readonly=True),
        #'state': fields.selection([('invoiced', 'paid', 'Done')], 'Order Status', readonly=True),
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
        cr.execute("""CREATE or REPLACE VIEW %s as (select pol.id ,po.partner_id ,date_order date,pos_reference ,product_id ,
        qty ,categ_id, price_subtotal, po.state
 from pos_order_line pol JOIN pos_order po ON po.id = pol.order_id
JOIN res_partner partner ON po.partner_id = partner.id
                LEFT JOIN product_product pr ON pr.id = pol.product_id
                left JOIN product_template pt ON pt.id = pr.product_tmpl_id
                WHERE ((EXTRACT (YEAR FROM po.date_order) = EXTRACT (YEAR FROM CURRENT_DATE)  or
                EXTRACT (YEAR FROM po.date_order) = EXTRACT (YEAR FROM CURRENT_DATE) -1))
                and po.state in ('paid','invoiced')
 order by partner_id, categ_id, pos_reference, pol.id )""" % (self._table))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: