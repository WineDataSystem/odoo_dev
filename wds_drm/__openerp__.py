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
    'category': 'sales',
    'version': '0.3',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'product',
        'sale',
        'wds_product_wine'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/wds_drm_preview_view.xml',
    ],
    'test': [],
    'js': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'images': [],
    'demo': [],
}
