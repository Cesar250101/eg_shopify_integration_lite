# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    eg_account_journal_id = fields.Many2one(comodel_name="eg.account.journal", string="Payment Gateway")

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        if res.invoice_origin:
            order_id = self.env["sale.order"].search([("name", "=", res.invoice_origin)])
            if order_id:
                res[
                    "eg_account_journal_id"] = order_id.eg_account_journal_id and order_id.eg_account_journal_id.id or None
        return res
