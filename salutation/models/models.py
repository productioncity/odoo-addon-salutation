# -*- coding: utf-8 -*-
from typing import Dict, Optional, Any, List, Tuple
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_given: Optional[str] = fields.Char(
        string="Given Name"
    )
    name_family: Optional[str] = fields.Char(
        string="Family Name"
    )
    name_salutation: Optional[str] = fields.Char(
        string="Salutation"
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

    @api.onchange('name', 'lang', 'title')
    def _onchange_name(self) -> None:
        """
        Onchange method to update name_given, name_family, and name_salutation
        based on the name field changes. Automatically generates these fields
        if they are not set.
        """
        for record in self:
            if record.company_type == 'person':
                name_parts = record._generate_name_parts(record.name)
                if not record.name_given:
                    record.name_given = name_parts['given']
                if not record.name_family:
                    record.name_family = name_parts['family']
                if not record.name_salutation:
                    record.name_salutation = name_parts['salutation']

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
            'salutation': salutation,
        }

    @api.model_create_multi
    def create(self, vals_list: List[Dict[str, Any]]) -> models.BaseModel:
        """
        Overrides the create method to populate name parts if not overridden by the user.
        Handles batch creation.

        Args:
            vals_list: List of dictionaries of values for creating new records.

        Returns:
            The created ResPartner records.
        """
        for vals in vals_list:
            if vals.get('company_type', 'company') == 'person':
                name_parts = self._generate_name_parts(vals.get('name', ''))
                vals.setdefault('name_given', name_parts['given'])
                vals.setdefault('name_family', name_parts['family'])
                vals.setdefault('name_salutation', name_parts['salutation'])
        return super().create(vals_list)

    def write(self, vals: Dict[str, Any]) -> bool:
        """
        Overrides the write method to update name parts if the name changes and if not
        overridden by the user.

        Args:
            vals: Dictionary of values for updating the record.

        Returns:
            True if the write operation was successful, False otherwise.
        """
        if 'name' in vals:
            for record in self:
                if record.company_type == 'person':
                    name_parts = record._generate_name_parts(vals.get('name', record.name))
                    updates = {}
                    if not vals.get('name_given'):
                        updates['name_given'] = name_parts['given']
                    if not vals.get('name_family'):
                        updates['name_family'] = name_parts['family']
                    if not vals.get('name_salutation'):
                        updates['name_salutation'] = name_parts['salutation']
                    if updates:
                        vals.update(updates)
        return super().write(vals)

    def name_get(self) -> List[Tuple[int, str]]:
        """
        Override the default name_get method to generate name parts if they are not
        set, based on the contact's primary name field.

        Returns:
            List of tuples containing record IDs and display names.
        """
        result: List[Tuple[int, str]] = []
        for record in self:
            if record.company_type == 'person':
                if not record.name_given or not record.name_family or not record.name_salutation:
                    name_parts = record._generate_name_parts()
                    if not record.name_given:
                        record.name_given = name_parts['given']
                    if not record.name_family:
                        record.name_family = name_parts['family']
                    if not record.name_salutation:
                        record.name_salutation = name_parts['salutation']
            result.append((record.id, record.name))
        return result

    def _update_existing_contacts(self) -> None:
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