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
        active_id = self._context.get('active_id',False)
        if self._context.get('active_model',False) == 'product.template':
            product = self.env['product.template'].browse(active_id)
            products = self.env['product.template'].search([('product_wine_id','=',product.product_wine_id.id),('id','!=',product.id)]).ids
        else:
            products = self.env['product.template'].search([('product_wine_id','=',active_id)]).ids
        return products

    @api.model
    def _get_result(self):
        active_id = self._context.get('active_id',False)
        if self._context.get('active_model',False) == 'product.template':
            product = self.env['product.template'].browse(active_id)
            products = self.env['product.template'].search([('product_wine_id','=',product.product_wine_id.id),('id','!=',product.id)])
        else:
            products = self.env['product.template'].search([('product_wine_id','=',active_id)])
        product_name = []
        for p in products:
            _logger.info(p)
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
        active_id = self._context.get('active_id',False)
        if self._context.get('active_model',False) == 'product.template':
            product = self.env['product.template'].browse(active_id)
            product.product_wine_id.write({'wine_updated':False})
        else:
            wine = self.env['wds.product.wine'].browse(active_id)
            wine.write({'wine_updated':False})
        return {}
