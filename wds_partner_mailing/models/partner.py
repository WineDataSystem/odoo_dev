# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv.osv import Model, TransientModel
from openerp.osv.orm import browse_null
from openerp.osv.orm import browse_record_list
from openerp import tools
from openerp.tools.safe_eval import safe_eval
from datetime import date, time, datetime
import dateutil



class partner_class(models.Model):
    _inherit = "res.partner"

    # /**
    #  * Show Order from Opportunity View
    #  */
    def show(self, cr, uid, ids, context=None):
        context=context or {}
        res_id = ids[0]
        res_model = 'res.partner'

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Contact',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': res_model,
            'res_id':res_id,
            'context':context,
        }

        return action

    mailing_list_ids = fields.Many2many('mail.mass_mailing.list',string=_("Mailing lists"))

    '''
    def create(self, cr, uid, values, context=None):
        import pudb; pudb.set_trace()
        create_id = super(partner_class,self).create(cr, uid, values, context=context)
        mail_contact_proxy = self.pool.get("mail.mass_mailing.contact")
        partner_proxy = self.pool.get("res.partner")

        partner = partner_proxy.browse(cr, uid, create_id, context=context)
        for ml in partner.mailing_list_ids:
            #unlink old ones in case the name changes
            ids_to_del = mail_contact_proxy.search(cr, uid, [('email', '=', partner.email), ('list_id', '=',ml.id)], context=context)
            mail_contact_proxy.unlink(cr, uid, ids_to_del, context=context)

            #create
            mail_contact_proxy.create(cr, uid, {
                'email':partner.email,
                'name': partner.name,
                'list_id': ml.id,
                'opt_out': partner.opt_out,
                }, context=context)

        return create_id
    '''

    def write(self, cr, uid, ids, values, context=None):
        #import pudb; pudb.set_trace()
        write_id = super(partner_class,self).write(cr, uid, ids, values, context=context)
        mail_contact_proxy = self.pool.get("mail.mass_mailing.contact")
        partner_proxy = self.pool.get("res.partner")

        partner = partner_proxy.browse(cr, uid, ids, context=context)[0]
        for ml in partner.mailing_list_ids:
            #unlink old ones in case the name changes
            ids_to_del = mail_contact_proxy.search(cr, uid, [('email', '=', partner.email), ('list_id', '=',ml.id)], context=context)
            mail_contact_proxy.unlink(cr, uid, ids_to_del, context=context)

            #create
            mail_contact_proxy.create(cr, uid, {
                'email':partner.email,
                'name': partner.name,
                'list_id': ml.id,
                'opt_out': partner.opt_out,
                }, context=context)

        return write_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


