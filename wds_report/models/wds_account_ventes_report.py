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
    _description = "Analyse des ventes"
    _auto = False
    _rec_name = 'date'
    _columns = {
        'date': fields.date('Date ', readonly=True),  # TDE FIXME master: rename into date_effective
        'date_created': fields.date('Date de création', readonly=True),
        'date_maturity': fields.date('Date Maturity', readonly=True),
        'fiscal_position': fields.many2one('account.fiscal.position','Fiscal Position', readonly=True),
        'ref': fields.char('Reference', readonly=True),
        'typref':fields.char('Type de ventes', readonly=True),
        'description': fields.char('Description', readonly=True),
        'nbr': fields.integer('# d\'éléments', readonly=True),
        'debit': fields.float('Debit', readonly=True),
        'credit': fields.float('Credit', readonly=True),
        'balance': fields.float('CA', readonly=True),
        'currency_id': fields.many2one('res.currency', 'Monnaie', readonly=True),
        'country_id': fields.many2one('res.country', 'Pays',readonly=True),
        'country_group_id': fields.many2one('res.country.group', 'Groupe Pays', readonly=True),
        'amount_currency': fields.float('Amount Currency', digits_compute=dp.get_precision('Account'), readonly=True),
        'period_id': fields.many2one('account.period', 'Période', readonly=True),
        'account_id': fields.many2one('account.account', 'Compte', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', readonly=True),
        'product_id': fields.many2one('product.product', 'Produit', readonly=True),
        'categ_id': fields.many2one('product.category', 'Catégorie Produit', readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'Unité de mesure', readonly=True),
        'move_state': fields.selection([('draft','Unposted'), ('posted','Posted')], 'Status', readonly=True),
        'move_line_state': fields.selection([('draft','Unbalanced'), ('valid','Valid')], 'State of Move Line', readonly=True),
        'reconcile_id': fields.many2one('account.move.reconcile', '', readonly=True),
        'partner_id': fields.many2one('res.partner','Partenaire', readonly=True),
        'section_id': fields.many2one('crm.case.section', 'Equipe de vente', readonly=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Compte analytique', readonly=True),
        'quantity': fields.float('Quantité', digits=(16,2), readonly=True),  # TDE FIXME master: rename into product_quantity
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
            select id, date, date_maturity,date_created,fiscal_position,ref,typref,move_state,reconcile_id,partner_id,
            section_id,description,product_id,categ_id,product_uom_id,company_id,journal_id,fiscalyear_id,period_id,account_id,type,
            user_type,nbr,quantity,currency_id,country_id,
            case when res_country_group_id is NULL or res_country_group_id=0 then 1 else res_country_group_id end country_group_id,
            amount_currency,debit,credit,balance from (
            select
                l.id as id,
                am.date as date,
                l.date_maturity as date_maturity,
                l.date_created as date_created,
                case when ai.fiscal_position is NULL then 4
                when ai.fiscal_position=0 then 4
                else ai.fiscal_position end fiscal_position,
                case when am.name is not NULL then am.name else l.ref end as ref,
                case when substring(l.ref, 1 , 1)= 'F' or upper(substring(l.ref, 1 , 2))='SO' then '1-FAC'
                     when substring(l.ref, 1 , 1)in ('M','N','P') then '2-POS' else '3-AUT' end as typref,
                am.state as move_state,
                l.state as move_line_state,
                l.reconcile_id as reconcile_id,
                l.partner_id as partner_id,
                case when ai.section_id is not null then ai.section_id
                     when rp.section_id is not null then rp.section_id
                     else 36 end section_id,
                l.name as description,
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
                case when rp.country_id is NULL or rp.country_id=0 then 76
                when ai.fiscal_position=0 then 76
                else rp.country_id end country_id,
                l.amount_currency as amount_currency,
                l.debit as debit,
                l.credit as credit,
                coalesce(l.credit, 0.0) - coalesce(l.debit, 0.0) as balance
            from
                account_move_line l
                left join account_account a on (l.account_id = a.id)
                left join account_move am on (am.id=l.move_id) and l.ref not like 'POS%'
                left join account_period p on (am.period_id=p.id)
                left join account_invoice ai on (case when am.name is not null then am.name else l.ref end) = ai.number
                left join pos_order po on l.ref = po.pos_reference
                left join res_partner rp on l.partner_id= rp.id
                left join product_product pp on l.product_id=pp.id
                left join product_template pt on pp.product_tmpl_id=pt.id
                where l.state != 'draft' and a.code like '70%'
            ) y left join res_country_res_country_group_rel rcrcg on country_id=rcrcg.res_country_id)
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
