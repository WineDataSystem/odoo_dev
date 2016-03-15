import xmlrpclib
import collections
import re
# v8 credentials
dbname = 'test1'
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
#ids = sock.execute(dbname, uid, pwd, 'ir.ui.view', 'search', [('id', '=', 1103)])
attach = sock.execute(dbname, uid, pwd, 'ir.attachment', 'read', [69])

"""
for a in attach:
    print a['datas']
    
    values = {'name':'test1.jpg',
              'datas':a['datas']}
    v9attach = sock1.execute(dbname1, uid1, pwd1, 'ir.attachment', 'create', values)

"""

attach = sock1.execute(dbname1, uid1, pwd1, 'ir.attachment', 'read', [53])
print attach[0]