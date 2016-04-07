# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv.osv import Model, TransientModel
from openerp.osv.orm import browse_null
from openerp.osv.orm import browse_record_list
from openerp import tools
from openerp.tools.safe_eval import safe_eval
from datetime import date, time, datetime
import dateutil



class opportunity(models.Model):
    _inherit = "crm.lead"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


