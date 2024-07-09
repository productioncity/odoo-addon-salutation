# -*- coding: utf-8 -*-
"""
This module enhances the Marketing Automation module by incorporating salutation fields.
"""

from typing import List, Tuple
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class MarketingActivityExtension(models.AbstractModel):
    """Wrapper for extending Marketing Activity with additional fields."""
    _name = 'salutation.marketing.activity.extension'
    _description = 'Marketing Activity Extension Wrapper'

    @api.model
    def _register_hook(self) -> None:
        """Register hook to enhance `marketing.activity` model if it exists."""
        marketing_model_exists: bool = self.env.get('marketing.activity') is not None

        if marketing_model_exists:
            class MarketingAutomation(models.Model):
                """
                Dynamically extend the `marketing.activity` model.

                Extends the `marketing.activity` model with additional fields relevant
                to contact salutations, including given name, family name, and salutation.
                """
                _inherit = 'marketing.activity'

                @api.model
                def _get_recipient_available_fields(self) -> List[Tuple[str, str]]:
                    """
                    Extend the recipient fields for marketing automation activities.

                    Returns:
                        List[Tuple[str, str]]: Extended list of recipient fields including
                        given name, family name, and salutation.
                    """
                    fields: List[Tuple[str, str]] = super()._get_recipient_available_fields()
                    extended_fields = [
                        ('name_given', 'Given Name'),
                        ('name_family', 'Family Name'),
                        ('name_salutation', 'Salutation')
                    ]
                    fields.extend(extended_fields)
                    return fields

            # Register the dynamically created MarketingAutomation class
            MarketingAutomation._build_model(self.env['ir.model'])
            _logger.info(
                "'marketing.activity' model found and extended in salutation.marketing.activity.extension"
            )
        else:
            # Gather all models that start with 'marketing.'
            marketing_models: List[str] = [model for model in self.env.registry.keys() if model.startswith('marketing.')]
            _logger.warning(
                ("Model 'marketing.activity' does not exist, extension not registered in "
                 "salutation.marketing.activity.extension.\n"
                 "Available 'marketing.' models: %s"), marketing_models
            )