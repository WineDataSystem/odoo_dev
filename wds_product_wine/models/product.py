# -*- coding: utf-8 -*-

from openerp import fields, models, _




class partner(models.Model):
    _inherit = "res.partner"


    w_siret = fields.Char("SIRET")
    w_fda = fields.Char("FDA")
    w_accise = fields.Char("N° accise")
    w_winepro = fields.Boolean("Pro du vin",help="Cochez cette case si ce client est un professionnel du vin.")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


