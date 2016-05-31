# -*- coding: utf-8 -*-
import time
import openerp.addons.decimal_precision as      dp
# from openerp                            import  tools, api
# from openerp.osv                        import  osv, fields
# from openerp.tools.translate            import  _
from openerp.tools                      import  ustr
from openerp import tools, models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

def now():
    return time.strftime('%Y')

class product_template(models.Model):
    _inherit ='product.template'

    def get_vintages(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Vintage',
                'view_type' : 'form',
                'view_mode' : 'form,tree,kanban',
                'res_model' : 'product.template',
                'res_id'    : ids,
                'context'   : context,
                'target'    :'current',
                }
        return action

    def list_vintages(self, cr, uid, context=None):
        ng = dict(self.name_search(cr,uid,'',[]))
        print "NG %s" %(ng,)
        ids = ng.keys()
        print "ids %s" %(ids,)
        result = []
        for vintage in self.browse(cr, uid, ids, context=context):
            print '##################'
            print vintage
            print '##################'
            print vintage.vintage
            print '##################'
            result.append((vintage.vintage,ng[vintage.id],vintage.vintage,))
        return result
#     def list_journals(self, cr, uid, context=None):
#         ng = dict(self.pool.get('account.journal').name_search(cr,uid,'',[]))
#         ids = ng.keys()
#         result = []
#         for journal in self.pool.get('account.journal').browse(cr, uid, ids, context=context):
#             result.append((journal.id,ng[journal.id],journal.type,
#                 bool(journal.currency),bool(journal.analytic_journal_id)))
#         return result

    # , 'product_wine_id.name','product_wine_id.appellation_id','product_wine_id.brand_id','product_wine_id.color_id','product_wine_id.grape_id'

    def get_wine_name(self,cr,uid,vals,product_id=False,context=None):
        if context is None:
            context = {}
        name = ''
        if (product_id and product_id.w_iswine) or vals.get('w_iswine',False):
            name = ''
            ## INFOS PRODUCT_WINE_ID
            wine_vals = {}
            if (product_id and product_id.product_wine_id) or vals.get('product_wine_id',False):
                if vals.get('product_wine_id',False):
                    wine = self.pool.get('wds.product.wine').browse(cr,uid,vals['product_wine_id'],context=context)
                    wine_vals['name'] = wine.name
                    if wine.grape_id:
                        wine_vals['grape'] = wine.grape_id.name
                    if wine.appellation_id or wine.color_id:
                        if wine.appellation_id:
                            wine_vals['appellation'] = wine.appellation_id.name
                        if wine.color_id:
                            wine_vals['color'] = wine.color_id.name
                else:
                    wine_vals['name'] = product_id.product_wine_id.name
                    if product_id.product_wine_id.grape_id:
                        wine_vals['grape'] = product_id.product_wine_id.grape_id.name
                    if product_id.product_wine_id.appellation_id or product_id.product_wine_id.color_id:
                        if product_id.product_wine_id.appellation_id:
                            wine_vals['appellation'] = product_id.product_wine_id.appellation_id.name
                        if product_id.product_wine_id.color_id:
                            wine_vals['color'] = product_id.product_wine_id.color_id.name
            name += wine_vals['name']
            ## VINTAGE
            if vals.has_key('vintage') and vals['vintage']:
                name += ' '+str(vals['vintage'])
            elif not vals.has_key('vintage') and product_id and product_id.vintage > 0:
                name += ' '+str(product_id.vintage)
            uom_id = vals['uom_id'] if vals.get('uom_id', False) else False
            # Y a t il quelque chos à mettre entre les parnthèses
            if (wine_vals.get('appellation', False) or wine_vals.get('color', False) or wine_vals.get('grape', False)
                or uom_id or ((product_id and product_id.alcoholic_strength > 0) or (vals.has_key('alcoholic_strength') and vals['alcoholic_strength']))
                or ((product_id and product_id.agricultural_type_id) or (vals.has_key('agricultural_type_id') and vals['agricultural_type_id']))
                or ((product_id and product_id.winetax) or (vals.has_key('winetax') and vals['winetax']))
                or ((product_id and product_id.customize_name) or (vals.has_key('customize_name') and vals['customize_name']))
            ):
                name += ' ('
                if wine_vals.get('appellation',False) or wine_vals.get('color',False) or wine_vals.get('grape',False):
                    if wine_vals.get('appellation',False):
                        name += wine_vals['appellation']
                    if wine_vals.get('grape', False):
                        name += ', ' + wine_vals['grape']
                    if wine_vals.get('color',False):
                        name += ' '+wine_vals['color']

                if uom_id:
                    uom = self.pool.get('product.uom').browse(cr,uid,uom_id,context=context)
                else:
                    uom = product_id.uom_id
                name += ', '+uom.name
                ## ALCOHOLIC STRENGTH
                if vals.has_key('alcoholic_strength') and vals['alcoholic_strength']:
                    name += ', '+str(vals['alcoholic_strength'])+'% Vol.'
                elif not vals.has_key('alcoholic_strength') and product_id and product_id.alcoholic_strength > 0:
                    name += ', '+str(product_id.alcoholic_strength)+'% Vol.'
                ## AGRICULTURAL TYPE ID
                if vals.has_key('agricultural_type_id') and vals['agricultural_type_id']:
                    agri_type = self.pool.get('wds.agriculturaltype').browse(cr,uid,vals['agricultural_type_id'])
                    name += ', '+agri_type.name
                elif not vals.has_key('agricultural_type_id') and product_id and product_id.agricultural_type_id:
                    name += ', '+product_id.agricultural_type_id.name
                ## WINETAX
                if vals.has_key('winetax') and vals['winetax']:
                    name += ', '+vals['winetax']
                elif not vals.has_key('winetax') and product_id and product_id.winetax:
                    name += ', '+product_id.winetax
                ## CUSTOMIZE NAME
                if vals.has_key('customize_name') and vals['customize_name']:
                    name += ', '+vals['customize_name']
                elif not vals.has_key('customize_name') and product_id and product_id.customize_name:
                    name += ', '+product_id.customize_name
                name += ')'
        return name

    # @api.v8
    # @api.model
    # def create(self,vals):
    #     if vals.get('w_iswine',False):
    #         vals['name'] = self.get_wine_name(vals)
    #     return super(product_template, self).create(vals)

    def create(self,cr,uid,vals,context=None):
        context = dict(context or {})
        if vals.get('w_iswine',False):
            vals['name'] = self.get_wine_name(cr,uid,vals,False,context)
        return super(product_template, self).create(cr,uid,vals,context)

    # @api.v8
    # @api.model
    # def write(self, vals):
    #     if self.w_iswine or vals.get('w_iswine',False):
    #         vals['name'] = self.get_wine_name(vals)
    #     return super(product_template, self).write(vals)

    def write(self,cr,uid,ids,vals,context=None):
        context = dict(context or {})
        for product in self.browse(cr,uid,ids,context=context):
            if product.w_iswine or vals.get('w_iswine',False):
                vals['name'] = self.get_wine_name(cr,uid,vals,product,context)
        return super(product_template, self).write(cr,uid,ids,vals,context)

        # supprimé dans original
        # print "'##############"
        # print values
        # print "'##############"
        # value_proxy=self.pool.get('product.attribute.value')
        # attr_proxt =self.pool.get('product.attribute')
        # attrs_ids=attr_proxt.search(cr, uid, ['|',('name', 'like', 'vintage'),('name', 'like', 'Vintage')], limit=1)
        # if not isinstance(attrs_ids, (int, long)):
        #     attrs_id=attrs_ids[0]
        # else:
        #     attrs_id=attrs_ids
        #
        # print '########'
        # print 'attrs_id: %s' %(attrs_id,)
        # print '########'
        #
        # attribute_ids=values.get('attribute_value_ids')[0][2]
        # value_objs=value_proxy.browse(cr,uid,attribute_ids,context=context)
        # print '########'
        # print 'value_objs: %s' %(value_objs,)
        # print '########'
        #
        # for value_obj in value_objs:
        #     if value_obj.attribute_id.id == attrs_id:
        #         values['vintage']=value_obj.name
        #         print '########'
        #         print 'vintage: %s' %(values.get('vintage',''),)
        #         print '########'
        # supprimé jusque là

        # vintage = values.get('vintage',False)
        #name    = values.get('name',False)
        # product_wine_id    = values.get('product_wine_id',False)
        #
        # name=product_wine_id and self.pool.get('wds.product.wine').browse(cr,uid,int(product_wine_id),context=context).name or False
        # name3=""
        # w_bio = wds_agriculturaltype
        # if name:
        #     for i in range(len(name)):
        #         if name[i] !=" " or (name[i+1] !="1" and name[i+1] !="2" ):
        #             name3 +=ustr(name[i])
        #         if name[i] ==" " and (name[i+1] =="1" or name[i+1] =="2" ):
        #             break
        # if name3 and name3!="" and vintage:
        #     name2=ustr(name3+' '+ustr(vintage))
        # elif vintage:
        #     name2=ustr(vintage)
        # else:
        #     name2=ustr(now)
        # values['name']=ustr(name2) + " " + w_bio
        # return super(product_template,self).create(cr,uid,values,context=context)

    # def onchange_vintage(self,cr,uid,ids,product_wine_id,vintage,context=None):
    #     vintage=ustr(vintage)
        # name=ustr(name)
        # name=product_wine_id and self.pool.get('wds.product.wine').browse(cr,uid,int(product_wine_id),context=context).name or False
        # name3=""
        # w_bio=ustr(wds_agriculturaltype)
        # if name:
        #     for i in range(len(name)):
        #         if name[i] !=" " or (name[i+1] !="1" and name[i+1] !="2" ):
        #             name3 +=ustr(name[i])
        #         if name[i] ==" " and (name[i+1] =="1" or name[i+1] =="2" ):
        #             break
        # if name3 and name3!="":
        #     name2=ustr(name3+' '+vintage+' '+w_bio)
        # else:
        #     name2=ustr(vintage+' '+w_bio)
        # return self.write(cr,uid,ids,{'name':name2},context=context)
    # def name_get(self, cr, uid, ids, context=None):
    #     if isinstance(ids, (list, tuple)) and not len(ids):
    #         return []
    #     if isinstance(ids, (long, int)):
    #         ids = [ids]
    #     reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
    #     res = []
    #     for record in reads:
    #         name = record['name']
    #         if record['parent_id']:
    #             name = record['parent_id'][1]+' - '+name
    #         res.append((record['id'], name))
    #     return res
    #
    # def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.name_get(cr, uid, ids, context=context)
    #     return dict(res)
    #
    # def add_vine(self, cr, uid, ids, context=None):
    #     ids = ids[0]
    #     if context!=None:
    #         ctx = dict(context)
    #         ctx.update({
    #                     'parent_id':ids,
    #                     })
    #     else:
    #         ctx=({
    #               'parent_id':ids,
    #               })
    #     action = {
    #             'type'      : 'ir.actions.act_window',
    #             'name'      : 'Vine',
    #             'view_type' : 'form',
    #             'view_mode' : 'form',
    #             'res_model' : 'product.template',
    #             'context'   : ctx,
    #             'target'    :'new',
    #             }
    #     return action
    #
    # def add_vintage(self, cr, uid, ids, context=None):
    #     ids = ids[0]
    #     if context!=None:
    #         ctx = dict(context)
    #         ctx.update({
    #                     'parent_id':ids,
    #                     })
    #     else:
    #         ctx=({
    #                 'parent_id':ids,
    #                 })
    #     action = {
    #             'type'      : 'ir.actions.act_window',
    #             'name'      : 'Vintage',
    #             'view_type' : 'form',
    #             'view_mode' : 'form',
    #             'res_model' : 'product.template',
    #             'context'   : ctx,
    #             'target'    :'new',
    #             }
    #     return action
    #
    # def add_offer(self, cr, uid, ids, context=None):
    #     ids = ids[0]
    #     if context!=None:
    #         ctx = dict(context)
    #         ctx.update({
    #                     'parent_id':ids,
    #                     'is_offer': True
    #                     })
    #     else:
    #         ctx=({
    #                 'parent_id':ids,
    #                 'is_offer': True
    #                 })
    #     action = {
    #             'type'      : 'ir.actions.act_window',
    #             'name'      : 'Price Offer',
    #             'view_type' : 'form',
    #             'view_mode' : 'form',
    #             'res_model' : 'product.template',
    #             'context'   : ctx,
    #             'target'    :'new',
    #             }
    #     return action

    def show_sub_products(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Sub Products',
                'view_type' : 'form',
                'view_mode' : 'form,kanban,tree',
                'res_model' : 'product.template',
                'res_id'    : ids,
                'context'   : context,
                'target'    :'new',
                }
        return action

    name = fields.Char(default='/')
    w_iswine = fields.Boolean('Select if wine')
    vintage = fields.Selection([(num, str(num)) for num in sorted(range(1900,int(now())+1), reverse=True)], 'Vintage')
    alcoholic_strength = fields.Float(ustr('Alcoholic strength (%vol.)'))
    product_wine_id = fields.Many2one('wds.product.wine','wine',help='Select a wine for this product.',ondelete='restrict')
    agricultural_type_id = fields.Many2one('wds.agriculturaltype', 'Agricultural type', )
    winetax = fields.Selection([(tax, str(tax)) for tax in ['CRD','Neutre','Acquit','?']], 'Wine Tax')
    customize_name = fields.Char('Customization name')

    # _columns = {
    #             'w_iswine'              : fields.boolean('Select if wine'),
    #             'vintage'               : fields.selection([(num, str(num)) for num in sorted(range(1900,int(now())+1), reverse=True)], 'Vintage',),
    #             'alcoholic_strength'    : fields.float(ustr('Alcoholic strength (%vol.)')),
                # 'classification_id'     : fields.many2one('wds.classification', 'Classification',track_visibility='onchange', ),
                # 'press_ids'             : fields.one2many('wds.press','product_id','Presses'),
                # 'product_wine_id'       : fields.many2one('wds.product.wine','wine',help='Select a wine for this product.',ondelete='restrict'),
                # 'agricultural_type_id': fields.many2one('wds.agriculturaltype', 'Agricultural type', ),

        #                 'is_offer'              : fields.boolean('Is Offer'),
#                 'parent_id'             : fields.many2one('product.template','Parent Product', select=True, ondelete='cascade'),
#                 'child_ids'             : fields.one2many('product.template','parent_id', string='Child Products'),
#                 'parent_left'           : fields.integer('Left Parent', select=1),
#                 'parent_right'          : fields.integer('Right Parent', select=1),
#                 'complete_name'         : fields.function(_name_get_fnc, type="char",translate=True, string='Name'),
                #offer:
                #natif...+
#                 'format'                : fields.char('Format',size=50),
                # 'winetax'               : fields.selection([(tax, str(tax)) for tax in ['CRD','acquit','?']], 'Wine Tax',),#Régie
#                 'supplier_wds_id'        : fields.many2one('res.partner',string="Supplier",domain="[('supplier','=',True)]" ),
#                 'conditioning'          : fields.selection([(num, str(num)) for num in range(1, 24)], ustr('Conditioning'),),
#                 'package_type'               : fields.selection([(str(type), str(type)) for type in ['CBO','BTL','CBO','CBOP','CBN','CTD','CTN','TB','VRAC','Cuve']], ustr('Type'),),
#                 'quantity_wm'           : fields.integer('Quantity'),
    #             }
    # _defaults = {
    #              'name':'/',
    #             }
#     _parent_name = "parent_id"
#     _parent_store = True
#     _parent_order = 'sequence, name'
#     _order = 'parent_left'
#     _constraints = [
#         (osv.osv._check_recursion, 'Error ! You cannot create recursive Wine Product.', ['parent_id'])
#         ]
#     def child_get(self, cr, uid, ids):
#         return [ids]


# class wds_press(osv.Model):
#     _name ='wds.press'
#     def _now(self,cr,uid,context=None):
#         return time.strftime('%Y-%m-%d')
#     _columns = {
#                 'name'          : fields.many2one('wds.press.comment.type', 'Comment type',),
#                 'lang_id'       : fields.many2one('res.lang','Language',),
#                 'partner_id'    : fields.many2one('res.partner','Partner'),
#                 'date'          : fields.date('Date'),
#                 'note'          : fields.char('Note',size=20,translate=True),
#                 'priority'      : fields.many2one('wds.press.comment.priority', 'Priority'),
#                 'link'          : fields.char('Link'),#FIXME: in xml code add widget="url"
#                 'comment'       : fields.text('Comment',translate=True),
#                 'product_id'    : fields.many2one('product.template','Product'),
#                 }
#     _defaults = {
#                  'date':_now,
#                 }
    #
    # def show_press_form(self, cr, uid, ids, context=None):
    #     ids = ids[0]
    #     action = {
    #             'type'      : 'ir.actions.act_window',
    #             'name'      : 'Press',
    #             'view_type' : 'form',
    #             'view_mode' : 'form,tree',
    #             'res_model' : 'wds.press',
    #             'res_id'    : ids,
    #             'context'   : context,
    #             'target'    : 'new',
    #             }
    #     return action
#
# class wds_press_comment_type(osv.Model):
#     _name ='wds.press.comment.type'
#     _columns = {
#                 'name'          : fields.char('name',size=50,translate=True),
#                 }
# class wds_press_comment_priority(osv.Model):
#     _name ='wds.press.comment.priority'
#     _columns = {
#                 'name'          : fields.char('name',size=50,translate=True),
#                 }
# class wds_classification(osv.Model):
#     _name ='wds.classification'
#     _columns = {
#                 'name'          : fields.char('name', size=250, translate=True),
#                 }


class wds_agriculturaltype(models.Model):
    _name ='wds.agriculturaltype'

    name = fields.Char('Name',translate=True)
    shortname = fields.Char('Short name', translate=True)

    # _columns = {
    #             'name'          : fields.char('name', translate=True),
    #             }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
