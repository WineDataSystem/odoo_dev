# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class update_wine_product(models.TransientModel):

    _name = 'update.wine.product'

    @api.model
    def _get_product_ids(self):
        res = {}
        wine_id = self._context.get('active_id',False)
        products = self.env['product.template'].search([('product_wine_id','=',wine_id)]).ids
        return products

    @api.model
    def _get_result(self):
        wine_id = self._context.get('active_id',False)
        products = self.env['product.template'].search([('product_wine_id','=',wine_id)])
        product_name = []
        for p in products:
            product_name.append(p.name.encode('utf8'))
        list_product = '\n'.join(product_name)
        result = _("Following the changes, product names below will be updated : \n\n %s" % (list_product))
        return result

    product_ids = fields.Many2many('product.template','product_template_wine_update_rel','product_id','wizard_id','Products',default=_get_product_ids)
    result = fields.Text('Result', default=_get_result)

    @api.one
    def update_products(self):
        for product in self.product_ids:
            product.write({})
        wine_id = self._context.get('active_id',False)
        wine = self.env['wds.product.wine'].browse(wine_id)
        wine.write({'wine_updated':False})
        return {}
