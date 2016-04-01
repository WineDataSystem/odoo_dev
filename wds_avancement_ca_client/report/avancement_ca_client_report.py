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

class avancement_ca_client_report(osv.osv):
    _name = "avancement.ca.client.report"
    _description = "Avancement CA Client"
    _auto = False
    _rec_name = 'partner_id'

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
        'partner_id': fields.many2one('res.partner', 'Partenaire', readonly=True),
        'invoicenb': fields.float('Invoice Num', readonly=True),
        'currency_id': fields.many2one('res.currency', 'Monnaie', readonly=True),
        'company_id': fields.many2one('res.company', 'Societe', readonly=True),
        'user_id': fields.many2one('res.users', 'Vendeur', readonly=True),
        'ca_annee': fields.float('CA Année en cours', readonly=True),
        'ca_prev_annee': fields.float('CA Année précédente', readonly=True),
        'percentca': fields.float('Avancement %', readonly=True),
        # 'user_currency_price_average': fields.function(_compute_amounts_in_user_currency, string="Prix de Vente Moyen", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
        # 'currency_rate': fields.float('Currency Rate', readonly=True),
        'nbr': fields.integer('Nb Ligne de facture', readonly=True),
    }
    _order = 'ca_annee desc'

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

    def _select(self):
        select_str = """
            SELECT sub.id, sub.partner_id,sub.invoicenb,sub.currency_id,sub.ca_annee, sub.ca_prev_annee,
            CASE when sub.ca_prev_annee =0 then 100 else (((sub.ca_annee - sub.ca_prev_annee) / sub.ca_prev_annee) * 100) +100 end as percentca,
            sub.nbr
        """
        return select_str

    def _sub_select(self):
        select_str = """
                SELECT min(ai.partner_id) as id, ai.partner_id ,
                    count(distinct ai.number) AS invoicenb,
                    ai.currency_id,
                    sum(CASE when EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE) then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - ai.amount_total ELSE ai.amount_total end else 0 end ) ca_annee ,
                    sum(CASE when EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE) -1  then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - ai.amount_total ELSE ai.amount_total end else 0 end ) ca_prev_annee,
                    count(*) AS nbr
        """
        return select_str

    def _from(self):
        from_str = """
                FROM  account_invoice ai
                JOIN res_partner partner ON ai.partner_id = partner.id
                WHERE (EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE)  or
                EXTRACT (YEAR FROM ai.date_invoice) = EXTRACT (YEAR FROM CURRENT_DATE) -1) and ai.type in ('out_invoice','out_refund')
                and ai.state = 'paid'
        """
        return from_str

    def _group_by(self):
        group_by_str = """
                GROUP BY partner_id,ai.currency_id
        """
        return group_by_str

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (

            %s
            FROM (
                %s %s %s
            ) AS sub

        )""" % (
                    self._table,
                    self._select(), self._sub_select(), self._from(), self._group_by()))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: