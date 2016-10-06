$(document).ready(function () {
    'use strict';
console.debug("[comunicaciones] Custom JS for comunicaciones is loading...");
var div_adicionados=[]
//~ para selection
$('.js_jpv_asunto_comunicaciones').live('change',function(){
    var select=$(this);
    var asunto_id=select.val();
    if (asunto_id){
        var option=$('.js_jpv_asunto_comunicaciones option[value="'+asunto_id+'"]');
            var name_text=option.attr('name_text');
            var tipo_campo=option.attr('tipo_campo');
        if (tipo_campo=='text'){
            remover_subasuntos(asunto_id);
            var input='<div class="form-group" id="'+asunto_id+'">'+
                 '<label>'+name_text+'</label>'+
                 '<input type="text" class="form-control" name="textSolicitud_'+asunto_id+'" value=""'+
                 ' required="required" mensaje="'+name_text+'"/>'+
                 '</div>'
            select.parents('div[class="form-group"]').after(input);
            var ids=[]
            select_adicionados(select,asunto_id);
            }
        }else{
            remover_div_select(select);
            }
    
    if (asunto_id && typeof tipo_campo != 'undefined' && tipo_campo!='text'){
        var organizacion_id=$('#organizacionId').val()
        var referencia=$('#referencia').val()
        var datos_post={
                'organizacion_id':organizacion_id,
                'referencia':referencia,
                'asunto_id':asunto_id,
                'tipo_campo':tipo_campo
                }
        $.ajax({
              url: "/comunicaciones/asuntos",
              data :datos_post ,
              type : 'POST',
              dataType : 'json',
              beforeSend: function( xhr ) {
                $('#img-form1').show()
                $('#EptEnviarComunicaciones').hide()
              }
            })
              .done(function(data) {
                  
                  remover_subasuntos(asunto_id);
                  select_adicionados(select,asunto_id);
                  var resultado;
                  switch(tipo_campo){
                      case 'checkbox':
                        resultado=asunto_checkbox(data,asunto_id);
                        select_adicionados(select,asunto_id);
                        break;
                      case 'selection':
                        resultado=asunto_select(data,asunto_id);
                         select_adicionados(select,asunto_id);
                        break;
                        case 'proyecto':
                        resultado=proyecto_select(data,asunto_id);
                        select_adicionados(select,'proyecto'+asunto_id);
                        break;
                        case 'periodo':
                        resultado=periodo_select(data,asunto_id);
                        select_adicionados(select,'periodo'+asunto_id);
                        break;
                                }
                    $('#img-form1').hide()
                    $('#EptEnviarComunicaciones').show()
                  select.parents('div[class="form-group"]').after(resultado);
              });
        }
    })
    //~ ********************para checkbox*******************************
    $('.js_jpv_asunto_comunicaciones_ch').live('change',function(){
    var checkbox=$(this);
    var checked=$(this).is(':checked');
    var asunto_id=checkbox.val();
    if (asunto_id && checked){
            var name_text=checkbox.attr('name_text');
            var tipo_campo=checkbox.attr('tipo_campo');
        if (tipo_campo=='text'){
            remover_subasuntos(asunto_id);
            var input='<div class="form-group" id="'+asunto_id+'">'+
                 '<label>'+name_text+'</label>'+
                 '<input type="text" class="form-control" name="textSolicitud_'+asunto_id+'" value=""'+
                 ' required="required" mensaje="'+name_text+'"/>'+
                 '</div>'
            checkbox.parents('div[class="form-group"]').after(input);
            var ids=[]
            div_adicionados[''+asunto_id+'']=asunto_id
            }
        }else{
            remover_subasuntos(asunto_id)
            $('#'+div_adicionados[''+asunto_id+'']).remove();
            }
    
    if (asunto_id && typeof tipo_campo != 'undefined' && tipo_campo!='text' && checked==true){
        switch(tipo_campo){
                case 'false':
                    return
                break;
                }
        var organizacion_id=$('#organizacionId').val()
        var referencia=$('#referencia').val()
        var datos_post={
                'organizacion_id':organizacion_id,
                'referencia':referencia,
                'asunto_id':asunto_id,
                'tipo_campo':tipo_campo
                }
        $.ajax({
              url: "/comunicaciones/asuntos",
              data :datos_post ,
              type : 'POST',
              dataType : 'json',
              beforeSend: function( xhr ) {
                $('#img-form1').show()
                $('#EptEnviarComunicaciones').hide()
              }
            })
              .done(function(data) {
                  
                  remover_subasuntos(asunto_id);
                  select_adicionados(checkbox,asunto_id);
                  var resultado;
                  switch(tipo_campo){
                      case 'checkbox':
                        resultado=asunto_checkbox(data,asunto_id);
                        div_adicionados[''+asunto_id+'']=asunto_id
                        break;
                      case 'selection':
                        resultado=asunto_select(data,asunto_id);
                         div_adicionados[''+asunto_id+'']=asunto_id
                        break;
                        case 'proyecto':
                        resultado=proyecto_select(data,asunto_id);
                        div_adicionados['proyecto'+asunto_id+'']=asunto_id
                        break;
                        case 'periodo':
                        resultado=periodo_select(data,asunto_id);
                        div_adicionados['periodo'+asunto_id+'']=asunto_id
                        break;
                                }
                    $('#img-form1').hide()
                    $('#EptEnviarComunicaciones').show()
                  checkbox.parents('div[class="form-group"]').after(resultado);
              });
        }
    })
    //~ ********************para checkbox*******************************
    //~ function que genera los asuntos tipo select
    function asunto_select(data,asunto_id){
        var select='<div class="form-group" id="'+asunto_id+'">'
        select+='<select name="asunto_'+asunto_id+'" class="form-control js_jpv_asunto_comunicaciones" title="Seleccione"  required="required" mensaje="El Sub-Asunto ">'
        select+='<option value="" selected="selected" >Seleccione el Sub-Asunto</option>'
        $.each(data,function(clave,value){
                select+='<option'+
                        ' value="'+value['id']+'"'+
                        ' name_text="'+value['name_text']+'"'+
                        ' tipo_campo="'+value['tipo_campo']+'">'+value['asunto']+'</option>'
            });
        select+='</select>'
        select+='</div>'
        return select
        }
    //~ function que genera los selección de proyecto
    function proyecto_select(data,asunto_id){
        var tabla='<div class="table-responsive">'+
                  '<table class="table" id="jpv_com_proyectAdd">'+
                    '<thead>'+
                      '<tr>'+
                        '<th>Correlativo</th>'+
                        '<th>Quitar</th>'+
                      '</tr>'+
                '</thead>'+
                '<tbody>'+
                '</tbody>'+
                '</table>'+
                '</div>'
        var select='<div class="form-group" id="proyecto'+asunto_id+'">'
        select+='<select name="proyecto_'+asunto_id+'" class="form-control  js_jpv_proyecto_comunicacion"  title="Seleccione"  required="required" mensaje="El Sub-Asunto ">'
        select+='<option value="" selected="selected" >Seleccione el correlativo del proyecto</option>'
        $.each(data,function(clave,value){
                select+='<option'+
                        ' value="'+value['id']+'"'+
                        ' correlativo="'+value['correlativo']+'"'+
                        ' name_text="'+value['name_text']+'"'+
                        ' tipo_campo="'+value['tipo_campo']+'">'+value['correlativo']+'</option>'
            });
        select+='</select>'
        select+='<div id="jpv_com_tabla_proyectos">'+tabla+'</div>'
        select+='</div>'
        return select
        }
    //funcion que agrega los proyectos a una tabla
    $('.js_jpv_proyecto_comunicacion').live('change',function(){
        var value=$(this).val();
        var option=$('.js_jpv_proyecto_comunicacion option[value="'+value+'"]');
        var correlativo=option.attr('correlativo');
        var tr='<tr id="tr'+value+'">'+
                '<td>'+correlativo+'</td>'+
                '<td class="jpv_com_trRemove" remover=tr'+value+' >'+
                ' <b style="cursor: pointer" ><p class="text-danger">X</p></b></td>'+
                '<input type="hidden" name="proyectosadd_'+value+'" value="'+value+'"'+
                '</tr>'
        $('#jpv_com_proyectAdd tr:last').after(tr);
        })
    
    //funcion que agrega los proyectos a una tabla
    //~ funcion que remueve el tr del proyecto seleccionado
    $('.jpv_com_trRemove').live('click',function(){
        var pivot=$(this).attr('remover');
        $('#'+pivot+'').remove();
        });
    //~ funcion que remueve el tr del proyecto seleccionado
     
    //~ function que genera los selección de proyecto
    function periodo_select(data,asunto_id){
        var select='<div class="form-group" id="periodo'+asunto_id+'">'
        select+='<select name="periodo_'+asunto_id+'" class="form-control js_jpv_asunto_comunicaciones" title="Seleccione"  required="required" mensaje="El Sub-Asunto ">'
        select+='<option value="" selected="selected" >Seleccione el periodo</option>'
        $.each(data,function(clave,value){
                select+='<option'+
                        ' value="'+value['id']+'"'+
                        ' name_text="'+value['name_text']+'"'+
                        ' tipo_campo="'+value['tipo_campo']+'">'+value['periodo']+'</option>'
            });
        select+='</select>'
        select+='</div>'
        return select
        }
    //~ function que genera los asuntos tipo checkbox
    function asunto_checkbox(data,asunto_id){
        var checkbox='<div class="form-group" id="'+asunto_id+'">'
        $.each(data,function(clave,value){
            checkbox+='<div class="checkbox">'+
            '<label><input type="checkbox" class="js_jpv_asunto_comunicaciones_ch"'+
            ' name="asunto_'+value['id']+'"'+
            ' grupo="asunto_'+asunto_id+'"'+
            ' label="'+value['asunto']+'"'+
            ' required="required" mensaje="El Asunto "'+
            ' name_text="'+value['name_text']+'"'+
            ' tipo_campo="'+value['tipo_campo']+'"'+
            ' value="'+value['id']+'">'+value['asunto']+'</label>'+
            '</div>'
            })
        checkbox+='</div>'
        return checkbox
        }
    //~ function que adiciona en la lista div_adicionados los div dependienetes, para el historico para removerlos 
    function select_adicionados(select,asunto_id){
        select.find('option').each(function(){
                var id=$(this).val()
                if(id){
                    div_adicionados[''+id+'']=asunto_id
                    }
                });
        }
    //~ function que remueve los div de cuando se selecciona seleccione asunto
    function remover_div_select(select){
        select.find('option').each(function(){
                 var id=$(this).val()
                if(id){
                    $('#'+div_adicionados[''+id+'']).remove();
                    }
                $.each(div_adicionados,function(clave,valor){
                    $('#'+div_adicionados[''+clave+'']).remove();
                    });
                });
        }
    //~ funccion para remover los sub-asuntos
    function remover_subasuntos(asunto_id){
        $('#'+div_adicionados[''+asunto_id+'']).find('option').each(function(){
                var value=$(this).val();
                console.log(value);
                remover_subasuntos(value);
                $('#'+div_adicionados[''+value+'']).remove();
            
            });
        $('#'+div_adicionados[''+asunto_id+'']).find('input').each(function(){
                var value=$(this).val();
                 remover_subasuntos(value);
                $('#'+div_adicionados[''+value+'']).remove();
            });
        $('#'+div_adicionados[''+asunto_id+'']).remove();
        }
//~ *********************configuración del campo file*************************************
$(".js_jpv_comunicaciones").fileinput({
    showClose: false,
    showCaption: false,
    browseLabel: 'Adjuntar archivo',
    removeLabel: '',
    browseIcon: '<i class="glyphicon glyphicon-folder-open">. </i> ',
    removeIcon: '<i class="glyphicon glyphicon-remove"></i>',
    removeTitle: 'Cancel or reset changes',
    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato .csv" style="width:80px">',
    layoutTemplates: {main2: '{preview} {remove} {browse}'},
    uploadAsync: true,
    showPreview: true,
    allowedFileExtensions: ['pdf',],
    maxFileCount: 1,
    msgErrorClass: 'alert alert-block alert-danger',
    elErrorContainer: '#kv-error-1',
   
});
//~ *********************configuración del campo file*************************************
console.debug("[comunicaciones] Custom JS for comunicaciones loaded!");
});
