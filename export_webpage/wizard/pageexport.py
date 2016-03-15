# -*- coding: utf-8 -*-
import xmlrpclib
import re
from openerp.osv import osv, fields
from openerp.tools.translate import _


class pageexport(osv.osv_memory):
    _name = 'pageexport'
    _description = 'Website Pages Export Wizard'

    _columns = {
        'name': fields.char('Target host', required=True, select=1),
        'port': fields.char('Target port', required=True),
        'db': fields.char('Target database', required=True),
        'user': fields.char('Target user', required=True),
        'pwd': fields.char('Target password', required=True),
        'page_ids': fields.many2many('ir.ui.view', 'rel_view_export', 'export_id', 'view_id', 'Origin Pages', domain=[('page','=',True),('name','not in',['About us', 'Contact us', 'Homepage'])]),
    }

    _defaults = {
            'name': 'localhost',
            'port': 9069,
            'db': 'demo_v9',
            'user': 'admin'
    }

    def pageexport(self, cr, uid, ids, context=None):
        for ew in self.browse(cr, uid, ids, context=context):
            pids = []
            for r in ew.page_ids:
                pids.append(r.id)
            dbname1 = ew['db']
            user1 = ew['user']
            pwd1 = ew['pwd']
            host1 = ew['name']
            port1 = ew['port']
            # target
            com1 = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/common"%(host1,port1))
            uid1 = com1.login(dbname1, user1, pwd1)
            sock1 = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/object"%(host1,port1))
            pages = self.pool.get('ir.ui.view')
            attachments = self.pool.get('ir.attachment')
            pages_obj = pages.browse(cr, uid, pids, context=context)
            pat = r'(?<=\chment/).+?(?=\/datas)'
            
            for p in pages_obj:
                # check if the page exists
                check_id = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'search', [('name', '=', p['name'])])
                if check_id:
                    raise osv.except_osv(_('Error!'), _('The page %s already exists.') % (p['name']))
                xml_id = sock1.execute(dbname1, uid1, pwd1, 'website', 'new_page', p['name'])
                # go through all attachments and export
                newarch = p.arch
                ids_str = re.findall(pat, newarch)
                # loop through match and export to v9 and then replace
                for id_str in ids_str:
                    a_id = int(id_str[:id_str.find("_")])
                    attch = attachments.browse(cr, uid, a_id, context=context)
                    values = {'name': attch.name, 'datas': attch.datas}
                    newattch_id = sock1.execute(dbname1, uid1, pwd1, 'ir.attachment', 'create', values)
                    newattch = sock1.execute(dbname1, uid1, pwd1, 'ir.attachment', 'read', newattch_id, ['website_url'])
                    newattch_src = str(newattch[0]['website_url'])
                    newattch_src = newattch_src[29:39]
                    newarch = newarch.replace(id_str, newattch_src)

                new_values = {
                    'website_meta_description': p['website_meta_description'],
                    'website_meta_keywords': p['website_meta_keywords'],
                    'website_meta_title': p['website_meta_title'],
                    'write_date': p.write_date,
                    'xml_id': p['xml_id'],
                    'arch': newarch,
                    'key': p['xml_id'],
                    'arch_db': newarch,
                }

                page_id = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'search', [('key', '=', xml_id)])
                res = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'write', page_id, new_values)
        return {'type': 'ir.actions.act_window_close'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
