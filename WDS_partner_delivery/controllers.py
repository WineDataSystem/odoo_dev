# -*- coding: utf-8 -*-
# class WdsPartnerDelivery(http.Controller):
#     @http.route('/WDS_partner_delivery/WDS_partner_delivery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/WDS_partner_delivery/WDS_partner_delivery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('WDS_partner_delivery.listing', {
#             'root': '/WDS_partner_delivery/WDS_partner_delivery',
#             'objects': http.request.env['WDS_partner_delivery.WDS_partner_delivery'].search([]),
#         })

#     @http.route('/WDS_partner_delivery/WDS_partner_delivery/objects/<model("WDS_partner_delivery.WDS_partner_delivery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('WDS_partner_delivery.object', {
#             'object': obj
#         })


from openerp.osv import fields,osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _delivery_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))

        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(partner.delivery_ids)
        except:
            pass
        return res

    _columns = {
        'delivery_count': fields.function(_delivery_count, string='# of Delivery Order', type='integer'),
        'delivery_ids': fields.one2many('stock.move','partner_id','Delivery Order')
    }