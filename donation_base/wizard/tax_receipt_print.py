# © 2014-2016 Barroux Abbey (http://www.barroux.org)
# © 2014-2016 Akretion France (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DonationTaxReceiptPrint(models.TransientModel):
    _name = "donation.tax.receipt.print"
    _description = "Print Donation Tax Receipts"

    @api.model
    def _get_receipts(self):
        return self.env["donation.tax.receipt"].search([("print_date", "=", False)])

    receipt_ids = fields.Many2many(
        "donation.tax.receipt",
        column1="print_wizard_id",
        column2="receipt_id",
        string="Receipts To Print",
        default=_get_receipts,
    )

    def print_receipts(self):
        self.ensure_one()
        if not self.receipt_ids:
            raise UserError(_("There are no tax receipts to print."))
        return self.env.ref("donation_base.report_donation_tax_receipt").report_action(
            self.receipt_ids
        )
