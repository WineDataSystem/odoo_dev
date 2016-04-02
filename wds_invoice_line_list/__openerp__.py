# -*- coding: utf-8 -*-
{
    'name': 'Invoice Line List',
    'version': '0.1',
    'category': 'Accounting',
    'sequence': 1,
    'summary': 'Add a list of all invoice_line existing',
    'description': """
    Add a list of all invoice_line existing
    """,
    'author': 'WineDataSystem',
    'website': 'https://www.winedatasystem.com',
    'depends': ['account',
                'sale',
                'crm'],
    'data': [
        # Views
        'views/invoice_line_list.xml',

        # Menus
        'menus/invoice_line_list.xml',
    ]
}
