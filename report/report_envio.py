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
from datetime import datetime, timedelta
import a_letras
import logging


class ReportEnvio(osv.AbstractModel):
    _name = 'report.distefano.report_envio'

    def fecha(self):
        d = timedelta(hours=6)
        return ( datetime.now() - d ).strftime("%d/%m/%Y %H:%M:%S")

    def total_cantidades(self, o):
        total = 0
        for l in o.move_lines:
            total += l.product_qty
        return total

    def total_precio(self, o):
        total = 0
        for l in o.move_lines:
            total += l.product_id.list_price
        return total

    def total_total(self, o):
        total = 0
        for l in o.move_lines:
            total += l.product_id.list_price*l.product_qty
        return total

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        envio_obj = self.pool['stock.picking']

        report = report_obj._get_report_from_name(cr, uid, 'distefano.report_envio')
        envios = envio_obj.browse(cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': envios,
            'a_letras': a_letras,
            'fecha': self.fecha,
            'total_cantidades': self.total_cantidades,
            'total_precio': self.total_precio,
            'total_total': self.total_total,
        }

        return report_obj.render(cr, uid, ids, 'distefano.report_envio', docargs, context=context)
