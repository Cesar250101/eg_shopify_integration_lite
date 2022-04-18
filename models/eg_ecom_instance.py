# -*- coding: utf-8 -*-import requests

import requests
from odoo import models, fields, api


class EgEComInstance(models.Model):
    _inherit = "eg.ecom.instance"

    provider = fields.Selection(selection_add=[("eg_shopify", "Shopify")])
    shopify_api_key = fields.Char(string="Api Key")
    shopify_password = fields.Char(string="Password")
    shopify_version = fields.Char(string="Version", default="2020-01")
    shopify_shop = fields.Char(string="Shop Name")
    spf_order_name = fields.Selection([("odoo", "By Odoo"), ("shopify", "By Shopify")], string="Sale Order Name")
    tax_add_by = fields.Selection([("odoo", "By Odoo"), ("shopify", "By Shopify")], string="Add Tax")
    #spf_last_order_date = fields.Datetime(string="Last Order Date", readonly=True)
    spf_last_order_date = fields.Datetime(string="Last Order Date")
    export_stock_date = fields.Datetime(string="Last update stock", readonly=True)

    def test_connection_of_instance(self, from_cron=None):
        header = {'Content-Type': 'application/json'}
        if from_cron:
            shop_url = "https://{}:{}@{}.myshopify.com/admin/api/{}/orders.json".format(self.shopify_api_key,
                                                                                        self.shopify_password,
                                                                                        self.shopify_shop,
                                                                                        self.shopify_version)
        else:
            shop_url = "https://{}:{}@{}.myshopify.com/admin/api/{}/orders.json".format(self.shopify_api_key,
                                                                                        self.shopify_password,
                                                                                        self.shopify_shop,
                                                                                        self.shopify_version)
        try:
            response = requests.request('get', shop_url, headers=header)
            if response.status_code == 200:
                self.connection_message = 'Connection Successfully'
            else:
                self.connection_message = 'Error'

        except Exception as e:
            self.connection_message = 'Error'

    @api.model
    def create_sequence_for_shopify_history(self):
        self.env["ir.sequence"].create({"name": "Shopify History Integration",
                                        "code": "eg.ecom.instance",
                                        "prefix": "SH",
                                        "padding": 3,
                                        "number_increment": 1})
