# -*- coding: utf-8 -*-
{
    'name': "salutation",

    'summary': "Adds salutation fields to contacts",

    'description': """
Adds salutation fields to contacts
    """,

    'author': "Production City",
    'website': "https://github.com/productioncity/odoo-addon-salutation",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/server_actions.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

