/** @odoo-module **/

import paymentForm from '@payment/js/payment_form';
import { RPCError } from '@web/core/network/rpc_service';
import { _t } from "@web/core/l10n/translation";

paymentForm.include({

    setup(){
        super.setup(...arguments)
    },

    // #=== DOM MANIPULATION ===#

    _cardgetInlineFormInputs: function () {
        // console.log("provider_id", this)
        return {
            card: document.getElementById(`o_cielo_card_${this.paymentContext.providerId}`),
            month: document.getElementById(`o_cielo_month_${this.paymentContext.providerId}`),
            year: document.getElementById(`o_cielo_year_${this.paymentContext.providerId}`),
            code: document.getElementById(`o_cielo_code_${this.paymentContext.providerId}`),
            name: document.getElementById(`o_cielo_card_holder_name_${this.paymentContext.providerId}`),
            brand: document.getElementById(`o_cielo_brand_${this.paymentContext.providerId}`),
        };
    },

    _getPaymentDetails: function (paymentOptionId) {
        const inputs = this._cardgetInlineFormInputs();
        return {
            cardData: {
                cardNumber: inputs.card.value.replace(/ /g, ''), // Remove all spaces
                month: inputs.month.value,
                year: inputs.year.value,
                cardCode: inputs.code.value,
                cardHolder: inputs.name.value,
                cardBrand: inputs.brand.value,
            },
        };
    },

    /**
     * Prepare the inline form of Demo for direct payment.
     *
     * @override method from @payment/js/payment_form
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'cielo') {
            this._super(...arguments);
            return;
        }

        if (flow === 'token') {
            return;
        }

        this._setPaymentFlow('direct');
    },

     // #=== PAYMENT FLOW ===#

    /**
     * Simulate a feedback from a payment provider and redirect the customer to the status page.
     *
     * @override method from payment.payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    async _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {

        if (providerCode !== 'cielo' || flow === 'token') {
           return this._super(...arguments); // Tokens are handled by the generic flow
        }

        const secureData = {
            ...this._getPaymentDetails(paymentOptionId),
        };

            if (!this._cardvalidateFormInputs(paymentOptionId)) {
                this._enableButton(); // The submit button is disabled at this point, enable it
                this.call('ui', 'unblock'); // The page is blocked at this point, unblock it.
                return Promise.resolve();
            }

        console.log("secureData", secureData)
        
        return this._cardresponseHandler(paymentOptionId,secureData);  
    },

    
    _cardresponseHandler: async function (paymentOptionId,secureData) {

        await this.rpc(
            this.paymentContext['transactionRoute'],
            this._prepareTransactionRouteParams(),
        ).then(processingValues => {
            return this.rpc('/payment/cielo/payment',{
                    'reference': processingValues.reference,
                    'partner_id': processingValues.partner_id,
                    'opaque_data': secureData,
            }).then(() => window.location = '/payment/status');            
        }).catch(error => {
            if (error instanceof RPCError) {
                this._displayErrorDialog(_t("Payment processing failed"), error.data.message);
                this._enableButton(); // The button has been disabled before initiating the flow.
            } else {
                return Promise.reject(error);
            }
        });
},

    _cardvalidateFormInputs: function (paymentOptionId) {
        const inputs_no_obj = this._cardgetInlineFormInputs();
        console.log("input", inputs_no_obj)
        const inputs = Object.values(inputs_no_obj);
        var cc_nbr = inputs_no_obj.card.value.replace(/ /g, '');
        if(cc_nbr){
            var valid_value = $.payment.validateCardNumber(cc_nbr);
            if(!valid_value){
                return false;
            }
        }
        var cc_cvc = inputs_no_obj.code.value;
        if(cc_cvc && cc_nbr){
            var card_type = $.payment.cardType(cc_nbr);
            var valid_value = $.payment.validateCardCVC(cc_cvc, card_type);
            if(!valid_value){
                return false;
            }
        }
        var month = inputs_no_obj.month.value || '';
        var year = inputs_no_obj.year.value || '';
        if(month && year){
            var valid_value = $.payment.validateCardExpiry(month, year);
            if (valid_value) {
                $(inputs[1]).parent().parent('.form-group').addClass('o_has_success').find('.form-control, .custom-select').addClass('is-valid');
                $(inputs[1]).parent().parent('.form-group').removeClass('o_has_error').find('.form-control, .custom-select').removeClass('is-invalid');
                $(inputs[1]).siblings('.o_invalid_field').remove();
            }else {
                $(inputs[1]).parent().parent('.form-group').addClass('o_has_error').find('.form-control, .custom-select').addClass('is-invalid');
                $(inputs[1]).parent().parent('.form-group').removeClass('o_has_success').find('.form-control, .custom-select').removeClass('is-valid');
                return false;
            }
        }
        return inputs.every(element => element.reportValidity());
    },

})