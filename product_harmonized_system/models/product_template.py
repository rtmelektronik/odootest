# Copyright 2011-2016 Akretion (http://www.akretion.com)
# Copyright 2009-2016 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hs_code_id = fields.Many2one(
        "hs.code",
        string="H.S. Code",
        company_dependent=True,
        ondelete="restrict",
        help="Harmonised System Code. Nomenclature is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org/. You can leave this field empty "
        "and configure the H.S. code on the product category.",
    )
    origin_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country of Origin",
        help="Country of origin of the product i.e. product " "'made in ____'.",
    )
    origin_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Country State of Origin",
        domain="[('country_id', '=?', origin_country_id)]",
        help="Country State of origin of the product.\n"
        "This field is used for the Intrastat declaration, "
        "selecting one of the Northern Ireland counties will set the code 'XI' "
        "for products from the United Kingdom whereas code 'XU' "
        "will be used for the other UK counties.",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_hs_code_recursively(self):
        res = self.env["hs.code"]
        if self:
            self.ensure_one()
            if self.hs_code_id:
                res = self.hs_code_id
            elif self.categ_id:
                res = self.categ_id.get_hs_code_recursively()
        return res
