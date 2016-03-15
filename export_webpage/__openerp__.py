# -*- coding: utf-8 -*-
{
    'name': "export_webpage",

    'summary': """
        Website Page Export
        exports webpages to another version""",

    'description': """
        This module allows to exports webpages to another version ..
    """,
    'author': "Diogo Duarte",
    'website': "http://odooclass.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/pageexport_view.xml',
    ],
    'demo': [
    ],
}