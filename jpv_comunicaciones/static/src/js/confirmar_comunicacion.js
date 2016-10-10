$(document).ready(function () {
    'use strict';
    console.debug("[comunicaciones] Custom JS for confir is loading...");
var ids_leidosept;
var comunicacion=function(){
    openerp.jsonRpc('/jpvconfirmar_comunicaciones', 'call', {}).then(function (comunicacion) {
        ids_leidosept=comunicacion.ids
        var cuerpo='';
        $.each(comunicacion.comunicaciones,function(index, value){
            //~ cuerpo+='<div class="well mt32">'
            var fecha_envio_a=''
            var fecha_envio=''
            if (value.create_date){
                fecha_envio_a=value.create_date.substring(0,10).split("-");
                fecha_envio=fecha_envio_a[2]+'-'+fecha_envio_a[1]+'-'+fecha_envio_a[0]
                }
            cuerpo+='<div class="panel panel-default">'
            cuerpo+='<div class="panel-heading"><b><p class="text-center">Solicitud: '+value.correlativo+'</p>Fecha de envío: '+fecha_envio+'</b>'
            cuerpo+='<img class="jpvcom_ocultarWebsite" src="/web/static/src/img/icons/terp-folder-green.png" align="right"></div>'
            cuerpo+='<div class="panel-body">'
            cuerpo+='Asunto: '+value.asunto_name+'<br/>'
            cuerpo+='Comunicación: '+value.comunicacion+'</strong><br/>'
            cuerpo+=value.adjunto
            $.each(value.respuestas,function(index, respuesta){
                var fecha_envio_a=respuesta.create_date.substring(0,10).split("-");
                var fecha_envio=fecha_envio_a[2]+'-'+fecha_envio_a[1]+'-'+fecha_envio_a[0]
                cuerpo+='<div class="panel panel-info mt8">'
                cuerpo+='<div class="panel-heading"><b><p class="text-center">RESPUESTA: '+respuesta.correlativo+'</p> Fecha de Respuesta: '+fecha_envio+'</b></div>'
                cuerpo+='<div class="panel-body">'
                cuerpo+=respuesta.comunicacion
                cuerpo+=respuesta.adjunto
                cuerpo+='</div>'
                cuerpo+='</div>'
                });
            cuerpo+='</div>'
            cuerpo+='</div>'
            })
        $.each(comunicacion.comunicaciones_masivas,function(index, value){
            var fecha_envio_a=''
            var fecha_envio=''
            if (value.create_date){
            var fecha_envio_a=value.create_date.substring(0,10).split("-");
            var fecha_envio=fecha_envio_a[2]+'-'+fecha_envio_a[1]+'-'+fecha_envio_a[0]
                }
            cuerpo+='<div class="panel panel-success">'
            cuerpo+='<div class="panel-heading"><b><p class="text-center">Comunicación Oficial: '+value.correlativo+'</p>Fecha de envío: '+fecha_envio+'</b>'
            cuerpo+='<img class="jpvcom_ocultarWebsite" src="/web/static/src/img/icons/terp-folder-green.png" align="right"></div>'
            cuerpo+='<div class="panel-body">'
            cuerpo+='Asunto: '+value.name+'<br/>'
            cuerpo+='Comunicación: '+value.comunicacion+'</strong><br/>'
            cuerpo+=value.adjunto
            cuerpo+='</div>'
            cuerpo+='</div>'
            });
        if (cuerpo){
            $('.cuerpo').html(cuerpo);
            $('.titulo').html('<strong class="text-success">Buzón de Comunicación Oficial.</strong>');
            $('.piemodal').html(' <button type="button" id="comunicacion_leido" class="btn btn-primary"><b>Leído</b></button>');
            $('#Modal_sin_botton').modal('show');
            }
        });
        }
comunicacion();
$('#comunicacion_leido').live('click', function () {
     openerp.jsonRpc('/jpvComunicacionesLeidos', 'call', ids_leidosept);
     $('#Modal_sin_botton').modal('hide');
            });
$('.Eptcom_ocultarWebsite').live('click', function () {
    $(this).parent().parent().hide()
    });
console.debug("[comunicaciones] Custom JS for confir loaded!");
});
