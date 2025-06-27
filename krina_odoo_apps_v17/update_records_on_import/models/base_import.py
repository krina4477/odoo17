# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields, _


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    def execute_import(self, fields, columns, options, dryrun=False):
        if 'field_to_check' in options:
            return super(Import, self.with_context(field_to_check=self._context.get('field_to_check'))).execute_import(fields,
                                                                                                                 columns,
                                                                                                                 options,
                                                                                                                 dryrun=dryrun)
        else:
            return super(Import, self).execute_import(fields, columns, options, dryrun=dryrun)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _load_records_create(self, values):
        new_vals = values if type(values) == list else [values]
        record_ids = self.env[self._name]
        for vals in new_vals:
            record_id = False
            if 'field_to_check' in self._context and self._context.get('field_to_check') in vals:
                field_name = self._context.get('field_to_check')
                field_value = vals.get(field_name)
                if field_value:

                    record_id = self.search([(field_name, '=', field_value)], limit=1)
                    if record_id:
                        record_id.write(vals)
                if not record_id:
                    record_id = self.create(vals)
                record_ids += record_id
        if record_ids:
            return record_ids
        return super(BaseModel, self)._load_records_create(values)
