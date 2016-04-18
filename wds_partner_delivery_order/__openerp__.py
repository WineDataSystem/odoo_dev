# -*- coding: utf-8 -*-
{
    'name': "WDS partner delivery order",

    'summary': """
        Ajout Smart-Button pour les livraisons""",

    'description': """
        Add a smart button in order to show delivery order linked to a partner
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Partner',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'partner_delivery_order.xml',
    ],
    'images': [],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}