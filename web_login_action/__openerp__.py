# -*- coding: utf-8 -*-
{
    'name': 'Web Login Action',
    'category': 'Uncategorized',
    'summary': 'Creates a one time login action',
    'website': 'https://odooclass.com',
    'version': '1.0',
    'description': """
Creates a one time login action
        """,
    'author': 'Diogo Duarte',
    'depends': ['base','web'],
    'installable': True,
    'data': [
        'templates.xml',
        'res_users_view.xml',
    ],
    'demo': [
    ],
    'application': True,
}
