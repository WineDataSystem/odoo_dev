# -*- coding: utf-8 -*-

{
    'name'          : 'WineDataSystem Partner Name',
    'version'       : '0.5',
    'sequence'      : '1',
    'author'        : 'WDS',
    'category'      : 'CRM',
    'depends'       : [
                       #do not import 'brand_manager' module!!(we have already the folder 'brand' in our project)!

                       ],
    'demo'          : [
                       ],
    'description'   : """Ajout Nom et Prénom sur Partner""",
    'qweb'          : [

                       ],
    'data'          : [
                        #views
                        'views/partner.xml',

                       ],
#     'test'             : ['static/src/tests/timer.js'],

    'images': [],
    'installable'   : True,
    'auto_install'  : False

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
