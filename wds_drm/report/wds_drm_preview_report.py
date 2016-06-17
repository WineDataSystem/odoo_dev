# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 Noviat nv/sa (www.noviat.com). All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools, models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

MONTHS = [
    (1,_('January')),
    (2,_('February')),
    (3,_('March')),
    (4,_('April')),
    (5,_('May')),
    (6,_('June')),
    (7,_('July')),
    (8,_('August')),
    (9,_('September')),
    (10,_('October')),
    (11,_('November')),
    (12,_('December')),
]

class wds_drm_preview_report(models.Model):
    _name = "wds.drm.preview.report"
    _description = "Preview DRM"
    _auto = False
    _order = 'date desc'

    date = fields.Date('Date',required=True)
    month = fields.Selection(MONTHS,'Month',required=True)
    year = fields.Char('Year',required=True)
    product_id = fields.Many2one('product.template','Product',required=True)
    winetax = fields.Selection([(tax, str(tax)) for tax in ['CRD','Neutre','Acquit','?']], 'Wine Tax')
    wine_type_id = fields.Many2one('wds.wine.type','Wine Type', required=True)
    appellation_id = fields.Many2one('wds.appellation','appellation', required=True)
    volume = fields.Float('Volume (L)',digits=(12,5),required=True)
    country_id = fields.Many2one('res.country','Destination country',required=True)
    country_group_id = fields.Many2one('res.country.group','Country Group',required=True)
    partner_id = fields.Many2one('res.partner','Partner',required=True)
    alcoholic_strength = fields.Float(tools.ustr('Alcoholic strength (%vol.)'))
    w_iswine = fields.Boolean('Select if wine', required=True)
    warehouse_id = fields.Many2one('stock.warehouse','Warehouse',required=True)


    def init(self,cr):
        default_country_ref = self.pool['ir.model.data'].get_object_reference(cr,1,'base','fr')
        default_country_id = default_country_ref and default_country_ref[1] or False
        case_country = 'CASE WHEN part.country_id is Null THEN %s ELSE part.country_id END' % default_country_id

        default_group_country_ref = self.pool['ir.model.data'].get_object_reference(cr,1,'base','europe')
        default_group_country_id = default_group_country_ref and default_group_country_ref[1] or False
        tools.drop_view_if_exists(cr, 'wds_drm_preview_report')
        cr.execute("""CREATE or REPLACE view wds_drm_preview_report as (
                SELECT
                    m.id as id,
                    m.date date,
                    EXTRACT (MONTH FROM m.date) as month,
                    EXTRACT (YEAR FROM m.date) as year,
                    pt.id as product_id,
                    pt.winetax as winetax,
                    w.wine_type_id as wine_type_id,
                    w.appellation_id as appellation_id,
                    {0} as country_id,
                    CASE WHEN cg_rel.res_country_group_id is not Null THEN cg_rel.res_country_group_id ELSE {1} END as country_group_id,
                    CASE WHEN m.partner_id is Null THEN sp.partner_id ELSE m.partner_id END as partner_id,
                    pt.alcoholic_strength as alcoholic_strength,
                    pt.w_iswine as w_iswine,
                    CASE WHEN m.warehouse_id is Null THEN
                        (CASE WHEN spt.warehouse_id is not Null THEN
                            spt.warehouse_id else sw.id
                        END)
                        ELSE m.warehouse_id
                    END as warehouse_id,
                    (CASE WHEN pu.uom_type = 'bigger' THEN product_uom_qty*pu.factor ELSE product_uom_qty/pu.factor END) as volume
                FROM stock_move m LEFT JOIN product_product p ON p.id = m.product_id
                LEFT JOIN product_uom pu ON pu.id = m.product_uom
                LEFT JOIN stock_picking_type spt ON spt.id = m.picking_type_id
                LEFT JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
                LEFT JOIN stock_picking sp ON sp.id = m.picking_id
                LEFT JOIN product_template pt ON pt.id = p.product_tmpl_id
                LEFT JOIN res_partner part ON part.id = m.partner_id
                LEFT JOIN wds_product_wine w ON w.id = pt.product_wine_id
                LEFT JOIN res_country c ON c.id = ({0})
                LEFT JOIN res_country_res_country_group_rel cg_rel ON cg_rel.res_country_id = ({0})
                WHERE spt.code = 'outgoing'
                AND m.state = 'done')
            """.format(case_country,default_group_country_id))
