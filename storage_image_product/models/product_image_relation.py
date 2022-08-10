# Copyright 2018 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <https://github.com/hparfr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductImageRelation(models.Model):
    _name = "product.image.relation"
    _inherit = "image.relation.abstract"
    _description = "Product Image Relation"

    attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        string="Attributes",
        domain="[('id', 'in', available_attribute_value_ids)]",
    )
    # This field will list all attribute value used by the template
    # in order to filter the attribute value available for the current image
    available_attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        string="Available Attributes",
        compute="_compute_available_attribute",
    )
    product_tmpl_id = fields.Many2one("product.template")
    tag_id = fields.Many2one("image.tag", domain=[("apply_on", "=", "product")])

    @api.depends("image_id", "product_tmpl_id.attribute_line_ids.value_ids")
    def _compute_available_attribute(self):
        # the depend on 'image_id' only added for triggering the onchange
        for rec in self:
            rec.available_attribute_value_ids = rec.product_tmpl_id.mapped(
                "attribute_line_ids.value_ids"
            )

    def _match_variant(self, variant):
        return not bool(
            self.attribute_value_ids
            - variant.mapped(
                "product_template_attribute_value_ids.product_attribute_value_id"
            )
        )
