# -*- coding: utf-8 -*-
import openerp

from openerp import tools, models, fields, api, _
from openerp.osv.osv import osv


class WDSDepartment(models.Model):
    _name = 'wds.department'
    _rec_name = 'display_name'
    _order = 'sequence asc'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Nom')
    number = fields.Char(string='Numéro')
    display_name = fields.Char(compute='_compute_display_name', string='Département', store=True)
    active = fields.Boolean(string='Actif', default=True)

    @api.multi
    @api.depends('name', 'number')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name + ' (' + rec.number + ')'

class DepartmentToPartner(models.Model):
    _inherit = 'res.partner'

    wds_department = fields.Many2one('wds.department', string='Département')

