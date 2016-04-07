# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.osv.osv import Model, TransientModel
from openerp.osv.orm import browse_null
from openerp.osv.orm import browse_record_list
from openerp import tools
from openerp.tools.safe_eval import safe_eval
from datetime import date, time, datetime
import dateutil



class sale_order(models.Model):
    _inherit = "sale.order"


    def action_quotation_send(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        #import pudb; pudb.set_trace()
        # get the mailing lists of the so client
        so_proxy = self.pool.get("sale.order")
        filter_proxy = self.pool.get("ir.filters")
        self_obj = so_proxy.browse(cr, uid, ids, context=context)[0]

        #lookup ir_filters to get those related to sale_order and is_offer = True
        #filter_ids = filter_proxy.search(cr, uid, [('model_id', '=', 'sale.order'), ('domain', 'like', "[('is_offer','=',True)]")], context=context)
        filters = filter_proxy.get_filters(cr, uid, 'sale.order')

        filter_ids = []
        if self_obj.is_offer:
            filter_domain = "[('is_offer','=',True)]".replace(" ", "").lower()
        else:
            filter_domain = "[('is_offer','=',False)]".replace(" ", "").lower()

        for filter in filters:
            domain = filter['domain']
            toto = domain.replace(" ", "").lower()
            if not (toto == filter_domain):
                    continue
            filter_ids.append(filter['id'])


        mail_list = []
        #now filter contacts and add their mails to the list
        for partner in self_obj.partner_id.child_ids: #contacts
            for ml in partner.mailing_list_ids :
                if ml.ir_filter_id.id in filter_ids:
                    mail_list.append(partner.id)


        if len(mail_list) == 0: mail_list.append(self_obj.partner_id.id) # default value
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'sale.order',
            'default_partner_ids': mail_list,
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_type': 'email',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


