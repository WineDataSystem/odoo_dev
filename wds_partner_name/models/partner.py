# -*- coding: utf-8 -*-

from openerp import fields, models, _, api
from openerp.osv.osv import Model, TransientModel
from openerp.osv.orm import browse_null
from openerp.osv.orm import browse_record_list
from openerp import tools
from openerp.tools.safe_eval import safe_eval
from datetime import date, time, datetime
import dateutil



class partner_class(models.Model):
    _inherit = "res.partner"
    last_name = fields.Char(_('Nom'), onchange="compute_name")
    first_name = fields.Char(_('Prénom'), onchange="compute_name")


    @api.onchange('first_name', 'last_name')
    def compute_name(self):
        first = self.first_name or ''
        last = self.last_name or ''
        self.name = '%s %s' % (first, last)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


