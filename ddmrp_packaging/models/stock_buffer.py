# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockBuffer(models.Model):
    _inherit = "stock.buffer"

    packaging_id = fields.Many2one(
        string="Packaging",
        comodel_name="product.packaging",
        check_company=True,
        domain="[('product_id', '=', product_id), "
        "'|', ('company_id', '=', False), "
        "('company_id', '=', company_id)]",
        compute="_compute_packaging_id",
        store=True,
        readonly=False,
    )
    package_multiple = fields.Float()
    # make qty_multiple a stored computed field:
    qty_multiple = fields.Float(
        compute="_compute_qty_multiple", store=True, readonly=False,
    )

    @api.constrains("product_id", "packaging_id")
    def _check_product_packaging(self):
        for rec in self:
            if (
                rec.packaging_id.product_id
                and rec.packaging_id.product_id != rec.product_id
            ):
                raise ValidationError(
                    _("Please, select a packaging of the buffered product.")
                )

    @api.depends("packaging_id", "packaging_id.qty", "package_multiple")
    def _compute_qty_multiple(self):
        for rec in self:
            if rec.packaging_id.qty:
                rec.qty_multiple = rec.packaging_id.qty * rec.package_multiple
            else:
                # Default value on parent definition
                rec.qty_multiple = 1

    @api.depends("product_id")
    def _compute_packaging_id(self):
        for rec in self:
            if (
                rec.product_id
                and rec.packaging_id
                and rec.packaging_id.product_id != rec.product_id
            ):
                rec.packaging_id = False

    @api.onchange("packaging_id", "procure_uom_id", "qty_multiple")
    def _onchange_packaging_id(self):
        res = self._check_package()
        if not res:
            # Check is Ok, we can change package multiple to keep alignment:
            if self.packaging_id.qty:
                self.package_multiple = self.qty_multiple / self.packaging_id.qty
        return res

    def _check_package(self):
        pack = self.packaging_id
        qty = self.qty_multiple
        procure_uom = self.procure_uom_id or self.product_uom
        q = self.product_uom._compute_quantity(pack.qty, procure_uom)
        if qty and q and round(qty % q, 2):
            newqty = qty - (qty % q) + q
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _(
                        "This product is packaged by %.2f %s. You should "
                        "set 'Qty Multiple' to %.2f %s."
                    )
                    % (pack.qty, self.product_uom.name, newqty, procure_uom.name),
                },
            }
        return {}

    def _prepare_procurement_values(
        self, product_qty, date=False, group=False,
    ):
        values = super()._prepare_procurement_values(
            product_qty=product_qty, date=date, group=group
        )
        if self.packaging_id:
            values["product_packaging_id"] = self.packaging_id
        return values
