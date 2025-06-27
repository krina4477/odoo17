# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import binascii
import logging
import re
from textwrap import shorten
from odoo import http, models, fields, _
from odoo.http import request
from odoo.tools import OrderedSet, escape_psql, html_escape as escape
from odoo.addons.website.controllers.main import Website
logger = logging.getLogger(__name__)

class WebsiteCr(Website):

    @http.route('/website/snippet/autocomplete', type='json', auth='public', website=True)
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        res_val = super(WebsiteCr, self).autocomplete(search_type=search_type, term=term, order=order, limit=limit, max_nb_chars=max_nb_chars, options=options)
        order = self._get_search_order(order)
        options = options or {}
        results_count, search_results, fuzzy_term = request.website._search_with_fuzzy(search_type, term, limit, order, options)
        if not results_count:
            return {
                'results': [],
                'results_count': 0,
                'parts': {},
            }
        term = fuzzy_term or term
        search_results = request.website._search_render_results(search_results, limit)

        mappings = []
        results_data = []
        for search_result in search_results:
            results_data += search_result['results_data']
            mappings.append(search_result['mapping'])
        if search_type == 'all':
            # Only supported order for 'all' is on name
            results_data.sort(key=lambda r: r.get('name', ''), reverse='name desc' in order)
        results_data = results_data[:limit]
        result = []

        def get_mapping_value(field_type, value, field_meta):
            if field_type == 'text':
                if value and field_meta.get('truncate', True):
                    value = shorten(value, max_nb_chars, placeholder='...')
                if field_meta.get('match') and value and term:
                    pattern = '|'.join(map(re.escape, term.split()))
                    if pattern:
                        parts = re.split(f'({pattern})', value, flags=re.IGNORECASE)
                        if len(parts) > 1:
                            value = request.env['ir.ui.view'].sudo()._render_template(
                                "website.search_text_with_highlight",
                                {'parts': parts}
                            )
                            field_type = 'html'

            if field_type not in ('image', 'binary') and ('ir.qweb.field.%s' % field_type) in request.env:
                opt = {}
                if field_type == 'monetary':
                    opt['display_currency'] = options['display_currency']
                elif field_type == 'html':
                    opt['template_options'] = {}
                value = request.env[('ir.qweb.field.%s' % field_type)].value_to_html(value, opt)
            return escape(value)

        for record in results_data:
            mapping = record['_mapping']
            mapped = {
                '_fa': record.get('_fa'),
            }
            for mapped_name, field_meta in mapping.items():
                value = record.get(field_meta.get('name'))
                if not value:
                    mapped[mapped_name] = ''
                    continue
                field_type = field_meta.get('type')
                if field_type == 'dict':
                    # Map a field with multiple values, stored in a dict with values type: item_type
                    item_type = field_meta.get('item_type')
                    mapped[mapped_name] = {}
                    for key, item in value.items():
                        mapped[mapped_name][key] = get_mapping_value(item_type, item, field_meta)
                else:
                    is_true = True
                    if mapped_name == 'detail':
                        if record.get('id', False):
                            p_id = request.env['product.template'].browse(int(record.get('id', 0)))
                            if p_id.is_call_price:
                                is_true = False
                    if is_true:
                        mapped[mapped_name] = get_mapping_value(field_type, value, field_meta)
                    else:
                        mapped[mapped_name] = ''
            result.append(mapped)
        res_val.update({'results': result})
        return res_val


class CreateCallPrice(http.Controller):

    @http.route('/create/call/price', type='json', auth="public", website=True, csrf=False)
    def create_call_price(self, first_name=None,last_name=None,email_name=None,contact_no=None,no_of_quantity=None,message=None,**post):
        if first_name and email_name and contact_no and no_of_quantity and message:
            val = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email_name,
                    'mobile': contact_no,
                    'quantity': no_of_quantity,
                    'message': message
            }
            call_price_id = request.env['call.price'].sudo().create(val)
            if call_price_id:
                return {'status': True}
        else:
            return {'status': False}