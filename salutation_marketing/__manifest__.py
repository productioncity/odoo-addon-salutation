{
    # The name of the addon
    'name': "salutation_marketing",

    # A summary of the addon
    'summary': "Adds salutation fields, given name, and family name fields to marketing automation emails.",

    # A detailed description of the addon
    'description': """
    This addon enhances the Marketing Automation module in Odoo by adding the following fields to emails:
    - Salutation
    - Given Name
    - Family Name

    """,

    # Author information
    'author': "Production City",
    'website': "https://github.com/productioncity/odoo-addon-salutation",

    # The license type for this addon (commercial license)
    'license': "OPL-1",

    # The category and version of the addon
    'category': "Customizations",
    'version': '0.6',

    # Dependencies needed for this addon to work correctly
    'depends': ['base', 'contacts', 'salutation'],

    # Data that is always loaded
    'data': [
    ],
    
    # Data loaded in demonstration mode
    'demo': [
    ],

    # Image or icon for the addon
    'images': [
        'static/description/icon.png'
    ],
}
