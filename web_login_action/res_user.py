# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID, models
from openerp.osv import fields, osv
from openerp.tools.translate import _


class res_users(osv.osv):

    _inherit = "res.users"
    
    _columns = {
        'action_id_init': fields.many2one('ir.actions.actions', 'Init Action', help="If specified, this action will be opened at log on for this user, just the first time."),
    }

    def clear_init_action(self, cr, uid, ids, context=None):
        self.pool['res.users'].write(cr, SUPERUSER_ID, [uid], {'action_id_init': False}, context=context)