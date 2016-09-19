# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
from openerp import models

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    _columns = {
        'tipo': fields.selection([ ('no negociable', 'No negociable'), ('negociable', 'Negociable'), ], 'Tipo')
    }

# Creacion Campo y metodo onchange para asignar usuario a un grupo determinado en Bank statements  
class account_bank_statement_distefano(models.Model):
    _inherit='account.bank.statement'
    _columns= {
        'pos_config_id': fields.many2one('pos.config', 'Tienda',required=True),
    }

    def onchange_bank_statement_grupo(self,cr,uid,ids,context=None):
        vals = {}
    	objeto=self.pool.get("res.users").browse(cr,uid,uid)
    	vals.update({'pos_config_id': objeto.pos_config})
        return {'value': vals}