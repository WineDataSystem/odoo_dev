# -*- coding: utf-8 -*-
{
    'name': "WDS Partner Pro",

    'summary': """
        Fonctions Pro sur clients""",

    'description': """
        Ce module permet d'ajouter des champs pour les professionnels
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'templates.xml',
        # 'views/openacademy.xml',
        'views/partner.xml',
        # 'views/session_workflow.xml',
        # 'reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}