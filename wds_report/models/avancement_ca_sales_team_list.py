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

class avancement_ca_client_list(osv.osv):
    _name = "avancement.ca.sales.team.list"
    _description = "Avancement CA Client par sales team"
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
    def _compute_av(self):
        if self.ca_prev_annee <> 0:
            self.percentca_calc = (((self.ca_annee - self.ca_prev_annee) / self.ca_prev_annee) * 100) +100
        else:
            self.percentca_calc=0


    _columns = {
        # 'date': fields.date('Date', readonly=True),
        'id': fields.many2one('crm.case.section', 'Sales Team'),
        'section_id': fields.many2one('crm.case.section', 'Sales Team'),
        'qty_annee': fields.float('Qté Eq75 N', readonly=True),
        'qty_prev_annee': fields.float('Qté Eq75 N-1', readonly=True),
        'qtye_annee': fields.float('Qté Eq75 N', readonly=True),
        'qtye_prev_annee': fields.float('Qté Eq75 N-1', readonly=True),
        'balance_annee': fields.float('CA N', readonly=True),
        'balance_prev_annee': fields.float('CA N-1', readonly=True),
        'percentca': fields.float('Evolution %', readonly=True),

    }
    _order = 'section_id'

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
            select id, section_id, qty_annee, qty_prev_annee,qtye_annee, qtye_prev_annee, balance_annee,balance_prev_annee,
             CASE when balance_prev_annee =0 then 100 else (((balance_annee - balance_prev_annee) / balance_prev_annee) * 100) +100 end as percentca
             from (select case when ai.section_id is not null then ai.section_id
                     when rp.section_id is not null then rp.section_id
                     else 36 end id,
                     case when ai.section_id is not null then ai.section_id
                     when rp.section_id is not null then rp.section_id
                     else 36 end section_id,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE) then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - l.quantity ELSE l.quantity end else 0 end ) qty_annee ,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE)- 1 then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - l.quantity ELSE l.quantity end else 0 end ) qty_prev_annee ,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE) then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - (l.quantity*factor/0.75) ELSE (l.quantity*factor/0.75) end else 0 end ) qtye_annee ,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE)- 1 then
                    CASE WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                    THEN - (l.quantity*factor/0.75) ELSE (l.quantity*factor/0.75) end else 0 end ) qtye_prev_annee ,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE) then
                    coalesce(l.credit, 0.0) - coalesce(l.debit, 0.0) else 0 end ) balance_annee,
                sum(CASE when EXTRACT (YEAR FROM l.date) = EXTRACT (YEAR FROM CURRENT_DATE) - 1 then
                    coalesce(l.credit, 0.0) - coalesce(l.debit, 0.0) else 0 end ) balance_prev_annee
            from
                account_move_line l
                left join account_account a on (l.account_id = a.id)
                left join account_move am on (am.id=l.move_id)
                left join account_period p on (am.period_id=p.id)
                left join account_invoice ai on l.ref = ai.number
                left join pos_order po on l.ref = po.pos_reference
                left join res_partner rp on l.partner_id= rp.id
                left join product_product pp on l.product_id=pp.id
                left join product_template pt on pp.product_tmpl_id=pt.id
                left join product_uom u on pt.uom_id = u.id
                where l.state != 'draft' and a.code like '70%'
                group by
              case when ai.section_id is not null then ai.section_id
                     when rp.section_id is not null then rp.section_id
                     else 36 end) sub
        """
        return select_str

    def action_avancement_ca_cust_salesteam_list(self, cr, uid, ids, context=None):
        if context is None: context = {}
        if context.get('active_model') != self._name:
            context.update(active_ids=ids, active_model=self._name)
        section_id = self.pool.get("avancement.ca.sales.team.list").create(
            cr, uid, {}, context=context)
        return {
            'name': _("Avancement CA par client dans sales Team"),
            'view_mode': 'list',
            'view_id': False,
            'view_type': 'list',
            'res_model': 'avancement.ca.cust.salesteam.list',
            'res_id': section_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': context
        }

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (%s
            )""" % (
                    self._table,
                    self._select()))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: