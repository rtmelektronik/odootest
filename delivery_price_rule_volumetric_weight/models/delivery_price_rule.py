# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class DeliveryPriceRule(models.Model):
    _inherit = "delivery.price.rule"

    variable = fields.Selection(
        selection_add=[("volumetric_weight", "Volumetric weight")],
    )
    variable_factor = fields.Selection(
        selection_add=[("volumetric_weight", "Volumetric weight")],
    )
