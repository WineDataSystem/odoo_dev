# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions

class partner(models.Model):
	_inherit = 'res.partner'

	# ajout de colonnes
	instructor = fields.Boolean("Instructor", default=False)

	session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
