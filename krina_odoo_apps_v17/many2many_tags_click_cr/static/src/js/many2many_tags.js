/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Many2ManyTagsField, many2ManyTagsField } from "@web/views/fields/many2many_tags/many2many_tags_field";

export class TagsOpenMany2ManyTagsField extends Many2ManyTagsField {
    setup(){
        super.setup(...arguments);
        this.actionService = useService("action");
    }

    getTagProps(record) {
        const props = super.getTagProps(record);
        props.onClick = (ev) => this.onOpenClick(ev, record);
        return props;
    }
    onOpenClick(ev, record) {
        if(record.resModel && record.id){
            this.actionService.doAction({
                type: "ir.actions.act_window",
                res_model: record.resModel,
                res_id: record.resId,
                views: [[false, "form"]],
                view_mode: "form",
            });
        }
    }
}

export const tagsOpenMany2ManyTagsField = {
    ...many2ManyTagsField,
    component: TagsOpenMany2ManyTagsField,
};

registry.category("fields").add("many2many_tags_open", tagsOpenMany2ManyTagsField);