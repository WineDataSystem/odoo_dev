# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools


class tstram_report(osv.osv):
    _name = "tstram.report"
    _description = "Tstram Report"
    _auto = False
    _rec_name = 'date_invoice'
    _columns = {
        'date_due': fields.date('Order Date'),
        'partner_id': fields.many2one('res.partner', 'Supplier'),
        'type': fields.selection([
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Supplier Invoice'),
            ('out_refund', 'Customer Refund'),
            ('in_refund', 'Supplier Refund'),
        ], string='Type'),
        'four_mnt2014': fields.float('Montant Fournisseurs 2014'),
        'four_mnt2015': fields.float('Montant Fournisseurs 2015'),
        'cli_mnt2014': fields.float('Montant Clients 2014'),
        'cli_mnt2015': fields.float('Montant Clients 2015'),
        'date_invoice': fields.date('Order Date'),
    }
    
    _order = 'date_invoice desc'
    
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'tstram_report')
        cr.execute("""
            create or replace view tstram_report as (
                SELECT
                  i.id,
                  i.date_due,
                  i.partner_id,
                  i.type,
                  case when(i.type='in_invoice' and i.date_invoice >= '2014-01-01' and i.date_invoice <= '2014-12-31' ) then i.amount_total else 0 end four_mnt2014,
                  case when(i.type='in_invoice' and i.date_invoice >= '2015-01-01' and i.date_invoice <= '2015-12-31' ) then i.amount_total else 0 end four_mnt2015,
                  case when(i.type='out_invoice' and i.date_invoice >= '2014-01-01' and i.date_invoice <= '2014-12-31' ) then i.amount_total else 0 end cli_mnt2014,
                  case when(i.type='out_invoice' and i.date_invoice >= '2015-01-01' and i.date_invoice <= '2015-12-31' ) then i.amount_total else 0 end cli_mnt2015,
                  i.date_invoice
                FROM
                  public.account_invoice i)
        """)