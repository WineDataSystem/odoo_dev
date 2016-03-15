# -*- coding: utf-8 -*-
{
    'name': 'Customer Leads Report',
    'category': 'Reporting',
    'summary': 'Module Summary',
    'website': 'odooclass.com',
    'version': '1.0',
    'description': """
Customer Leads Report
        """,
    'author': 'Diogo Duarte',
    'depends': ['base', 'crm'],
    'installable': True,
    'data': [
        'customerleads_view.xml',
        'report/customerleads_view.xml',
    ],
    'demo': [
    ],
    'application': True,
}
