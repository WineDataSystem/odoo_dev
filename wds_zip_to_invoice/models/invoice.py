import openerp

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import models

class ZipToInvoice(models.Model):
    _inherit = 'account.invoice'

    _columns = {
        'partner_zip': fields.related('partner_id', 'zip', relation='res.partner', type='char', string='Partner Zip', readonly=True),
        'wds_department': fields.related('partner_id', 'wds_department', 'display_name', relation='res.partner', type='many2one', string='Company Department', readonly=True)
    }
