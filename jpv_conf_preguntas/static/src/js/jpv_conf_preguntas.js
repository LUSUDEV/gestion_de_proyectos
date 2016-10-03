$(document).ready(function () {
     
    console.debug('inicio archivo js');    
     
     tActions = '<div class="file-actions">\n' +
        '    <div class="file-footer-buttons">\n' +
        '        {delete}{other}' +
        '    </div>\n' +
        '    <div class="file-upload-indicator" title="{indicatorTitle}">{indicator}</div>\n' +
        '    <div class="clearfix"></div>\n' +
        '</div>';
    
    $(".input-file").each(function(file){
        $(this).fileinput({
        uploadUrl:' ',
        showRemove:true,
        uploadAsync:false,
        actionUpload:false,
        showUpload:false,
        showCaption: true,
        defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px"/>',
        autoReplace: false,
        maxFileCount:parseInt($(this).attr('maxfilecount')),
        allowedFileExtensions: ["pdf"],
        });
        
        });
        
    
    
    $(".input-image").each(function(img){
        $(this).fileinput({
        uploadUrl:' ',
        showRemove:true,
        uploadAsync:false,
        actions: tActions,
        showUpload:false,
        showCaption: true,
        defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px"/>',
        autoReplace: false,
        maxFileCount:parseInt($(this).attr('maxfilecount')),
        allowedFileExtensions: ["png", "jpg", "jpeg","pdf"],
        });
        
        });
    
        
        
        
    
    $('input.rif').mask("A-00000000-0"); 
    $('input.rif').on('change',function(){
        $(this).val($(this).val().toUpperCase());
        });
    //~ 
    $('input.jpv_conf_date').mask("99-99-9999");
    
    $('input.jpv_conf_date').datepicker({
        dateFormat: "dd-mm-yy"
        });

    $('input.jpv_conf_date').on('change', function(){
        my_id=((event.currentTarget.id).split('-')).pop();
        console.log(my_id);

    });
    
        
    $('input.numerico').mask("#.##0,00", {reverse: true});
    $('input.numerico').css("text-align",'right');
      
    
    //~ campos checkbox************
    
    $('input[type="checkbox"]').on('change',function(event){
        my_id=((event.currentTarget.id).split('-')).pop();
        count=0;
        count_true=0;
        if(event.currentTarget.attributes.dependiente){
            question_dependent=limpia_cadenas(event.currentTarget.attributes.dependiente.value);
            var other_answer=new Array;
            for (i in question_dependent){
                count=0;
                count_true=0;
                other_answer.push(limpia_cadenas($('div[id='+question_dependent[i][0]+']').attr("dependencia")));
                if (event.currentTarget.checked){
                    if (question_dependent[i][1]=='abre'){
                        if (other_answer[i].length){
                            for (r in other_answer[i]){
                                if (other_answer[i][r][0] !== my_id){
                                    if (other_answer[i][r][1] == question_dependent[i][1]){
                                        count++;
                                        if ($('option[respuesta_id='+other_answer[i][r][0]+']').length){
                                            count_true++;
                                            }
                                        if (($('input[respuesta_id='+other_answer[i][r][0]+']').length) && ($('input[respuesta_id='+other_answer[i][r][0]+']').is(':checked'))){
                                            count_true++;
                                            }
                                    }
                                }
                            }
                            if(count==count_true){showdiv(question_dependent[i][0],300);}
                        }
                        else{
                        showdiv(question_dependent[i][0],300);    
                        }
                    }
                }
                else{
                    if(question_dependent[i][1]=='abre'){
                        hidediv(question_dependent[i][0],300);
                        }
                }
            }
        }
    });
    
    //~ campos radio************
    
    $('input[type="radio"]').on('change',function(event){
        my_id=((event.currentTarget.id).split('-')).pop();
        if(event.currentTarget.attributes.dependiente){
            question_dependent=limpia_cadenas(event.currentTarget.attributes.dependiente.value);
            var other_answer=new Array;
            for (i in question_dependent){
                count=0;
                count_true=0;
                other_answer.push(limpia_cadenas($('div[id='+question_dependent[i][0]+']').attr("dependencia")));
                if (event.currentTarget.checked){
                    if (question_dependent[i][1]=='abre'){
                        if (other_answer[i].length){
                            for (r in other_answer[i]){
                                if (other_answer[i][r][0] !== my_id){
                                    if (other_answer[i][r][1] == question_dependent[i][1]){
                                        count++;
                                        if ($('option[respuesta_id='+other_answer[i][r][0]+']').length){
                                            if($('option[respuesta_id='+other_answer[i][r][0]+']').is(':selected')){
                                                count_true++;
                                                }
                                            }
                                        if (($('input[respuesta_id='+other_answer[i][r][0]+']').length) && ($('input[respuesta_id='+other_answer[i][r][0]+']').is(':checked'))){
                                            count_true++;
                                            }
                                    }
                                }
                            }
                            //~ if(count==count_true){$('div[id='+question_dependent[i][0]+']').show(300);}
                            if(count==count_true){showdiv(question_dependent[i][0],300);}
                        }
                        else{
                        showdiv(question_dependent[i][0],300);
                        }
                    }
                    else{
                        hidediv(question_dependent[i][0],300);
                    }
            }
            else{   console.log('escenario 2 hide');
                    console.log(question_dependent[i][0]);    
                    hidediv(question_dependent[i][0],300);
                    }
        }
    }
    });
    
    
    
    
    //~ campos select************
    
    $('select.selectpicker').on('change',function(event){
        if(!event.target.selectedOptions[0].attributes.respuesta_id){
            return false;
            }
        my_id=event.target.selectedOptions[0].attributes.respuesta_id.value;
        if(event.target.selectedOptions[0].attributes.dependiente){
            question_dependent=limpia_cadenas(event.target.selectedOptions[0].attributes.dependiente.value);
            var other_answer=new Array;
            for (i in question_dependent){
                count=0;
                count_true=0;
                other_answer.push(limpia_cadenas($('div[id='+question_dependent[i][0]+']').attr("dependencia")));
                if (question_dependent[i][1]=='abre'){
                    if (other_answer[i].length){
                        for (r in other_answer[i]){
                            if (other_answer[i][r][0] !== my_id){
                                if (other_answer[i][r][1] == question_dependent[i][1]){
                                    count++;
                                    if ($('option[respuesta_id='+other_answer[i][r][0]+']').length){
                                        if($('option[respuesta_id='+other_answer[i][r][0]+']').parent().parent()[0].name==$(this)[0].name){count_true++;}
                                            else{if($('option[respuesta_id='+other_answer[i][r][0]+']').is(':selected')){count_true++;}}
                                        }
                                    if (($('input[respuesta_id='+other_answer[i][r][0]+']').length) && ($('input[respuesta_id='+other_answer[i][r][0]+']').is(':checked'))){
                                        count_true++;
                                        }
                                }
                            }
                        }
                        if(count==count_true){$('div[id='+question_dependent[i][0]+']').show(300);}
                        if(count==count_true){showdiv(question_dependent[i][0],300);}
                    }
                    else{
                    showdiv(question_dependent[i][0],300);    
                    }
                }
                else{
                    hidediv(question_dependent[i][0],300);
                }
            }
        }
    });
    
    
    function limpia_cadenas(cadena){
        if (!cadena){
             return ""   
            }
        cadena=(cadena).split('-');
        cadena.pop()
        for (r in cadena){
            cadena[r]=(cadena[r]).split('#');
            }
        return cadena;
        }
        
        
    function showdiv(id, duration){
        $('div[id='+id+']').show(duration,function(){
            $('div[id='+id+']').css('overflow','inherit');
            new_class=$('div[id='+id+']').attr("color");
            old_class=$('div.panel-heading').parent()[0].classList[1];
            if(new_class!==old_class){
                $('div.panel-heading').parent().removeClass(old_class).addClass(new_class);
                }
                if(new_class == 'panel-info'){
                    agregar_btn_culminacion();
                    $('input[name="culminacion"]').attr('value','True')
                    }
                else{
                    if ($('input[name="status"]').attr('value')!== 'Culminado'){
                    console.log('quito el boton');
                    $('button#declarar').remove();
                    $('input[name="culminacion"]').attr('value','False');
                    $('input[name=declarar_culminacion]').attr('value','False');
                    }
                    }
            });
        checkedForm($('#form1'));
        return true;
        }
        
    function agregar_btn_culminacion(){
        if (!$('#form1').find('button#declarar').length){
        button_declarar=$('#form1').find('button#id_guardar_rendicion_jpv');
        id_button_declarar=button_declarar.attr('id');
        button_declarar.removeClass('btn-primary').addClass('btn-info');
        button_declarar.removeClass('glyphicon-send').addClass('glyphicon-floppy-save');
        button_declarar.html('Guardar')
        button_declarar.after('<button type="button" id="declarar" ref="advertencia" css=" js_submit" class="btn btn-primary glyphicon glyphicon-send">Declarar</button>');        
        }
        }
    
        
    function hidediv(id, duration){
        if(!$('div[id='+id+']').is(':hidden')){
            $('div[id='+id+']').hide(duration,function(){
                text=$('div[id='+id+']').find('input:text, textarea');
                select=$('div[id='+id+']').find('select.selectpicker');
                radio=$('div[id='+id+']').find('input:radio');
                checkbox=$('div[id='+id+']').find('input:checkbox');
                if(text.length){text.val('');}
                if(select.length){ 
                    select.selectpicker('deselectAll');
                    select.change();
                    }
                if(radio.length){
                    radio.removeAttr('checked');
                    radio.change();
                    }
                if(checkbox.length){
                    checkbox.removeAttr('checked');
                    checkbox.change();
                    }
            checkedForm($('#form1'));
            });
            }else{
            checkedForm($('#form1'));   
                }
        return true;
        }
    
    function checkedForm($form) {
                    inputs=$form.find('input, textarea, select');
                    fields_required='';
                    for (r in inputs){
                        if(typeof(inputs[r])=='object'){
                            if(!$(inputs[r]).is(':hidden') && $(inputs[r]).attr('name')){
                                fields_required+=$(inputs[r]).attr('name')+'#';
                            }else{
                                if($(inputs[r]).is('select') && !$(inputs[r]).parent().is(':hidden')){
                                fields_required+=$(inputs[r]).attr('name')+'#';   
                                    }
                                }
                        }
                    }
                    $('input[name=fields_required]').val(fields_required);
                }
                   
    checkedForm($('#form1'));
    
    if ($('input[name=rendicion_id]').length){
        var rendicion_id=parseInt($('input[name=rendicion_id]').val());
        openerp.jsonRpc('/rendicion/busca_respuestas', 'call', {'id':rendicion_id}).then(function (respuesta) {
            set_conduct(respuesta);
        }).fail(function (source, error) {
                   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                            '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                            '<strong class="text-danger">Debug</strong>'+
                                            '<p>'+error.data.debug+'</p>');
                    $('#AJAXErrorModal').modal('show');
                });
        }
        
    function set_conduct(respuestas){
        ms=respuestas.preguntas_ms
        p_culminacion=respuestas.preguntas_culminacion
        for (i in ms){
            element=$('input[name^='+ms[i].pregunta_id+'-'+ms[i].tipo_pregunta+'][value="'+ms[i].respuesta+'"]');
            div=$('div[id="'+ms[i].pregunta_id+'"]');
            div.addClass("hidden");
            element.prop("checked", true);
            element.change();
            }
        for (pc in p_culminacion){
            if (p_culminacion[pc].tipo_pregunta == 'select'){
                element=$('select[name^='+p_culminacion[pc].pregunta_id+'-'+p_culminacion[pc].tipo_pregunta+']');
                element.selectpicker('val',p_culminacion[pc].respuesta);
                element.change();
                }
            if (p_culminacion[pc].tipo_pregunta == 'text' || p_culminacion[pc].tipo_pregunta == 'numerico' || p_culminacion[pc].tipo_pregunta == 'rif' || p_culminacion[pc].tipo_pregunta == 'date'){
                element=$('input[name^='+p_culminacion[pc].pregunta_id+'-'+p_culminacion[pc].tipo_pregunta+']');
                element.val(p_culminacion[pc].respuesta);
                }
            if (p_culminacion[pc].tipo_pregunta == 'radio' || p_culminacion[pc].tipo_pregunta == 'checkbox'){
                element=$('input[name^='+p_culminacion[pc].pregunta_id+'-'+p_culminacion[pc].tipo_pregunta+'][value="'+p_culminacion[pc].respuesta+'"]');
                element.prop("checked", true);
                element.change();
                }
            if (p_culminacion[pc].tipo_pregunta == 'img'){
                element=$('input[name^='+p_culminacion[pc].pregunta_id+'-'+p_culminacion[pc].tipo_pregunta+']');
                files=p_culminacion[pc].files
                var preview = new Array
                var PreviewConfig = new Array
                inputs_file=''
                for (file in files){
                    preview.push("<img style='height:160px' src='data:"+files[file].type+
                                ";base64,"+files[file].datas+"' file_id='"+files[file].id+"'>");
                    PreviewConfig.push({caption: files[file].name, width: "120px", url: ""});
                    inputs_file+='<input type="hidden" value="data:'+files[file].type+
                                ';base64,'+files[file].datas+';file_id='+files[file].id+
                                '" file_id="'+files[file].id+'" file-name="'+files[file].name+
                                '" input-file-name="'+element.attr('name')+'" name="'+element.attr('name')+
                                '-'+file+'-'+files[file].name+'" />';
                    }
                element.fileinput('refresh',{
                    uploadUrl:' ',
                    showRemove:true,
                    uploadAsync:false,
                    showUpload:false,
                    showCaption: true,
                    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px">',
                    autoReplace: false,
                    overwriteInitial: false,
                    maxFileCount:parseInt(element.attr('maxfilecount')),
                    allowedFileExtensions: ["png", "jpg", "jpeg","pdf"],
                    initialPreview:preview,
                    initialPreviewConfig:PreviewConfig,
                    });
                element.after(inputs_file);
                }
            if (p_culminacion[pc].tipo_pregunta == 'file'){
                element=$('input[id*='+p_culminacion[pc].pregunta_id+'-'+p_culminacion[pc].tipo_pregunta+']');
                files=p_culminacion[pc].files
                var preview = new Array
                var PreviewConfig = new Array
                inputs_file=''
                for (file in files){
                    preview.push('<object class="file-object" data="data:'+files[file].type+
                                ';base64,'+files[file].datas+'" file_id="'+files[file].id+
                                '" type="application/pdf" width="160px" height="160px" internalinstanceid="3"></object>');
                    PreviewConfig.push({caption: files[file].name, width: "120px", url: ""});
                    inputs_file+='<input type="hidden" value="data:'+files[file].type+
                                ';base64,'+files[file].datas+';file_id='+files[file].id+
                                '" file_id="'+files[file].id+'" file-name="'+files[file].name+
                                '" input-file-name="'+element.attr('name')+'" name="'+element.attr('name')+
                                '-'+file+'-'+files[file].name+'" />';
                    }
                element.fileinput('refresh',{
                    uploadUrl:' ',
                    showRemove:true,
                    uploadAsync:false,
                    showUpload:false,
                    showCaption: true,
                    defaultPreviewContent: '<img src="/website_apiform/static/src/images/open_folder.png" alt="Formato png,jpg,jpeg,pdf" style="width:80px">',
                    autoReplace: false,
                    overwriteInitial: false,
                    maxFileCount:parseInt(element.attr('maxfilecount')),
                    allowedFileExtensions: ["pdf"],
                    initialPreview:preview,
                    initialPreviewConfig:PreviewConfig,
                    });
                element.after(inputs_file);
                }
            div=$('div#'+p_culminacion[pc].pregunta_id+'');
            $('input[name=edicion]').attr('value','True');
            //~ div.addClass('hidden');
            }
    }
    
    
    $('tr.desplegar_avance').on('click', function(){
        id=$(this).attr('ref');
        button=$(this);
        $('tbody[id='+id+']').toggle("swing",function(event){});
        
        });
                    
    
    
    
    
            $('a.question_description').live('click', function (event){
                var informacion=$(this).attr('ref-contenido');
                var titulo=$(this).attr('ref-titulo');
                html=$.parseHTML($('#'+informacion).html());
                if (!html){html=[{data:"Sin Descripción..."}];}
                $('.titulo').html('<strong class="text-info">'+$('#'+titulo+'').html()+'</strong>');
                $('.cuerpo').html(html[0].data);
                $('#AJAX_Modal').modal('show');
                
            });
            
            
            $('button#declarar').live('click', function (event){
                var informacion=$(this).attr('ref');
                //~ var titulo=$(this).attr('ref-titulo');
                var titulo='Declaración';
                html=$.parseHTML($('#'+informacion).html());
                nombre_responsable=$('input[name="nombre_responsable"]').attr('value');
                nombre_entidad=$('input[name="nombre_entidad"]').attr('value');
                tipo_entidad=$('input[name="tipo_entidad"]').attr('value');
                tipo_entidad=tipo_entidad.toLowerCase();
                if (html){
                    html[0].data=html[0].data.replace('[name]',nombre_responsable);
                    html[0].data=html[0].data.replace('[ci]','Cedula del alcalde');
                    html[0].data=html[0].data.replace('[entidad_name]',nombre_entidad);
                    html[0].data=html[0].data.replace('[tipo_entidad_name]',tipo_entidad);
                    }
                if (!html){html=[{data:"Sin texto..."}];}
                $('.titulo').html('<strong class="text-info">'+titulo+'</strong>');
                //~ $('.titulo').html('<strong class="text-info">'+$('#'+titulo+'').html()+'</strong>');
                $('.cuerpo').html(html[0].data);
                buttons=$('#AJAX_Modal div.modal-footer').find('button');
                if (buttons.length == 1){
                    buttons.after('<button type="button" id="declarar2" class="btn btn-primary glyphicon glyphicon-send" data-dismiss="modal">Declarar</button>')
                    }
                $('#AJAX_Modal').modal('show');
                
            });
           
            $('button#declarar2').live('click', function (event){
                $(this).remove();
                setTimeout(function(){
                var titulo='Advertencia';
                var cuerpo='<strong>¿Esta seguro(a) que desea realizar la rendición de cuentas para este proyecto?'+
                            'Recuerde la información suministrada en este formulario debe ser fidedigna y una vez '+
                            'que realice la rendición no podrá editar la misma.<strong>';
                $('.r_titulo').html('<strong class="text-info">'+titulo+'</strong>');
                $('.r_cuerpo').html(cuerpo);
                $('#AJAX_Modal_rendicion').modal('show');
            }, 500);
            });
            
            
                
                
                
                
                
            
            
            $('button#id_enviar_rendicion_jpv').live('click', function (event){
                $('#form1').find('input[name=declarar_culminacion]').attr('value','True')
                $('button#id_guardar_rendicion_jpv').click();
                
                
            });
            
    $('.agregarFilaMeta').live('click', function (event){
            var ref=$(this).attr('ref');
            body = $('#'+ref);
            var tr = $('tr:last', body);
            var trid = tr.attr('id')
            tr_id=trid.split("_")
            cont=parseInt(tr_id[1])+1
            new_id=tr_id[0]+'_'+cont
            var new_tr=tr.clone(true)
            new_tr.attr('id',new_id)
            $(new_tr).find('input:text,input[type=number],select').each(function(){
                            var name=$(this).attr('name');
                            name=name.split("_")
                            name.pop()
                            name=name.join("_")
                            $(this).attr('name',name+'_'+cont);
                            $(this).attr('id',name+'_'+cont);
                            if (name.split("-")[3]=="accion"){
                                $(this).val('0');
                            }else{
                                $(this).val('');
                                }
            });
            //~ $('input[name*='']')
            $(new_tr).find('button:button').each(function(){
                             name=name.split("_")
                             $(this).attr('ref',new_id);
            });
            $(new_tr).appendTo(body)
        });
        
        $('.adquisicion').on('change', function(){
        tr=$(this).parent().parent()
        tr.find('input:text,input[type=number],select').each(function(){
                            var name=$(this).attr('name');
                            if (name.split("-")[3]=="accion"){
                                if ($(this).val() !== '0'){
                                    $(this).attr('value','1');
                                }
                            }
            });
        });
        
        $(".eliminarFilaMeta").live('click', function (){
            var ref_body=$(this).attr('ref_body');
            var n=$('#'+ref_body+' tr').length
            if (n > 1){
                var tr=$(this).closest('tr');
                tam=tr.find('input:text,input[type=number],select').length
                tr.find('input:text,input[type=number],select').each(function(i){
                            var name=$(this).attr('name');
                            if (name.split("-")[3]=="accion"){
                                name_accion=name;
                                accion=$(this).val();
                            }
                            if (name.split("-")[3]=="id"){
                                name_id=name;
                                id=$(this).val();
                            }
                            if (i==tam-1){
                                crear_tr_hidden(tr,name_accion,accion,name_id,id);
                                tr.remove();
                                }
                });
                
            }
        });
        
            
            
        function crear_tr_hidden(tr,name_accion,accion,name_id,id){
            if (accion !== "0"){
                tr.after('<tr class="hidden"><td><input name="'+name_accion+'" value="2"></td><td><input name="'+name_id+'" value="'+id+'"></td></tr>');
                }
            }
            
            
        
        $("#id_guardar_rendicion_jpv").click( function() {
             var apiform_panel=$(this).apiform_panel()
             var form=$(this).attr('form');
             var gif=$('#img-'+form);
             var context=apiform_panel.context('#form1');
             if (context.campovacios=='no'){
                  var panramentros={'gif':gif,'boton':this};
                  if ($('input[name=declarar_culminacion]').attr('value') == 'False' && $('input[name="culminacion"]').attr('value')=='True'){
                        alert('¡Operacion Realizada!\n Datos Actualizados Correctamente\n Recuerde que la rendición de cuenta no estará completa hasta que no haga la declaración');
                  }
                 apiform_panel.ajax.enviar(context.destino,context.datos,panramentros);
             }
            
             });    
             
     openerp.jsonRpc("/proyecto/fecha", 'call', {
            
            }).then(function(res){
                fecha=res.split('-')
                dia=fecha[2]
                mes=fecha[1]
                anio=fecha[0]
                var fecha_actual = String(dia+"-"+mes+"-"+anio);
                
                fecha_actual = new Date(anio,mes-1,dia);

                
                
                $( "#6-date" ).change(function() {
                    fecha_inicio=$('#6-date').val();
                    fecha_i=fecha_inicio.split('-')
                    fecha_ini=new Date(fecha_i[2], fecha_i[1] - 1, fecha_i[0]);
                    if (fecha_i[2] < 2000)
                        {
                        cuerpo='El año ingresado es invalido'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Aviso!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#6-date').datepicker("setDate",'');
                        }
                    if(fecha_ini > fecha_actual){
                        cuerpo='La fecha de inicio no puede ser mayor a la fecha de hoy'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Aviso!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#6-date').datepicker("setDate",'');
                        }
                });

                $( "#24-date" ).change(function() {
                    fecha_culminacion=$('#24-date').val();
                    fecha_c=fecha_culminacion.split('-')
                    fecha_cul=new Date(fecha_c[2], fecha_c[1] - 1, fecha_c[0]);
                    if($('input[name=fecha_inicio_proyecto]').length){
                        fecha_inicio=$('input[name=fecha_inicio_proyecto]').attr('value')
                    }else{
                        fecha_inicio=$('#6-date').val();
                    }
                    fecha_i=fecha_inicio.split('-')
                    fecha_ini=new Date(fecha_i[2], fecha_i[1] - 1, fecha_i[0]);
                    if (fecha_cul < fecha_ini)
                        {
                        cuerpo='La fecha de culminacion no puede ser menor a la fecha de inicio'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Aviso!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#24-date').datepicker("setDate",'');
                        }

                });
        });
            
      console.debug('fin archivo js');  
      
    });
    
