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
from openerp.osv import fields,osv
import openerp.addons.decimal_precision as dp

class wds_account_ventes_report(osv.osv):
    _name = "wds.account.ventes.report"
    _description = "Journal Ventes Analysis"
    _auto = False
    _rec_name = 'date'
    _columns = {
        'date': fields.date('Effective Date', readonly=True),  # TDE FIXME master: rename into date_effective
        'date_created': fields.date('Date Created', readonly=True),
        'date_maturity': fields.date('Date Maturity', readonly=True),
        'fiscal_position': fields.many2one('account.fiscal.position','Fiscal Position', readonly=True),
        'ref': fields.char('Reference', readonly=True),
        'typref':fields.char('TypeRef', readonly=True),
        'nbr': fields.integer('# of Items', readonly=True),
        'debit': fields.float('Debit', readonly=True),
        'credit': fields.float('Credit', readonly=True),
        'balance': fields.float('Montant', readonly=True),
        'currency_id': fields.many2one('res.currency', 'Currency', readonly=True),
        'country_id': fields.many2one('res.country', 'Country',readonly=True),
        'amount_currency': fields.float('Amount Currency', digits_compute=dp.get_precision('Account'), readonly=True),
        'period_id': fields.many2one('account.period', 'Period', readonly=True),
        'account_id': fields.many2one('account.account', 'Account', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'categ_id': fields.many2one('product.category', 'Category of Product', readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'Product Unit of Measure', readonly=True),
        'move_state': fields.selection([('draft','Unposted'), ('posted','Posted')], 'Status', readonly=True),
        'move_line_state': fields.selection([('draft','Unbalanced'), ('valid','Valid')], 'State of Move Line', readonly=True),
        'reconcile_id': fields.many2one('account.move.reconcile', 'Reconciliation number', readonly=True),
        'partner_id': fields.many2one('res.partner','Partner', readonly=True),
        'section_id': fields.many2one('crm.case.section', 'Sales Team', readonly=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
        'quantity': fields.float('Products Quantity', digits=(16,2), readonly=True),  # TDE FIXME master: rename into product_quantity
        'user_type': fields.many2one('account.account.type', 'Account Type', readonly=True),
        'type': fields.selection([
            ('receivable', 'Receivable'),
            ('payable', 'Payable'),
            ('cash', 'Cash'),
            ('view', 'View'),
            ('consolidation', 'Consolidation'),
            ('other', 'Regular'),
            ('closed', 'Closed'),
        ], 'Internal Type', readonly=True, help="This type is used to differentiate types with "\
            "special effects in Odoo: view can not have entries, consolidation are accounts that "\
            "can have children accounts for multi-company consolidations, payable/receivable are for "\
            "partners accounts (for debit/credit computations), closed for depreciated accounts."),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
    }

    _order = 'date desc'

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        for arg in args:
            if arg[0] == 'period_id' and arg[2] == 'current_period':
                current_period = period_obj.find(cr, uid, context=context)[0]
                args.append(['period_id','in',[current_period]])
                break
            elif arg[0] == 'period_id' and arg[2] == 'current_year':
                current_year = fiscalyear_obj.find(cr, uid)
                ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
                args.append(['period_id','in',ids])
        for a in [['period_id','in','current_year'], ['period_id','in','current_period']]:
            if a in args:
                args.remove(a)
        return super(wds_account_ventes_report, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False,lazy=True):
        if context is None:
            context = {}
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        if context.get('period', False) == 'current_period':
            current_period = period_obj.find(cr, uid, context=context)[0]
            domain.append(['period_id','in',[current_period]])
        elif context.get('year', False) == 'current_year':
            current_year = fiscalyear_obj.find(cr, uid)
            ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
            domain.append(['period_id','in',ids])
        else:
            domain = domain
        return super(wds_account_ventes_report, self).read_group(cr, uid, domain, fields, groupby, offset, limit, context, orderby,lazy)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'wds_account_ventes_report')
        cr.execute("""
            create or replace view wds_account_ventes_report as (
            select
                l.id as id,
                am.date as date,
                l.date_maturity as date_maturity,
                l.date_created as date_created,
                case when ai.fiscal_position is NULL then 4
                when ai.fiscal_position=0 then 4
                else ai.fiscal_position end fiscal_position,
                am.ref as ref,
                case when substring(am.ref, 1 , 1)= 'F' or upper(substring(am.ref, 1 , 2))='SO' then '1-FAC'
                     when substring(am.ref, 1 , 1)in ('M','N','P') then '2-POS' else '3-AUT' end as typref,
                am.state as move_state,
                l.state as move_line_state,
                l.reconcile_id as reconcile_id,
                l.partner_id as partner_id,
                case when ai.section_id is not null then ai.section_id
                     when rp.section_id is not null then rp.section_id
                     else 36 end section_id,
                l.product_id as product_id,
                case when categ_id is not null then categ_id else 304 end categ_id,
                l.product_uom_id as product_uom_id,
                am.company_id as company_id,
                am.journal_id as journal_id,
                p.fiscalyear_id as fiscalyear_id,
                am.period_id as period_id,
                l.account_id as account_id,
                l.analytic_account_id as analytic_account_id,
                a.type as type,
                a.user_type as user_type,
                1 as nbr,
                l.quantity as quantity,
                l.currency_id as currency_id,
                case when rp.country_id is NULL or rp.country_id=0 then 76 else rp.country_id end country_id,
                l.amount_currency as amount_currency,
                l.debit as debit,
                l.credit as credit,
                coalesce(l.credit, 0.0) - coalesce(l.debit, 0.0) as balance
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
                where l.state != 'draft' and a.code like '70%'
            )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
