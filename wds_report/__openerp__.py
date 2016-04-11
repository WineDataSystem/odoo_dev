# -*- coding: utf-8 -*-
{
    'name': "WDS Report",

    'summary': """
        Menu de suvi d'activité""",

    'description': """
        Création d'un menu qui permet d'afficher la rapports spécifiques à WineDataSystem
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.2b',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wds_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}