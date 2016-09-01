$(document).ready(function () {
    'use strict';
    console.debug("[apiform_panel] Custom JS for apiform_panel is loading...");
         var apiform_panel = apiform_panel || {};
         apiform_panel.context=function(form_id){
             var datosfile;
             var campovacios='no';
             var cuerpomodal='';
             var opcionesRadio= new Object();
             var datos_form=$(form_id).serializeArray();
             var destino=$(form_id).attr('action');
             var datos_post=$(form_id).serialize();
             //~ $(form_id).find('input:file').each(function(){
                            //~ 
                      //~ });
                      
            $(form_id).find('select[required][mensaje]').each(function(){
                        var name=$(this).attr('name');
                        var required=$(this).attr('required');
                        var mensaje=$(this).attr('mensaje');
                        var value=$(this).val();
                        if (value == '' && required=='required' && typeof mensaje != 'undefined') {
                            campovacios='si';
                           opcionesRadio[''+mensaje+'']=mensaje
                           $(this).css("border-color", "red");
                            }else{
                                $(this).css("border", " 1px #ccc solid ");
                                }
                });
            $(form_id).find('input:radio[required][mensaje]').each(function(){
                        var name=$(this).attr('name');
                        var required=$(this).attr('required');
                        var mensaje=$(this).attr('mensaje');
                        var value=$(form_id+' input:radio[name='+name+']:checked').val();
                        if (typeof value == 'undefined' && required=='required' && typeof mensaje != 'undefined') {
                            campovacios='si';
                           opcionesRadio[''+mensaje+'']=mensaje
                           $(this).css("border-color", "#ccc");
                            }
                        });
            $.each(opcionesRadio,function(index,opcion){
                    cuerpomodal+='Las opciones de: '+' '+opcion+'</br>';;
                });
            $(form_id).find('input:text[required][mensaje], textarea[required][mensaje]').each(function(){
                            var value=$(this).val();
                            var required=$(this).attr('required');
                            var mensaje=$(this).attr('mensaje');
                            if($.trim(value)=='' && required=='required' && typeof mensaje != 'undefined'){
                                campovacios='si';
                                cuerpomodal+= 'El Campo '+' '+mensaje+' </br>';
                                $(this).css("border-color", "red");
                                }else{
                                     $(this).css("border", " 1px #ccc solid ");
                                    }
                                        });
            $(form_id).find('input[type=number][required][mensaje]').each(function(){
                            var value=$(this).val();
                            var required=$(this).attr('required');
                            var mensaje=$(this).attr('mensaje');
                            if($.trim(value)=='' && required=='required' && typeof mensaje != 'undefined'){
                                campovacios='si';
                                cuerpomodal+= 'El Campo '+' '+mensaje+' </br>';
                                $(this).css("border-color", "red");
                                }else{
                                    $(this).css("border-color", "#ccc");
                                    }
                                        });
            $(form_id).find('input[type=checkbox][required][mensaje][name][label]').each(function(){
                var value=$(this).val();
                var grupo=$(this).attr('grupo');
                var label=$(this).attr('label');
                var mensaje=$(this).attr('mensaje');
                var checked=$(form_id).find('input[type=checkbox][grupo="'+grupo+'"]').is(':checked');
                if (checked==false){
                                campovacios='si';
                                cuerpomodal+= 'El Campo '+' '+mensaje+' '+label+' </br>';
                                $(this).css("border", "red");
                    }else{
                        $(this).css("border", "#ccc");
                        }
                });
            if (campovacios=='si'){
                $('.cuerpo').html('<strong class="text-danger">'+cuerpomodal+'<br>¡Requerido(s)!</strong>');
                $('.titulo').html('<strong>Formulario Incompleto.</strong>');
                $('#AJAX_Modal').modal('show');
                return {campovacios:campovacios}
                }
             $(form_id).find('input[type="file"][widget]').each(function(input){
                 var input=this;
                 var cargaImagen=new openerp.website.cargaImagen();
                 var name,value;
                 if($(input).attr('widget')=='apiform_image'){
                     name=input.name
                     value=input.src
                     if(value){
                         value=value.split(',');
                     value=value[1]
                     datosfile={
                     'name':name,
                     'value':value
                     }
                    datos_post+='&'+name+'='+value;
                    datos_form.push(datosfile);
                     }
                         }
                
                 
                 });
               
                var datos= new Object();
                 $.each(datos_form,function(name,value){
                    var input;
                     datos[''+value.name+'']=value.value;
                     });
             return {datos:datos,destino:destino,datos_post:datos_post,campovacios:campovacios}
             }
         apiform_panel.ajax={
            enviar:function(destino,datos,panramentros){
                     $(panramentros['gif']).show()
                     $(panramentros['boton']).hide()
                     openerp.jsonRpc(destino, 'call', datos).then(function (respuesta) {
                        
                    if (respuesta['modal']){
                        $.each(respuesta['modal'], function( clave, valor ) {
                            $('.'+clave).html(valor)
                        });
                        $(panramentros['gif']).hide()
                        $(panramentros['boton']).show()
                         $('#AJAX_Modal').modal('show');
                        }
                    if (respuesta['error_campos']){
                        var cuerpo=' ';
                        $.each(respuesta['error_campos'], function( clave, valor ) {
                        cuerpo+=clave+' '+valor+'<br>';
                        });
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Error de campos de Formularios.</strong>');
                        $('#AJAX_Modal').modal('show');
                        $(panramentros['gif']).hide()
                        $(panramentros['boton']).show()
                        }else{
                                if(typeof panramentros['fn'] != 'undefined'){
                                    panramentros['fn'](panramentros['fn_parametros'],respuesta)
                                    }
                            }
                    if (respuesta['mycontext']){
                        $.each(respuesta['mycontext'], function( clave, valor ) {
                            $('.'+clave).html(valor)
                        });
                            }
                     if (respuesta['redirect']){
                            $(location).attr('href',respuesta['redirect']);
                            }
                    
                }).fail(function (source, error) {
                    if (typeof error.data != 'undefined'){
                       $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                                '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                                '<strong class="text-danger">Debug</strong>'+
                                                '<p>'+error.data.debug+'</p>');
                    }else{
                        $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                                '<p>Fallo de conexión</p>'+
                                                '<strong class="text-danger">Debug</strong>'+
                                                '<p>Error de servidor</p>');
                        
                        
                        }
                    $('#AJAXErrorModal').modal('show');
                    $(panramentros['gif']).hide()
                     $(panramentros['boton']).show()
                });
                
            }
            
             }
             
             //~ creo el pliguin del apiform_panel donde le digo que si le pansan un parametro
             //~ llamado context retorne return apiform_panel.context($this);
             //~ este metodo devuelve los siguintes datos: {datos:datos,destino:destino,datos_post:datos_post}
             //~ de lo contrario devuelve el objeto apiform_panel con el cual pueden llamar a la clase apiform_panel.ajax
             //~ y en esta apunta a su metodo apiform_panel.ajax.enviar el cual recibe como parametros destino,datos
             //~ ejemplo:
             
             //~ $(".clase o id_del_boton ").click( function( event ) {
            //~ var v=$('#id_del_formulario').apiform_panel();
                    //~ optienes el contexto del formulario con v.context
            //~ var conte=v.context('#id_del_formulario');
                    //~ puedes recorrer los compos del formulario de la siguiente manera
             //~ $.each(conte['datos'], function( clave, valor ) {
                 //~ console.log(valor.value)
                //~ 
                 //~ });
            //~ v.ajax.enviar(conte.destino,conte.datos_post)
             //~ });  
            $.fn.apiform_panel = function (options) {
                var $this = $(this), data = $this.data('apiform_panel');
                if (options== 'context') {
                    return apiform_panel.context($this);
                    }
                if (!data) {
                return apiform_panel
                }
                
                };
                
             
             
             
             
         
         $("#id_enviar").click( function() {
             var form=$(this).attr('form1');
             var gif=$('#img-'+form);
             var context=apiform_panel.context('#form1');
             if (context.campovacios=='no'){
                  var panramentros={'gif':gif,'boton':this}
                 apiform_panel.ajax.enviar(context.destino,context.datos,panramentros);
             }
            
             });
         
    //~ Envio de checkbox bootstrapSwitch
    
    $('input[type="checkbox"]').on('switchChange.bootstrapSwitch', function(value, state) {
                   var auto_envio= $(this).attr('auto_envio')
                     if (auto_envio!=null){
                         var SI=$(this).attr('auto_envio').toUpperCase();
                         }
                     var auto_envio=$(this).attr('auto_envio')
                     if (SI=='SI' | SI=='1'){
                         var destino=$(this).attr('destino');
                         var datos_post={ id : $(this).val(),'state':state }
                         apiform_panel.ajax.enviar(destino,datos_post)
                         }
                    });
   
    console.debug("[apiform_panel] Custom JS for apiform_panel loaded!");
    });


//~ function botton_enviar(form,datos,action){
                //~ this.form=form;
                //~ this.datos=datos;
                //~ this.action=action;
                //~ }
        //~ botton_enviar.prototype.form_datos=function(){
            //~ return $(this.form).serializeArray();
        //~ }
        //~ botton_enviar.prototype.form_destino=function(){
                //~ console.log('hola mundo'+this.form_datos())
                //~ if (this.action==null){
                    //~ return $(this.form).attr('action');
                                    //~ }
                    //~ return this.action
                                    //~ }
        //~ 
        //~ botton_enviar.prototype.datos_post=function() {
                //~ if (this.datos==null){
                    //~ return $(this.form).serialize();
                                    //~ }
                    //~ return this.datos
                                    //~ 
            //~ }
        //~ botton_enviar.prototype.enviar=function() {
                        //~ event.preventDefault();
                      //~ console.log('dafjakjfjafljkl'+this.form_destino()+'ggsdg');
                       //~ $.ajax({
                                //~ url :this.form_destino(),
                                //~ data : this.datos_post(),
                                //~ type : 'POST',
                                //~ dataType : 'json',
                                //~ success: function(response, status, xhr, wfe){
                                    //~ },
                                //~ timeout: 5000,
                                //~ error : function(jqXHR, textStatus, errorThrown) {
                                     //~ $('#AJAXErrorModal').modal('show');
                                //~ }
                            //~ });
            //~ 
            //~ 
            //~ }
        //~ 
    //~ 
    //~ 
    //~ $("#id_enviar").click( function( event ) {
        //~ var enviar=new botton_enviar('#form1');
        //~ enviar.enviar();
        //~ });
