# -*- coding: utf-8 -*-

{
    'name'          : 'WDS Product',
    'version'       : '0.5',
    'sequence'      : '1',
    'author'        : 'WineDataSystem',
    'category'      : 'Sales',
    'depends'       : [
                       #do not import 'brand_manager' module!!(we have already the folder 'brand' in our project)!
                       'base',
                       'product',
                       # 'crm',
                       # 'sale',
                       # 'document',
                       ],
    'demo'          : [
                       ],
    'description'   : """WineDataSystem Product Definition""",
    'qweb'          : [

                       ],
    'data'          : [

                       'appellation/appellation_view.xml',
                       'brand/product_brand_view.xml',
                       'wine/wine_view.xml',
                       'wine/wine_data.xml',
                       'vintage/product_data.xml',
                       'vintage/product_view.xml',
                       'vintage/press_view.xml',
                       'offers/product_product_view.xml',
                       'offers/product_product_data.xml',
                        'menu_view.xml',

                       #
                       ],
#     'test'             : ['static/src/tests/timer.js'],

    'installable'   : True,
    'auto_install'  : False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
