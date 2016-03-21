# -*- coding: utf-8 -*-

{
    'name' : 'WDS_Customer_report',
    'version' : '1.0',
    'author' : 'WineDataSystem',
    'category' : 'Sales',
    'description' : """

    """,
    'website': 'https://www.winedatasystem.com/',
    'depends' : ['base_setup', 'product', 'analytic', 'board', 'edi', 'report'],
    'data': [
        'report/account_invoice_report_view_wds.xml',
    ],
    'qweb' : [

    ],
    'demo': [

    ],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
