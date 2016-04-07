# -*- coding: utf-8 -*-

{
    'name'          : 'WineDataSystem Mailing',
    'version'       : '0.5',
    'sequence'      : '1',
    'author'        : 'WDS',
    'category'      : 'Wine Data Management',
    'depends'       : [
                       #do not import 'brand_manager' module!!(we have already the folder 'brand' in our project)!
                       'mass_mailing',
                       ],
    'demo'          : [
                       ],
    'description'   : """Trade WineDataSystem module""",
    'qweb'          : [

                       ],
    'data'          : [
                        #views
                        'views/partner.xml',

                       ],
#     'test'             : ['static/src/tests/timer.js'],

    'installable'   : True,
    'auto_install'  : False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
