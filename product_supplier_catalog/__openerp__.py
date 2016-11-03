# -*- coding: utf-8 -*-
##############################################################################
#
#    product_supplier_catalog module for OpenERP, Module to import supplier catalog
#    Copyright (C) 2016 MIROUNGA (<http://www.mirounga.fr/>)
#              Christophe CHAUVET <christophe.chauvet@gmail.com>
#
#    This file is a part of product_supplier_catalog
#
#    product_supplier_catalog is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    product_supplier_catalog is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product Supplier Catalog',
    'version': '1.0',
    'category': 'Purchase',
    'description': """Module to import supplier catalog""",
    'author': 'MIROUNGA',
    'website': 'http://www.mirounga.fr/',
    'depends': [
        'product',
        'purchase',
    ],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'view/product.xml',
        'wizard/create_product_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
