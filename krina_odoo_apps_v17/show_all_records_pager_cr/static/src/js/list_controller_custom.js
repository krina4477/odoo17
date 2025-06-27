/** @odoo-module **/

import { Pager } from "@web/core/pager/pager";
import { Component, useExternalListener, useState } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";

patch(Pager.prototype,{
    setup()
    {
        super.setup();
    },
    _showAll(ev){
        if($(ev.target).hasClass('o_pager_show_all')){
              this.setValue("1-" + this.props.total);
            if(!this.initial_limit){
                this.initial_limit = 80
            }
            $(ev.target).text("Reset").removeClass('o_pager_show_all');
            this.setValue("1-" + this.props.total);
        }
        else{
            $(ev.target).text("Show All").addClass('o_pager_show_all');
            this.setValue('1-80');
        }
    }
});