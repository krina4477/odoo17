function FileUploadData(){
    $('.o_import_update_option').change(function(ev){
        if($(this).is(':checked')){
            $(".o_import_update_option").not($(this)).prop('checked',false);
        }
    })
}