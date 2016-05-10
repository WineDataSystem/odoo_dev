# -*- coding: utf-8 -*-
import openerp
from   openerp                  import tools
from   openerp.osv              import osv, fields
from   openerp.tools.translate  import _
# pour API & Json 
from openerp.tools import  ustr
import urllib
import urllib2
try:
    import simplejson as json
except ImportError:
    import json     # noqa



class wm_domain(osv.osv_memory):
    _name ='wds.domain'
    _columns = { 
                'name'              : fields.char('Name'),
                'numenr'            : fields.char('Numenr'),
                }

class wm_param_step1(osv.osv_memory):
    _name ='wds.param_step1'
    
    _columns = { 
                'name'              : fields.char('Name'),
                'value'             : fields.char('Value'),
                'wds_sync_id'       : fields.many2one('wds.sync','Sync WDS API')
                }

class wm_param_step2(osv.osv_memory):
    _name ='wds.param_step2'
    
    _columns = { 
                'name'              : fields.char('Name'),
                'value'             : fields.char('Value'),
                'wds_sync_id'       : fields.many2one('wds.sync','Sync WDS API')
                }
    
class wds_sync(osv.osv_memory):
    _name ='wds.sync'
  
    _columns = { 
                #Step1:
                'url'               : fields.char('Url'),
                'proxy_handler'     : fields.char('Proxy handler'),
                'protocol'          : fields.char('Protocol'), 
                'domain_id'         : fields.many2one('wds.domain','Domain'),
                'user'              : fields.char('User'), 
                'password'          : fields.char('Password'), 
                'other_step1'       : fields.one2many('wds.param_step1','wds_sync_id','Other attributes'),
                #Step2:
                'token'             : fields.char('Token'),
                'output'            : fields.char('Output'),
                'device'            : fields.char('Device'),
                'url_2'             : fields.char('Url.2'),
                'other_step2'       : fields.one2many('wds.param_step2','wds_sync_id','Other attributes'),
                'var_t'             :fields.char('Var T'),
                #Step3:
                'wds_winery_ids'    : fields.one2many('wds.winery','wds_sync_id','Wds Winery'),
                'select_all'        : fields.boolean('Select All'),
                #others:
                'required_domain'   : fields.boolean('Required Domain'),
                'winery_json_text'  : fields.text('Winerys'),
                }
    
    _defaults = {
                 #step1:
                'url'               : "http://manager.winedatasystem.com/api4/AUTH/default.aspx",
                'proxy_handler'     : "88.190.48.222",
                'protocol'          : "http",
                'user'              : "af@winedatasystem.com", 
                'password'          : "aymeric", 
                #step2:
                'output'            : "json",
                'device'            : "ipad",
                'url_2'             : "http://www.charleswines.com/api4/CATALOG/?m=catalog",
                'var_t'             : "vineyard",
                #others;
                'required_domain'   : False,
               }
    
    def token(self,dct):
        return dct
        
    def recover_token(self, cr, uid,ids, context=None):
        message = 'Alert !'
        title='unable to find token number !'
        url=context.get('url',False)
        protocol=ustr(context.get('protocol',""))
        proxy_handler=ustr(context.get('proxy_handler',""))
        user=context.get('user',False)
        password=context.get('password',False)
        domain_id=int(context.get('domain_id',False))
        required_domain=int(context.get('required_domain',False))
        domain_proxy=self.pool.get('wds.domain')
        domain_obj=False
        if required_domain and domain_id:
            domain_obj=domain_proxy.browse(cr,uid,domain_id,context=context)
        Url = "%s?login=%s&pass=%s" % (url,user,password)
        if required_domain and domain_obj:
            Url="%s&domain=%s"%(Url,domain_obj.numenr)
        print Url
        Url = Url.encode('utf8')
 
        proxy_handler = urllib2.ProxyHandler({'http':'http://'+proxy_handler})
        #opener = urllib2.build_opener()
        #opener.add_handler(proxy_handler)
        #urllib2.install_opener(opener)
        #req = urllib2.Request(Url)
        proxy_handler1 = urllib2.ProxyHandler({'http': 'http://88.190.48.222'})
        print ">>>>>>>>>>>>Proxy handler 1>>>>>> %s"% (proxy_handler1,)
        print ">>>>>>>>>>>>Proxy handler>>>>>> %s"% (proxy_handler,)
        opener = urllib2.build_opener()
        opener.add_handler(proxy_handler)
        urllib2.install_opener(opener)
        the_url = 'http://manager.winedatasystem.com/api4/AUTH/default.aspx?login=af@winedatasystem.com&pass=aymeric'
        print ">>>>>>>>>>>>the url>>>>>> %s"% (the_url,)
        print ">>>>>>>>>>>>Url>>>>>> %s"% (Url,)
        req=urllib2.Request(Url) 
        print "REQ: %s "%(req,)
        
        handle = urllib2.urlopen(req)
        print "HANDLE: %s "%(handle,)
        
	try:
        #    dct = json.load(urllib2.urlopen(req))
            dct=json.load(handle)
            print "DCT: %s "%(dct,)
        except Exception, e:
            raise osv.except_osv(_('Network error'),
                                 _('Cannot contact api server. Please make sure that your internet connection is up and running (%s).') % e)

#         data = urllib.urlopen(Url).read()
#         dct=json.loads(data,object_hook=self.token)
        if "error" in dct:
            numerr=int(dct['error'])
            if numerr==11:
                message = 'Wrong credential !'
                title='Login / password incorrect !'
            elif numerr==12:
                message = 'Alert !'
                title='Multi domain!'
                todel_ids=domain_proxy.search(cr, uid, [],context=context)
                domain_proxy.unlink(cr,uid,todel_ids,context=context)
                self.write(cr,uid,ids,{'required_domain':True,'token':False},context=context)
                for elt in dct.get('domain',False):
                    values={
                            'name'   : elt.get('name',False),
                            'numenr' : elt.get('numenr',False),
                            }
                    print domain_proxy.create(cr,uid,values,context=context)
            elif numerr==13:
                message = 'Alert !'
                title='Crédential good but not with this userorg !'
            elif numerr==14:
                message = 'Alert !'
                title='Token is no longer valid !'
            elif numerr==15:
                message = 'Alert !'
                title='Account desactivated !'
            elif numerr==16:
                message = 'Alert !'
                title='Licence not up to date !'
        else:
            if "auth" in dct and dct.get('auth',False)=="success" and "token" in dct:
                self.write(cr, uid,ids,{'token':dct['token']}, context=context)
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Sync Winery From WDS API',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'wds.sync',
                'res_id'    : ids[0],
                'context'   : context,
                'target'    : 'new',
                }
        return action
     
    def wds_winery_recov(self,Liste):
        return Liste

    def clean_wds(self, cr, uid, ids, context=None):
        domain_proxy=self.pool.get('wds.domain')
        winery_proxy = self.pool.get('wds.winery')
        todel_ids=domain_proxy.search(cr, uid, [],context=context)
        domain_proxy.unlink(cr,uid,todel_ids,context=context)
        self.write(cr,uid,ids,{'required_domain':False},context=context)
        todel_ids=winery_proxy.search(cr, uid, [],context=context)
        winery_proxy.unlink(cr,uid,todel_ids,context=context)
        return True

    def sync_wine(self, cr, uid, ids, context=None):
        self.clean_wds(cr,uid,ids,context=context)
        winery_proxy = self.pool.get('wds.winery')
        url_2=context.get('url_2',False)
        output=context.get('output',False)
        device=context.get('device',False)
        token=context.get('token',"False")
        proxy_handler=ustr(context.get('proxy_handler',""))
        protocol=ustr(context.get('protocol',""))
        Url = "%s&token=%s&output=%s&device=%s" % (url_2,token,output,device)
        print "Second URl"
        print Url
        
        proxy_handler = urllib2.ProxyHandler({protocol: protocol+'://'+proxy_handler})
        opener = urllib2.build_opener()
        opener.add_handler(proxy_handler)
        urllib2.install_opener(opener)
        req = urllib2.Request(Url)
        data = urllib2.urlopen(req).read()
        self.write(cr, uid,ids,{'winery_json_text':data}, context=context)
        Liste=json.loads(data,object_hook=self.wds_winery_recov)
        values={}
        for obj in Liste:
            vals={
                'vinyard_numenr'    : obj.get('numenr',False),#numenr
                'ceo'               : obj.get('ceo',False),
                'country'           : obj.get('country',False),
                'city'              : obj.get('city',False),
                'name'              : obj.get('name',False),
                'zip'               : obj.get('zip',False),
                'gps_lat'           : obj.get('gps_lat',False),
                'gps_long'          : obj.get('gps_lon',False),
                'pitch_en'          : obj.get('pitch_en',False),
                'pitch_fr'          : obj.get('pitch_fr',False),
                'surface'           : obj.get('surface',False),
                'website'           : obj.get('website',False),
                'wds_sync_id'       : ids[0],
                'terroir_fr'        : obj.get('terroir_fr',False),
                'terroir_en'        : obj.get('terroir_en',False),
                'history_fr'        : obj.get('histoire_fr',False),
                'history_en'        : obj.get('histoire_en',False),
                'file'              : obj.get('file',False),
                'file_vine'         : obj.get('file_vigne',False),
                'file_chais'        : obj.get('file_chais',False),
                'file_propriete'    : obj.get('file_propriete',False),
                'type'              : int(obj.get('type',False)),
                'is_vinyard'        : True,
                'exist'             : False,
                }
            stock_proxy=self.pool.get('stock.location')
            exist_ids=stock_proxy.search(cr, uid, [('vinyard_numenr','=',obj.get('numenr',False))],context=context)
            if exist_ids :
                vals.update({
                           'exist': True,
                           })
            winery_proxy.create(cr,uid,vals,context=context)
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Sync Winery From WDS API',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'wds.sync',
                'res_id'    : ids[0],
                'context'   : context,
                'target'    : 'new',
                }
        return action
    
    def create_temporary_winery(self, cr, uid, ids, context=None):
        self.clean_wds(cr,uid,ids,context=context)
        winery_proxy = self.pool.get('wds.winery')
        json_txt=context.get('winery_json_text',False)
        Liste=json.loads(json_txt,object_hook=self.wds_winery_recov)
        values={}
        for obj in Liste:
            vals={
                'vinyard_numenr'    : obj.get('numenr',False),
                'ceo'               : obj.get('ceo',False),
                'country'           : obj.get('country',False),
                'city'              : obj.get('city',False),
                'name'              : obj.get('name',False),
                'zip'               : obj.get('zip',False),
                'gps_lat'           : obj.get('gps_lat',False),
                'gps_long'          : obj.get('gps_lon',False),
                'pitch_en'          : obj.get('pitch_en',False),
                'pitch_fr'          : obj.get('pitch_fr',False),
                'surface'           : obj.get('surface',False),
                'website'           : obj.get('website',False),
                'wds_sync_id'       : ids[0],
                'terroir_fr'        : obj.get('terroir_fr',False),
                'terroir_en'        : obj.get('terroir_en',False),
                'history_fr'        : obj.get('histoire_fr',False),
                'history_en'        : obj.get('histoire_en',False),
                'file'              : obj.get('file',False),
                'file_vine'         : obj.get('file_vigne',False),
                'file_chais'        : obj.get('file_chais',False),
                'file_propriete'    : obj.get('file_propriete',False),
                'type'              : int(obj.get('type',False)),
                'is_vinyard'        : True,
                'exist'             : False,
                }
            stock_proxy=self.pool.get('stock.location')
            exist_ids=stock_proxy.search(cr, uid, [('vinyard_numenr','=',obj.get('numenr',False))],context=context)
            if exist_ids :
                vals.update({
                           'exist': True,
                           })
            winery_proxy.create(cr,uid,vals,context=context)
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Sync Winery From WDS API',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'wds.sync',
                'res_id'    : ids[0],
                'context'   : context,
                'target'    : 'new',
                }
        return action
    #for each winery do :
    def create_product(self,cr, uid, ids,numenr,context=None):
        product_proxy = self.pool.get('product.product')
        url_2=context.get('url_2',False)
        output=context.get('output',False)
        device=context.get('device',False)
        token=context.get('token',False)
        var_t=context.get('var_t',False)
        proxy_handler=ustr(context.get('proxy_handler',""))
        protocol=ustr(context.get('protocol',""))
        Url = "%s&token=%s&output=%s&device=%s&numenr=%s&t=%s" % (url_2,token,output,device,numenr,var_t)
        Url = Url.encode('utf8')

        proxy_handler = urllib2.ProxyHandler({protocol: protocol+'://'+proxy_handler})
        opener = urllib2.build_opener()
        opener.add_handler(proxy_handler)
        urllib2.install_opener(opener)
        req = urllib2.Request(Url)
	try:
            dict = json.load(urllib2.urlopen(req))
        except Exception, e:
            raise osv.except_osv(_('Network error'),
                                 _('Cannot contact api server. Please make sure that your internet connection is up and running (%s).') % e)
        for obj in dict:
#             for elt in dct.get('domain',False):
#                     values={
#                             'name'   : elt.get('name',False),
#                             'numenr' : elt.get('numenr',False),
#                             }
#                     print domain_proxy.create(cr,uid,values,context=context)
            vals={
                'numenr'        : obj.get('numenr',False),
                'name'          : obj.get('name',False),
                'is_a_vintage'  : True,
                }
            exist_ids=product_proxy.search(cr, uid, [('numenr','=',obj.get('numenr',False))],context=context)
            if not exist_ids :
                product_proxy.create(cr,uid,vals,context=context)
        return True
    def winery_create(self,cr, uid, ids, context=None):
        winery_proxy = self.pool.get('wds.winery')
        winery_ids=winery_proxy.search(cr, uid, [],context=context)
        country_proxy = self.pool.get('res.country')
        stock_proxy = self.pool.get('stock.laocation')
        partner_proxy = self.pool.get('res.partner')
        contact_values={}
        values={}
        objs=winery_proxy.browse(cr,uid,winery_ids,context=context)
        for obj in objs:
            self.create_product(cr, uid, ids,obj.vinyard_numenr,context=context)
            country_ids=country_proxy.search(cr, uid, [('name','like',obj.country)],context=context)
            if isinstance(country_ids, (int, long)):
                country_ids = [country_ids]
            vals={
                'vinyard_numenr'    : obj.vinyard_numenr,
                'ceo'               : obj.ceo,
                'name'              : obj.name,
                'pitch_en'          : obj.pitch_en,
                'pitch_fr'          : obj.pitch_fr,
                'surface'           : obj.surface,
                'terroir_fr'        : obj.terroir_fr,
                'terroir_en'        : obj.terroir_en,
                'history_fr'        : obj.history_fr,
                'history_en'        : obj.history_en,
                'file'              : obj.file,
                'file_vine'         : obj.file_vine,
                'file_chais'        : obj.file_chais,
                'file_propriete'    : obj.file_propriete,
                'usage'             :'supplier',
#                 'type_partner'      : obj.type,
                'is_vinyard'        : True,
                }
            stock_proxy=self.pool.get('stock.location')
            exist_ids=stock_proxy.search(cr, uid, [('vinyard_numenr','=',obj.vinyard_numenr)],context=context)
            if isinstance(exist_ids, (int, long)):
                exist_ids = [exist_ids]
            contact_exist_ids=partner_proxy.search(cr, uid, [('name','like',obj.ceo),('property_stock_supplier','in',exist_ids)],context=context)
            if isinstance(contact_exist_ids, (int, long)):
                contact_exist_ids = [contact_exist_ids]
            contact_exist_ids2=partner_proxy.search(cr, uid, [('name','=',obj.ceo)],context=context)
            if isinstance(contact_exist_ids2, (int, long)):
                contact_exist_ids2 = [contact_exist_ids2]
            if exist_ids :
                stock_proxy.write(cr,uid,exist_ids,vals,context=context)
                if contact_exist_ids :
                    contact_values={
                                'country_id'        : country_ids and country_ids[0] or False,
                                'city'              : obj.city,
                                'zip'               : obj.zip,
                                'partner_latitude'  : obj.gps_lat,
                                'partner_longitude' : obj.gps_long,
                                'date_localization' : fields.date.context_today(self, cr, uid, context=context),
                                'website'           : obj.website,
                                'is_company'        : False,
                                'supplier'          : True,
                                'customer'          : False,
                                'function'          : 'owner',
                                'employee'          : True,
                                'is_vinyard_owner'  : True,
                                }
                    partner_proxy.write(cr,uid,contact_exist_ids,contact_values,context=context)
                    partner_proxy.geo_localize(cr, uid, contact_exist_ids, context=context)
                    stock_proxy.write(cr,uid,exist_ids,{'partner_id':contact_exist_ids[0]},context=context)
                else:
                    contact_values.update({'name': obj.ceo,'property_stock_supplier':int(exist_ids[0]),'property_stock_customer':int(exist_ids[0])})
                    part_id1=partner_proxy.create(cr,uid,contact_values,context=context)
                    partner_proxy.geo_localize(cr, uid, part_id1, context=context)
                    stock_proxy.write(cr,uid,exist_ids,{'partner_id':part_id1},context=context)
            else:
                winery_id=stock_proxy.create(cr,uid,vals,context=context)
                values={
                        'country_id'        : country_ids and country_ids[0] or False,
                        'city'              : obj.city,
                        'zip'               : obj.zip,
                        'partner_latitude'  : obj.gps_lat,
                        'partner_longitude' : obj.gps_long,
                        'date_localization' : fields.date.context_today(self, cr, uid, context=context),
                        'website'           : obj.website,
                        'is_company'        : False,
                        'supplier'          : True,
                        'customer'          : False,
                        'function'          : 'owner',
                        'employee'          : True,
                        'is_vinyard_owner'  : True,
                        'name'              : obj.ceo,
                        'property_stock_supplier':int(winery_id),
                        'property_stock_customer':int(winery_id),
                        }
#                 if contact_exist_ids2:
#                     partner_proxy.write(cr,uid,contact_exist_ids2,values,context=context)
#                 else:
#                     values['parent_id']=int(winery_id)
                part_id=partner_proxy.create(cr,uid,values,context=context)
                partner_proxy.geo_localize(cr, uid, [part_id], context=context)
                stock_proxy.write(cr,uid,winery_id,{'partner_id':part_id},context=context)
        if context!=None:
            ctx = dict(context)
            ctx.update({
                        'default_is_vinyard' : True,
                        })
        action = {
                'type'      : 'ir.actions.act_window',
                'name'      : 'Winery',
                'view_type' : 'form',
                'view_mode' : 'tree,form',
                'res_model' : 'stock.location',
                'res_id'    : ids[0],
                'context'   : ctx,
                'target'    : 'current',
                'domain'    : [('is_vinyard','=',True)],
                }
        self.clean_wds(cr,uid,ids,context=context)
        return action

class wds_winery(osv.osv_memory):
    _name ='wds.winery'
    _columns = {          
            'name'          : fields.char(' Winery',help="Name of winery"),
            'wds_sync_id'   : fields.many2one('wds.sync','Wds Sync'),
            'vinyard_numenr': fields.char('Numenr',),
            'city'          : fields.char('City'),
            'zip'           : fields.char('Zip'),
            'choose'        : fields.boolean('Choose'),
            'gps_lat'       : fields.char('gps_lat'),
            'gps_long'      : fields.char('gps_long'),
            'pitch_en'      : fields.text('Pitch En'),
            'pitch_fr'      : fields.text('Pitch Fr'),
            'surface'       : fields.char('surface'),
            'website'       : fields.char('website'),
            'ceo'           : fields.char('CEO'),
            'country'       : fields.char('Country'),
            'sequence'      : fields.integer('sequence'),
            'exist'         : fields.boolean('Already exist'),
            'terroir_fr'    : fields.text('Terroir fr'),
            'terroir_en'    : fields.text('Terroir en'),
            'history_fr'    : fields.text('History fr'),
            'history_en'    : fields.text('History en'),
            'file'          : fields.char('File'),
            'file_vine'     : fields.char('File Vigne'),
            'file_chais'    : fields.char('File Chais'),
            'file_propriete': fields.char('File Propriete'),
            'type'          : fields.integer('Type'),
            'is_vinyard'    : fields.boolean('Is Vinyard'),
            }
    _defaults={
        'is_vinyard' : True,
    }
   
