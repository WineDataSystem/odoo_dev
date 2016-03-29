# -*- coding: utf-8 -*-
{
    'name': "WDS partner Stock Move",

    'summary': """
        Ajout Smart-Button pour les Mouvements de stocks""",

    'description': """
        Add a smart button in order to show stock move linked to a partner
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Partner',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}