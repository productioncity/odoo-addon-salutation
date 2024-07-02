# -*- coding: utf-8 -*-
from typing import Dict, Optional
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_given = fields.Char(
        string="Given Name",
        default=lambda self: self._default_name_given(),
    )
    name_family = fields.Char(
        string="Family Name",
        default=lambda self: self._default_name_family(),
    )
    name_salutation = fields.Char(
        string="Salutation",
        default=lambda self: self._default_name_salutation(),
    )

    REVERSE_LANGUAGES = [
        'zh_CN',  # Chinese (Simplified)
        'zh_TW',  # Chinese (Traditional)
        'ko_KR',  # Korean
        'ja_JP',  # Japanese
        'vi_VN',  # Vietnamese
        'hu_HU',  # Hungarian
        'mn_MN',  # Mongolian
    ]

    @api.model
    def _default_name_given(self) -> str:
        """
        Returns the default given name based on the contact's name and language.
        """
        return self._generate_name_parts()['given']
    
    @api.model
    def _default_name_family(self) -> str:
        """
        Returns the default family name based on the contact's name and language.
        """
        return self._generate_name_parts()['family']
    
    @api.model
    def _default_name_salutation(self) -> str:
        """
        Returns the default salutation based on the contact's name and language.
        """
        return self._generate_name_parts()['salutation']
    
    @api.model
    def _generate_name_parts(self, name: Optional[str] = None) -> Dict[str, str]:
        """
        Generates name parts based on the contact's name and language settings.
        
        Args:
            name: Name to generate parts from. Defaults to self.name.
        
        Returns:
            A dictionary containing 'given', 'family', and 'salutation' name parts.
        """
        name = name or self.name or ''
        name_parts = name.split()
        lang = self.lang or self.env.user.lang or 'en_US'
        title = self.title.shortcut if self.title else ''
        
        if lang in self.REVERSE_LANGUAGES:
            given_name = name_parts[-1] if name_parts else ''
            family_name = name_parts[0] if name_parts else ''
        else:
            given_name = name_parts[0] if name_parts else ''
            family_name = name_parts[-1] if name_parts else ''
        
        salutation = f"{title} {family_name}" if title else given_name

        return {
            'given': given_name,
            'family': family_name,
            'salutation': salutation
        }

    @api.model
    def create(self, vals: Dict) -> 'ResPartner':
        """
        Overrides create method to populate name parts if not overridden by user.
        
        Args:
            vals: Values for the new record.
        
        Returns:
            The created ResPartner record.
        """
        if vals.get('company_type', 'company') != 'company':
            name_parts = self._generate_name_parts(vals.get('name', ''))
            vals.setdefault('name_given', name_parts['given'])
            vals.setdefault('name_family', name_parts['family'])
            vals.setdefault('name_salutation', name_parts['salutation'])
        return super().create(vals)
    
    def write(self, vals: Dict) -> bool:
        """
        Overrides write method to update name parts if the name changes and if not overridden by user.
        
        Args:
            vals: Values for the record update.
        
        Returns:
            True if the write operation was successful, False otherwise.
        """
        result = super().write(vals)
        for record in self:
            if record.company_type == 'individual' and 'name' in vals:
                name_parts = record._generate_name_parts()
                updates = {
                    'name_given': vals.get('name_given', name_parts['given']),
                    'name_family': vals.get('name_family', name_parts['family']),
                    'name_salutation': vals.get('name_salutation', name_parts['salutation']),
                }
                super(ResPartner, record).write(updates)
        return result
    
    def _update_existing_contacts(self):
        """
        Method to update existing contacts to populate new fields.
        """
        partners = self.search([])
        for partner in partners:
            name_parts = partner._generate_name_parts()
            partner.write({
                'name_given': name_parts['given'],
                'name_family': name_parts['family'],
                'name_salutation': name_parts['salutation'],
            })