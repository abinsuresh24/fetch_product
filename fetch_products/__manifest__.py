# -*- coding: utf-8 -*-
{
    'name': "Fetch Products",
    'version': '15.0.1.0.0',
    'author': "Cybrosys Technologies",
    'category': 'Sales',
    'summary': 'Fetch Products',
    'description': """
     Transfer products from odoo15 to odoo16""",
    'depends': ['base', 'sale_management', 'product'],
    'data': ['security/ir.model.access.csv',
             'views/transfer_menu_view.xml',
             'wizard/fetch_db_view.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
