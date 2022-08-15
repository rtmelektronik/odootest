# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import pip

from . import controllers
from . import models
from . import wizards

try:
    import openupgradelib
except ImportError:
    print('\n There was no such module named -openupgradelib- installed')
    print('xxxxxxxxxxxxxxxx installing openupgradelib xxxxxxxxxxxxxx')
    pip.main(['install', 'openupgradelib'])