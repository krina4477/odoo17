# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, fields, models
from odoo.osv import expression


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    def _get_default_tag_id(self):
        return self.env.ref('payment_customer_tags_cr.res_partner_category_all', False)

    tag_ids = fields.Many2many('res.partner.category', string="Customer Tags", default=_get_default_tag_id)

    @api.model
    def _get_compatible_providers(
            self, company_id, partner_id, amount, currency_id=None, force_tokenization=False,
            is_express_checkout=False, is_validation=False, **kwargs
    ):
        # Compute the base domain for compatible providers.
        domain = [
            *self.env['payment.provider']._check_company_domain(company_id),
            ('state', 'in', ['enabled', 'test']),
        ]

        # Handle the is_published state.
        if not self.env.user._is_internal():
            domain = expression.AND([domain, [('is_published', '=', True)]])

        # Handle the partner country; allow all countries if the list is empty.
        partner = self.env['res.partner'].browse(partner_id)
        if partner.country_id:  # The partner country must either not be set or be supported.
            domain = expression.AND([
                domain,
                ['|', ('available_country_ids', '=', False), ('available_country_ids', 'in', [partner.country_id.id])],
                ['|', ('tag_ids', '=', False), ('tag_ids', 'in', partner.category_id.ids)]
            ])

        # Handle the maximum amount.
        currency = self.env['res.currency'].browse(currency_id).exists()
        if not is_validation and currency:  # The currency is required to convert the amount.
            company = self.env['res.company'].browse(company_id).exists()
            date = fields.Date.context_today(self)
            converted_amount = currency._convert(amount, company.currency_id, company, date)
            domain = expression.AND([
                domain, [
                    '|', '|',
                    ('maximum_amount', '>=', converted_amount),
                    ('maximum_amount', '=', False),
                    ('maximum_amount', '=', 0.),
                ]
            ])

        # Handle the available currencies; allow all currencies if the list is empty.
        if currency:
            domain = expression.AND([
                domain, [
                    '|',
                    ('available_currency_ids', '=', False),
                    ('available_currency_ids', 'in', [currency.id]),
                ]
            ])

        # Handle tokenization support requirements.
        if force_tokenization or self._is_tokenization_required(**kwargs):
            domain = expression.AND([domain, [('allow_tokenization', '=', True)]])

        if force_tokenization or self._is_tokenization_required(**kwargs):
            domain = expression.AND([domain, [('support_tokenization', '=', True)]])

        # Handle express checkout.
        if is_express_checkout:
            domain = expression.AND([domain, [('allow_express_checkout', '=', True)]])

        # Search the providers matching the compatibility criteria.
        compatible_providers = self.env['payment.provider'].search(domain)
        return compatible_providers
