# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    _columns = {
        'tipo': fields.selection([ ('no negociable', 'No negociable'), ('negociable', 'Negociable'), ], 'Tipo')
    }
