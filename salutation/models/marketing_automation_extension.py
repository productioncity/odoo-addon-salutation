from odoo import api, models

class MarketingAutomation(models.Model):
    _inherit = 'marketing.activity'

    @api.model
    def _get_recipient_available_fields(self):
        """
        Extend the recipient fields for marketing automation activities.
        """
        fields = super(MarketingAutomation, self)._get_recipient_available_fields()
        fields.append(('name_given', 'Given Name'))
        fields.append(('name_family', 'Family Name'))
        fields.append(('name_salutation', 'Salutation'))
        return fields
