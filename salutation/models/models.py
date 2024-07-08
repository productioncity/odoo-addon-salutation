# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Union, Tuple
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_given: Optional[str] = fields.Char(string="Given Name")
    name_family: Optional[str] = fields.Char(string="Family Name")
    name_salutation: Optional[str] = fields.Char(string="Salutation")

    is_given_name_manual: bool = fields.Boolean(string="Is Given Name Manual", default=False)
    is_family_name_manual: bool = fields.Boolean(string="Is Family Name Manual", default=False)
    is_salutation_manual: bool = fields.Boolean(string="Is Salutation Manual", default=False)

    REVERSE_LANGUAGES: List[str] = [
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
        """Onchange method to update name_given, name_family, and name_salutation
        based on the name field changes. Automatically generates these fields
        if they are not set or not manually overridden.
        """
        for record in self:
            if record.company_type == 'person':
                name_parts = record._generate_name_parts(record.name)
                if not record.is_given_name_manual:
                    record.name_given = name_parts['given']
                if not record.is_family_name_manual:
                    record.name_family = name_parts['family']
                if not record.is_salutation_manual:
                    record.name_salutation = name_parts['salutation']

    @api.onchange('name_given')
    def _onchange_name_given(self) -> None:
        """Onchange method to set the is_given_name_manual flag when the given name is changed."""
        for record in self:
            name_parts = record._generate_name_parts(
                record.name, record.title.shortcut if record.title else '', record.lang
            )
            if record.name_given and record.name_given != name_parts['given']:
                record.is_given_name_manual = True
            else:
                record.is_given_name_manual = False

    @api.onchange('name_family')
    def _onchange_name_family(self) -> None:
        """Onchange method to set the is_family_name_manual flag when the family name is changed."""
        for record in self:
            name_parts = record._generate_name_parts(
                record.name, record.title.shortcut if record.title else '', record.lang
            )
            if record.name_family and record.name_family != name_parts['family']:
                record.is_family_name_manual = True
            else:
                record.is_family_name_manual = False

    @api.onchange('name_salutation')
    def _onchange_name_salutation(self) -> None:
        """Onchange method to set the is_salutation_manual flag when the salutation is changed."""
        for record in self:
            name_parts = record._generate_name_parts(
                record.name, record.title.shortcut if record.title else '', record.lang
            )
            if record.name_salutation and record.name_salutation != name_parts['salutation']:
                record.is_salutation_manual = True
            else:
                record.is_salutation_manual = False

    @api.model
    def _generate_name_parts(
        self, 
        name: Optional[str] = None, 
        title: Optional[str] = None, 
        lang: Optional[str] = None
    ) -> Dict[str, str]:
        """Generates name parts based on the contact's name and language settings.

        Args:
            name (Optional[str]): Name to generate parts from. Defaults to self.name.
            title (Optional[str]): Title to use for the salutation. Defaults to self.title.shortcut.
            lang (Optional[str]): Language code to use for generating name parts. Defaults to self.lang or self.env.user.lang.

        Returns:
            Dict[str, str]: A dictionary containing 'given', 'family', and 'salutation' name parts.
        """
        name = name or self.name or ''
        name_parts = name.split()
        lang = lang or self.lang or self.env.user.lang
        title = title or (self.title.shortcut if self.title else '')

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
        """Overrides the create method to populate name parts if not overridden by the user.
        Handles batch creation.

        Args:
            vals_list (List[Dict[str, Any]]): List of dictionaries of values for creating new records.

        Returns:
            models.BaseModel: The created ResPartner records.
        """
        for vals in vals_list:
            if vals.get('company_type', 'company') == 'person':
                name_parts = self._generate_name_parts(
                    vals.get('name', ''), 
                    vals.get('title', {}).get('shortcut', ''), 
                    vals.get('lang', '')
                )
                if not vals.get('is_given_name_manual', False):
                    vals.setdefault('name_given', name_parts['given'])
                if not vals.get('is_family_name_manual', False):
                    vals.setdefault('name_family', name_parts['family'])
                if not vals.get('is_salutation_manual', False):
                    vals.setdefault('name_salutation', name_parts['salutation'])
        return super().create(vals_list)

    def write(self, vals: Dict[str, Any]) -> bool:
        """Overrides the write method to update name parts if the name changes
        and if not overridden by the user.

        Args:
            vals (Dict[str, Any]): Dictionary of values for updating the record.

        Returns:
            bool: Returns True if the write operation was successful, False otherwise.
        """
        if 'name' in vals:
            for record in self:
                if record.company_type == 'person':
                    title_shortcut = (None if not record.title else record.title.shortcut)
                    if 'title' in vals:
                        title = self.env['res.partner.title'].browse(vals['title'])
                        if title.exists():
                            title_shortcut = title.shortcut

                    name_parts = record._generate_name_parts(
                        vals['name'] if 'name' in vals else record.name,
                        title_shortcut,
                        vals.get('lang', record.lang)
                    )
                    updates: Dict[str, str] = {}

                    if 'name_given' not in vals and not record.is_given_name_manual:
                        updates['name_given'] = name_parts['given']
                    if 'name_family' not in vals and not record.is_family_name_manual:
                        updates['name_family'] = name_parts['family']
                    if 'name_salutation' not in vals and not record.is_salutation_manual:
                        updates['name_salutation'] = name_parts['salutation']

                    if updates:
                        vals.update(updates)
        return super().write(vals)

    def name_get(self) -> List[Tuple[int, str]]:
        """Override the default name_get method to generate name parts if they are not
        set, based on the contact's primary name field.

        Returns:
            List[Tuple[int, str]]: List of tuples containing record IDs and display names.
        """
        result: List[Tuple[int, str]] = []
        for record in self:
            if record.company_type == 'person':
                name_parts = record._generate_name_parts()
                if not record.name_given and not record.is_given_name_manual:
                    record.name_given = name_parts['given']
                if not record.name_family and not record.is_family_name_manual:
                    record.name_family = name_parts['family']
                if not record.name_salutation and not record.is_salutation_manual:
                    record.name_salutation = name_parts['salutation']
            result.append((record.id, record.name))
        return result

    def _update_existing_contacts(self) -> None:
        """Method to update existing contacts to populate new fields."""
        _logger.info("Starting to update existing contacts...")

        partners = self.search([])
        for partner in partners:
            _logger.info(f"Processing partner: {partner.name}")

            if partner.company_type == 'person':
                name_parts = partner._generate_name_parts()
                updates: Dict[str, str] = {}
                if not partner.name_given and not partner.is_given_name_manual:
                    updates['name_given'] = name_parts['given']
                if not partner.name_family and not partner.is_family_name_manual:
                    updates['name_family'] = name_parts['family']
                if not partner.name_salutation and not partner.is_salutation_manual:
                    updates['name_salutation'] = name_parts['salutation']

                if updates:
                    _logger.info(f"Updating partner ({partner.id}) with data: {updates}")
                    try:
                        success = partner.write(updates)
                        if success:
                            _logger.info(f"Successfully updated partner ({partner.id})")
                        else:
                            _logger.error(f"Failed to update partner ({partner.id})")
                        self.env.cr.commit()  # Ensure the transaction is saved.
                    except Exception as e:
                        _logger.exception(f"Exception when updating partner ({partner.id}): {str(e)}")
                else:
                    _logger.info(f"No updates needed for partner: {partner.name}")

        _logger.info("Completed updating existing contacts.")

    def reset_name_parts(self) -> None:
        """Method to reset name parts and their manual flags to auto-generated values."""
        for record in self:
            if record.company_type == 'person':
                name_parts = record._generate_name_parts()
                record.write({
                    'name_given': name_parts['given'],
                    'name_family': name_parts['family'],
                    'name_salutation': name_parts['salutation'],
                    'is_given_name_manual': False,
                    'is_family_name_manual': False,
                    'is_salutation_manual': False,
                })

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    @api.model
    def _get_partner_fields(self) -> Dict[str, str]:
        """Extend the partner fields shown as merge variables in email templates.

        Returns:
            Dict[str, str]: Dictionary of partner fields including given name, family name, and salutation.
        """
        partner_fields = super()._get_partner_fields()
        partner_fields.update({
            'name_given': 'Given Name',
            'name_family': 'Family Name',
            'name_salutation': 'Salutation'
        })
        return partner_fields
