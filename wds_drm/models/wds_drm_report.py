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

class wds_drm_report(osv.osv):
    _name = "wds.drm.report"
    _description = "DRM"
    _auto = False
    # _rec_name = 'id'



    _columns = {
        'id': fields.integer('Id', readonly=True),
        'period': fields.char('Période', readonly=True),
        'location_id': fields.many2one('stock.location', 'Location', required=True, readonly=True),
        'docdouane': fields.char('Document Douanier', size=128, readonly=True),
        'partner_id': fields.many2one('res.partner', 'Partenaire', readonly=True),
        'origin': fields.char('Source Document', readonly=True),
        'sit_fisc': fields.char('Situation fiscale',size=128, readonly=True),
        'cum_hl': fields.float('Volume en HL', readonly=True),

    }


    _depends = {
        'account.invoice': [
            'account_id', 'amount_total', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term',
            'period_id', 'residual', 'state', 'type', 'user_id','number',
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
            select partner_id id,
            period, location_id , docdouane, partner_id, origin, sit_fisc,cum_hl
            from (
            select period,location_id,docdouane,
            Case when docdouane in ('DAE','DAA') then partner_id else 507 end partner_id,
            Case when docdouane in ('DAE','DAA') then origin else '   ' end origin,
            Case when docdouane in ('DAE','DAA') and zone_livr = 'FR' then 'SUSPENSION'
                 when docdouane in ('DAE','DAA') and zone_livr <> 'FR' then 'EXONERATION'
                 else 'DROITS ACQUITTES' end sit_fisc,
            sum(cumqty)/100 cum_hl
            from
            (
            select period, location_id ,
            case when sub.winetax <> 'CRD' or zone_livr = 'EU' then 'DAE'
                 when zone_livr= 'HEU' then 'DAA'
                 else '   ' end docdouane,
            partner_id,
            cumqty,
            origin,
            zone_livr

            from
            (select (EXTRACT (YEAR FROM sm.date) * 100) + EXTRACT (month FROM sm.date) period, location_id,pu.name,pu.uom_type, pu.factor, origin,
            partner_id,spt.name,
            CASE WHEN spt.name = 'PoS Orders' then 'FR'
                 WHEN rp.country_id = 76 then 'FR'
                 WHEN rp.country_id is NULL then 'FR'
                 WHEN rcg.name in ('Suède','ROE') then 'EU'
                 ELSE 'HEU' end zone_livr,
                 pt.winetax,
                 rc.name,
            case when uom_type = 'bigger' then sum(product_uom_qty*factor) else sum(product_uom_qty/factor) end cumqty, sum(product_uom_qty)
            from stock_move sm join product_uom pu on sm.product_uom = pu.id
            join stock_picking_type spt on picking_type_id=spt.id
            left outer join res_partner rp on sm.partner_id=rp.id
            left outer join res_country rc on rp.country_id = rc.id
            left outer join res_country_res_country_group_rel rcgr on rp.country_id = rcgr.res_country_id
            left outer join res_country_group rcg on rcgr.res_country_group_id = rcg.id
            join product_product pp on sm.product_id= pp.id
            join product_template pt on pp.product_tmpl_id= pt.id
            where pu.category_id = 5 and spt.code = 'outgoing'
            group by EXTRACT (YEAR FROM sm.date) , EXTRACT (MONTH FROM sm.date) , location_id,pu.name, pu.factor,pu.uom_type, origin, partner_id,spt.name
            ,rp.country_id,rcg.name,rc.name,pt.winetax) sub) sub2
            group by period, location_id , DOCDOUANE,
            Case when DOCDOUANE in ('DAE','DAA') then partner_id else 507 end ,
            Case when docdouane in ('DAE','DAA') then origin else '   ' end ,
            Case when DOCDOUANE in ('DAE','DAA') and zone_livr = 'FR' then 'SUSPENSION'
                 when DOCDOUANE in ('DAE','DAA') and zone_livr <> 'FR' then 'EXONERATION'
                 else 'DROITS ACQUITTES' end ) sub3
                 order by period,location_id
             """
        return select_str

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (%s
            )""" % (
                    self._table,
                    self._select()))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: