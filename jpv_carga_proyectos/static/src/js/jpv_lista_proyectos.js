$(document).ready(function () {
  console.debug("[jpv_lista_proyectos] Custom JS for jpv_rendicion is loading...");
  var $ = window.jQuery 
  var deferred=$.Deferred();
  var lista_proyectos;

	if ($('#proyectos_completos').length){
    datos={'page_limit':30,
            'num':0,
            'fin':0,
            'cantidad_proyectos':0,
            'domain':$('#domain').val(),
            'lista_proyectos_ids':[]}             
    } 

	var lista_proyecto = function(datos){
    $('#proyectos_completos').html('<tr id="Cargando">'+
                        '<td colspan="5" align="center" >'+
                        '<img src="/web/static/src/img/throbber-large.gif"/>'+
                        '<br/>Cargando Proyectos...'+
                        '</td></tr>');
    
    openerp.jsonRpc('/jpv_mostrar_proyectos', 'call', datos).then(function (respuesta) {
    	proyectos_data=respuesta.carga_proyecto_data;
      lista_proyectos=proyectos_data
    	proyectos_ids=respuesta.proyectos_ids;
    	cantidad_proyectos=respuesta.proyectos_ids.length;
      datos.cantidad_proyectos=cantidad_proyectos;
    	fin=respuesta.page_limit;
      datos.fin=fin;
      datos.lista_proyectos_ids=proyectos_ids;
      parametros([{'metodo':'armar_botones_proyectos',
                   'parametros':{'proyectos_data':proyectos_data,
                                'proyectos_ids':proyectos_ids,
                                'cantidad_proyectos':cantidad_proyectos,
                                'num':datos.num,
                                'fin':fin
                    }}],function(respuesta){
        if(proyectos_data.length<cantidad_proyectos){
        respuesta.armar_botones_proyectos=respuesta.armar_botones_proyectos+'<tr id="jpvProyectosTrMas" class="jpvProyectosTrMas">'
                    +'<td colspan="5" align="center" >'
                    +'<button type="button" id="verMasProyectos" class="btn btn-primary verMasProyectos">Ver Más</button>'
                    +'</br>'+datos.fin+' de '+datos.cantidad_proyectos+' Proyectos </td>'+
                  '</tr>';
        }
        datos.num=datos.fin;
        $('#Cargando').remove();
        $('#proyectos_completos').html(respuesta.armar_botones_proyectos);

      });
      }).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
    }
    

	var parametros= function(datos,callback){
		var respuesta;
		openerp.jsonRpc('self', 'call', {'datos':datos}).then(function (respuesta) {
			respuesta = respuesta;
      callback(respuesta);
    	});
	};
  if ($('#proyectos_completos').length){
         lista_proyecto(datos);
    } 
 
  

  function peticionjpvVerMas(datos){
    openerp.jsonRpc('jpvProyectosVerMas', 'call', datos).then(function (respuesta) {
        var fin=respuesta.fin
        datos.fin=fin;
        parametros([{'metodo':'armar_botones_proyectos',
                   'parametros':{'proyectos_data':respuesta.proyectos_data,
                                'proyectos_ids':datos.lista_proyectos_ids,
                                'cantidad_proyectos':datos.cantidad_proyectos,
                                'num':datos.num,
                                'fin':fin
                    }}],function(respuesta){
        var tr=respuesta.armar_botones_proyectos;
        if(datos.fin<datos.cantidad_proyectos){
        tr=tr+'<tr id="jpvProyectosTrMas" class="jpvProyectosTrMas">'
                    +'<td colspan="5" align="center" >'
                    +'<button type="button" id="verMasProyectos" class="btn btn-primary verMasProyectos">Ver Más</button>'
                    +'</br>'+datos.fin+' de '+datos.cantidad_proyectos+' Proyectos </td>'+
                  '</tr>';
        }
        // $('#proyectos_completos').html(respuesta.armar_botones_proyectos);
        datos.num=datos.fin;
        $('#jpvProyectosTrMas').remove();
        $('#proyectos_completos').append(tr);
      });
        }).fail(function (source, error) {
             $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                        '<p>'+error.data.name+': '+error.data.message+'</p>'+
                        '<strong class="text-danger">Debug</strong>'+
                        '<p>'+error.data.debug+'</p>');
            $('#AJAXErrorModal').modal('show');
          });
    }

  function peticionjpvVerRendir(datos){
    openerp.jsonRpc('jpvProyectosVerRendir', 'call', datos).then(function (respuesta) {
        var fin=respuesta.fin
        parametros([{'metodo':'armar_botones_proyectos',
                   'parametros':{'proyectos_data':respuesta.proyectos_data,
                                'proyectos_ids':datos.lista_proyectos_ids,
                                'cantidad_proyectos':datos.cantidad_proyectos,
                                'num':datos.num,
                                'fin':fin
                    }}],function(respuesta){
        var tr=respuesta.armar_botones_proyectos;
        if(datos.fin<datos.cantidad_proyectos){
        tr=tr+'<tr id="jpvProyectosTrMas" class="jpvProyectosTrMas">'
                    +'<td colspan="5" align="center" >'
                    +'<button type="button" id="verMasProyectos" class="btn btn-primary verMasProyectos">Ver Más</button>'
                    +'</br>'+datos.fin+' de '+datos.cantidad_proyectos+' Proyectos </td>'+
                  '</tr>';
        }
        // $('#proyectos_completos').html(respuesta.armar_botones_proyectos);
        datos.num=datos.fin;
        datos.fin=fin;
        $('#jpvProyectosTrMas').remove();
        $('#proyectos_completos').html(tr);
      });
        }).fail(function (source, error) {
             $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                        '<p>'+error.data.name+': '+error.data.message+'</p>'+
                        '<strong class="text-danger">Debug</strong>'+
                        '<p>'+error.data.debug+'</p>');
            $('#AJAXErrorModal').modal('show');
          });
    }

    $('#verMasProyectos').live('click',function(){
        var botton=$(this);
        var tr_id=botton.parent().parent().attr('id');
        var td=botton.parent();
        td.html('<img src="/web/static/src/img/throbber-large.gif"/>'
        +'<br/>Cargando más proyectos');
        peticionjpvVerMas(datos);
    });

    $('#proyectos_rendir').live('click',function(){
        datos.lista_proyectos_ids=proyectos_x_rendir;
        datos.num=0;
        datos.cantidad_proyectos=proyectos_x_rendir.length;
        datos.fin=datos.page_limit;
        $('#proyectos_completos').html('<tr id="Cargando">'+
                        '<td colspan="5" align="center" >'+
                        '<img src="/web/static/src/img/throbber-large.gif"/>'+
                        '<br/>Cargando Proyectos...'+
                        '</td></tr>');
        peticionjpvVerRendir(datos);      
      });

 console.debug("[jpv_lista_proyectos] Custom JS for jpv_rendicion is loaded.");   
});
