# -*- coding: utf-8 -*-

{
    'name': 'Python Running Status',
    'version': '1.0.0.1',
    'summary': """Display Running Python Version and List Of Packages Installed. Pip libraries""",
    'description': """Display Running Python Version and List Of Packages Installed.""",
    'category': 'Base',
    'author': 'bisolv',
    'website': "",
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['base_setup'],

    'data': [
        'security/ir.model.access.csv',
        'views/config_view.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.gif'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
