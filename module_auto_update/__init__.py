# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import pip
try:
    import scipy
except ImportError:
    print('\n There was no such module named -openupgradelib- installed')
    print('xxxxxxxxxxxxxxxx installing openupgradelib xxxxxxxxxxxxxx')
    pip.main(['install', 'scipy'])
from . import models
from .hooks import uninstall_hook
