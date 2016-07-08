# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today OpenERP SA (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.tools.translate import _
import a_letras
import logging


class ReportFacturaOnline(osv.AbstractModel):
    _name = 'report.distefano.report_factura_online'

    def total_descuento(self, o):
        t = 0
        for l in o.invoice_line:
            t += ( l.price_unit * l.discount/100 ) * l.quantity
        return t

    def anio(self, o):
        partes = o.date_invoice.split('-')
        if len(partes) > 0:
            return partes[0]
        else:
            return ''

    def mes(self, o):
        partes = o.date_invoice.split('-')
        if len(partes) > 1:
            return partes[1]
        else:
            return ''

    def dia(self, o):
        partes = o.date_invoice.split('-')
        if len(partes) > 2:
            return partes[2]
        else:
            return ''

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        invoice_obj = self.pool['account.invoice']

        report = report_obj._get_report_from_name(cr, uid, 'distefano.report_factura_online')
        invoices = invoice_obj.browse(cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': invoices,
            'a_letras': a_letras,
            'total_descuento': self.total_descuento,
            'anio': self.anio,
            'dia': self.dia,
            'mes': self.mes,
        }

        return report_obj.render(cr, uid, ids, 'distefano.report_factura_online', docargs, context=context)
