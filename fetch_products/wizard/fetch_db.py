# -*- coding: utf-8 -*-
import xmlrpc
from odoo import fields, models
from odoo.exceptions import ValidationError


class FetchDBWiazrd(models.TransientModel):
    """Class defined for wizard view for data migration"""
    _name = "fetch.db.wizard"
    _description = "Fetch database"

    db_one = fields.Char(string="Database From", required=True,
                         default=lambda self: self.env.cr.dbname,
                         help="Database from the products transfers")
    db_one_url = fields.Char(string="URL", required=True)
    db_one_username = fields.Char(string="Username", required=True)
    db_one_password = fields.Char(string="Password", required=True)
    db_two = fields.Char(string="Database To", required=True,
                         help="Database to the products receives")
    db_two_url = fields.Char(string="URL", required=True)
    db_two_username = fields.Char(string="Username", required=True)
    db_two_password = fields.Char(string="Password", required=True)

    def action_done(self):
        """Function defined for data migration"""
        try:
            url_db1 = self.db_one_url
            db_1 = self.db_one
            username_db_1 = self.db_one_username
            password_db_1 = self.db_one_password
            common_1 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_db1))
            models_1 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_db1))
            common_1.version()

            url_db2 = self.db_two_url
            db_2 = self.db_two
            username_db_2 = self.db_two_username
            password_db_2 = self.db_two_password
            common_2 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_db2))
            models_2 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_db2))
            common_2.version()
            uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1,
                                            {})
            uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2,
                                            {})

            db_1_products = models_1.execute_kw(db_1, uid_db1, password_db_1,
                                                'product.template',
                                                'search_read',
                                                [[]], {
                                                    'fields': ['id', 'name',
                                                               'list_price',
                                                               'standard_price',
                                                               'categ_id',
                                                               'default_code']})
            old_products = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                               'product.template',
                                               'search_read', [[]], )
            product_list = []
            for line in old_products:
                product_list.append(line['name'])
            for rec in db_1_products:
                if rec['name'] not in product_list:
                    models_2.execute_kw(db_2, uid_db2, password_db_2,
                                        'product.template', 'create',
                                        [{
                                            'name': rec['name'],
                                            'list_price': rec['list_price'],
                                            'standard_price': rec[
                                                'standard_price'],
                                            'default_code': rec['default_code'],
                                        }])
        except:
            raise ValidationError("Invalid values")
