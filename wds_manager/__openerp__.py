# -*- coding: utf-8 -*-


{
    'name': 'WDS Manager Connect',
    'version': '0.1',
    'sequence': '1',
    'author': 'WDS',
    'category': 'Sales Management',
    'depends': ['base','base_geolocalize', 'website_google_map', 'decimal_precision', 'wds_product','mail','product'],
    'demo': [],
    'description': """  Wine Data System Api to Odoo  """,
    'data': [
             'apitodoo_view.xml',
             ],
    'test': [
             ],
    'installable'   : True,
    'auto_install'  : False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
