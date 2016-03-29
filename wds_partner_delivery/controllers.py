# -*- coding: utf-8 -*-
# class WdsPartnerDelivery(http.Controller):
#     @http.route('/wds_partner_delivery/wds_partner_delivery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wds_partner_delivery/wds_partner_delivery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wds_partner_delivery.listing', {
#             'root': '/wds_partner_delivery/wds_partner_delivery',
#             'objects': http.request.env['wds_partner_delivery.wds_partner_delivery'].search([]),
#         })

#     @http.route('/wds_partner_delivery/wds_partner_delivery/objects/<model("wds_partner_delivery.wds_partner_delivery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wds_partner_delivery.object', {
#             'object': obj
#         })


from openerp.osv import fields,osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _delivery_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))

        try:
            for partner in self.browse(cr, uid, ids, context):
                res[name] = len(partner.delivery_ids)
        except:
            pass
        return res

    _columns = {
        'delivery_count': fields.function(_delivery_count, string='# of Delivery Order', type='integer'),
        'delivery_ids': fields.one2many('stock.picking','name','Delivery Order')
    }