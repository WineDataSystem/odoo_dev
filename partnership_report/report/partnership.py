# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools


class partnership_report(osv.osv):
    _name = "partnership.report"
    _description = "Partnership Report"
    _auto = False
    _rec_name = 'date_invoice'
    _columns = {
        'date_due': fields.date('Order Date'),
        'company_id': fields.many2one('res.company', 'Company'),
        'partner_id': fields.many2one('res.partner', 'Supplier'),
        'type': fields.selection([
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Supplier Invoice'),
            ('out_refund', 'Customer Refund'),
            ('in_refund', 'Supplier Refund'),
        ], string='Type'),
        'date_invoice': fields.date('Order Date'),
        'user_id': fields.many2one('res.users', 'User'),
        'amount_total': fields.float('Amount Total'),
        'state': fields.selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
        ], string='Status'),
    }
    
    _order = 'date_invoice desc'
    
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'partnership_report')
        cr.execute("""
            create or replace view partnership_report as (
                SELECT
                  i.id,
                  i.date_due,
                  i.company_id,
                  i.partner_id,
                  i.type,
                  i.state,
                  i.date_invoice,
                  i.user_id,
                  i.amount_total
                FROM
                  account_invoice i
                  )
        """)