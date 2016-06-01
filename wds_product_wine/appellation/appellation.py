# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _

class wds_appellation(osv.Model):

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','region_id','country_id','appellation_type_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['appellation_type_id']:
                name = record['appellation_type_id'][1]+' > '+name
                if record['region_id']:
                    name = record['region_id'][1]+' > '+name
                    if record['country_id']:
                        name = record['country_id'][1]+' > '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "wds.appellation"
    _description = "Wine appellation"
    _columns = {
        'name'                  : fields.char('Name', size=64, required=True, translate=True, select=True),
        #'vintage_ids'           : fields.one2many('product.product','appellation_id','Vintage',required=False),
        'complete_name'         : fields.function(_name_get_fnc, type="char", string='Name'),
        'appellation_type_id'    : fields.many2one('wds.appellation.type','Type', required=True),
        'region_id'             : fields.many2one('wds.region','Region'),
        'country_id'            : fields.related('region_id','country_id',relation='res.country',type='many2one',string='Country',store=True,select=True,readonly=True),
    }

class wds_region(osv.Model):
    _name = 'wds.region'
    _columns = {
        'name'                  : fields.char('name',size=150,select=1, translate=True),
        'country_id'            : fields.many2one('res.country','Country'),
    }

class wds_appellation_type(osv.Model):#FIXEME: write xmlcode
    _name = 'wds.appellation.type'
    _columns = {
        'name'                  : fields.char('name',size=150,select=1, translate=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
