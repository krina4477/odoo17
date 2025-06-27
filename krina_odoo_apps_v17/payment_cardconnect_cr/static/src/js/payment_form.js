/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";
import paymentForm from '@payment/js/payment_form';
import { jsonrpc } from "@web/core/network/rpc_service";
//import { rpc } from "@web/core/network/rpc";

import { useService } from "@web/core/utils/hooks";

paymentForm.include({

//    init() {
//        this._super(...arguments);
//        this.notification = this.bindService("notification");
//    },





    // #=== PAYMENT FLOW ===#

    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'cardconnect') {
            this._super(...arguments);
            return;
        }
        const cc_number = document.getElementById('cc_number').value;
        const cc_brand = document.getElementById('cc_brand').value;
        const cc_holder_name = document.getElementById('cc_holder_name').value;
        const cc_expiry = document.getElementById('cc_expiry').value;
        const cc_cvc = document.getElementById('cc_cvc').value;

            // Perform validation checks
        if (!cc_number || !cc_brand || !cc_holder_name || !cc_expiry || !cc_cvc) {
                if (!cc_number) {
                    $('input#cc_number').addClass('is-invalid o_has_error').removeClass('o_has_success is-valid');
                }
                if (!cc_brand) {
                    $('input#cc_brand').addClass('is-invalid o_has_error').removeClass('o_has_success is-valid');
                }
                if (!cc_holder_name) {
                    $('input#cc_holder_name').addClass('is-invalid o_has_error').removeClass('o_has_success is-valid');
                }
                if (!cc_expiry) {
                    $('input#cc_expiry').addClass('is-invalid o_has_error').removeClass('o_has_success is-valid');
                }
                if (!cc_cvc) {
                    $('input#cc_cvc').addClass('is-invalid o_has_error').removeClass('o_has_success is-valid');
                }
            }

            // If all required fields are filled, proceed with the payment RPC call
        if (cc_number && cc_brand && cc_holder_name && cc_expiry && cc_cvc) {
                jsonrpc('/payment/cardconnect/s2s/create_json_3ds', {
                        'reference': processingValues.reference,
                        'provider_id': processingValues.provider_id,
                        'partner_id': processingValues.partner_id,
                        'cc_number': cc_number,
                        'cc_brand': cc_brand,
                        'cc_holder_name': cc_holder_name,
                        'cc_expiry': cc_expiry,
                        'cc_cvc': cc_cvc

//                rpc("/payment/cardconnect/s2s/create_json_3ds", {
//                        'reference': processingValues.reference,
//                        'provider_id': processingValues.provider_id,
//                        'partner_id': processingValues.partner_id,
//                        'cc_number': cc_number,
//                        'cc_brand': cc_brand,
//                        'cc_holder_name': cc_holder_name,
//                        'cc_expiry': cc_expiry,
//                        'cc_cvc': cc_cvc

                }).then(paymentResponse => {
                    if (paymentResponse && paymentResponse.error) {
                        this._displayErrorDialog(
                            _t("Server Error"),
                            _t("We are not able to process your payment."),
                            paymentResponse.error
                        );
                    } else {
                        // Redirect to status page after successful payment
                        window.location = '/payment/status';
                    }
                }).catch((error) => {
                    error.event.preventDefault();
                    this._displayErrorDialog(
                        _t("Server Error"),
                        _t("We are not able to process your payment."),
                        error.message.data.message
                    );
                });
         } else {
            console.log("this._displayErrorDialog",this._displayErrorDialog)
            return  this._displayErrorDialog(
                    _t("Server Error"),
                    _t("Please Check card details"),
                );
            }

    },
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {

       console.log("paymentMethodCodeS",paymentMethodCode)
       console.log("providerCode",providerCode)
       if (providerCode !== 'cardconnect') {
            return this._super(...arguments);
       }else if (flow === 'token') {
            return Promise.resolve();
       }
        this._setPaymentFlow('direct');
        return Promise.resolve();
    },

});


