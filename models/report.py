# -*- coding: utf-8 -*-
# © 2016 Davide Corio - Abstract
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class Mixin(object):

    extra_funcs = ()

    def get_docargs(self, report):
        docargs = {
            'doc_ids': self._ids,
            'docs': self,
            'doc_model': report.model,
        }
        return docargs

    @api.multi
    def render_html(self, data=None):
        name = self._name.split('report.')[-1]
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(name)
        docargs = self.get_docargs(report)
        for k in self.extra_funcs:
            docargs[k] = getattr(self, k)
        return report_obj.render(name, docargs)


class InvoiceReport(models.AbstractModel, Mixin):
    _name = 'report.account.report_invoice'

    extra_funcs = (
        'get_analytic_lines',
    )

    def get_analytic_lines(self, inv):
        line_model = self.env['account.analytic.line']
        lines = line_model.search([('invoice_id', '=', inv.id)])
        return lines
