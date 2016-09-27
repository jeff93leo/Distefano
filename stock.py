# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
import xlrd
import base64
import logging

class stock_picking_type(osv.osv):
    _inherit = "stock.picking.type"
    _columns = {
        'group_id': fields.many2one('res.groups', 'Grupo'),
    }

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _order = "date desc"
    _columns = {
        'dest_id': fields.many2one('stock.location', 'Enviar a: '),
    }

    def cambiar_destino(self, cr, uid, ids, context=None):
        for pick in self.browse(cr, uid, ids, context=context):
            destino_id = pick.picking_type_id.default_location_dest_id.id
            if pick.dest_id:
                destino_id = pick.dest_id.id
            move_ids = [x.id for x in pick.move_lines]
            self.pool.get('stock.move').write(cr, uid, move_ids, {'location_dest_id': destino_id}, context=context)
        return True

class distefano_lineas_diferencia(osv.osv):
    _name = "distefano.lineas_diferencia"
    _columns = {
        'inventario': fields.many2one('stock.inventory', 'Inventario'),
        'producto_tmpl_id': fields.many2one('product.template', 'Producto'),
        'cantidad': fields.float('Cantidad teorica', digits_compute=dp.get_precision('Product Unit of Measure')),
        'cantidad_real': fields.float('Cantidad real', digits_compute=dp.get_precision('Product Unit of Measure')),
        'diferencia': fields.float('Diferencia', digits_compute=dp.get_precision('Product Unit of Measure')),
    }

class stock_inventory(osv.osv):
    _inherit = "stock.inventory"

    def generar_diferencias(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context=context):

            del_ids = [x.id for x in i.lineas_diferencia]
            self.pool.get('distefano.lineas_diferencia').unlink(cr, uid, del_ids, context=context)

            totales = {}
            for l in i.line_ids:
                t_id = l.product_id.product_tmpl_id.id
                if t_id not in totales:
                    totales[t_id] = {'producto_tmpl_id': t_id, 'cantidad': 0, 'cantidad_real': 0}

                totales[t_id]['cantidad'] += l.theoretical_qty
                totales[t_id]['cantidad_real'] += l.product_qty

            for v in totales.values():
                self.pool.get('distefano.lineas_diferencia').create(cr, uid, {'inventario': i.id, 'producto_tmpl_id': v['producto_tmpl_id'], 'cantidad': v['cantidad'], 'cantidad_real': v['cantidad_real'], 'diferencia': v['cantidad_real']-v['cantidad']}, context=context)
        return True

    def cargar_inventario(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context=context):
            productos = {}
            no_encontrados = []
            book = xlrd.open_workbook(file_contents=base64.b64decode(i.archivo))
            sh = book.sheet_by_index(0)

            existing_ids = []
            lineas_inventario = {}
            for l in i.line_ids:
                existing_ids.append(l.id)
                lineas_inventario[l.product_id.id] = l.id
            self.pool.get('stock.inventory.line').write(cr, uid, existing_ids, {'product_qty': 0}, context=context)

            for rx in range(sh.nrows):
                producto = str(sh.cell_value(rowx=rx, colx=0))
                listado = self.pool.get('product.product').search(cr, uid, [('ean13','like',producto)], context=context)

                if len(listado) == 1:
                    if listado[0] not in productos:
                        productos[listado[0]] = 0
                    productos[listado[0]] += 1
                else:
                    no_encontrados.append(producto)

            for p in productos.keys():
                producto = self.pool.get('product.product').browse(cr, uid, p, context=context)
                if producto.id in lineas_inventario:
                    self.pool.get('stock.inventory.line').write(cr, uid, lineas_inventario[producto.id], {'product_qty': productos[p]}, context=context)
                else:
                    self.pool.get('stock.inventory.line').create(cr, uid, {'inventory_id': i.id, 'location_id': i.location_id.id, 'product_id': producto.id, 'product_qty': productos[p]}, context=context)

            self.pool.get('stock.inventory').write(cr, uid, i.id, {'codigos_erroneos': '\n'.join(no_encontrados)}, context=context)
        return True

    _columns = {
        'lineas_diferencia': fields.one2many('distefano.lineas_diferencia', 'inventario', 'Diferencias'),
        'archivo': fields.binary('Archivo de carga'),
        'codigos_erroneos': fields.text('Codigos no encontrados'),
        'nota': fields.text('Nota'),
    }

class stock_order_inventory(osv.osv):
    _inherit = "stock.inventory"
    _order = "date desc"
