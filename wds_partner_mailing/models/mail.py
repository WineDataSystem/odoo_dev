# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv.osv import Model, TransientModel
from openerp.osv.orm import browse_null
from openerp.osv.orm import browse_record_list
from openerp import tools
from openerp.tools.safe_eval import safe_eval
from datetime import date, time, datetime
import dateutil



class mailing_list(models.Model):
    _inherit = "mail.mass_mailing.list"

    ir_filter_id = fields.Many2one("ir.filters", string=_("Appliquer à"))



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


