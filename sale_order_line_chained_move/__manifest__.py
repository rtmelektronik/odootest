# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Line Chained Move",
    "summary": """
        This module adds a field on sale order line to get all related move lines""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["rousseldenis"],
    "website": "https://github.com/OCA/sale-workflow",
    "depends": ["sale_stock"],
    "demo": ["demo/sale_order.xml"],
    "post_init_hook": "post_init_hook",
}
