# -*- coding: utf-8 -*-
{
    'name': "WDS Report",

    'summary': """
        Menu de suivi d'activité""",

    'description': """
        Création d'un menu qui permet d'afficher les rapports spécifiques à WineDataSystem
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','mrp','product'],

    # always loaded
    'data': [
        'security/wdsreport.xml',
        'security/ir.model.access.csv',
        'wds_report.xml',
        'report/account_customer_report_view.xml',
    ],
    'test': [

    ],
    'js': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'images': [],
    # only loaded in demonstration mode
    'demo': [

    ],
}