# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    running_python_version = fields.Char(default=lambda x: x.get_python_version())

    def get_python_version(self):
        from platform import python_version
        return "Python %s" % python_version()

    def button_open_python_packages(self):
        self.ensure_one()
        self.env['python.package.installed'].sudo().update_packages()
        return {'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'target': 'new',
                'res_model': 'python.package.installed',
                'name': "%s Installed Packages" % self.running_python_version,
                }


class PythonPackageInstalled(models.Model):
    _name = 'python.package.installed'
    _description = 'Python Package Installed'

    name = fields.Char(string="Package")
    version = fields.Char(string="Installed Version")

    def update_packages(self):
        import pkg_resources
        installed_packages = pkg_resources.working_set

        self.search([]).unlink()
        for package in installed_packages:
            vals = {'name': package.key, 'version': package.version, }
            self.create([vals])
