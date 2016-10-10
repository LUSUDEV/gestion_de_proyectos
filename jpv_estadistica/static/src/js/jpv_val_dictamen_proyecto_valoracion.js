$(document).ready(function () {
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
var cant_proyecto_diferidos=0;
//~ inicio de grafica general
var periodo_id=$("#jpvgraficaGeneralVal").attr('periodo_id');

if($("#jpvDictamenesProyectosValoracion").length){
        
        var datos_proyectosenvaloracion={
                'opcion':'proyectosenvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'jpvDictamenesProyectosValoracion',
                'estado_id':'0',
                'entidad_id':'0'}
        $("#jpvDictamenesProyectosValoracion").jpv_estadisticas(datos_proyectosenvaloracion);
        
        
    }

//~ mostrar y oculata tabla de las causas
$('#jpvMostarTablaCausasDiferidos').click(function(){
    $('#jpvTablaRefValoracion').toggle();
    
    });
//~ tabla de diferidos
if($("#jpvTablaRefValoracion").length){
        openerp.jsonRpc('jpvEstadisticasTablaValoracion', 'call', {'periodo_id':periodo_id}).then(function (respuesta) {
                cant_proyecto_diferidos=respuesta.diferido
				var tabla='<table class="table table-condensed">'+
                            '<thead>'+
                              '<tr>'+
                                '<th>Pregunta - Motivo</th>'+
                                '<th>Sub Motivo</th>'+
                              '</tr>'+
                            '</thead>'+
                            '<tbody>';
                var tr='';
                $.each(respuesta.diferido,function(index,causa){
                    tr=tr+'<tr>'+
                            '<td>'+index+'</td>';
                            var datos_subcausas=''
                            $.each(causa,function(index2,subcausa){
                                datos_subcausas=datos_subcausas+'</br>'+subcausa;
                                
                                });
                    tr=tr+'<td>'+datos_subcausas+'</td></tr>';
                    });
                tabla=tabla+tr+'</tbody>'+
                            '</table>';
                $('#jpvTablaRefValoracion').html(tabla);
                //~ var total=randon.datos.cargados+randon.datos.aprobados+randon.datos.cancelados+randon.datos.diferidos+randon.datos.negados
                //~ $('#jpvtotal_general').html('<h4>Total de Proyectos '+total+'</h4>')
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
        
        
    }
//~ inicio de grafica  de barra valoracion
    if($("#jpvEstadisticasValoracion").length){
        var datos_barramotivosproydiferidosvaloracion={
                'opcion':'barramotivosproydiferidosvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'jpvEstadisticasValoracion',
                'estado_id':'',
                'entidad_id':''}
        $("#jpvEstadisticasValoracion").jpv_estadisticas(datos_barramotivosproydiferidosvaloracion);
        
        }
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
});
