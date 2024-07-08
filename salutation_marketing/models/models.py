# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Union, Tuple
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MarketingAutomation(models.Model):
    _inherit = 'marketing.activity'

    @api.model
    def _get_recipient_available_fields(
        self
    ) -> List[Union[Tuple[str, str]]]:
        """
        Extend the recipient fields for marketing automation activities.
        """
        fields = super()._get_recipient_available_fields()
        fields.append(('name_given', 'Given Name'))
        fields.append(('name_family', 'Family Name'))
        fields.append(('name_salutation', 'Salutation'))
        return fields
