# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.sql import drop_view_if_exists

class quants_report(osv.osv):
    _name = "distefano.quants_report"
    _description = "Inventario con variantes"
    _auto = False
    _rec_name = 'product_template_id'

    _columns = {
        'qty': fields.float('Cantidad', readonly=True),
        'location_id': fields.many2one('stock.location', 'Ubicacion', readonly=True),
        'product_template_id': fields.many2one('product.template', 'Producto', readonly=True),
        'talla_id': fields.many2one('product.attribute.value', 'Talla', readonly=True),
        'color_id': fields.many2one('product.attribute.value', 'Color', readonly=True),
        'active': fields.boolean('Activo'),
    }
    _order = 'qty desc'

    def init(self, cr):
        drop_view_if_exists(cr, 'distefano_quants_report')
        cr.execute("""
            create or replace view distefano_quants_report as (
            select
                min(q.id) as id,
                sum(q.qty) as qty,
                q.location_id as location_id,
                p.product_tmpl_id as product_template_id,
                p.active as active,
                vpr1.att_id as color_id,
                vpr2.att_id as talla_id
            from
                stock_quant q join product_product p on (q.product_id = p.id)
                join product_attribute_value_product_product_rel vpr1 on(p.id = vpr1.prod_id)
                join product_attribute_value v1 on(vpr1.att_id = v1.id and v1.attribute_id = 1)
                join product_attribute_value_product_product_rel vpr2 on(p.id = vpr2.prod_id)
                join product_attribute_value v2 on(vpr2.att_id = v2.id and v2.attribute_id = 2)
            group by location_id, product_template_id, color_id, talla_id, active
            )""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
