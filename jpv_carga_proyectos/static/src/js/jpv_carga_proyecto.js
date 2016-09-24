$(document).ready(function () {
    
                
    //~ limpia todos los campos al refrescar el navegador
    
    function resetForm($form) {
        $form.find('input:text, input:password, input:file, textarea').val('');
        $form.find('select').val('');
        $form.find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');
    }

    resetForm($('#formcrearproyecto'));
    
    
    
     //~ cortar una cadena de caracteres  y adicionar el boton de leer mas para poder
    //~ visualiazar el texto cortado de la cadena
    
     var proyectos_ept = proyectos_ept || {};
         proyectos_ept.leer_mas_nombre=function(body){
            var cant_tr=body.find('tr').length
            cont=1
            while (cont <= cant_tr){
                var caracteres_mostrar=92
                var contenido=$(".limitar_caracteres_"+cont).html()
                if (String(contenido).length > caracteres_mostrar){
                    var resumen = contenido.substr(0,caracteres_mostrar);
                    var todo=contenido.substr(caracteres_mostrar,String(contenido).length - caracteres_mostrar)
                    var nuevo_contenido=resumen+'<span class="complete">'+' </span><span class="more" style="cursor:pointer"><a>Leer mas...</a></span>'
                        $('.limitar_caracteres_'+cont).html(nuevo_contenido)
                    }
                $(".more").toggle(function(){
                    contenido_completo_abrir='<span class="complete">'+todo+' </span><span class="more" style="cursor:pointer"><a><span class="glyphicon glyphicon-circle-arrow-up "></a></span>'
                    $(this).html(contenido_completo_abrir).siblings(".complete_"+cont).show();
                    }, 
                    function(){
                        leer_mas="<a>Leer Mas...</a>"
                        $(this).html(leer_mas).siblings(".complete_"+cont).hide();
                        }
                        )
                cont=cont+1
                }
             }
             
    $.fn.proyectos_ept = function (options) {
                var $this = $(this), data = $this.data('proyectos_ept');
                if (options== 'leer_mas_nombre') {
                    return proyectos_ept.leer_mas_nombre($this);
                    }
                if (!data) {
                return proyectos_ept
                }
                };
     proyectos_ept.leer_mas_nombre($('#proyectos_completos'));
    
    
    
    
    
    $("textarea[maxlength]").keyup(function(){
        
        var limit=$(this).attr("maxlength");
        var value=$(this).val();
        var current=value.length;
        if (limit<current){
            $(this).val(value.substring(0,limit))
            }
        })
    
    
    
    //~ linea de jquery util para los mensaje de ayuda al pasar el cursor del maouse por el elemento html
    
    $('[data-toggle="popover"]').popover();
    
    //~ mascara de fecha
        
    $('.date_proyecto_ept').mask('00-00-0000');
    
    //~ mascara de monto
        
    $('.monto').mask("#.##0,00", {reverse: true});
                
    //~ ocultar, mostrar y limpiar obra civil
    
    var obra_civil = jQuery('#obra_civil');
    $(obra_civil).click(function(event) {
        if (obra_civil.is(':checked')) {
            if ($("#subcategoria").val()==''){
                cuerpo='Debe seleccionar una Subcategoria'
                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                $('.titulo').html('<strong>Aviso!</strong>')
                $('#AJAX_Modal').modal('show');
                obra_civil.removeAttr('checked')
            }
            else{
                $("#cantidad_unidad").removeClass('hidden');
                $("#tipo_obra").removeClass('hidden');
            }
        } 
        else {
            $("#cantidad_unidad").addClass('hidden');
            $("#obra_confirm").removeAttr('checked');
            $("#cantidad_unidad").find('input:text,select,input[type=number]').each(function(){
                        $(this).val('');
            });
            $("#tipo_obra").addClass('hidden');
            $('#tipo_obra').find('input:radio').each(function(){
                    $(this).removeAttr('checked');
            $('#unidad option[value!=""]').remove();
            });
        }
    });
                
    //~ ocultar, mostrar y limpiar adquisicion de equipos
                
    var adquisi_equipo=jQuery('#adquisi_equipo');
    $(adquisi_equipo).click(function(event){
        if (adquisi_equipo.is(':checked')) {
            $("#t_adquisi_equipo, #agregarFila").removeClass('hidden');
        } 
        else {
            $("#equi_confirm").removeAttr('checked');
            $("#t_adquisi_equipo, #agregarFila").addClass('hidden');
            $("#t_adquisi_equipo1").find('input:text, input:password, input:file, select, textarea,input[type=number]').val('');
            var n=$('#t_adquisi_equipo1 tr').length
            $('#t_adquisi_equipo1 tr').each(function (){
                if (n > 1){
                    $(this).remove();
                    n--;
                };
            });
        }
    });
                
    //~ ocultar, mostrar  y limpiar adquisicion de maquinarias
                           
    var adquis_maqui=jQuery('#adquis_maqui');
    $(adquis_maqui).click(function(event){
        if (adquis_maqui.is(':checked')) {
            $("#t_adquis_maqui,#agregarFila2").removeClass('hidden');
        } 
        else {
            $("#maqui_confirm").removeAttr('checked');
            $("#t_adquis_maqui,#agregarFila2").addClass('hidden');
            $("#t_adquis_maqui1").find('input:text, input:password, input:file, select, textarea,input[type=number]').val('');
            var m=$('#t_adquis_maqui1 tr').length
            $('#t_adquis_maqui1 tr').each(function (){  
                if (m > 1){
                    $(this).remove();
                    m--;
                };
            });
        };
    });
                
    //~ ocultar, mostrar y limpiar adquisicion de vehiculos
           
    var adquis_vehiculo=jQuery('#adquis_vehiculo');
    $(adquis_vehiculo).click(function(event){
        if (adquis_vehiculo.is(':checked')) {
            $("#t_adquis_vehiculo,#agregarFila3").removeClass('hidden');
        } 
        else {
            
            $("#vehic_confirm").removeAttr('checked');
            $("#t_adquis_vehiculo,#agregarFila3").addClass('hidden');
            $("#t_adquis_vehiculo1").find('input:text, input:password, input:file, select, textarea,input[type=number]').val('');
            var v=$('#t_adquis_vehiculo1 tr').length
            $('#t_adquis_vehiculo1 tr').each(function (){
                if (v > 1){
                    $(this).remove();
                    v--;
                };
            });
        };
    });
                
    //~ ocultar, mostrar y limpiar materiales de insumo
                
    var adquis_materiales=jQuery('#adquis_materiales');
    $(adquis_materiales).click(function(event){
        if (adquis_materiales.is(':checked')) {
            $("#t_adquis_materiales,#agregarFila4").removeClass('hidden');
        } 
        else {
            $("#mater_confirm").removeAttr('checked');
            $("#t_adquis_materiales,#agregarFila4").addClass('hidden');
            $("#t_adquis_materiales1").find('input:text, input:password, input:file, select, textarea,input[type=number]').val('');
            var mi=$('#t_adquis_materiales1 tr').length
            console.log(mi)
            console.log(mi)
            console.log(mi)
            console.log(mi)
            $('#t_adquis_materiales1 tr').each(function (){
                if (mi > 1){
                    $(this).remove();
                    mi--;
                };
            });
        };
    });
               
    //~ ocultar, mostrar y limpiar semovientes
                
    var adquis_semovientes=jQuery('#adquis_semovientes');
    $(adquis_semovientes).click(function(event){
        if (adquis_semovientes.is(':checked')) {
            $("#t_adquis_semovientes,#agregarFila5").removeClass('hidden');
        } 
        else {
            $("#semovi_confirm").removeAttr('checked');
            $("#t_adquis_semovientes,#agregarFila5").addClass('hidden');
            $("#t_adquis_semovientes1").find('input:text, input:password, input:file, select, textarea,input[type=number]').val('');
            var semov=$('#t_adquis_semovientes1 tr').length
            console.log(semov)
            console.log(semov)
            console.log(semov)
            console.log(semov)
            console.log(semov)
            $('#t_adquis_semovientes1 tr').each(function (){
                if (semov > 1){
                    $(this).remove();
                    semov--;
                };
            });
        };
    });
                
                
    //~ jquery para adjuntar archivos
                
            
    $(".input-files_proyecto").fileinput({
        uploadUrl:"",
        showRemove:true,
        uploadAsync:true,
        showUpload:false,
        showCaption: false,
        showBrowserAdd:true ,
        autoReplace: true,
        allowedFileExtensions: ["pdf"],    });
            
    //~ jquery para adjuntar imagenes
                
    $(".input-imagen_proyecto").fileinput({
        uploadUrl:"",
        showRemove:true,
        uploadAsync:true,
        showUpload:false,
        showCaption: false,
        showBrowserAdd:true ,
        autoReplace: true,
        allowedFileExtensions: ["png", "jpg", "jpeg"],
    });
        
    //~ funciones para sumar valores recibidos desde un imput y devolver un total en otro input
        
    $('input.directos').on('change', function(event){
        var valor_1=$('#directo_masculino').val()
        var valor_2=$('#directo_femenino').val()
        suma_beneficios(parseInt(valor_1),parseInt(valor_2),event.currentTarget.classList[1]);
    });
    $('input.indirectos').on('change', function(event){
        var valor_1=$('#indirecto_masculino').val()
        var valor_2=$('#indirecto_femenino').val()
        suma_beneficios(parseInt(valor_1),parseInt(valor_2),event.currentTarget.classList[1]);
    });
    $('input.beneficiario').on('change', function(event){
        var valor_1=$('#benef_masculino').val()
        var valor_2=$('#benef_femenino').val()
        suma_beneficios(parseInt(valor_1),parseInt(valor_2),event.currentTarget.classList[1]);
    });
            
    function suma_beneficios(cant1,cant2,tipo){
        if (isNaN(cant1)==true){
            cant1=0
            }
        if (isNaN(cant2)==true){
            cant2=0
            }
        total=cant1+cant2
        $('input.total_'+tipo).val(total);
        $('.total_'+tipo).text(total);
    };
        
        
    //~ filtro de las categorias de acuerdo a un tipo de sector
        
    $('select#tipo_sector').on('change', function(event){
        var id=$('#tipo_sector').val()
        openerp.jsonRpc("/proyecto/crear/categoria", 'call', {
            'id': id}).then(function(res){
                ids=res[1]
                $('#categoria option[value!=""]').remove();
                $('#subcategoria option[value!=""]').remove();
                $('#obra_civil').removeAttr('checked')
                $('input[name=tipo_obra]').removeAttr('checked')
                $('#aval,#adquis_semovientes,#coordenada').removeAttr('checked')
                $("#cantidad_unidad,#tipo_obra,#adqui_semovi,#t_adquis_semovientes,#agregarFila5,#coord_f" ).addClass('hidden');
                $("#aval_file").addClass('hidden');
                $("#cantidad_unidad,#t_adquis_semovientes1,#coord_f").find('input:text,select,input[type=number]').each(function(){
                            $(this).val('');
                            });
                $('#unidad option[value!=""]').remove();
                var semov=$('#t_adquis_semovientes1 tr').length
                $('#t_adquis_semovientes1 tr').each(function (){
                    if (semov > 1){
                        $(this).remove();
                        semov--;
                    };
                });
                for(i in ids ){
                    $('#categoria').append(new Option(res[0][i], ids[i], false));
                }
            });
    });
            
    //~ filtro de las subcategorias de acuerdo a una categoria
        
    $('select#categoria').on('change', function(event){
        var id=$('#categoria').val()
        var prueba=$('#categoria option:selected').text()
        openerp.jsonRpc("/proyecto/crear/categoria", 'call', {
            'id': id}).then(function(res){
                ids=res[1]
                $('#subcategoria option[value!=""]').remove();
                for(i in ids ){
                    $('#subcategoria').append(new Option(res[0][i], ids[i], false));
                }
                $('#obra_civil').removeAttr('checked')
                $('input[name=tipo_obra]').removeAttr('checked')
                $('#aval,#adquis_semovientes,#coordenada').removeAttr('checked')
                $("#cantidad_unidad,#tipo_obra,#adqui_semovi,#t_adquis_semovientes,#agregarFila5,#coord_f" ).addClass('hidden');
                $("#aval_file").addClass('hidden');
                $("#cantidad_unidad,#t_adquis_semovientes1,#coord_f").find('input:text,select,input[type=number]').each(function(){
                            $(this).val('');
                            });
                $('#unidad option[value!=""]').remove();
                var semov=$('#t_adquis_semovientes1 tr').length
                $('#t_adquis_semovientes1 tr').each(function (){
                    if (semov > 1){
                        $(this).remove();
                        semov--;
                    };
                });
            });
    });
            
    //~ limpiar campos de obra civil al cambiar la subcategoria y validar si es semovientes
        
    $('select#subcategoria').on('change', function(event){
        var ids_sub=$(this).val()
        $('#obra_civil').removeAttr('checked')
        $('input[name=tipo_obra]').removeAttr('checked')
        $('#aval').removeAttr('checked')
        $("#cantidad_unidad,#tipo_obra" ).addClass('hidden');
        $("#aval_file").addClass('hidden');
        $("#cantidad_unidad").find('input:text,select,input[type=number]').each(function(){
                $(this).val('');
        $('#unidad option[value!=""]').remove();
        });
        if ($('#subcategoria option:selected').text()=='Sistema Productivo Animal'){
                $("#adqui_semovi").removeClass('hidden');
        }
        else{
            $("#adqui_semovi,#t_adquis_semovientes,#agregarFila5").addClass('hidden')
            $('#adquis_semovientes').removeAttr('checked')
            $("#t_adquis_semovientes1").find('input:text, select,input[type=number]').each(function(){
                $(this).val('');
            });
            var semov=$('#t_adquis_semovientes1 tr').length
            $('#t_adquis_semovientes1 tr').each(function (){
                if (semov > 1){
                    $(this).remove();
                    semov--;
                };
            });
        }
        openerp.jsonRpc("/proyecto/coordenadas", 'call', {
            'ids_sub': ids_sub}).then(function(res){
            if(res==true){
                $('#coordenada').attr('checked',true);;
            }
            else{
                $('#coordenada').removeAttr('checked')
            }
            if ( $('#coordenada').is(':checked')) {
                $("#coord_f").removeClass('hidden');
            } 
            else {
                $("#coord_f").addClass('hidden');
                $("#coord_f").find('input:text, select,input[type=number]').each(function(){
                    $(this).val('');
                });
            }
        });   
    });
        
    //~ filtro de los municipios de acuerdo al estado
        
    $('select#estado').on('change', function(event){
        var id_estado=$('#estado').val()
        var id_entidad=$('#entidad').val()
        openerp.jsonRpc("/proyecto/crear/municipio", 'call', {
            'id_estado': id_estado,
            'id_entidad':id_entidad}).then(function(res){
                ids=res[1]
                $('#municipio option[value!=""]').remove();
                $('#parroquia option[value!=""]').remove();
                for(i in ids ){
                    $('#municipio').append(new Option(res[0][i], ids[i], false));
                }
        });
        openerp.jsonRpc("/proyecto/filtrarhuso", 'call', {
            'id_estado': id_estado,}).then(function(res_h){
                ids_h=res_h[1]
                $('#huso option[value!=""]').remove();
                $('#husof option[value!=""]').remove();
                for(i in ids_h ){
                    
                    $('#huso').append(new Option(res_h[0][i], ids_h[i], false));
                    $('#husof').append(new Option(res_h[0][i], ids_h[i], false));
                }
        });
    });
        
    //~ filtro de las parroquias de acuerdo al municipio
        
    $('select#municipio').on('change', function(event){
        var id_municipio=$('#municipio').val()
        openerp.jsonRpc("/proyecto/crear/parroquia", 'call', {
            'id_municipio': id_municipio,}).then(function(res){
                ids=res[1]
                $('#parroquia option[value!=""]').remove();
                for(i in ids ){
                    $('#parroquia').append(new Option(res[0][i], ids[i], false));
                }
        });
    });
                
    //~ filtro de las caracteristicas del vehiculo de acuerdo al tipo
        
    $(function(){
        $('.vehiculo').live('click', function (event){
            var id_uso=$(this).val();
            var name=$(this).attr('name');
            name=name.split('_')
            
            openerp.jsonRpc("/proyecto/crear/caracateristica_vehiculo", 'call', {
                'id_uso': id_uso,}).then(function(res){
                    ids=res[1]
                    
                    $('#vehiculo_caracteristica_select_'+name[3]+' option[value!=""]').remove();
                    $('#vehiculo_tipo_text_'+name[3]+' option[value!=""]').remove();
                    for(i in ids ){
                        $('#vehiculo_caracteristica_select_'+name[3]).append(new Option(res[0][i], ids[i], false));
                    }
                });
        });
    });
    
    //~ filtro del tipo del vehiculo de acuerdo a su caracteristica
    $(function(){
        $('.vehiculo_caract').live('click', function (event){
            var id_tipo=$(this).val();
            var name=$(this).attr('name');
            name=name.split('_')
            openerp.jsonRpc("/proyecto/crear/tipo_vehiculo", 'call', {
                'id_tipo': id_tipo,}).then(function(res){
                    ids=res[1]
                    $('#vehiculo_tipo_text_'+name[3]+' option[value!=""]').remove();
                    for(i in ids ){
                        $('#vehiculo_tipo_text_'+name[3]).append(new Option(res[0][i], ids[i], false));
                    }
            });
            
        });
    });
    
    
    //~ filtro de los semovientes de acuerdo a su grupo etario
    
    $(function(){
        $('.semoviente_especie').live('click', function (event){
            var id_tipo=$(this).val();
            var name=$(this).attr('name');
            name=name.split('_')
            openerp.jsonRpc("/proyecto/crear/grupo_semoviente", 'call', {
                'id_tipo': id_tipo,}).then(function(res){
                    ids=res[1]
                    $('#semovientes_grupo_select_'+name[3]+' option[value!=""]').remove();
                    $('#semovientes_uso_select_'+name[3]+' option[value!=""]').remove();
                    $('#semovientes_proposito_select_'+name[3]+' option[value!=""]').remove();
                    for(i in ids ){
                        $('#semovientes_grupo_select_'+name[3]).append(new Option(res[0][i], ids[i], false));
                    }
            });
            
        });
    });
    
    //~ filtro de los semovientes de acuerdo a su uso
    
    $(function(){
        $('.semoviente_grupo').live('click', function (event){
            var id_tipo=$(this).val();
            var name=$(this).attr('name');
            name=name.split('_')
            openerp.jsonRpc("/proyecto/crear/uso_semoviente", 'call', {
                'id_tipo': id_tipo,}).then(function(res){
                    ids=res[1]
                    $('#semovientes_uso_select_'+name[3]+' option[value!=""]').remove();
                    $('#semovientes_proposito_select_'+name[3]+' option[value!=""]').remove();
                    for(i in ids ){
                        $('#semovientes_uso_select_'+name[3]).append(new Option(res[0][i], ids[i], false));
                    }
            });
            
        });
    });
    
    //~ filtro de los semovientes de acuerdo a su proposito
    
    $(function(){
        $('.semoviente_uso').live('click', function (event){
            var id_tipo=$(this).val();
            var name=$(this).attr('name');
            name=name.split('_')
            openerp.jsonRpc("/proyecto/crear/proposito_semoviente", 'call', {
                'id_tipo': id_tipo,}).then(function(res){
                    ids=res[1]
                    $('#semovientes_proposito_select_'+name[3]+' option[value!=""]').remove();
                    for(i in ids ){
                        $('#semovientes_proposito_select_'+name[3]).append(new Option(res[0][i], ids[i], false));
                    }
            });
            
        });
    });
        
    //~ valida que el monto no sea mayor al monto disponible
        
    $('#monto_proyecto').on('change', function(event){
            var monto_disponible=$('p#monto_disponible').text()
            var monto_proyecto=$(this).val()
            monto_disponible=monto_disponible.split(',')
            entero_disp=monto_disponible[0].split('.')
            decimal_disp=monto_disponible[1]
            monto_disp=entero_disp.join('')
            monto_disponible1=monto_disp+'.'+decimal_disp
            monto_proyecto=monto_proyecto.split(',')
            entero=monto_proyecto[0].split('.')
            decimal=monto_proyecto[1]
            monto=entero.join('')
            monto_proyect=monto+'.'+decimal
            if(parseFloat(monto_disponible1)<parseFloat(monto_proyect)){
                cuerpo='El monto que desea asignar a su proyecto no esta disponible en la cuenta asignada'
                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                $('.titulo').html('<strong>Error!</strong>')
                $('#AJAX_Modal').modal('show');
                $(this).val('');
            };
    });
            
            
    //~ validar aval de acuerdo a la subcategoria
        
    $('input[name=tipo_obra]').on('change', function(event){
        var tipo_obra=$(this).attr('id');
        var subacategoria=$('#subcategoria').val();
        openerp.jsonRpc("/proyecto/crear/validar_aval", 'call', {
            'tipo_obra': tipo_obra,
            'subacategoria':subacategoria,}).then(function(res){
                if(res==true){
                    $('#aval').attr('checked',true);
                    }
                else{
                    $('#aval').removeAttr('checked')
                    }
                if ( $('#aval').is(':checked')) {
                    $("#aval_file").removeClass('hidden');
                    cuerpo='Este proyecto requiere un aval'
                    $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                    $('.titulo').html('<strong>Aviso!</strong>')
                    $('#AJAX_Modal').modal('show');
                    } 
                else {
                    $("#aval_file").addClass('hidden');
                    $("#aval_file").find('input:file').each(function(){
                        $(this).val('')
                    });
                }
        });
       
       openerp.jsonRpc("/proyecto/crear/unidad",'call',{
            'tipo_obra': tipo_obra,
            'subacategoria':subacategoria,}).then(function(res){
                    ids=res[1]
                    $('#unidad option[value!=""]').remove();
                    for(i in ids ){
                        $('#unidad').append(new Option(res[0][i], ids[i], false));
                    }
        });      
    });
            
    //~ VALIDACION DE PROYECTO DE MANTENIMIENTO
            
    var proyect_mantenimiento=jQuery('#proyect_mantenimiento');
    $(proyect_mantenimiento).click(function(event){
        if (proyect_mantenimiento.is(':checked')) {
            $("#caracteristicas_generales").addClass('hidden');
            $("#tipo_obra, #aval_file, #cantidad_unidad, #t_adquisi_equipo, #t_adquis_maqui, #t_adquis_vehiculo, #t_adquis_materiales, .agregarFila").addClass('hidden');
            $("#caracteristicas_generales").find('input:text,input:file,input[type=number], select').each(function(){
                $(this).val('');
            }) 
           $('#caracteristicas_generales').find('input:radio, input:checkbox').each(function(){
                $(this).removeAttr('checked');
            });
            var n=$('#t_adquisi_equipo1 tr').length
            $('#t_adquisi_equipo1 tr').each(function (){
                if (n > 1){
                    $(this).remove();
                    n--;
                };
            });
            var m=$('#t_adquis_maqui1 tr').length
            $('#t_adquis_maqui1 tr').each(function (){
                if (m > 1){
                    $(this).remove();
                    m--;
                };
            });
            var v=$('#t_adquis_vehiculo1 tr').length
            $('#t_adquis_vehiculo1 tr').each(function (){
                if (v > 1){
                    $(this).remove();
                    v--;
                };
            });
            var mi=$('#t_adquis_materiales1 tr').length
            $('#t_adquis_materiales1 tr').each(function (){
                if (mi > 1){
                    $(this).remove();
                    mi--;
                };
            });
            var mi=$('#t_adquis_semovientes1 tr').length
            $('#t_adquis_semovientes1 tr').each(function (){
                if (mi > 1){
                    $(this).remove();
                    mi--;
                };
            });
            $("#monto_mant_disp").removeClass('hidden');
        }
        else {
            $("#caracteristicas_generales").removeClass('hidden');
            $("#proyect_manten_confirm").removeAttr('checked');
            $("#monto_mant_disp").addClass('hidden');
            $("#t_adquis_semovientes,#agregarFila5").addClass('hidden');
            
            var subacategoria=$('#subcategoria').val();
            if (subacategoria==98){
				$("#adqui_semovi").removeClass('hidden');
				
				}
        };
    });

    $("#editar_proyecto_2" ).click(function() {
        
        var gif=$('#gifbusq_avanz');
        var body_id='#tbody_proyecto_id'
        //~ form principal
        var formid_editar_principal='#form2';
        var apiform_principal=$(formid_editar_principal).apiform_panel();
        var Cont_principal=apiform_principal.context(formid_editar_principal);
        
        //~ form auxiliar
        var form_editar_auxiliar='#form_editar_auxiliar';
        var apiform_auxiliar=$(form_editar_auxiliar).apiform_panel();
        var Cont_auxiliar=apiform_auxiliar.context(form_editar_auxiliar);
        
        
        var datos_post={'post_principal':Cont_principal.datos,'post_auxiliar':Cont_auxiliar.datos}
        var panramentros={'gif':gif,'boton':this}
        if (Cont_principal.campovacios=='no'){
            apiform_principal.ajax.enviar(Cont_principal.destino,datos_post,panramentros)
            }
    
     });

    $("#cancelar_proyecto_confirm" ).click(function() {
        proyecto_id=$("#proyecto_id").val()
        openerp.jsonRpc("/proyecto/cancelar", 'call', {
                'proyecto_id': proyecto_id,}).then(function(res){
                    if (res==true){
                       location.reload();
                       }
                });
        
    
     });
     
     
     //~ boton para editar proyeto

    $("#editar_proyecto_confirm" ).click(function() {
        var form=$(this).attr('form1');
        var gif=$('#img-'+form);
        var body_id='#tbody_proyecto_id'
        //~ form principal
        var formid_editar_principal='#form2';
        var apiform_principal=$(formid_editar_principal).apiform_panel();
        var Cont_principal=apiform_principal.context(formid_editar_principal);
        
        //~ form auxiliar
        var form_editar_auxiliar='#form_editar_auxiliar';
        var apiform_auxiliar=$(form_editar_auxiliar).apiform_panel();
        var Cont_auxiliar=apiform_auxiliar.context(form_editar_auxiliar);
        
        
        var datos_post={'post_principal':Cont_principal.datos,'post_auxiliar':Cont_auxiliar.datos}
        var panramentros={'gif':gif,'boton':this}
        if (Cont_principal.campovacios=='no'){
            apiform_principal.ajax.enviar(Cont_principal.destino,datos_post,panramentros)
            }
        $('#editar_proyecto_confirm').show()
     });
        
    //~ boton para guardar proyectos nuevos
    
    $("#enviar_proyecto" ).click(function() {
        var monto=$("#monto_proyecto").val()
        if (parseFloat(monto)<-1){
            cuerpo='El monto a registrar para el proyecto debe ser mayor a 0.00'
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            }
        else{
            var form='#formcrearproyecto';
            var gif=$('#gifbusq_avanz');
            var v=$(form).apiform_panel();
            var formCont=v.context(form);
            var panramentros={'gif':gif,'boton':this}
           
            if (formCont.campovacios=='no'){
             v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
         }
        };
    });
                    
    //~ validar campos que su valor sea mayor a 0
   
    $('.mayor_0').on('change', function(event){
        var campo=$(this).attr('mensaje')
        var monto=$(this).val()
        if (parseInt(monto)<1){
            cuerpo=('El campo '+campo+' Debe ser mayor a 0')
            $(this).val('')
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
        }
    }); 
                        
    //~ validar coordenadas
                   
   
   
   $('.coordenada').on('change', function(event){
        var campo=$(this).attr('mensaje')
        var name=$(this).attr('name')
        var coord=$(this).val()
        
        coord_validacion=coord.split('.')
        
        if (coord_validacion.length==1){
            
            
            if ((name=='coord_este' || name=='coord_este_f') && (parseInt(coord)>999999)){
                cuerpo=('El campo '+campo+' no deber ser mayor a 999999')
                $(this).val('')
                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                $('.titulo').html('<strong>Aviso!</strong>')
                $('#AJAX_Modal').modal('show');
            }
            if ((name=='coord_norte' || name=='coord_norte_f') && (parseInt(coord)>1999999)){
                cuerpo=('El campo '+campo+' no deber ser mayor a 1999999')
                $(this).val('')
                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                $('.titulo').html('<strong>Aviso!</strong>')
                $('#AJAX_Modal').modal('show');
            }
            
            }
        else{
            cuerpo=('El campo '+campo+' debe contener solo numeros enteros')
            $(this).val('')
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            }
        
        
    });
    
    //~ mostrar y editar imagen
    
    
    var solo_lectura=$('#solo_lectura').attr('value')
    var solo_lecturass=$('#objeto_fotos_datas').attr('value')
    
    
    if(solo_lectura=='True'){
            $('input[name="fotos_id"]').fileinput("disable");
            $('input[name="fotos_id"]').fileinput('refresh',{
                    showClose:false,
                    initialPreview:[]
                    });   }
    
    if($('input[name*="objeto_fotos"]').length){
        imagen_data=$('input[name="objeto_fotos_datas"]').attr('value');        
        imagen_name=$('input[name="objeto_fotos_name"]').attr('value'); 
        imagen_type=$('input[name="objeto_fotos_mimetype"]').attr('value'); 
        imagen_id=$('input[name="objeto_fotos_id"]').attr('value'); 
        
        var image_element=$('input[name="fotos_id"]')
        image_element.fileinput('refresh',{
                    uploadUrl:'',
                    showRemove:true,
                    //~ showClose:false,
                    uploadAsync:false,
                    showUpload:false,
                    showCaption: true,
                    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px">',
                    autoReplace: false,
                    overwriteInitial: false,
                    maxFileCount:1,
                    allowedFileExtensions: ["png", "jpg", "jpeg","pdf"],
                    initialPreview:["<img style='height:160px' src='data:"+imagen_type+
                                    ";base64,"+imagen_data+"' file_id='"+imagen_id+"'>"],
                    initialPreviewConfig:[{caption: imagen_name, width: "120px", url: ""}],
                    });   
        if(solo_lectura=='True'){
            image_element.fileinput("disable");
            image_element.fileinput('refresh',{
            
                    showClose:false,
                    });   
                }
        image_element.after('<input type="hidden" value="data:'+imagen_type+
                                ';base64,'+imagen_data+';file_id='+imagen_id+
                                '"file_id="'+imagen_id+'" file-name="'+imagen_name+'" input-file-name="'+
                                image_element.attr('name')+'" name="'+image_element.attr('name')+
                                '-'+1+'-'+imagen_name+'" />');
        }   
    
    var solo_lectura_aval=$('#solo_lectura_aval').attr('value')
    
    if(solo_lectura_aval=='True'){
            $('input[name="aval_ids"]').fileinput("disable");
            $('input[name="aval_ids"]').fileinput('refresh',{
                    showClose:false,
                    initialPreview:[]
                    });   }
    
    if($('input[name*="objeto_aval"]').length){
        file_data=$('input[name="objeto_aval_datas"]').attr('value');        
        file_name=$('input[name="objeto_aval_name"]').attr('value'); 
        file_type=$('input[name="objeto_aval_type"]').attr('value'); 
        file_id=$('input[name="objeto_aval_id"]').attr('value'); 
        
        
        var file_element=$('input[name="aval_ids"]')
        file_element.fileinput('refresh',{
                    uploadUrl:'',
                    showRemove:true,
                    //~ showClose:false,
                    uploadAsync:false,
                    showUpload:false,
                    showCaption: true,
                    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px">',
                    autoReplace: false,
                    overwriteInitial: false,
                    maxFileCount:1,
                    allowedFileExtensions: ["png", "jpg", "jpeg","pdf"],
                    initialPreview:['<object class="file-object" data="data:'+file_type+
                                    ';base64,'+file_data+'" file_id="'+file_id+
                                    '" type="application/pdf" width="160px" height="160px" internalinstanceid="3"></object>'],
                    initialPreviewConfig:[{caption: file_name, width: "120px", url: ""}],
                    });
                    if(solo_lectura=='True'){
                        file_element.fileinput("disable");
                        file_element.fileinput('refresh',{
                    showClose:false,
                    });   }   
       
                
        file_element.after('<input type="hidden" value="data:'+file_type+
                                ';base64,'+file_data+';file_id='+file_id+
                                '"file_id="'+file_id+'" file-name="'+file_name+'" input-file-name="'+
                                file_element.attr('name')+'" name="'+file_element.attr('name')+
                                '-'+1+'-'+file_name+'" />');
        }   
        
        
        
    $("#proyectos_entidad" ).click(function() {
         $("#entidades").removeClass('hidden');
         $("#proyecto_no").removeClass('hidden');
         $("#alcaldias").addClass('hidden');
         $("#gobernacion").addClass('hidden');
         $("#mensaje_sin_proyecto").addClass('hidden');
    });
   
    $("#proyectos_alcaldia" ).click(function() {
         $("#alcaldias").removeClass('hidden');
         $("#mensaje_sin_proyecto").removeClass('hidden');
         $("#entidades").addClass('hidden');
         $("#proyecto_no").addClass('hidden');
    });
    
    $("#proyectos_gobernacion" ).click(function() {
         $("#gobernacion").removeClass('hidden');
         $("#mensaje_sin_proyecto").removeClass('hidden');
         $("#entidades").addClass('hidden');
         $("#proyecto_no").addClass('hidden');
    });
   
        
        
           
});




           

            
            
