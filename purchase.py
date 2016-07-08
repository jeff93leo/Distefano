# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
import logging

class purchase_order(osv.osv):
    _inherit = "purchase.order"
    _columns = {
        'departamento_id': fields.many2one('hr.department', 'Departamento'),
    }
