# -*- coding: utf-8 -*-
from openerp import api, models

#class account_analytic_balance(report_sxw.rml_parse):

class ProjectDetails(models.AbstractModel):
    _name = 'report.project_report.report_projectdetail'
    
    
    
    def dd(self):
        return "isto e um test"
    
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('project_report.report_projectdetail')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'dd': self.dd,
        }
        return report_obj.render('project_report.report_projectdetail', docargs)
    