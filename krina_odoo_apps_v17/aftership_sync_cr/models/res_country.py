# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

try:
    import pycountry
except ImportError:
    pass


class ResCountry(models.Model):
    _inherit = 'res.country'

    code_alpha3 = fields.Char(
        string='Country Code (3-letter)', size=3, store=True,
        help='ISO 3166-1 alpha-3 (three-letter) code for the country',
        compute="_compute_codes")
    code_numeric = fields.Char(
        string='Country Code (numeric)', size=3, store=True,
        help='ISO 3166-1 numeric code for the country',
        compute="_compute_codes")

    @api.depends('code')
    def _compute_codes(self):
        for country in self:
            c = False
            for country_type in ['countries', 'historic_countries']:
                try:
                    c = getattr(pycountry, country_type).get(
                        alpha_2=country.code)
                except KeyError:
                    try:
                        c = getattr(pycountry, country_type).get(
                            alpha2=country.code)
                    except KeyError:
                        pass
                if c:
                    break
            if c:
                country.code_alpha3 = getattr(c, 'alpha_3',
                                              getattr(c, 'alpha3', False))
                country.code_numeric = c.numeric
            else:
                country.code_alpha3 = False
                country.code_numeric = False
