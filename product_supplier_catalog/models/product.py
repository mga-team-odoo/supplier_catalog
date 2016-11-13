# -*- coding: utf-8 -*-
##############################################################################
#
# product_supplier_catalog module for OpenERP, Module to import supplier
# catalog
# Copyright (C) 2016 MIROUNGA (<http://www.mirounga.fr/>)
#           Christophe CHAUVET <christophe.chauvet@gmail.com>
#
# This file is a part of product_supplier_catalog
#
# product_supplier_catalog is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# product_supplier_catalog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.osv import fields
import openerp.addons.decimal_precision as dp
import logging
logger = logging.getLogger('product_supplier_catalog')


class product_supplier_catalog(orm.Model):
    _name = 'product.supplier.catalog'
    _description = 'Store catalog come from the supplier'

    _columns = {
        'name': fields.char('Product name', size=128,
                            help='Name of the product'),
        'code': fields.char('Product code', size=64,
                            help='Code of the product'),
        'manufacturer_id': fields.many2one(
            'res.partner', 'Manufacturer',
            help='Manufacturer for this product'),
        'ean13': fields.char('EAN 13', size=13, help='Barcode product'),
        'uom_id': fields.many2one('product.uom', 'Unit', required=True,
                                  help='Unit for create this product'),
        'weight': fields.float(
            'Gross Weight', digits_compute=dp.get_precision('Stock Weight'),
            help='Gross weight'),
        'weight_net': fields.float(
            'Net Weight', digits_compute=dp.get_precision('Stock Weight'),
            help='Net weight'),
        'date_eol': fields.date(
            'End of life',
            help='Date when the product become at end of life'),
        'line_ids': fields.one2many(
            'product.supplier.catalog.line', 'supp_cat_id', 'Lines',
            help='Supplier line'),
        'category_ids': fields.one2many(
            'product.supplier.category', 'supp_cat_id', 'Categories',
            help='Categories for this product on the suppliers'),
        'product_id': fields.many2one('product.product', 'Product',
                                      help='Product link'),
        'description': fields.text('Description', help='Sale description'),
        'warranty': fields.float('Warranty', help='Warranty for this product'),
        'public_price': fields.float(
            'Public Price', digits_compute=dp.get_precision('Product Price'),
            help='Public price or catalog price'),
    }

    _defaults = {
        'weight': 0.0,
        'weight_net': 0.0,
        'public_price': 0.0,
        'warranty': 0.0,
    }

    def _find_product(self, cr, uid, psc, context=None):
        pro_obj = self.pool['product.product']
        if psc.ean13:
            p_ids = pro_obj.search(cr, uid, [('ean13', '=', psc.ean13)],
                                   context=context)
            if p_ids:
                return p_ids[0]

        if psc.code:
            args = [
                ('manufacturer_pref', '=', psc.code),
            ]
            if psc.manufacturer_id:
                args.append(('manufacturer', '=', psc.manufacturer_id.id))
            p_ids = pro_obj.search(cr, uid, args, context=context)

            if p_ids:
                return p_ids[0]

        return False

    def _find_link(self, cr, uid, ids, context):
        """
        Link with own product, by ean13, manufacturer code, or product code
        :return: Number of link updated
        """
        count = 0
        for psc in self.browse(cr, uid, ids, context=context):
            if not psc.product_id:
                product_id = self._find_product(cr, uid, psc, context=context)
                if product_id:
                    psc.write({'product_id': product_id})
                    count += 1
        return count

    def synchronize(self, cr, uid, ids, context=None):
        """
        Link own product with supplier product, for further updates.
        """
        count = 0
        logger.info('Start synchronize supplier catalog')
        offset = 0
        if not ids:
            ids = [1]
        while ids:
            logger.info('Offset %i' % offset)
            ids = self.search(cr, uid, [], offset=offset, limit=100)
            count += self._find_link(cr, uid, ids, context=context)
            offset += len(ids)
        logger.info('%i products link updated' % count)
        logger.info('End synchronize supplier catalog')
        return True


class product_supplier_catalog_line(orm.Model):
    _name = 'product.supplier.catalog.line'
    _description = 'Supplier catalog line'

    _columns = {
        'supp_cat_id': fields.many2one(
            'product.supplier.catalog', 'product catalog',
            help='Help note'),
        'supplier_id': fields.many2one(
            'res.partner', 'Supplier', required=True,
            help='Supplier'),
        'name': fields.char('Product supplier name', size=128,
                            help='Product supplier name'),
        'code': fields.char('Product supplier code', size=64,
                            help='Product supplier code'),
        'sku': fields.char('SKU', size=64, help='SKU for this supplier'),
        'min_qty': fields.float(
            'Min Qty',
            help='Minimum quantity to order on this supplier'),
        'purchase_price': fields.float(
            'Purchase Price', digits_compute=dp.get_precision('Product Price'),
            help='our purchase price'),
        'delay': fields.integer(
            'Delivery delay',
            help='Number of days to deliver the product'),
    }

    _defaults = {
        'min_qty': 0.0,
        'purchase_price': 0.0,
        'delay': 1,
    }


class product_supplier_category(orm.Model):
    _name = 'product.supplier.category'
    _description = "Supplier's category"

    _columns = {
        'supp_cat_id': fields.many2one(
            'product.supplier.catalog', 'product catalog',
            help='Link to the supplier catalog'),
        'name': fields.char('Category name', size=128,
                            help='name of teh category on the supplier'),
        'code': fields.char('Category code', size=64,
                            help='Code of the category on the supplier'),
    }


class product_category(orm.Model):
    _inherit = 'product.category'

    _columns = {
        'compute_coeff': fields.float(
            'Compute Coeff',
            help='Compute standard price when convert product '
                 'catalog on product'),
    }

    _defaults = {
        'compute_coeff': 1.0,
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
