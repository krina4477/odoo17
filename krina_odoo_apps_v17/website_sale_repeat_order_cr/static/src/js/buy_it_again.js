/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";

$(document).ready(function(){
    $('.js_buy_it_again').click(function(e){
        var currentRow = $(this).closest("tr");
        var product_id = currentRow.find("td:eq(1)").text();
        var add_qty = currentRow.find("td:eq(3)").text();
        jsonrpc('/buy/product/again', {
            'product_id':product_id,
            'add_qty':add_qty
        }).then(function (data) {
            if (data.result){
                location.reload();
            }
            else{
                location.reload();
            }
        })
    });

    $('.js_copy_order').click(function(e){
        var data = [];
        $(".table tr").each(function(){
            var currentRow = $(this);
            var product_id = currentRow.find("td:eq(1)").text();
            var add_qty = currentRow.find("td:eq(3)").text();
            if (product_id && add_qty) {
                var dict = {};
                dict.id = parseInt(product_id);
                dict.qty = parseInt(add_qty);
                data.push(dict);
            }
        });
        jsonrpc('/copy/order', {
            'data':data
        }).then(function (data) {
            if (data.result){
                window.location.href = '/shop/cart'
            }
            else{
                window.location.href = '/shop/cart'
            }
        })
    });

    $('.js_copy_order_from_tree').click(function(e){
        var currentRow = $(this).closest("tr");
        var order_id = currentRow.find("td:eq(1)").text();
        jsonrpc('/copy/order/from/tree', {
            'order_id':parseInt(order_id),
        }).then(function (data) {
            if (data.result){
                window.location.href = '/shop/cart'
            }
            else{
                window.location.href = '/shop/cart'
            }
        })
    });

});