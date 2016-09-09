$(document).ready(function () {
    
    
    function solicitud_cambio($form) {
		
		
		//~ solicitud=$(this).find('#solicitud');
		var solicitud = $('#solicitud');
        if (solicitud.is(':checked')) {
			var codigo=$('p#codigo_proyecto').text()
            var id_proyecto = $('#id_proyecto').val();
            openerp.jsonRpc("/proyecto/solicitud_cambio", 'call', {
            'id_proyecto': id_proyecto}).then(function(res){
                
        
                
                cuerpo='<div class="panel panel-success">'
				cuerpo+='<div class="panel-heading"><b><p class="text-center">Solicitud de cambio del proyecto: '+codigo+' </p></div>'
				cuerpo+='<div class="panel-body">'
				cuerpo+='<input type="text" class="hidden" id="solicitud_id" name="solicitud_id" value="'+res[0]+'"/>'
				cuerpo+='Usted ha realizado una solicitud de cambio en los siguientes campos:<br/>'
				cuerpo+='</div>'
				cuerpo+='</div>'
				
				
				for(i in res ){
					if(res[i]['tipo_campo']=='char'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="sector">'+res[i]["char_viejo"]+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="sector">'+res[i]["char_nuevo"]+'</p>'
                        cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='integer'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['integer_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['integer_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='float'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['float_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['float_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='text'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['text_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['text_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='datetime'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['datetime_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['datetime_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='estado_id'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['estado_id_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['estado_id_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='municipio_id'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['municipio_id_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['municipio_id_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='parroquia_id'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['parroquia_id_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['parroquia_id_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='huso_id'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['huso_id_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['huso_id_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
					if(res[i]['tipo_campo']=='husof_id'){
						cuerpo+='<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">'+res[i]["campo"]+'</h3></div><div class="panel-body">'
						cuerpo+='<label for="">Contenido Actual</label><p name="">'+res[i]['husof_id_viejo']+'</p>'
						cuerpo+='<label for="">Contenido Nuevo</label><p name="">'+res[i]['husof_id_nuevo']+'</p>'
						cuerpo+='</div></div>'
						}
                }
				
				
				
		
				$('.cuerpo').html(cuerpo);
				$('.titulo').html('<strong class="text-success">Solicitud de cambio.</strong>');
				$('.piemodal').html(' <button type="button" id="rechazar_solicitud" class="btn btn-danger"><b>Rechazar</b></button> <button type="button" id="aceptar_solicitud" class="btn btn-primary"><b>Aceptar</b></button>');
				$('#Modal_sin_botton').modal('show');
                
                
                
                
            });
            
            
      
            }
		
		
    }

    solicitud_cambio($('ept_carga_proyectos.proyecto_vista_solo_lectura'));   
    
    
   
    
    $('#aceptar_solicitud').live('click', function () {
		solicitud_id=$("#solicitud_id").val()
		openerp.jsonRpc("/proyecto/aceptar/solicitud_cambio", 'call', {
			'solicitud': solicitud_id,}).then(function(res){
				if (res==true){
				   location.reload();
				   }
			});
     
     
		$('#Modal_sin_botton').modal('hide');
            });
            
    $('#rechazar_solicitud').live('click', function () {
		solicitud_id=$("#solicitud_id").val()
		openerp.jsonRpc("/proyecto/rechazar/solicitud_cambio", 'call', {
			'solicitud': solicitud_id,}).then(function(res){
				if (res==true){
				   location.reload();
				   }
			});
     
		$('#Modal_sin_botton').modal('hide');
            });
});
