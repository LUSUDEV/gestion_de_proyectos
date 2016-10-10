$(document).ready(function () {
    'use strict';
console.debug("[enviar val] Custom JS for valoración is loading...");
var navegadores={'mozilla':43,'chrome':43};
var navegador_datos=''
jQuery.each (jQuery.browser, function (i, val) {
        navegador_datos+=i+': '+val+', '
         $.each(navegadores,function(navegador,version){
             if (i==navegador){
                 var version_n=jQuery.browser.version
                 version_n=parseInt(version_n.substring(0,2))
                 if(parseInt(version_n)<version){
                     $('#mesaje_version').html('<div class="alert alert-danger"><b>¡Alerta! Debe actualizar su Navegador para que el sistema le fucione correctamente.</b></div>')
                     }
                 }
             });
        });
//~ $('#version_navegador').html(navegador_datos) esta linia muestra la version del navegador
$(".js_EnviarValoracionEpt").click( function( event ) {
            var form=$(this).attr('form');
            var proyecto_id=$(this).attr('proyecto_id');
            var gif=$('#img-'+form);
            var tr_id=$(this).attr('tr_id')
            var v=$('#'+form).apiform_panel();
            var formCont=v.context('#'+form);
            var fncerrar=function(tr_id){
                    $('.'+tr_id).toggle("swing");
                    $('.js_val_exito'+proyecto_id+tr_id).show(1000)
                    $('#AJAX_Modal').modal('hide');
                    var new_position = jQuery("#a"+tr_id).offset();
                    window.scrollTo(new_position.left,new_position.top);
                    
                 }
            if (formCont.campovacios=='no'){
                var panramentros={'fn':fncerrar,'fn_parametros':tr_id,'gif':gif,'boton':this}
                v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
                }
             
             });



$(".js_jpv_valoracionCsv").fileinput({
    uploadUrl:'/jpv_carga_valoracion/csv', // server upload action
    showClose: false,
    showCaption: false,
    browseLabel: 'Cargar Formato',
    removeLabel: '',
    browseIcon: '<i class="glyphicon glyphicon-folder-open">. </i> ',
    removeIcon: '<i class="glyphicon glyphicon-remove"></i>',
    removeTitle: 'Cancel or reset changes',
    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato .csv" style="width:80px">',
    layoutTemplates: {main2: '{upload}{preview} {remove} {browse}'},
    uploadAsync: true,
    showPreview: true,
    allowedFileExtensions: ['csv'],
    maxFileCount: 5,
    msgErrorClass: 'alert alert-block alert-danger',
    elErrorContainer: '#kv-error-1',
    uploadExtraData: {
        obj_valoracion_id: $('#obj_valoracion_idfile').val(),
        tipo_valoracion: $('#tipo_valoracionfile').val(),
        asignacion_id:$('#asignacion_idfile').val(),
    }
    }).on('filebatchpreupload', function(event, data) {
        var n = data.files.length, files = n > 1 ? n + ' files' : 'one file';
        if (!window.confirm("Are you sure you want to upload " + files + "?")) {
            return {
                message: "Upload aborted!", 
                data:{} 
            };
        }
        $('#kv-success-1').html('<h4>Estatu de Carga</h4><ul></ul>').hide();
    }).on('fileuploaded', function(event, data, id, index) {
    if (data.response.modal){
            $.each(data.response.modal, function( clave, valor ) {
                            $('.'+clave).html(valor)
                        });
                         $('#AJAX_Modal').modal('show');
        }else{
             var fname = data.files[index].name,
                out = '<li>' + 'Carga de Archivo # ' + (index + 1) + ' - '  +  
                    fname + ' exitosa.' + '</li>';
            $('#kv-success-1').append(out);
            $('#kv-success-1').fadeIn('slow');
            }
   
});

console.debug("[enviar val] Custom JS for valoración loaded!");
});
