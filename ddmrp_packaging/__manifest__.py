# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "DDMRP Packaging",
    "summary": "DDMRP integration with packaging",
    "version": "13.0.1.7.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/ddmrp",
    "category": "Warehouse Management",
    "depends": ["ddmrp"],
    "data": ["views/stock_buffer_view.xml", "wizards/make_procurement_buffer_view.xml"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
}
