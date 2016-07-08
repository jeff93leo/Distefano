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

class ReportPedidoOnline(osv.AbstractModel):
    _name = 'report.distefano.report_pedido_online'

    def hora(self):
        d = timedelta(hours=6)
        return ( datetime.now() - d ).strftime("%H:%M:%S")


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
        order_obj = self.pool['pos.order']

        report = report_obj._get_report_from_name(cr, uid, 'distefano.report_pedido_online')
        orders = order_obj.browse(cr, uid, ids, context=context)

        # for p in orders:
        #     if p.state == 'draft':
        #         raise osv.except_osv('Error', 'No se puede imprimir una factura en borrador')
        #
        #     if p.impreso == 0:
        #         self.pool.get('pos.order').write(cr, uid, p.id, { 'impreso': 1 })
        #     elif p.impreso == 1:
        #         if uid == 1:
        #             pedidos = self.pool.get('pos.order').search(cr, uid, [('session_id','=',p.session_id.id)], order="name desc")
        #             if p.id != pedidos[0]:
        #                 raise osv.except_osv('Error', 'No se puede imprimir esta factura por que no es la última')
        #
        #             self.pool.get('pos.order').write(cr, uid, p.id, { 'impreso': 2 })
        #         else:
        #             raise osv.except_osv('Error', 'Solo el supervisor puede reimprimir una factura')
        #     else:
        #         raise osv.except_osv('Error', 'No se puede reimprimir una factura una segunda vez')

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': orders,
            'a_letras': a_letras,
            'total_descuento': self.total_descuento,
            'anio': self.anio,
            'dia': self.dia,
            'mes': self.mes,
            'hora': self.hora,
        }

        return report_obj.render(cr, uid, ids, 'distefano.report_pedido_online', docargs, context=context)
