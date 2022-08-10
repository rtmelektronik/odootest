# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Link between resource bookings and surveys",
    "summary": "Access survey answers from resource booking",
    "version": "13.0.1.0.1",
    "development_status": "Beta",
    "category": "Appointments",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "depends": ["resource_booking", "survey"],
    "external_dependencies": {"python": ["freezegun"]},
    "data": [
        "views/resource_booking_type_views.xml",
        "views/resource_booking_views.xml",
    ],
}
