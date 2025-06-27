/** @odoo-module 
 * 
 * @private
 * @param {boolean} blockUI
 * @return {void}
 * 
 **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service"; 
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { dialogService } from "@web/core/dialog/dialog_service";

publicWidget.registry.test = publicWidget.Widget.extend({
    selector: '.o_wsale_product_page',
    events: Object.assign({}, publicWidget.Widget.prototype.events, {
        'click .js_apply_submit_button': '_js_apply_submit_button',
    }),
    init() {
    	this._super(...arguments);
    	this.dialog = this.bindService("dialog");
    },
    _js_apply_submit_button: async function(ev){
    		var self = this
    	    var first_name = $('#first-name').val();
            var last_name = $('#last-name').val();
            var email_name = $('#email').val();
            var contact_no = $('#contact').val();
            var no_of_quantity = $('#quantity').val();
            var message = $('#message').val();
            
            if(first_name){
                $('#first-name').removeClass('is-invalid');
            }else{
                $('#first-name').addClass('is-invalid');
            }

            if(email_name){
                $('#email').removeClass('is-invalid');
            }else{
                $('#email').addClass('is-invalid');
            }

            if(contact_no){
                $('#contact').removeClass('is-invalid');
            }else{
                $('#contact').addClass('is-invalid');
            }

            if(no_of_quantity){
                $('#quantity').removeClass('is-invalid');
            }else{
                $('#quantity').addClass('is-invalid');
            }

            if(message){
                $('#message').removeClass('is-invalid');
            }else{
                $('#message').addClass('is-invalid');
            }
            if (first_name && email_name && contact_no && no_of_quantity && message)
            {	
                
        		jsonrpc('/create/call/price', 
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email_name': email_name,
                    'contact_no': contact_no,
                    'no_of_quantity': no_of_quantity,
                    'message': message,
                }).then(function (data) 

                {   
                    if (data.status){
                        
                        alert ("Thank you, your enquiry has been submitted successfully.Our Executive will contact you shortly.")
                    }
                    else {

                        alert("Something went wrong please try after sometime.")
                    }
                });
            }
            return false;
    	}
 	});
	

	$(document).ready(function($)
	{
	    var $cf = $('#quantity');
	    $cf.blur(function(e)
	    {
	        var quantity = $(this).val();
	        if (isNaN(quantity))
	        {
	            alert('Please enter a valid quantity!!');
	            $('#quantity').val('');
	        }
	    });
	});