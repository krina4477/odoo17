/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { registry } from "@web/core/registry";
import { FormController } from '@web/views/form/form_controller';
import { ListController } from '@web/views/list/list_controller';

patch(FormController.prototype, {
    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems();
        if (session.hasGroup){

            delete menuItems.delete;
        }
        return menuItems
    }
});

patch(ListController.prototype, {
    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems();
        if (session.hasGroup){

            delete menuItems.delete;
        }
        return menuItems
    }
});