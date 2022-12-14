# Copyright 2021-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    overdue_invoice_count = fields.Integer(
        compute="_compute_overdue_invoice_count_amount",
        string="# of Overdue Invoices",
        compute_sudo=True,
        store=True,
        index=True
    )
    
    overdue_invoice_count = fields.Integer(
        compute="_compute_overdue_invoice_count_amount",
        string="# of Overdue Invoices",
        compute_sudo=True,
        store=True,
        index=True
    )
    company_currency_id = fields.Many2one(
        related="company_id.currency_id", store=True, string="Company Currency"
    )
    commercial_partner_invoicing_id = fields.Many2one(
        related="partner_invoice_id.commercial_partner_id",
        string="Commercial Invoicing Partner",
    )

    @api.depends("partner_invoice_id", "company_id")
    def _compute_overdue_invoice_count_amount(self):
        for order in self:
            count = amount = 0
            partner = order.partner_invoice_id
            if partner:
                # the use of commercial_partner is in the method below
                count, amount = partner._prepare_overdue_invoice_count_amount(
                    order.company_id.id
                )
            order.overdue_invoice_count = count
            order.overdue_invoice_amount = amount

    def jump_to_overdue_invoices(self):
        self.ensure_one()
        action = self.partner_invoice_id._prepare_jump_to_overdue_invoices(
            self.company_id.id
        )
        return action
