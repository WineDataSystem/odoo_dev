import xmlrpclib
import collections
# v8 credentials
dbname = 'demo1'
user = 'admin'
pwd = 'a'
host = "localhost"
port = 8069
# v9 credentials
dbname1 = 'demo_v9'
user1 = 'admin'
pwd1 = 'a'
host1 = "localhost"
port1 = 9069
# v8
com = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/common"%(host,port))
uid = com.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/object"%(host,port))
# v9
com1 = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/common"%(host1,port1))
uid1 = com1.login(dbname1, user1, pwd1)
sock1 = xmlrpclib.ServerProxy("http://%s:%s/xmlrpc/object"%(host1,port1))
# get the v8 pages
ids = sock.execute(dbname, uid, pwd, 'ir.ui.view', 'search', [('page', '=', True)])
pages = sock.execute(dbname, uid, pwd, 'ir.ui.view', 'read', ids)


for p in pages:
    if p['name'] not in ['About us', 'Contact us', 'Homepage']:
        xml_id = sock1.execute(dbname1, uid1, pwd1, 'website', 'new_page', p['name'])
        print p
        new_values = {
            'model_data_id': p['model_data_id'],
            'website_meta_description': p['website_meta_description'],
            'website_meta_keywords': p['website_meta_keywords'],
            'website_meta_title': p['website_meta_title'],
            'write_date': p['write_date'],
            'xml_id': p['xml_id'],
            'arch': p['arch'],
            'key': p['xml_id'],
            'arch_db': p['arch']
        }
        page_id = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'search', [('key', '=', xml_id)])
        print "_____page_id_____", page_id, xml_id
        res = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'write', page_id, new_values)
        


print "----------------------------------------------v9----------------------"




ids1 = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'search', [('page', '=', True)])
res1 = sock1.execute(dbname1, uid1, pwd1, 'ir.ui.view', 'read', ids1)


"""
    def new_page(self, cr, uid, name, template='website.default_page', ispage=True, context=None):
        context = context or {}
        imd = self.pool.get('ir.model.data')
        view = self.pool.get('ir.ui.view')
        template_module, template_name = template.split('.')

        # completely arbitrary max_length
        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)

        try:
            # existing page
            imd.get_object_reference(cr, uid, template_module, page_name)
        except ValueError:
            # new page
            _, template_id = imd.get_object_reference(cr, uid, template_module, template_name)
            page_id = view.copy(cr, uid, template_id, context=context)
            page = view.browse(cr, uid, page_id, context=context)
            page.write({
                'arch': page.arch.replace(template, page_xmlid),
                'name': page_name,
                'page': ispage,
            })
            imd.create(cr, uid, {
                'name': page_name,
                'module': template_module,
                'model': 'ir.ui.view',
                'res_id': page_id,
                'noupdate': True
            }, context=context)
        return page_xmlid
 
"""

#result = sock.execute(dbname, uid, pwd, 'ir.ui.view', 'write', 1012, data)