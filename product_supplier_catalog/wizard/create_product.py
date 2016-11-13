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

# from openerp.osv import osv
from openerp.osv import orm
from openerp.osv import fields


class create_product(orm.TransientModel):
    _name = 'create.supplier.product'
    _description = 'Create supplier product'

    _columns = {
        'product_id': fields.many2one(
            'product.product', 'Product',
            help='Existing product in the database'),
        'categ_id': fields.many2one(
            'product.category', 'Category',
            required=True,
            help='Category for these product'),
    }

    def create_or_update_product(self, cr, uid, ids, context=None):
        lines_ids = context.get('active_ids', [])
        this = self.browse(cr, uid, ids[0], context=context)
        pro_obj = self.pool['product.product']
        for line in self.pool['product.supplier.catalog'].browse(
                cr, uid, lines_ids, context=context):
            product_id = False
            if line.product_id:
                # update
                pass
            else:
                args = {
                    'name': line.name,
                    'default_code': line.code,
                    'manufacturer_pref': line.code,
                    'manufacturer_pname': line.name,
                    'categ_id': this.categ_id.id,
                    'uom_id': line.uom_id.id,
                    'uom_po_id': line.uom_id.id,
                    'type': 'product',
                    'ean13': line.ean13,
                    'state': 'sellable',
                    'warranty': line.warranty,
                    'list_price': line.public_price,
                }
                if line.manufacturer_id:
                    args['manufacturer'] = line.manufacturer_id.id

                standard_price = 0.0
                sinfo_args = []
                for sinfo in line.line_ids:
                    sinfo_args.append((0, 0, {
                        'name': sinfo.supplier_id.id,
                        'product_name': sinfo.name,
                        'product_code': sinfo.code,
                        'min_qty': sinfo.min_qty or 1.0,
                        'delay': sinfo.delay,
                        'pricelist_ids': [(0, 0, {
                            'price': sinfo.purchase_price,
                            'min_quantity': 1.0,
                        })],
                    }))
                    if not standard_price:
                        # Todo add compute on category or company
                        standard_price = sinfo.purchase_price

                if sinfo_args:
                    args['seller_ids'] = sinfo_args
                args['standard_price'] = standard_price

                product_id = pro_obj.create(cr, uid, args, context=context)

            if product_id:
                line.write({'product_id': product_id}, context=context)

        return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
