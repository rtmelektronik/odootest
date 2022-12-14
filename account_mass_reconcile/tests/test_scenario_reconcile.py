# © 2014-2016 Camptocamp SA (Damien Crier)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, tools
from odoo.modules import get_module_resource
from odoo.tests import common


class TestScenarioReconcile(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestScenarioReconcile, cls).setUpClass()
        tools.convert_file(
            cls.cr,
            "account",
            get_module_resource("account", "test", "account_minimal_test.xml"),
            {},
            "init",
            False,
            "test",
        )
        cls.rec_history_obj = cls.env["mass.reconcile.history"]
        cls.mass_rec_obj = cls.env["account.mass.reconcile"]
        cls.invoice_obj = cls.env["account.move"]
        cls.bk_stmt_obj = cls.env["account.bank.statement"]
        cls.bk_stmt_line_obj = cls.env["account.bank.statement.line"]
        cls.acc_move_line_obj = cls.env["account.move.line"]
        cls.mass_rec_method_obj = cls.env["account.mass.reconcile.method"]
        cls.account_fx_income_id = cls.env.ref("account.income_fx_income").id
        cls.account_fx_expense_id = cls.env.ref("account.income_fx_expense").id
        cls.acs_model = cls.env["res.config.settings"]

        acs_ids = cls.acs_model.search(
            [("company_id", "=", cls.env.ref("base.main_company").id)]
        )

        values = {"group_multi_currency": True}

        if acs_ids:
            acs_ids.write(values)
        else:
            default_vals = cls.acs_model.default_get([])
            default_vals.update(values)
            acs_ids = cls.acs_model.create(default_vals)

    def test_scenario_reconcile(self):
        # create invoice
        invoice = self.invoice_obj.with_context(default_type="out_invoice").create(
            {
                "type": "out_invoice",
                "company_id": self.ref("base.main_company"),
                "journal_id": self.ref("account.sales_journal"),
                "partner_id": self.ref("base.res_partner_12"),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "[FURN_7800] Desk Combination",
                            "account_id": self.ref("account.a_sale"),
                            "price_unit": 1000.0,
                            "quantity": 1.0,
                            "product_id": self.ref("product.product_product_3"),
                        },
                    )
                ],
            }
        )
        # validate invoice
        invoice.post()
        self.assertEqual("posted", invoice.state)

        # create bank_statement
        statement = self.bk_stmt_obj.create(
            {
                "balance_end_real": 0.0,
                "balance_start": 0.0,
                "date": fields.Date.today(),
                "journal_id": self.ref("account.bank_journal"),
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "amount": 1000.0,
                            "partner_id": self.ref("base.res_partner_12"),
                            "name": invoice.name,
                            "ref": invoice.name,
                        },
                    )
                ],
            }
        )

        # reconcile
        line_id = None
        for l in invoice.line_ids:
            if l.account_id.internal_type == "receivable":
                line_id = l
                break

        for statement_line in statement.line_ids:
            statement_line.process_reconciliation(
                [
                    {
                        "move_line": line_id,
                        "credit": 1000.0,
                        "debit": 0.0,
                        "name": invoice.name,
                    }
                ]
            )

        # unreconcile journal item created by previous reconciliation
        lines_to_unreconcile = self.acc_move_line_obj.search(
            [("reconciled", "=", True), ("statement_id", "=", statement.id)]
        )
        lines_to_unreconcile.remove_move_reconcile()

        # create the mass reconcile record
        mass_rec = self.mass_rec_obj.create(
            {
                "name": "mass_reconcile_1",
                "account": line_id.account_id.id,
                "reconcile_method": [(0, 0, {"name": "mass.reconcile.simple.partner"})],
            }
        )
        # call the automatic reconciliation method
        mass_rec.run_reconcile()
        invoice.invalidate_cache()
        self.assertEqual("paid", invoice.invoice_payment_state)

    def test_scenario_reconcile_currency(self):
        currency_rate = (
            self.env["res.currency.rate"]
            .sudo()
            .search(
                [
                    ("currency_id", "=", self.ref("base.USD")),
                    ("company_id", "=", self.ref("base.main_company")),
                ]
            )
            .filtered(lambda r: r.name == fields.Date.today())
        )
        if not currency_rate:
            # create currency rate
            self.env["res.currency.rate"].create(
                {
                    "name": fields.Date.today(),
                    "currency_id": self.ref("base.USD"),
                    "rate": 1.5,
                }
            )
        else:
            currency_rate = fields.first(currency_rate)
            currency_rate.rate = 1.5
        # create invoice
        invoice = self.invoice_obj.with_context(default_type="out_invoice").create(
            {
                "type": "out_invoice",
                "company_id": self.ref("base.main_company"),
                "currency_id": self.ref("base.USD"),
                "journal_id": self.ref("account.sales_journal"),
                "partner_id": self.ref("base.res_partner_12"),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "[FURN_7800] Desk Combination",
                            "account_id": self.ref("account.a_sale"),
                            "price_unit": 1000.0,
                            "quantity": 1.0,
                            "product_id": self.ref("product.product_product_3"),
                        },
                    )
                ],
            }
        )
        # validate invoice
        invoice.post()
        self.assertEqual("posted", invoice.state)

        # create bank_statement
        statement = self.bk_stmt_obj.create(
            {
                "balance_end_real": 0.0,
                "balance_start": 0.0,
                "date": fields.Date.today(),
                "journal_id": self.ref("account.bank_journal_usd"),
                "currency_id": self.ref("base.USD"),
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "amount": 1000.0,
                            "amount_currency": 1500.0,
                            "partner_id": self.ref("base.res_partner_12"),
                            "name": invoice.name,
                            "ref": invoice.name,
                        },
                    )
                ],
            }
        )

        # reconcile
        line_id = None
        for l in invoice.line_ids:
            if l.account_id.internal_type == "receivable":
                line_id = l
                break

        for statement_line in statement.line_ids:
            statement_line.process_reconciliation(
                [
                    {
                        "move_line": line_id,
                        "credit": 1000.0,
                        "debit": 0.0,
                        "name": invoice.name,
                    }
                ]
            )
        # unreconcile journal item created by previous reconciliation
        lines_to_unreconcile = self.acc_move_line_obj.search(
            [("reconciled", "=", True), ("statement_id", "=", statement.id)]
        )
        lines_to_unreconcile.remove_move_reconcile()

        # create the mass reconcile record
        mass_rec = self.mass_rec_obj.create(
            {
                "name": "mass_reconcile_1",
                "account": line_id.account_id.id,
                "reconcile_method": [(0, 0, {"name": "mass.reconcile.simple.partner"})],
            }
        )
        # call the automatic reconcilation method
        mass_rec.run_reconcile()
        invoice.invalidate_cache()
        self.assertEqual("paid", invoice.invoice_payment_state)
