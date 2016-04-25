# -*- coding: utf-8 -*-
{
    'name': "WDS Coût Produits",

    'summary': """
        Menu de suivi d'activité""",

    'description': """
        Création d'une liste qui permet de gérer les couts de revient des produits
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','mrp','product','product_margin','product_extended','product_email_template'],

    # always loaded
    'data': [''
        'security/wdsprodcost.xml',
        'security/ir.model.access.csv',
        'wds_produits_costs.xml',

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