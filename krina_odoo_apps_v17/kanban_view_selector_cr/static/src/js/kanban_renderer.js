/** @odoo-module **/
//  Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
//  See LICENSE file for full copyright and licensing details.

import { patch } from "@web/core/utils/patch";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { registry } from '@web/core/registry';
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { KanbanColumnQuickCreate } from "@web/views/kanban/kanban_column_quick_create";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { KanbanRecordQuickCreate } from "@web/views/kanban/kanban_record_quick_create";
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { kanbanView } from "@web/views/kanban/kanban_view";

patch(KanbanRenderer.prototype,{
    toggleSelection() {
        const checked = $('input[type=checkbox]:checked');
        const list = this.props.list;
        var inputselected = Object.values(checked)
        var iter = 0;
        var loopstop = inputselected.length - 2;
        if (checked.length > 0) {
            inputselected.forEach((select) => {
                if(iter < loopstop ){
                    list.records.forEach((record) => {
                        if(select.id == record.id){ 
                            record._toggleSelection(true);
                        }
                        else{
                            record._toggleSelection(false);
                            this.isDomainSelected = false;
                        }
                    });
                    iter += 1;
                }
            });
        }
        else {
            list.records.forEach((record) => {
                record._toggleSelection(false);
                list.selectDomain(false);
            });

        }
    },

});








