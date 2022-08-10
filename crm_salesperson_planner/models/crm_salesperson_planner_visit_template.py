# Copyright 2021 Sygel - Valentin Vinagre
# Copyright 2021 Sygel - Manuel Regidor
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmSalespersonPlannerVisitTemplate(models.Model):
    _name = "crm.salesperson.planner.visit.template"
    _description = "Crm Salesperson Planner Visit Template"
    _inherit = "calendar.event"

    name = fields.Char(
        string="Visit Template Number", default="/", readonly=True, copy=False,
    )
    partner_ids = fields.Many2many(
        string="Customer",
        relation="salesperson_planner_res_partner_rel",
        default=False,
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        help="Used to order Visits in the different views",
        default=20,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    user_id = fields.Many2one(
        string="Salesperson",
        tracking=True,
        default=lambda self: self.env.user,
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)
        ],
    )
    categ_ids = fields.Many2many(relation="visit_category_rel",)
    alarm_ids = fields.Many2many(relation="visit_calendar_event_rel")
    state = fields.Selection(
        string="Status",
        required=True,
        copy=False,
        tracking=True,
        selection=[
            ("draft", "Draft"),
            ("in-progress", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
    )
    visit_ids = fields.One2many(
        comodel_name="crm.salesperson.planner.visit",
        inverse_name="visit_template_id",
        string="Visit Template",
    )
    visit_ids_count = fields.Integer(
        string="Number of Sales Person Visits", compute="_compute_visit_ids_count"
    )
    auto_validate = fields.Boolean(string="Auto Validate", default=True)
    rrule_type = fields.Selection(default="daily", required=True,)
    last_visit_date = fields.Date(
        string="Last Visit Date", compute="_compute_last_visit_date", store=True
    )
    final_date = fields.Date(string="Repeat Until")
    allday = fields.Boolean(default=True)
    recurrency = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "crm_salesperson_planner_visit_template_name",
            "UNIQUE (name)",
            "The visit template number must be unique!",
        ),
    ]

    def _compute_visit_ids_count(self):
        visit_data = self.env["crm.salesperson.planner.visit"].read_group(
            [("visit_template_id", "in", self.ids)],
            ["visit_template_id"],
            ["visit_template_id"],
        )
        mapped_data = {
            m["visit_template_id"][0]: m["visit_template_id_count"] for m in visit_data
        }
        for sel in self:
            sel.visit_ids_count = mapped_data.get(sel.id, 0)

    @api.depends("visit_ids.date")
    def _compute_last_visit_date(self):
        for sel in self.filtered(lambda x: x.visit_ids):
            sel.last_visit_date = sel.visit_ids.sorted(lambda x: x.date)[-1].date
        self.filtered(lambda x: not x.visit_ids).write({"last_visit_date": False})

    # overwrite
    # default _search method gives an error when trying to access
    # instances of the model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        return super(models.Model, self)._search(args)

    @api.constrains("partner_ids")
    def _constrains_partner_ids(self):
        for sel in self:
            if len(sel.partner_ids) > 1:
                raise ValidationError(_("Only one customer is allowed"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "salesperson.planner.visit.template"
                )
        return super().create(vals_list)

    # overwrite
    # Calling _update_cron from default write funciont is not
    # necessary in this case
    def write(self, vals):
        return super(models.Model, self).write(vals)

    # overwrite
    # default unlink method gives an error when trying to access
    # instances of the model
    def unlink(self, can_be_deleted=True):
        return super(models.Model, self).unlink()

    def action_view_salesperson_planner_visit(self):
        action = self.env.ref(
            "crm_salesperson_planner.all_crm_salesperson_planner_visit_action"
        ).read()[0]
        action["domain"] = [("id", "=", self.visit_ids.ids)]
        action["context"] = {
            "default_partner_id": self.partner_id.id,
            "default_visit_template_id": self.id,
            "default_description": self.description,
        }
        return action

    def action_validate(self):
        self.write({"state": "in-progress"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_draft(self):
        self.write({"state": "draft"})

    def filter_dates(self, recurrences, days="7"):
        last_date = recurrences[-1].date()
        reference_date = self.start_date
        visit_date = fields.Datetime.from_string(reference_date)
        last_visit_date = False
        if not self.last_visit_date:
            last_visit_date = visit_date
        else:
            last_visit_date = fields.Datetime.from_string(
                self.last_visit_date + relativedelta(days=1)
            )
        max_date = fields.Date.today() + relativedelta(
            days=days, hours=23, minutes=59, seconds=59
        )
        recurrences = list(
            filter(
                lambda a: a.replace(tzinfo=None) <= max_date
                and a.replace(tzinfo=None) > last_visit_date,
                recurrences,
            )
        )
        return recurrences, last_date

    def _create_visits(self, days=7):
        visits_vals = []
        for sel in self:
            recurrences = self._get_recurrent_date_by_event()
            days, last_date = sel.filter_dates(recurrences, days)
            for day in days:
                visits_vals.append(
                    {
                        "partner_id": sel.partner_ids[0].id,
                        "date": day.date(),
                        "sequence": sel.sequence,
                        "user_id": sel.user_id.id,
                        "description": sel.description,
                        "company_id": sel.company_id.id,
                        "visit_template_id": sel.id,
                    }
                )
            if days and days[-1].date() >= last_date:
                sel.write({"state": "done"})
        return visits_vals

    def create_visits(self, days=7):
        for sel in self:
            visit_vals = sel._create_visits(days=days)
            visits = self.env["crm.salesperson.planner.visit"].create(visit_vals)
            if visits and sel.auto_validate:
                visits.action_confirm()

    def _cron_create_visits(self, days=7):
        templates = self.search([("state", "=", "in-progress")])
        templates.create_visits(days=days)

    # overwrite
    def get_recurrent_ids(self, domain, order=None):
        return self.search([domain], order=order)

    # overwrite
    def create_attendees(self):
        return []
