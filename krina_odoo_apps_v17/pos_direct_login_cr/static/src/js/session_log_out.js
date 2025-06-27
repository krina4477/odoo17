/** @odoo-module */
// Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
// See LICENSE file for full copyright and licensing details.

import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { ConnectionAbortedError, ConnectionLostError, rpcService } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import {ErrorPopup} from "@point_of_sale/app/errors/popups/error_popup";

patch(ClosePosPopup.prototype,{
       setup(){
            super.setup();
       },
       async closeSession() {
            this.customerDisplay?.update({ closeUI: true });
            if (this.pos.config.cash_control) {
                const response = await this.orm.call(
                    "pos.session",
                    "post_closing_cash_details",
                    [this.pos.pos_session.id],
                    {
                        counted_cash: parseFloat(
                            this.state.payments[this.props.default_cash_details.id].counted
                        ),
                    }
                );

                if (!response.successful) {
                    return this.handleClosingError(response);
                }
            }

            try {
                await this.orm.call("pos.session", "update_closing_control_state_session", [
                    this.pos.pos_session.id,
                    this.state.notes,
                ]);
            } catch (error) {
                if (!error.data && error.data.message !== "This session is already closed.") {
                    throw error;
                }
            }

            try {
                const bankPaymentMethodDiffPairs = this.props.other_payment_methods
                    .filter((pm) => pm.type == "bank")
                    .map((pm) => [pm.id, this.getDifference(pm.id)]);
                const response = await this.orm.call("pos.session", "close_session_from_ui", [
                    this.pos.pos_session.id,
                    bankPaymentMethodDiffPairs,
                ]);
                if (!response.successful) {
                    return this.handleClosingError(response);
                }

                const permission = await this.orm.call("pos.session", "get_permission_for_log_out", [
                        this.pos.pos_session.id,
                        this.pos.pos_session.config_id[0]
                    ]);

                if(permission == true){
                    window.location = "/web/session/logout";
                }else{
                    window.location = "/web#action=point_of_sale.action_client_pos_menu";
                }

            } catch (error) {
                if (error instanceof ConnectionLostError) {
                    throw error;
                } else {
                    const permission = await this.orm.call("pos.session", "get_permission_for_log_out", [
                        this.pos.pos_session.id,
                        this.pos.pos_session.config_id[0]
                    ]);

                    if(permission == true){
                        window.location = "/web/session/logout";
                    }else{
                        window.location = "/web#action=point_of_sale.action_client_pos_menu";
                    }
                }
            }
       },
});



