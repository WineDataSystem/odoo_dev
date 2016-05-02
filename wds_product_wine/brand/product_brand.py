# -*- encoding: utf-8 -*-
from openerp.osv import orm, fields


class product_brand(orm.Model):
    _name = 'wds.product.brand'
    def get_products(self, cr, uid, ids, context):
        if isinstance(ids, (int, long)):
            ids = [ids]
        obj=self.browse(cr, uid, ids, context=context)[0]
        context['default_product_brand_id'] = obj.id
        return {
             'domain'    : [('id','in', [o.id for o in obj.product_template_ids])],
             'name'      : 'Products',
             'type'      : 'ir.actions.act_window',
             'view_type' : 'form',
             'view_mode' : 'kanban,form,tree',
             'res_model' : 'product.template',
             'context'   : context,
         }
    def get_brand(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Brand',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'wds.product.brand',
                'res_id'    : ids,
                'context'   : context,
                'target'    :'current',
                }
        return action

    def _product_count(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for self_obj in self.browse(cr,uid,ids,context=context):
            product_ids = self.pool.get('product.template').search(cr, uid, [('product_brand_id', 'in', [self_obj.id])], context=context)
            res[self_obj.id] =len(product_ids)
        return res
    def _get_short_name(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for self_obj in self.browse(cr,uid,ids,context=context):
            name=self_obj.name
            if self_obj.name:
                short_name= len(self_obj.name) > 26 and name[0:23]+'...' or name
                res[self_obj.id] =short_name
            else:
                res[self_obj.id] =name
        return res
            
    
    _columns = {
        'name'                  : fields.char('Brand Name',required=True),
        'name_short'            : fields.function(_get_short_name,type='char',string='Brand short Name'),
        'description'           : fields.text('Description', translate=True),
        'partner_id'            : fields.many2one('res.partner','Partner',help='Select a winery for this brand if it exists.',ondelete='restrict'),
        'logo'                  : fields.binary('Logo File'),
        'product_template_ids'  : fields.one2many('product.template', 'product_brand_id', 'Products'),
        'product_count'         : fields.function(_product_count, type='integer', string="Product Count"),
        'product_wine_ids'      : fields.one2many('wds.product.wine','brand_id','Wines'),
        'product_vintage_ids'   : fields.related('product_wine_ids','product_template_ids', relation='product.template',type='one2many',string='Vintages'),
    }


class product_template(orm.Model):
    _inherit = 'product.template'
    _columns = {
        'product_brand_id': fields.many2one(
            'wds.product.brand',
            'Brand',
            help='Select a brand for this product.',
            ondelete='restrict')
    }
