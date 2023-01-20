from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero
import subprocess
import sys
import logging

_logger = logging.getLogger(__name__)

class PipInstall(models.TransientModel):
    _name='pip.install.wizard'
    name = fields.Char(string="Write Cammand")

    def action_install_now(self):
        cammand=self.name
        cammand=cammand.split(' ')
        try: 
            result=subprocess.run([sys.executable, "-m", *cammand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open('pip_install.log', 'a+') as log_file:
                log_file.write(result.stdout + result.stderr)    
            raise UserError(result.stdout + result.stderr)
        except Exception as e:
            _logger.error('Error in PIP install: %s', e)
            raise UserError(_('There was an error installing the package. Please see the log for more information.')
