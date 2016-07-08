# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
import logging

class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
        'codigo_base': fields.char('Codigo de Barras Base'),
    }

    def name_get(self, cr, uid, ids, context=None):
        def _name_get(d):
            name = d.get('name','')
            code = d.get('default_code',False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)

        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'default_code'], context=context)
        res = []
        for record in reads:
            res.append(_name_get(record))
        return res

    def create_variant_ids(self, cr, uid, ids, context=None):
        ref = ''
        for t in self.browse(cr, uid, ids):
            for p in t.product_variant_ids:
                logging.warn(p.default_code)
                if p.default_code:
                    ref = p.default_code

        logging.warn(ref)
        ret = super(product_template, self).create_variant_ids(cr, uid, ids, context=context)

        for t in self.browse(cr, uid, ids):
            if t.codigo_base:

                codigo = t.codigo_base
                talla = ''
                color = ''

                for p in t.product_variant_ids:
                    for v in p.attribute_value_ids:

                        if v.attribute_id.id == 1:
                            color = v.codigo_barras or ''
                        if v.attribute_id.id == 2:
                            talla = v.codigo_barras or ''

                    completo = codigo + talla + color

                    self.pool.get('product.product').write(cr, uid, p.id, {'ean13': completo, 'default_code': ref})

        return ret

    # def create(self, cr, uid, vals, context=None):
    #     t_id = super(product_template, self).create(cr, uid, vals, context=context)
    #
    #     for t in self.browse(cr, uid, t_id):
    #         logging.warn(t)
    #         for p in t.product_variant_ids:
    #             logging.warn(vals['default_code'])
    #             self.pool.get('product.product').write(cr, uid, p.id, {'default_code': vals['default_code']})
    #
    #     return t_id

class product_attribute_value(osv.osv):
    _inherit = "product.attribute.value"
    _columns = {
        'codigo_barras': fields.char('Codigo de Barras'),
    }

class product_product(osv.osv):
    _inherit = "product.product"

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
        res = super(product_product, self).read_group(cr, uid, domain, fields, groupby, offset=offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
        if 'qty_available' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    qty_available = 0.0
                    for line2 in self.browse(cr, uid, lines, context=context):
                        qty_available += line2.qty_available
                    line['qty_available'] = qty_available
        return res
