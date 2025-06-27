# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import api, fields, models, _
from odoo.osv.expression import AND, OR

import json
from datetime import datetime


class PosConfigCacheData(models.Model):
    _name = "pos.config.cache.data"

    config_id = fields.Many2one("pos.config", string="Pos Config")
    model_name = fields.Char("Model Name")
    session_id = fields.Many2one("pos.session", string="Pos Session", domain=[('active', '=', False)])

    def import_cache_data_config(self, config):
        models = [
            'product.product',
        ]
        session_id = self.env['pos.session'].create({
            'config_id': config.id,
            'state': 'closed',
            'active': False,
        })
        for model_name in models:
            self.env['pos.config.cache.data'].create({
                'config_id': config.id,
                'model_name': model_name,
                'session_id': session_id.id
            })

    def import_cache_all_data_config(self, config):
        models = [
            'product.product',
        ]

        for model in models:
            count = 0
            existing_records = self.env['pos.config.cache.data'].search([
                ('model_name', '=', model),
                ('config_id', '=', config.id),
            ])

            # List to store values for bulk creation
            bulk_create_vals = []

            for record in existing_records:
                params = getattr(record.session_id, '_loader_params_%s' % model.replace('.', '_'), None)
                self.env['pos.config.cache.model.data'].search([('product_id', '=', False)]).unlink()
                data = self.env['pos.config.cache.model.data'].search_read([
                    ('config_id', '=', record.config_id.id),
                    ('model_name', '=', model)
                ], fields=['res_id'])
                ids = []
                for line in data:
                    ids.append(int(line['res_id']))
                selected_fields = self.env[model].search_read([
                    ('id', 'not in', ids),
                    ('available_in_pos', '=', True),
                ], fields=params()['search_params']['fields'])
                record.session_id._process_pos_ui_product_product(selected_fields)
                for product in selected_fields:
                    count = count + 1
                    vals = {
                        'config_id': record.config_id.id,
                        'session_id': record.session_id.id,
                        'model_name': model,
                        'res_id': product.get('id'),
                        'json_data': product[0] if type(product) is list else product,
                        'product_id': int(product.get('id')),
                    }
                    bulk_create_vals.append(vals)

            # Perform bulk create operations
            if bulk_create_vals:
                self.env['pos.config.cache.model.data'].create(bulk_create_vals)

    def import_cache_data(self):
        config_ids = self.env['pos.config'].search([])
        models = [
            'product.product',
        ]
        for config in config_ids:
            existing_session = self.env['pos.session'].search([
                ('config_id', '=', config.id),
                ('state', '=', 'closed'),
                ('active', '=', False),
            ], limit=1)

            if not existing_session:
                session_id = self.env['pos.session'].create({
                    'config_id': config.id,
                    'state': 'closed',
                    'active': False,
                })
            else:
                session_id = existing_session

            for model_name in models:
                existing_record = self.env['pos.config.cache.data'].search_count([
                    ('config_id', '=', config.id),
                    ('model_name', '=', model_name)
                ])
                if existing_record == 0:
                    self.env['pos.config.cache.data'].create({
                        'config_id': config.id,
                        'model_name': model_name,
                        'session_id': session_id.id
                    })

    def import_cache_all_data(self):
        models = [
            'product.product',
        ]

        for model in models:
            count = 0
            existing_records = self.env['pos.config.cache.data'].search([('model_name', '=', model)])

            # List to store values for bulk creation
            bulk_create_vals = []

            for record in existing_records:
                params = getattr(record.session_id, '_loader_params_%s' % model.replace('.', '_'), None)
                self.env['pos.config.cache.model.data'].search([('product_id', '=', False)]).unlink()
                data = self.env['pos.config.cache.model.data'].search_read([
                    ('config_id', '=', record.config_id.id),
                    ('model_name', '=', model)
                ], fields=['res_id'])
                ids = []
                for line in data:
                    ids.append(int(line['res_id']))
                selected_fields = self.env[model].search_read([
                    ('id', 'not in', ids),
                    ('available_in_pos', '=', True),
                ], fields=params()['search_params']['fields'])
                record.session_id._process_pos_ui_product_product(selected_fields)
                for product in selected_fields:
                    count = count + 1
                    vals = {
                        'config_id': record.config_id.id,
                        'session_id': record.session_id.id,
                        'model_name': model,
                        'res_id': product.get('id'),
                        'json_data': product[0] if type(product) is list else product,
                        'product_id': int(product.get('id')),
                    }
                    bulk_create_vals.append(vals)

            # Perform bulk create operations
            if bulk_create_vals:
                self.env['pos.config.cache.model.data'].create(bulk_create_vals)

    def import_update_cache_data(self):
        return True

    #     models = [
    #         'product.product',
    #     ]
    #
    #     for model in models:
    #         count = 0
    #         existing_records = self.env['pos.config.cache.data'].search([('model_name', '=', model)])
    #
    #         for record in existing_records:
    #             params = getattr(record.session_id, '_loader_params_%s' % model.replace('.', '_'), None)
    #             data = self.env['pos.config.cache.model.data'].search_read([
    #                 ('config_id', '=', record.config_id.id),
    #                 ('model_name', '=', model)
    #             ], fields=['res_id'])
    #             ids = []
    #             for line in data:
    #                 ids.append(line['res_id'])
    #             selected_fields = self.env[model].search_read([
    #                 ('id', 'in', ids),
    #                 ('available_in_pos', '=', True),
    #             ], fields=params()['search_params']['fields'], limit=5000)
    #             record.session_id._process_pos_ui_product_product(selected_fields)
    #             cofig = record.config_id.id
    #             session_id = record.session_id.id
    #             update_query = ''
    #             for product in selected_fields:
    #                 def serialize_datetime(o):
    #                     if isinstance(o, datetime):
    #                         return o.isoformat()
    #                     raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')
    #                 update_query += """UPDATE pos_config_cache_model_data SET json_data = '%s' WHERE res_id = %s;""" % (
    #                     json.dumps(product, default=serialize_datetime), product['id']
    #                 )
    #             if update_query:
    #                 self.env.cr.execute(update_query)
    #                 self.env.cr.commit()

    def _cache_data(self):
        model = self._context.get('model')
        # Fetch all records in one go, avoiding repeated database queries
        existing_records = self.env['pos.config.cache.data'].search([('model_name', '=', model)])

        # Prepare a list to store values for batch create/write
        vals_list = []
        for record in existing_records:
            data = record.session_id.with_context(record=record, custom_method=True).get_details(model)

            # Process data only if available
            if data:
                record.session_id._process_pos_ui_product_product(data)
                vals = {
                    'config_id': record.config_id.id,
                    'session_id': record.session_id.id,
                    'model_name': model,
                    'res_id': self._context.get('res_id'),
                    'json_data': data[0] if isinstance(data, list) else data,
                }
                vals_list.append(vals)

        # Perform batch processing for existing records
        if vals_list:
            # Optimize fetching of existing records by using a dictionary for quick lookup
            existing_record_ids = self.env['pos.config.cache.model.data'].search_read(
                [('config_id', 'in', [val['config_id'] for val in vals_list]),
                 ('session_id', 'in', [val['session_id'] for val in vals_list]),
                 ('model_name', '=', model),
                 ('res_id', '=', self._context.get('res_id'))],
                ['id', 'config_id', 'session_id']
            )

            existing_record_dict = {(rec['config_id'], rec['session_id']): rec['id'] for rec in existing_record_ids}

            for vals in vals_list:
                record_key = (vals['config_id'], vals['session_id'])
                if record_key in existing_record_dict:
                    # Update existing record
                    self.env['pos.config.cache.model.data'].browse(existing_record_dict[record_key]).write(vals)
                else:
                    # Create a new record
                    self.env['pos.config.cache.model.data'].create(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        result = super(ProductProduct, self).create(vals_list)
        if not self._context.get('skip_log'):
            for rec in result:
                self.env['pos.config.cache.data'].with_context(model='product.product', res_id=rec.id)._cache_data()
        return result

    def write(self, vals):
        result = super(ProductProduct, self).write(vals)
        for rec in self:
            if not self._context.get('skip_log'):
                if rec and rec.active:
                    self.env['pos.config.cache.data'].with_context(model='product.product',
                                                                   res_id=rec.id)._cache_data()
        return result


class PosSession(models.Model):
    _inherit = 'pos.session'

    active = fields.Boolean(default=True)

    def get_details(self, model):
        params = getattr(self, '_loader_params_%s' % model.replace('.', '_'), None)
        data = []
        dynamic_model = self.env[model]
        data_ids = dynamic_model.search_read(params()['search_params']['domain'])
        if data_ids:
            data = dynamic_model.search_read([('id', '=', data_ids[0].get('id'))],
                                             fields=params()['search_params']['fields'])

        return data

    # <------------------------- product.product ------------------------->

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        if self._context.get('custom_method', False) and self._context.get('res_id', False):
            result.get('search_params').get('domain').append(('id', '=', self._context.get('res_id')))
            return result
        else:
            return result
