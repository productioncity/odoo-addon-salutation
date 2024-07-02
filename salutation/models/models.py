# -*- coding: utf-8 -*-
from typing import Dict
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_given = fields.Char(string="Given Name", default=lambda self: self._default_name_given())
    name_family = fields.Char(string="Family Name", default=lambda self: self._default_name_family())
    name_salutation = fields.Char(string="Salutation", default=lambda self: self._default_name_salutation())

    REVERSE_LANGUAGES = ['ko_KR', 'ja_JP']  # Languages where the given name appears last

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
    def _generate_name_parts(self) -> Dict[str, str]:
        """
        Generates name parts based on the contact's name and language settings.

        Returns:
            Dict[str, str]: A dictionary containing 'given', 'family', and 'salutation' name parts.
        """
        name_parts = self.name.split() if self.name else []
        lang = self.lang or self.env.user.lang or 'en_US'
        title = self.title.shortcut if self.title else ''
        
        if lang in self.REVERSE_LANGUAGES:
            given_name = name_parts[-1] if name_parts else ''
            family_name = name_parts[0] if name_parts else ''
        else:
            given_name = name_parts[0] if name_parts else ''
            family_name = name_parts[-1] if name_parts else ''

        if title:
            salutation = f"{title} {family_name}"
        else:
            salutation = given_name

        return {
            'given': given_name,
            'family': family_name,
            'salutation': salutation
        }
    
    @api.model
    def create(self, vals: Dict) -> 'ResPartner':
        """
        Overrides the create method to populate name parts.

        Args:
            vals (Dict): Values for the new record.

        Returns:
            ResPartner: The created ResPartner record.
        """
        if 'name_given' not in vals or not vals['name_given']:
            name_parts = self._generate_name_parts(vals.get('name', ''))
            vals['name_given'] = name_parts['given']
        if 'name_family' not in vals or not vals['name_family']:
            name_parts = self._generate_name_parts(vals.get('name', ''))
            vals['name_family'] = name_parts['family']
        if 'name_salutation' not in vals or not vals['name_salutation']:
            name_parts = self._generate_name_parts(vals.get('name', ''))
            vals['name_salutation'] = name_parts['salutation']
        return super().create(vals)
    
    def write(self, vals: Dict) -> bool:
        """
        Overrides the write method to update name parts if the name changes.

        Args:
            vals (Dict): Values for the record update.

        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        result = super().write(vals)
        for record in self:
            if 'name' in vals:
                name_parts = record._generate_name_parts()
                updates = {
                    'name_given': name_parts['given'],
                    'name_family': name_parts['family'],
                    'name_salutation': name_parts['salutation']
                }
                super(ResPartner, record).write(updates)
        return result
