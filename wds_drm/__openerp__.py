# -*- coding: utf-8 -*-
{
    'name': "WDS DRM",

    'summary': """
        Menu Déclaration Récapitulative Mensuelle""",

    'description': """
        Création d'un menu qui permet d'afficher les rapports de la Déclaration Récapitulative Mensuelle
    """,

    'author': "WineDataSystem",
    'website': "http://www.winedatasystem.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','mrp','product','sale','wds_zip_to_invoice'],

    # always loaded
    'data': [
        'wds_drm.xml',
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