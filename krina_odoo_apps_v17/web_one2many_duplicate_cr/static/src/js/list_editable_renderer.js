/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";

patch(ListRenderer.prototype, {

    setup() {

        super.setup(...arguments);
    },
    
    async onCopyRecord(record) {

        if (this.isX2Many){

            if (record){

                var new_copy_data_dict = {};

                for (var fieldname in record.evalContextWithVirtualIds) {
                    if (record.evalContextWithVirtualIds.hasOwnProperty(fieldname)) {
                        var fieldvalue = record.evalContextWithVirtualIds[fieldname];
                        new_copy_data_dict['default_' + fieldname] = fieldvalue;
                    }
                }

                var context_to_pass = Object.assign({}, this.state.context, new_copy_data_dict);

                this.props.onAdd({ context: context_to_pass, editable: 'bottom' });

            }
        }    
    }
});

ListRenderer.template = "web.ListRenderer";