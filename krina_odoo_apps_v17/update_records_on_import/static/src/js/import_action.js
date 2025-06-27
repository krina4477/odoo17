/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { BaseImportModel } from "@base_import/import_model"

patch(BaseImportModel.prototype, {
    async _callImport(dryrun, args) {

        this.importOptionsValues['field_to_check'] = {'field_to_check': $('.o_import_update_option:checked').val()}
        try {
  
            const res = await this.orm.silent.call("base_import.import", "execute_import", args, {
                dryrun,
                context: {'field_to_check': $('.o_import_update_option:checked').val()},
            });
            return res;
        } catch (error) {

            // This pattern isn't optimal but it is need to have
            // similar behaviours as in legacy. That is, catching
            // all import errors and showing them inside the top
            // "messages" area.
            return { error };
        }
    }
})
