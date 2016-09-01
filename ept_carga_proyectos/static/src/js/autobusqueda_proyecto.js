$(document).ready(function(){
    //~ Metodo que se ejecuta cuando se inicia la busqueda avanzada de proyectos, para buscar municipios y tambien se ejecuta la busqueda de parroquia segun el municipio seleccionado
    $.each( $.find('#ept_busqueda_avanzada_pro'),function(){
        openerp.jsonRpc('/ept_cp_proyecto_consulta/busqueda_municipios', 'call', {}).then(function (data_municipio) {
            for (index in data_municipio){
                ids=data_municipio[index][1]
                for(index_ids in ids ){
                    $('#municipio_bq_avz_id').append(new Option(data_municipio[index][0][index_ids], ids[index_ids], false));
                }
            }
            $('select#municipio_bq_avz_id').on('change', function(event){
                    $('#parroquia_bq_avz_ids').find('option').remove();
                    var municipio_id=$('#municipio_bq_avz_id').val()
                    openerp.jsonRpc("/ept_cp_proyecto_consulta/busqueda_parroquias", 'call', {
                                'municipio_id': municipio_id,}).then(function(data_parroquia){
                            ids=data_parroquia[1]
                            for(index_ids in ids ){
                                $('#parroquia_bq_avz_ids').append(new Option(data_parroquia[0][index_ids], ids[index_ids], false));
                                
                            }
                            $('#parroquia_bq_avz_ids').selectpicker('refresh');
                                });
                        });
                $('#municipio_bq_avz_id').selectpicker('refresh');
                
            });
        
        });
    //~ Se utiliza la mascara para fecha
$('input.ept_date_buz_proy').mask("00-00-0000");
    $('input.ept_date_buz_proy').datepicker({
            dateFormat: "dd-mm-yy"
            });
    //~ metodos para selccionar y des-seleccionar con el puntero 
    $('.js_buscar').live( "mouseover", function() {
        $(this).css("background-color","#C0C0C0");
        $(this).css( 'cursor', 'pointer' );
        });
    $('.js_buscar').live( "mouseout", function() {
        $(this).css("background-color","#ffff");
        });
    //~ metodo que muestra o oculta la tabla para busqueda avanzada y para limpiar campos
    $("#desplega_busq_avzda").click(function(){
        $('.js_buscar').hide();
        $('#ept_buscador_proyecto').val('')
        $('.js_busqueda_avanzada_proy').toggle("swing",function(){
            $(this).css('overflow','inherit');
            $(this).find('select').selectpicker('deselectAll');
            $(this).find('input').val('');
            });
        
     });
     //~ metodo para limpiar campos con el botton
     $('#ept_limpia_campos_proy').click(function(){
            $('.js_busqueda_avanzada_proy').find('select').selectpicker('deselectAll');
            $('.js_busqueda_avanzada_proy').find('input').val('');
        });
    //~ Metodo que ejecuta cuando selecciona una opcion con el puntero o raton
    $('.js_buscar').live( "click", function() {
        var value=$(this).val();
        var id=$(this).attr('id');
        var name=$(this).attr('name');
        $('#ept_buscador_proyecto').val(name)
        openerp.jsonRpc('/ept_cp_proyecto_consulta/seleccion', 'call', {'id':id}).then(function (respuesta) {
            llenarTbodyProyecto(respuesta['datos']);
        }).fail(function (source, error) {
                   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                            '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                            '<strong class="text-danger">Debug</strong>'+
                                            '<p>'+error.data.debug+'</p>');
                    $('#AJAXErrorModal').modal('show');
                });
    });
    //~ Metodo para buscar con el teclado si pulsa enter 
    $( "#ept_buscador_proyecto" ).keyup(function(event) {
            $('.js_busqueda_avanzada_proy').hide();
            $('#buscando').html("<p align='center' >\
                                <img width='25px' \
                                height='25px' \
                                src='ept_carga_proyectos/static/src/img/ajax-loader.gif' />\
                                </p>");
            var value=$(this).val();
            if (value!=''){
            openerp.jsonRpc('/ept_cp_proyecto_consulta', 'call', {'key':value,'code':event.keyCode}).then(function (respuesta) {
                var uli='<ul class="list-group">';
                var li='';
                var resultado='';
                if(respuesta['code']!=13){
                    $('#lista_busqueda').show()
                $.each(respuesta['datos'], function( clave, valor ) {
                            li=li+'<li class="js_buscar list-group-item"\
                                    id="'+valor.id+'" name="'+valor.name+'">'+valor.name+'</li>'
                            });
                    var ulf='</ul>';
                        resultado=uli+li+ulf
                    $('#buscando').html('');
                    if(resultado!=uli+''+ulf){
                        $('#lista_busqueda').html(resultado);
                        $('#buscando').html('');
                        }else{
                            $('#lista_busqueda').html(uli+'<li class="list-group-item" >\
                                        Sin Resultados para la Busqueda</li>'+ulf);
                        }      
                }
                else{
                        llenarTbodyProyecto(respuesta['datos']);
                    }
                    }).fail(function (source, error) {
                       $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                                '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                                '<strong class="text-danger">Debug</strong>'+
                                                '<p>'+error.data.debug+'</p>');
                        $('#AJAXErrorModal').modal('show');
                    });
                    }else{
                       $('#lista_busqueda').hide();
                       $('#buscando').html('');
                       }
    });

    //~ Metodo que se utiliza para la busqueda avanzada 
    $( "#busca_avanzada" ).click(function() {
         var form='#ept_busqueda_avanzada_pro';
         var gif=$('#gifbusq_avanz');
         var body_id='#proyectos_completos'
         var v=$(form).apiform_panel();
         var formCont=v.context(form);
         var llenarbody=function(body_id,respuesta){
                if (respuesta['datos']){
                    llenarTbodyProyecto(respuesta['datos']);
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
            var panramentros={'fn':llenarbody,'fn_parametros':body_id,'gif':gif,'boton':this}
            v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }else{
                $('.titulo').html('<strong>Aviso!</strong>')
                $('.cuerpo').html('<h4 class="text-danger">Debe seleccionar por lo menos \
                                    un campo para la busqueda</h4>');
                $('#AJAX_Modal').modal('show');
                }
        });

//~ Funcion que retorna el valor con en la tabla el estatus esta aprobado
function llenarBotonAprobado(proyecto_id){
    var retorno='\<div class="btn-group">\
                <button type="button" class="btn btn-xs "><span class="glyphicon glyphicon-check"></span> Aprobado</button>\
                <button type="button" class="btn btn-xs dropdown-toggle" data-toggle="dropdown">\
                            <span class="caret"></span>\
                            <span class="sr-only">Desplegar menú</span>\
                          </button>\
                          <ul class="dropdown-menu">\
                            <li><a href="/avance/'+proyecto_id+'/">\
                                <h5><span class="glyphicon glyphicon-arrow-right"></span>\
                                Avance</h5>\
                                </a>\
                            </li>\
                            <li><a href="/avance/'+proyecto_id+'/">\
                                <h5><span class="glyphicon glyphicon-ok"></span>\
                                Culminación</h5>\
                                </a>\
                            </li>\
                          </ul>\
                          </div>'
                            //~ <li><a href="/cancelar/'+proyecto_id+'/">\
                                //~ <h5><span class="glyphicon glyphicon-remove"></span>\
                                //~ Cancelar</h5>\
                                //~ </a>\
                            //~ </li>\
    
    return retorno
    
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta aprobado
function llenarBotonAprobadoMigracion(){
    var retorno='\<div class="btn-group">\
                <button type="button" class="btn btn-xs "><span class="glyphicon glyphicon-check"></span> Aprobado</button>\
                <button type="button" class="btn btn-xs dropdown-toggle" data-toggle="dropdown">\
                            <span class="caret"></span>\
                            <span class="sr-only">Desplegar menú</span>\
                          </button>\
                          </div>'
    
    return retorno
    
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta Cancelado
function llenarBotonCancelado(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-hand-down"></span> Cancelado</button>'
    return retorno
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta diferido
function llenarBotonDiferido(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-refresh"></span> Diferido</button>'
    return retorno
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta negado
function llenarBotonNegado(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-remove-circle"></span> Negado</button>'
    return retorno
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta borrador o carga
function llenarBotonCarga(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-list-alt"></span> Borrador</button>'
    return retorno
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta en evaluacion
function llenarBotonEvaluacion(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-pencil"></span> Evaluación</button>'
    return retorno
    }
//~ Funcion que retorna el valor con en la tabla el estatus esta en culminado
function llenarBotonCulminado(){
    var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-pencil"></span> Culminado</button>'
    return retorno
    }

//~ Funcion que que llena la tabla (tbody) de proyectos segun el resultado obtenido en las busquedas anteriores
function llenarTbodyProyecto(respuesta){
        parametros([{'metodo':'armar_botones_proyectos',
                   'parametros':{'proyectos_data':respuesta,
                                'proyectos_ids':[respuesta[0].id],
                                'cantidad_proyectos':respuesta.length,
                                'num':0,
                                'fin':respuesta.length
                    }}],function(respuesta){
        $('#lista_busqueda').hide()
        $('#proyectos_completos').html(respuesta.armar_botones_proyectos);

      });

       
         
    }

    var parametros= function(datos,callback){
            var respuesta;
            openerp.jsonRpc('self', 'call', {'datos':datos}).then(function (respuesta) {
                respuesta = respuesta;
          callback(respuesta);
            });
        };
});
