# -*- encoding: utf-8 -*-
from openerp.osv import osv,orm, fields
from openerp import tools, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools              import  ustr

import logging
_logger = logging.getLogger(__name__)

class product_wine(orm.Model):
    _name = 'wds.product.wine'

    def get_wines(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Wines',
                'view_type' : 'form',
                'view_mode' : 'form,tree,kanban',
                'res_model' : 'wds.product.wine',
                'res_id'    : ids,
                'context'   : context,
                'target'    :'current',
                }
        return action

    def get_products(self, cr, uid, ids, context):
        if isinstance(ids, (int, long)):
            ids = [ids]
        obj=self.browse(cr, uid, ids, context=context)[0]
        context['default_product_wine_id'] = obj.id
        return {
             'domain'    : [('id','in', [o.id for o in obj.product_template_ids])],
             'name'      : 'Products',
             'type'      : 'ir.actions.act_window',
             'view_type' : 'form',
             'view_mode' : 'kanban,form,tree',
             'res_model' : 'product.template',
             'context'   : context,
         }
    def get_wine(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'wine',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'wds.product.wine',
                'res_id'    : ids,
                'context'   : context,
                'target'    :'current',
                }
        return action
    def _product_count(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for self_obj in self.browse(cr,uid,ids,context=context):
            product_ids = self.pool.get('product.template').search(cr, uid, [('product_wine_id', 'in', [self_obj.id])], context=context)
            res[self_obj.id] =len(product_ids)
        return res
    def _get_short_name(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for self_obj in self.browse(cr,uid,ids,context=context):
            name=self_obj.name
            short_name= len(self_obj.name) > 26 and name[0:23]+'...' or name
            res[self_obj.id] =short_name
        return res


    _columns = {
        'name'                  : fields.char('Wine Name',required=True),
        'name_short'            : fields.function(_get_short_name,type='char',string='Wine Short Name'),
        'description'           : fields.text('Description', translate=True),
        'partner_id'            : fields.many2one('res.partner','Partner',help='Select a winery for this wine if it exists.',ondelete='restrict'),
        'logo'                  : fields.binary('Logo File'),
        'product_template_ids'  : fields.one2many('product.template', 'product_wine_id', 'Products'),
        'product_count'         : fields.function(_product_count, type='integer', string="Product Count"),
        #refs###########################
        # 'refcour'               : fields.char('Ref Cour',size=50),
        #wine###########################
        'wds'                   : fields.char('WDS',size=50),
        'color_id'              : fields.many2one('wds.color','Color', required=True),
        'appellation_id'        : fields.many2one('wds.appellation','appellation', required=True),
        'hierarchy_id'          : fields.many2one('wds.hierarchy','Wine Hierarchy',),
        'grape_id'              : fields.many2one('wds.grape', 'Grape Variety', required=True),
        'catalog_ids'           : fields.many2many('wds.catalog', 'wds_product_catalog_2rel','product_id','catalog_id', 'Catalog'),
        'wine_type_id'          : fields.many2one('wds.wine.type','Wine Type', required=True),
        'brand_id'              : fields.many2one('wds.product.brand', 'Marque'),
        'wine_updated'          : fields.boolean('Wine updated',readonly=True),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if not vals.has_key('wine_updated'):
            vals.update({'wine_updated':True})
        return super(product_wine, self).write(cr ,uid, ids, vals, context=context)



try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from PIL import Image
from PIL import ImageEnhance
from random import randint

class wds_color(osv.Model):#
    _name ='wds.color'
    # bibliothéque Image
    def _image_resize_image_big(self, base64_source, size=(256, 256), encoding='base64', filetype='PNG', avoid_if_small=True):
        return tools.image_resize_image(base64_source, size, encoding, filetype, avoid_if_small)
    def _image_resize_image_medium(self,base64_source, size=(256, 256), encoding='base64', filetype='PNG', avoid_if_small=False):
        return tools.image_resize_image(base64_source, size, encoding, filetype, avoid_if_small)
    def _image_resize_image_small(self, base64_source, size=(64, 64), encoding='base64', filetype='PNG', avoid_if_small=False):
        return tools.image_resize_image(base64_source, size, encoding, filetype, avoid_if_small)
    def _image_get_resized_images_glass(self,base64_source, return_big=False, return_medium=True, return_small=True,
        big_name='image_glass', medium_name='image_medium_glass', small_name='image_small_glass',
        avoid_resize_big=True, avoid_resize_medium=False, avoid_resize_small=False):

        return_dict = dict()
        if return_big:
            return_dict[big_name] = self._image_resize_image_big(base64_source, avoid_if_small=avoid_resize_big)
        if return_medium:
            return_dict[medium_name] = self._image_resize_image_medium(base64_source, avoid_if_small=avoid_resize_medium)
        if return_small:
            return_dict[small_name] = self._image_resize_image_small(base64_source, avoid_if_small=avoid_resize_small)
        return return_dict
    #Fin de la bibliothéque
    def _image_get_resized_images_bottle(self,base64_source, return_big=False, return_medium=True, return_small=True,
        big_name='image_bottle', medium_name='image_medium_bottle', small_name='image_small_bottle',
        avoid_resize_big=True, avoid_resize_medium=False, avoid_resize_small=False):

        return_dict = dict()
        if return_big:
            return_dict[big_name] = self._image_resize_image_big(base64_source, avoid_if_small=avoid_resize_big)
        if return_medium:
            return_dict[medium_name] = self._image_resize_image_medium(base64_source, avoid_if_small=avoid_resize_medium)
        if return_small:
            return_dict[small_name] = self._image_resize_image_small(base64_source, avoid_if_small=avoid_resize_small)
        return return_dict
    #Fin de la bibliothéque
    #redimension de la taille de l'image:
    @api.multi
    def _get_bottle_image(self, name, args):
        return dict((p.id, self._image_get_resized_images_bottle(p.image_bottle)) for p in self)
    @api.one
    def _set_bottle_image(self, name, value, args):
        return self.write({'image_bottle': tools.image_resize_image_big(value)})
    #redimension de la taille de l'image:
    @api.multi
    def _get_glass_image(self, name, args):
        return dict((p.id, self._image_get_resized_images_glass(p.image_glass)) for p in self)
    @api.one
    def _set_glass_image(self, name, value, args):
        return self.write({'image_glass': tools.image_resize_image_big(value)})

    _columns = {
                'name'          : fields.char('name', translate=True),
                'sequence'         : fields.integer('Order'),
                'color_code'    : fields.char('Color Code'),
                'image_bottle'  : fields.binary('Image bottle'),
                'image_glass'   : fields.binary('Image Glass'),
                'image_medium_bottle': fields.function(_get_bottle_image, fnct_inv=_set_bottle_image,
                    string="Medium-sized image", type="binary", multi="_get_bottle_image",
                    store={'wds.color': (lambda self, cr, uid, ids, c={}: ids, ['image_bottle'], 10),},),
                'image_small_bottle': fields.function(_get_bottle_image, fnct_inv=_set_bottle_image,
                    string="Small-sized image", type="binary", multi="_get_bottle_image",
                    store={'wds.color': (lambda self, cr, uid, ids, c={}: ids, ['image_bottle'], 10),}),
                'image_medium_glass': fields.function(_get_glass_image, fnct_inv=_set_glass_image,
                    string="Medium-sized image", type="binary", multi="_get_glass_image",
                    store={'wds.color': (lambda self, cr, uid, ids, c={}: ids, ['image_glass'], 10),},),
                'image_small_glass': fields.function(_get_glass_image, fnct_inv=_set_glass_image,
                    string="Small-sized image", type="binary", multi="_get_glass_image",
                    store={'wds.color': (lambda self, cr, uid, ids, c={}: ids, ['image_glass'], 10),}),
                }

class wds_wine_type(osv.Model):
    _name ='wds.wine.type'

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' - '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    _columns = {
                'name'          : fields.char('Name', required=True, translate=True, select=True),
                'complete_name' : fields.function(_name_get_fnc, type="char",translate=True, string='Name'),
                'parent_id'     : fields.many2one('wds.wine.type','Parent Typr', select=True, ondelete='cascade'),
                'child_id'      : fields.one2many('wds.wine.type', 'parent_id', string='Child Types'),
                'sequence'      : fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of wine types."),
                'parent_left'   : fields.integer('Left Parent', select=1),
                'parent_right'  : fields.integer('Right Parent', select=1),
                'is_modified'   : fields.boolean('Is Modified',),
                'active'        : fields.boolean('Active'),
                'is_deleted'    : fields.boolean('Is Deleted'),
                }
    _defaults = {
                'active' : lambda *a : True,
                }
    _parent_name    = "parent_id"
    _parent_store   = True
    _parent_order   = 'sequence, name'
    _order          = 'parent_left'

    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive wine type.', ['parent_id'])
    ]
    def child_get(self, cr, uid, ids):
        return [ids]

class wds_catalog(osv.Model):
    _name = 'wds.catalog'
    _columns = {
        'name'          : fields.char('Name',size=150,select=1, translate=True),
        'is_modified'   : fields.boolean('Is Modified',),
        'active'        : fields.boolean('Active'),
        'is_deleted'    : fields.boolean('Is Deleted'),
        'sequence'      : fields.integer('Sequence'),
        'comment'       : fields.text('Comment', translate=True),
        'image'         : fields.binary('image', help='This field holds the image used as bottle image for the product, limited to 1024x1024px.'),
        'is_private'    : fields.boolean('Is Private'),
        'product_ids'   : fields.many2many('wds.product.wine', 'wds_product_catalog_2rel','catalog_id','product_id', 'Product'),
    }


class wds_hierarchy(osv.Model):
    _name ='wds.hierarchy'
    _columns = {
                'name'          : fields.char('name', translate=True),
                'is_by_default' : fields.boolean('Is by Default'),
                'order'         : fields.integer('Order'),
                }

class wds_grape(osv.Model):
    _name ='wds.grape'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
