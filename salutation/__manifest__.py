{
    # The name of the addon
    'name': "salutation",

    # A summary of the addon
    'summary': "Adds salutation, given name, and family name fields to contacts",

    # A detailed description of the addon
    'description': """
    This addon enhances the Contacts module in Odoo by adding the following fields:
    - Salutation
    - Given Name
    - Family Name
    
    This helps in better categorisation and personalisation of contact records.
    """,

    # Author information
    'author': "Production City",
    'website': "https://github.com/productioncity/odoo-addon-salutation",

    # The license type for this addon (commercial license)
    'license': "OPL-1",

    # The category and version of the addon
    'category': "Customizations",
    'version': '0.8',

    # Dependencies needed for this addon to work correctly
    'depends': ['base', 'contacts'],

    # Data that is always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/server_actions.xml',
    ],
    
    # Data loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # Image or icon for the addon
    'images': [
        'static/description/icon.png'
    ],
}
