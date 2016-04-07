# -*- coding: utf-8 -*-
from openerp import http

# class WdsMenu(http.Controller):
#     @http.route('/wds_menu/wds_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wds_menu/wds_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wds_menu.listing', {
#             'root': '/wds_menu/wds_menu',
#             'objects': http.request.env['wds_menu.wds_menu'].search([]),
#         })

#     @http.route('/wds_menu/wds_menu/objects/<model("wds_menu.wds_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wds_menu.object', {
#             'object': obj
#         })