# -*- coding: utf-8 -*-
# class WdsPartnerDelivery(http.Controller):
#     @http.route('/wds_partner_delivery_order_bis/wds_partner_delivery_order_bis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wds_partner_delivery_order_bis/wds_partner_delivery_order_bis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wds_partner_delivery_order_bis.listing', {
#             'root': '/wds_partner_delivery_order_bis/wds_partner_delivery_order_bis',
#             'objects': http.request.env['wds_partner_delivery_order_bis.wds_partner_delivery_order_bis'].search([]),
#         })

#     @http.route('/wds_partner_delivery_order_bis/wds_partner_delivery_order_bis/objects/<model("wds_partner_delivery_order_bis.wds_partner_delivery_order_bis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wds_partner_delivery_order_bis.object', {
#             'object': obj
#         })


from openerp.osv import fields,osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _pos_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))

        try:
            for partner in self.browse(cr, uid, ids, context):
               # res[partner.id] = len(partner.pos_ids)
               cr.execute("SELECT partner_id, sum(price_subtotal) \
                       FROM pos_order_line pol \
                       JOIN pos_order po on pol.order_id=po.id \
                       WHERE partner_id = %s \
                       GROUP BY partner_id;", (partner.id,))
               for partner_id, sum in cr.fetchall():
                    if partner_id not in res:
                        res[partner_id] = {}
                    res[partner_id] = sum
        except:
            pass
        return res

    _columns = {
        'pos_amount': fields.function(_pos_count, string='Valeur des POS Order', type='float'),
        #'pos_ids': fields.one2many('pos.order','partner_id','POS Order')
    }
