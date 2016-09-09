$(document).ready(function () {
    'use strict';
    console.debug("[movimientos] Custom JS for valoración is loading...");
        $('.ept_mov_cuentas').mask("99-99-9999");
        $('input.ept_mov_cuentas').datepicker({
            dateFormat: "dd-mm-yy"
        });
    $('.js_buscar_mov').live( "mouseover", function() {
        $(this).css("background-color","#C0C0C0");
        $(this).css( 'cursor', 'pointer' );
        });
    $('.js_buscar_mov').live( "mouseout", function() {
        $(this).css("background-color","#ffff");
        });
        
        $('#ept_limpia_campos_cta_mov').click(function(){
            $('.js_busqueda_avanzada_mov_cta').find('input:text').val('');
        });
    $('.js_buscar_mov').live( "click", function() {
        
        var value=$(this).val();
        var id=$(this).attr('id');
        console.log($(this).attr('name'))
        console.log($(this).attr('name'))
        console.log($(this).attr('name'))
        var name=$(this).attr('name');
        var cuenta_id2=$('#id_cuenta_busc_mov').val();
        $('#ept_buscador_movimientos').val(name)
        
        openerp.jsonRpc('/ept_cuentas/movimientos/seleccion', 'call', {'name':name,'id':id,'cuenta_id':cuenta_id2}).then(function (respuesta) {
            llenarTbodyConsMov(respuesta['datos']);
        }).fail(function (source, error) {
                   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                            '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                            '<strong class="text-danger">Debug</strong>'+
                                            '<p>'+error.data.debug+'</p>');
                    $('#AJAXErrorModal').modal('show');
                });
        });
    $("#desplega_busq_avzda_mov").click(function(){
        $('.js_buscar_mov').hide();
        $('#ept_buscador_movimientos').val('')
        $('.js_busqueda_avanzada_mov_cta').toggle("swing",function(){
            $(this).css('overflow','inherit');
            $(this).find('select').selectpicker('deselectAll');
            $(this).find('input:text').val('');
            });
        $('.js_imprimir_report').toggle("swing",function(){
            });
        
     });
    $( "#ept_buscador_movimientos" ).keyup(function(event) {
        $('.js_busqueda_avanzada_mov_cta').hide();
        //~ var imagen_gif="<p align='center' >\
                                //~ <img width='25px' \
                                //~ height='25px' \
                                //~ src='ept_cuentas/static/src/img/ajax-loader.gif' />\
                                //~ </p>"
        //~ $('#buscando_cta_mov').html(imagen_gif);
        $('#buscando_cta_mov').html('');
        var value=$(this).val();
        
            if (value!=''){
                var cuenta_id=$('#id_cuenta_busc_mov').val();
                openerp.jsonRpc('/ept_cuentas/movimientos', 'call', {'key':value,'code':event.keyCode,'cuenta_id':cuenta_id}).then(function (respuesta) {
                    var uli='<ul class="list-group">';
                    var li='';
                    var resultado='';
                    if(respuesta['code']!=13){
                            $('#lista_busqueda_cta_movimeinto').show()
                            $.each(respuesta['datos'], function( clave, valor ) {
                                console.log(valor)
                                console.log(valor)
                                li=li+'<li class="js_buscar_mov list-group-item"\
                                        id="'+valor.id2+'" name="'+valor.name2+'">'+valor.name2+'</li>'
                                });
                            var ulf='</ul>';
                            resultado=uli+li+ulf
                            $('#buscando_cta_mov').html('');
                            if(resultado!=uli+''+ulf){
                                $('#lista_busqueda_cta_movimeinto').html(resultado);
                                $('#buscando_cta_mov').html('');
                                }else{
                                    $('#lista_busqueda_cta_movimeinto').html(uli+'<li class="list-group-item" >\
                                                Sin Resultados para la Busqueda</li>'+ulf);
                                }
                            }
                            else{
                            llenarTbodyConsMov(respuesta['datos']);
                        }
                    
                    
                    }).fail(function (source, error) {
                       $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                                '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                                '<strong class="text-danger">Debug</strong>'+
                                                '<p>'+error.data.debug+'</p>');
                        $('#AJAXErrorModal').modal('show');
                        });
                }
                else{
                       $('#lista_busqueda_cta_movimeinto').hide();
                       $('#buscando_cta_mov').html('');
                       }
        });
    
        $( '#ept_cta_busca_mov' ).click(function() {
            var form='#ept_cons_movimiento';
            var gif=$('#gif_cons_mov');
            var body_id='#tbody_ept_cta_mov'
            var v=$(form).apiform_panel();
            var formCont=v.context(form);
            var llenartabla=function(body_id,respuesta){
                if (respuesta['datos']){
                    llenarTbodyConsMov(respuesta['datos']);
                }
            }
            var cont1=0;
            var inputs=$(form).find('input').length
            var selects=$(form).find('select').length
                $.each(formCont.datos, function(clave, valor) {
                    if((valor.length) == 0){
                    cont1=cont1+1
                    }
                });
            if (cont1 !== selects+inputs){
                var panramentros={'fn':llenartabla,'fn_parametros':body_id,'gif':gif,'boton':this}
                v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
                }else{
                    $('.titulo').html('<strong>Aviso!</strong>')
                    $('.cuerpo').html('<h4 class="text-danger">Debe seleccionar por lo menos \
                                    un campo para la busqueda</h4>');
                    $('#AJAX_Modal').modal('show');
                    }
            });
        
    function llenarTbodyConsMov(respuesta){
        var tr='';
        $.each(respuesta, function( clave, movimiento ) {
        tr=tr+'<tr class="js_tr_ept_scroll_ancho_edit">\
                    <td class="text-center">'+movimiento.fecha_movimiento+'</td>\
                    <td class="text-center">'+movimiento.accion+'</td>\
                    <td class="text-center">'+movimiento.name+'</td>\
                    <td class="text-center monto">'+movimiento.monto_egreso+'</td>\
                    <td class="text-center monto">'+movimiento.monto_ingreso+'</td>\
                    <td class="text-center monto">'+movimiento.monto_saldo+'</td>\
                </tr>'
        });
        $('#lista_busqueda_cta_movimeinto').hide()
        $('#buscando_cta_mov').html('');
        var resultado=tr;
        $('#buscando_cta_mov').html('');
        if(resultado==''){
            $('#buscando_cta_mov').html('');
        }else{
            $('#tbody_ept_cta_mov').html(resultado);
        }
    }
    console.debug("[movimientos] Custom JS for valoración loaded!");
    });
