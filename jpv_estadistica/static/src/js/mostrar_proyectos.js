$(document).ready(function () {
console.debug("[estadistica jpv] Custom JS for estadistica mostrar proyectos is loading...");
//~ muestras los proyectos diferidos con sus motivos 
$('#jpvMostarProyectosDiferidos').click(function(){
       var periodo_id=$('#periodo_select').val(); 
       var ciclo_id=$('#ciclo_select').val(); 
       var estado_id=$('#estado_select').val(); 
       var entidad_id=$('#entidad_select').val();
       if ($('#ListaProyectoDiferidos').find('table').length==0){
            console.log('sfkasfkasf444')
           var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
                openerp.jsonRpc('jpvMostarListaProyectosDiferidos', 'call', datos).then(function (respuesta) {
                    var tabla='<table class="table table-striped table-bordered">'+
                                    '<thead>'+
                                '<tr>'+
                            '<th>Correlativo</th>'+
                            '<th>Entidad</th>'+
                            '<th>Estado</th>'+
                            '<th>Motivo</th>'+
                            '<th>Monto</th>'+
                          '</tr>'+
                          '</thead>'+
                                '<tbody>';
                    var total=0;
                        $.each(respuesta,function(index,valor){
                            var pregunta_motivo='';
                                $.each(valor,function(index,motivo){
                                    pregunta_motivo=pregunta_motivo+' '+motivo.mensaje+'<br/>';
                                    });
                            tabla=tabla+'<tr>'+
                                '<td><a target="_blank" href="/web?debug=#id='+valor[0].proyecto_id+'&view_type=form&model=jpv_cp.carga_proyecto&menu_id=162&action=151">'+valor[0].correlativo+'</a></td>'+
                                '<td>'+valor[0].entidad+'</td>'+
                                '<td>'+valor[0].estado+'</td>'+
                                '<td>'+pregunta_motivo+'</td>'+
                                '<td>'+valor[0].monto_proyecto+'</td>'+
                                '</tr>';
                                total=total+parseFloat(valor[0].monto_proyecto);
                                });
                    tabla=tabla+'<tr align="right">'+
                            '<td colspan="4"><b>Total: </b></td>'+
                            '<td>'+total+'</td>'+
                            '</tr>';
                    tabla=tabla+'</tbody>'+
                        '</table>';
                
                $('#ListaProyectoDiferidos').html(tabla);
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
           
           
           }else{
               console.log('sfkasfkasf')
               $('#ListaProyectoDiferidos').toggle();
               } 
       
    });

//~ Muestras los proyectos en valoraciion y diferidos con sus motivos 
$('#jpvMostarProyectosEnValoracionDiferidos').click(function(){
        console.log('hola mundo');
       var periodo_id=$('#periodo_select').val();
       var ciclo_id=$('#ciclo_select').val(); 
       var estado_id=$('#estado_select').val(); 
       var entidad_id=$('#entidad_select').val();
       if ($('#ListaProyectoValoracionDiferidos').find('table').length==0){
           var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
                openerp.jsonRpc('jpvMostarListaProyectosValoracionDiferidos', 'call', datos).then(function (respuesta) {
                    var tabla='<table class="table table-striped table-bordered">'+
                                    '<thead>'+
                                '<tr>'+
                            '<th>Correlativo</th>'+
                            '<th>Entidad</th>'+
                            '<th>Estado</th>'+
                            '<th>Motivo</th>'+
                            '<th>Monto</th>'+
                          '</tr>'+
                          '</thead>'+
                                '<tbody>';
                    var total=0;
                        $.each(respuesta,function(index,valor){
                            var pregunta_motivo='';
                                $.each(valor,function(index,motivo){
                                    pregunta_motivo=pregunta_motivo+' '+motivo.mensaje+'<br/>';
                                    });
                            tabla=tabla+'<tr>'+
                                '<td><a target="_blank" href="/web?debug=#id='+valor[0].proyecto_id+'&view_type=form&model=jpv_cp.carga_proyecto&menu_id=162&action=151">'+valor[0].correlativo+'</a></td>'+
                                '<td>'+valor[0].entidad+'</td>'+
                                '<td>'+valor[0].estado+'</td>'+
                                '<td>'+pregunta_motivo+'</td>'+
                                '<td>'+valor[0].monto_proyecto+'</td>'+
                                '</tr>';
                                total=total+parseFloat(valor[0].monto_proyecto);
                                });
                    tabla=tabla+'<tr align="right">'+
                            '<td colspan="4"><b>Total: </b></td>'+
                            '<td>'+total+'</td>'+
                            '</tr>';
                    tabla=tabla+'</tbody>'+
                        '</table>';
                
                $('#ListaProyectoValoracionDiferidos').html(tabla);
      }).fail(function (source, error) {
             $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                        '<p>'+error.data.name+': '+error.data.message+'</p>'+
                        '<strong class="text-danger">Debug</strong>'+
                        '<p>'+error.data.debug+'</p>');
            $('#AJAXErrorModal').modal('show');
          });
           
           
           }else{
               
               $('#ListaProyectoValoracionDiferidos').toggle();
               } 
       
    });

//~ Muestras los proyectos x rendir 
$('#jpvMostarProyectosXRendir').click(function(){
      $('#ListaProyectosxrendir').html('<div class="col-md-12">'+
                        '<img src="/web/static/src/img/throbber-large.gif"/>'+
                        '<br/>Cargando Proyectos...'+
                        '</div>');
       var entidad_id=$('#entidad_select').val();
       if ($('#jpvMostarProyectosXRendir').find('table').length==0){
           var datos={'entidad_id':entidad_id}
                openerp.jsonRpc('jpvProyectosxRendirListaEstadistica', 'call', datos).then(function (respuesta) {
                    var tabla='<table class="table table-striped table-bordered">'+
                                    '<thead>'+
                                '<tr>'+
                            '<th>N#</th>'+
                            '<th class="col-md-3">Correlativo</th>'+
                            '<th class="col-md-6">Nombre</th>'+
                            '<th class="col-md-2">Monto</th>'+
                            '<th class="col-md-1">Estado</th>'+
                          '</tr>'+
                          '</thead>'+
                                '<tbody>';
                    var total=0;
                    $.each(respuesta,function(index,valor){
                            num=index+1;
                            tabla=tabla+'<tr>'+
                                '<td>'+num+'</td>'+
                                '<td class="col-md-3"><a target="_blank" href="/web?debug=#id='+valor.id+'&view_type=form&model=jpv_cp.carga_proyecto&menu_id=162&action=151">'+valor.correlativo+'</a></td>'+
                                '<td class="col-md-6">'+valor.nombre_proyecto+'</td>'+
                                '<td class="col-md-2">'+valor.monto_proyecto+'</td>'+
                                '<td class="col-md-1">'+valor.state+'</td>'+
                                '</tr>';
                          total=total+parseFloat(valor.monto_proyecto);
                          console.log('lkmkmkmkmkmk');
                         });
                    tabla=tabla+'</tbody>'+
                        '</table>';
                $('#ListaProyectosxrendir').html(tabla);
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
           
           
           }else{
               
               $('#ListaProyectosxrendir').toggle();
               } 
       
    });
console.debug("[estadistica jpv ] Custom JS for estadistica mostrar proyectos is loading...");
});
