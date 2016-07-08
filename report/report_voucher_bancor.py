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


class ReportVoucherBancor(osv.AbstractModel):
    _name = 'report.distefano.report_voucher_bancor'

    def totales(self, o):
        t = {'debito':0, 'credito':0}
        for l in o.move_ids:
            t['debito'] += l.debit
            t['credito'] += l.credit
        return t

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        voucher_obj = self.pool['account.voucher']

        report = report_obj._get_report_from_name(cr, uid, 'distefano.report_voucher_bancor')
        vouchers = voucher_obj.browse(cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': vouchers,
            'a_letras': a_letras,
            'totales': self.totales,
        }

        return report_obj.render(cr, uid, ids, 'distefano.report_voucher_bancor', docargs, context=context)
