# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase


class TestPOLineProcurementGroup(SavepointCase):
    @classmethod
    def setUpClass(cls):

        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        def _create_orderpoint(product, qty_min, qty_max, location):
            orderpoint_model = cls.env["stock.warehouse.orderpoint"]
            return orderpoint_model.create(
                {
                    "name": "OP/%s" % product.name,
                    "product_id": product.id,
                    "product_min_qty": qty_min,
                    "product_max_qty": qty_max,
                    "location_id": location.id,
                }
            )

        # Create supplier
        cls.pyromaniacs = cls.env["res.partner"].create(
            {"name": "Pyromaniacs Inc", "company_type": "company"}
        )
        cls.lighter = (
            cls.env["product.template"]
            .create(
                {
                    "name": "Lighter",
                    "type": "product",
                    "purchase_ok": True,
                    "seller_ids": [
                        (
                            0,
                            0,
                            {"name": cls.pyromaniacs.id, "min_qty": 1, "price": 1.0},
                        )
                    ],
                }
            )
            .product_variant_ids
        )

        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.warehouse.write({"reception_steps": "three_steps"})
        wh2 = cls.env["stock.warehouse"].create(
            {"name": "WH2", "code": "WH2", "partner_id": False}
        )
        # Create WH > WH2 PG and route
        cls.wh_wh2_pg = cls.env["procurement.group"].create(
            {"name": "WH > WH2", "move_type": "direct"}
        )
        wh_wh2_route = cls.env["stock.location.route"].create(
            {
                "name": "WH > WH2",
                "product_selectable": True,
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "WH>WH2",
                            "action": "pull",
                            "location_id": wh2.lot_stock_id.id,
                            "location_src_id": cls.warehouse.lot_stock_id.id,
                            "procure_method": "make_to_order",
                            "picking_type_id": cls.env.ref(
                                "stock.picking_type_internal"
                            ).id,
                            "group_propagation_option": "fixed",
                            "group_id": cls.wh_wh2_pg.id,
                            "propagate_cancel": True,
                        },
                    )
                ],
            }
        )
        cls.lighter.write({"route_ids": [(4, wh_wh2_route.id)]})
        _create_orderpoint(cls.lighter, 15, 30, cls.warehouse.lot_stock_id)
        _create_orderpoint(cls.lighter, 10, 20, wh2.lot_stock_id)

        # Force parent store computation after creation of WH2 because location
        # quantities are computed using parent_left _right in domain
        cls.env["stock.location"]._parent_store_compute()

    def test_po_line_proc_group(self):
        # Ensure PO lines generated by the scheduler have proper PG
        self.env["procurement.group"].run_scheduler()
        po = self.env["purchase.order"].search(
            [("partner_id", "=", self.pyromaniacs.id)]
        )
        self.assertEqual(len(po.order_line), 1)
        line = po.order_line[0]
        self.assertEqual(line.product_id, self.lighter)
        self.assertAlmostEqual(line.product_qty, 30)
        # Ensure stock moves generated by PO confirmation have proper PG
        po.button_confirm()
        self.assertEqual(len(po.picking_ids.move_lines), 1)
        move = po.picking_ids.move_lines[0]
        self.assertEqual(move.product_id, self.lighter)
        self.assertEqual(move.product_uom_qty, 30.0)
        self.assertEqual(move.location_dest_id, self.warehouse.wh_input_stock_loc_id)
