/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { ActionMenus} from "@web/search/action_menus/action_menus";

import { Component, onWillStart, onWillUpdateProps,useState } from "@odoo/owl";

export const STATIC_ACTIONS_GROUP_NUMBER = 1;
export const ACTIONS_GROUP_NUMBER = 100;




patch(ActionMenus.prototype,{

	get  printItems() {
        if (session.hasGroup) {
			return false;
        }
        const printActions = this.props.items.print || [];

        return printActions.map((action) => ({
            action,
            description: action.name,
            key: action.id,
        }));

    },



    async getActionItems(props) {


        return (props.items.action || []).map((action) => {

            if (action.callback) {
                if (session.hasGroup) {
                    this.HideActionPrint = session.hasGroup
                    return false;
                }
                return Object.assign(
                    { key: `action-${action.description}`, groupNumber: ACTIONS_GROUP_NUMBER },
                    action           
                );
            } 
            else {
                if (session.hasGroup) {
                    this.HideActionPrint = session.hasGroup
                    return false;
                }
               
                this.HideActionPrint = false
                return {
                    action,
                    description: action.name,
                    key: action.id,
                    groupNumber: action.groupNumber || ACTIONS_GROUP_NUMBER,
                };
            }
        });
    },
    
    

});
