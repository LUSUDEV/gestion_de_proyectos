$(document).ready(function () {
    
    //~ clonar elementos de una tabla
        
    $(function(){
        $('.agregarFila').live('click', function (event){
            var ref=$(this).attr('ref');
            body = $('#'+ref);
            var tr = $('tr:last', body);
            var trid = tr.attr('id')
            tr_id=trid.split("_")
            cont=parseInt(tr_id[1])+1
            new_id=tr_id[0]+'_'+cont
            var new_tr=tr.clone(true)
            new_tr.attr('id',new_id)
            $(new_tr).find('input:text').each(function(){
                            var name=$(this).attr('name');
                            name=name.split("_")
                            $(this).attr('name',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).attr('id',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).val('')
            })
            $(new_tr).find('input[type=number]').each(function(){
                            var name=$(this).attr('name');
                            name=name.split("_")
                            $(this).attr('name',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).attr('id',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).val('')
            })
            $(new_tr).find('select').each(function(){
                            var name=$(this).attr('name');
                            name=name.split("_")
                            $(this).attr('name',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).attr('id',name[0]+'_'+name[1]+'_'+name[2]+'_'+cont);
                            $(this).val('')
            })
            $(new_tr).find('button:button').each(function(){
                             name=name.split("_")
                             $(this).attr('ref',new_id);
            })
            $(new_tr).appendTo(body)
        });
        $(".eliminarFila").live('click', function (){
            var ref_body=$(this).attr('ref_body');
            var n=$('#'+ref_body+' tr').length
            if (n > 1){
                $(this).closest('tr').remove();
            };
        });
    });
});
