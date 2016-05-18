# -*- coding: utf-8 -*-

{
    'name'          : 'WDS Check Credit',
    'version'       : '0.1',
    'sequence'      : '1',
    'author'        : 'WDS',
    'website': "http://www.winedatasystem.com",
    'category': 'sales',
    'depends'       : [
                       #do not import 'brand_manager' module!!(we have already the folder 'brand' in our project)!
        'base', 'account', 'sale'
                       ],
    'demo'          : [
                       ],
    'description'   : """Contrôle si encours client dépassé""",
    'qweb'          : [

                       ],
    'data'          : [
                      "workflow/sale_workflow.xml",
                       ],
#     'test'             : ['static/src/tests/timer.js'],

    'images': [],
    'installable'   : True,
    'auto_install'  : False

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
