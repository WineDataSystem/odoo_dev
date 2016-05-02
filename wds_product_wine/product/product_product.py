# -*- coding: utf-8 -*-

import math
import re
import time
from openerp                    import tools
from openerp.osv                import osv, fields
from openerp.tools.translate    import _
from openerp.tools              import ustr

def now():
    return time.strftime('%Y')

class product_product(osv.Model):
    _inherit ='product.product'
    def onchange_vintage(self,cr,uid,ids,product_wine_id,vintage,context=None):
        return True
    def show_product_variants(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Product Variant',
                'view_type' : 'form',
                'view_mode' : 'form,kanban,tree',
                'res_model' : 'product.product',
                'res_id'    : ids,
                'context'   : context,
                'target'    : 'new',
                }
        return action

    def create(self,cr,uid,values,context=None):
        print "'##############"
        print values
        print "'##############"
        value_proxy=self.pool.get('product.attribute.value')
        attr_proxy =self.pool.get('product.attribute')
        bottle_size_proxy =self.pool.get('wds.bottle.size')
        attrs_format_ids=attr_proxy.search(cr, uid, [('name', 'ilike', 'format')], limit=1)
        if not isinstance(attrs_format_ids, (int, long)):
            attrs_id=attrs_format_ids[0]
        else:
            attrs_id=attrs_format_ids
        print '########'
        print 'attrs_id: %s' %(attrs_id,)
        print '########'
        attribute_ids=values.get('attribute_value_ids')[0][2]
        value_objs=value_proxy.browse(cr,uid,attribute_ids,context=context)
        print '########'
        print 'value_objs: %s' %(value_objs,)
        print '########'
        for value_obj in value_objs:
            if value_obj.attribute_id.id == attrs_id:
                bottle_size_id=bottle_size_proxy.search(cr, uid, [('name', 'ilike', value_obj.name)], limit=1)
                if isinstance(bottle_size_id, (int, long)):
                    values['format']=int(bottle_size_id)
                else:
                    values['format']=int(bottle_size_id)
                print '########'
                print 'format: %s' %(values.get('format',''),)
                print '########'
        return super(product_product,self).create(cr,uid,values,context=context)

    _columns = {
                'w_iswine': fields.boolean('Select if wine'),
                #offers:
                # 'offer_ids'             :fields.one2many('pricelist.partnerinfo','product_id','Offers',help="List of offers related to current product "),
                #Offer fields:
                'format'                : fields.many2one('wds.bottle.size','Format',track_visibility='onchange',),
                'label'                 : fields.many2one( 'wds.label','Label',track_visibility='onchange',),
                'has_logo_pregnant'     : fields.boolean('Logo Pregnant',help="Has logo pregnant ?"),
                'winetax'               : fields.many2one('wds.winetax','Wine Tax',track_visibility='onchange',),#Régie
                'conditioning'          : fields.selection([(num, str(num)) for num in range(1, 24)], ustr('Conditioning'),track_visibility='onchange',),      
                'package_type'          : fields.many2one('wds.package.type', ustr('Package Type'),track_visibility='onchange',),
                'unique_import_id'      : fields.char('Unique Import Id',track_visibility='onchange',),
                #Extra Fields Form WDS Database#################
                'average_age'           : fields.integer(ustr('Average age of the vines (years)'),size=4,track_visibility='onchange',),
                'production_area'       : fields.float('Production area (ha)',),
                'average_yield'         : fields.float(ustr('Average yield (hl / ha)'),),
                'plenting_density'      : fields.float(ustr('Planting density (trees / ha)'),),
                'agriculture_bio_id'    : fields.many2one('wds.agriculture_bio',ustr('Organic farming / rational'),),
                'terroir_ids'           : fields.many2many('wds.terroir', 'wds_wine_terroir_rel','product_id','terroir_id', 'Terroir',),
                'harvest_type_id'       : fields.many2one('wds.harvest_type',ustr('Type of harvest'),track_visibility='onchange',),
                'harvest_start_date'    : fields.date('Harvest Start Date'),  #second level of vintage, to manage appelation by duration
                'harvest_end_date'      : fields.date('Harvest End Date',),
                'sort_method_id'        : fields.many2one('wds.sort_method',ustr('Sort method'),track_visibility='onchange',),
                'appel_offres'          : fields.selection([('yes', 'Yes'), ('no', 'No')], 'Vigneron Independent',),
                #------------------------ Vinification---------------------------#
                'maceration_time'       : fields.integer(ustr('Maceration time'),size=4,),
                'maceration_time_type'  : fields.selection([('days', 'Days'), ('hours', 'Hours')], 'Maceration time type',),
                'select_Rearing_tank'   : fields.boolean('Select rearing tank'),
                'Rearing_tank'          : fields.selection([(num, str(num)) for num in range(0, 36)], 'Rearing tank (months)',),
                'select_barrel_aging'   : fields.boolean('Select barrel aging',),
                'barrel_aging'          : fields.selection([(num, str(num)) for num in range(0, 36)], 'Barrel aging (months)',),
                'new_barrels'           : fields.selection([(num, str(num)) for num in range(0, 100)], ustr('Including new barrels (%)'),),
                'assembling_date'       : fields.date('Assembling Date',),
                'bottling_date'         : fields.date('Bottling Date',),
                'plugging_id'           : fields.many2one('wds.plugging','Plugging',),
                'allergen_ids'          : fields.many2many('wds.allergen','wds_product_allergen_rel','product_id','allergen_id', 'Allergens',),#many2many_tags
                'visual_aspect_id'      : fields.many2one('wds.visual_aspect','Visual Aspect',),
                'aroma_ids'             : fields.many2many('wds.aroma', 'wds_vintage_aroma_2rel','product_id','aroma_id', 'Aroma',),
                'assembly_ids'          : fields.one2many('wds.assembly','product_id', 'Assembly',),
                'best_tasting_id'       : fields.selection([(num, str(num)) for num in range(1900, int(now())+1)], 'Best-tasting',),
                'aging_potential'       : fields.selection([(num, str(num)) for num in range(1, 100)], ustr('Aging potential (years)'),),
                'service_temperature'   : fields.selection([(num, str(num)) for num in range(7, 19)], ustr('Service temperature (°C)'),),                       
                #------------------------ Analse---------------------------------#
                'alcoholic_strength'    : fields.float(ustr('Alcoholic strength (%vol.)')),
                'total_acidity'         : fields.float(ustr('Total acidity (g/L)')),
                'reducing_sugars'       : fields.float(ustr('Reducing sugars (g/L)')),
                'so2free'               : fields.float(ustr('SO ² free (mg/L)')),
                'so2total'              : fields.float(ustr('SO ² total (mg/L)')),
                #------------------------ Médailles -----------------------------#
                'medal_ids'             : fields.one2many('wds.medal','product_id','Medals'),
                #------------------------ Conditionnement -----------------------#
                'hide_price'            : fields.boolean('Hide Price'),
                'wooden_case_x6'        : fields.boolean('Wooden Case (x6)'),
                'wooden_case_x12'       : fields.boolean('Wooden Case (x12)'),
                'cardboard_x6'          : fields.boolean('Cardboard (x6)'),
                'cardboard_x12'         : fields.boolean('Cardboard (x12)'),
                'available_format_ids'  : fields.one2many('wds.available.format','product_id','Available Formats'),
                #------------------------ Textes --------------------------------#
                'text_ids'              : fields.one2many('wds.text','product_id','Textes'),
                #------------------------ other Fields---------------------------#
                'attribute_value_related_ids': fields.related('attribute_value_ids',relation='product.attribute.value',type='many2many', string='Vintage', ),
                ################################################
    }
    _defaults = {
        }   

class wds_winetax(osv.Model):#:needed
    _name = 'wds.winetax'
    _columns = {
                'name'                  : fields.char('Name',size=150,select=1, translate=True),
                }
class wds_label(osv.Model):#:needed
    _name = 'wds.label'
    _columns = {
                'name'                  : fields.char('Name',size=300,select=1,required=True, translate=True),
                }
class wds_package_type(osv.Model):#:needed
    _name = 'wds.package.type'
    _columns = {
                'name'                  : fields.char('Name',size=150,select=1,required=True, translate=True),
                }    
class wds_bottle_size(osv.Model):#:needed
    _name ='wds.bottle.size'
    _columns = {
                'name'          : fields.char('name', size=50,required=True, translate=True),
                }
class wds_available_format(osv.Model):
    _name ='wds.available.format'
    _columns = {
                'name'          : fields.many2one('wds.bottle.size','Available Sizes',),
                'quantity'      : fields.integer('Quantity',size=8),
                'barcode'       : fields.char('Barcode',size=20),
                'price_range'   : fields.selection([(1, ustr('<4€')),(4, ustr('4-8€')),(8, ustr('8-15€')),(15, ustr('15-100€')),(100, ustr('>100€'))] ,'Price range',placeholder="--Price range--"),
                'product_id'    : fields.many2one('product.product','Product'),
                } 
#----------------------not needed yet----------------------------------------------
class wds_aroma(osv.Model):#FIXME: create xmlcode
    _name = 'wds.aroma'
    _columns = {
                'name'          : fields.char('Name',size=150,select=1,required=True, translate=True),
                }
class wds_visual_aspect(osv.Model):#FIXME: create xmlcode
    _name = 'wds.visual_aspect'
    _columns = {
                'name'          : fields.char('Name',size=150,select=1,required=True, translate=True),
                }
class wds_agriculture_bio(osv.Model):#FIXME: create xmlcode
    _name = 'wds.agriculture_bio'
    _columns = {
                'name'          : fields.char('name',size=150,select=1, translate=True),
                }
class wds_terroir(osv.Model):#FIXME: create xmlcode
    _name = 'wds.terroir'
    _columns = {
                'name'          : fields.char('name',size=150,select=1, translate=True),
                }
class wds_harvest_type(osv.Model):#FIXME: create xmlcode
    _name = 'wds.harvest_type'
    _columns = {
                'name'          : fields.char('name',size=150,select=1, translate=True),
                }
class wds_sort_method(osv.Model):#FIXME: create xmlcode
    _name = 'wds.sort_method'
    _columns = {
                'name'          : fields.char('name',size=150,select=1, translate=True),
                }
class wds_plugging(osv.Model):
    _name ='wds.plugging'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_allergen(osv.Model):
    _name ='wds.allergen'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_assembly(osv.Model):
    _name ='wds.assembly'
    _columns = {
                'name'          : fields.many2one('wds.grape','Grape', translate=True,),
                'percentage'    : fields.selection([(num, str(num)) for num in range(0, 100)],'Percentage',placeholder=ustr("%")),
                'product_id'    : fields.many2one('product.product', 'Product'),
                }
class wds_grape(osv.Model):
    _name ='wds.grape'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_medal(osv.Model):
    _name ='wds.medal'
    _columns = {
                'name'          : fields.many2one('wds.competition', 'Competition',),
                'year'          : fields.selection([(num, str(num)) for num in range(1900, int(now())+1)], 'Years',),
                'medal_type'    : fields.many2one('wds.medal.type','Medal Type',),
                'priority'      : fields.many2one('wds.priority', 'Priority'),
                'product_id'    : fields.many2one('product.product', 'Product'),
                }
    def show_medal_form(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'          : 'ir.actions.act_window',
                'name'          : 'Medals',
                'view_type'     : 'form',
                'view_mode'     : 'form,tree',
                'res_model'     : 'wds.medal',
                'res_id'        : ids,
                'context'       : context,
                'target'        :'new',
                }
        return action
class wds_priority(osv.Model):
    _name ='wds.priority'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_medal_type(osv.Model):
    _name ='wds.medal.type'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_competition(osv.Model):
    _name ='wds.competition'
    _columns = {
                'name'          : fields.char('name', translate=True),
                }
class wds_text(osv.Model):
    _name ='wds.text'
    _columns = {
                'name'          : fields.many2one('wds.press.comment.type', 'Comment type'),
                'lang_id'       : fields.many2one('res.lang','Language'),
                'partner_id'    : fields.many2one('res.partner','Partner'),
                'date'          : fields.date('Date'),
                'note'          : fields.char('Note',size=20,translate=True),
                'priority'      : fields.many2one('wds.press.comment.priority', 'Priority'),
                'link'          : fields.char('Link'),#FIXME: in xml code add widget="url"
                'comment'       : fields.text('Comment',translate=True),
                'product_id'    : fields.many2one('product.product','Product'),
                }
    def show_text_form(self, cr, uid, ids, context=None):
        ids = ids[0]
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Press',
                'view_type' : 'form',
                'view_mode' : 'form,tree',
                'res_model' : 'wds.text',
                'res_id'    : ids,
                'context'   : context,
                'target'    : 'new',
                }
        return action