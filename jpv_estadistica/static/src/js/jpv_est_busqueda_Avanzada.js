$(document).ready(function () {
console.debug("[estadistica val] Custom JS for estadistica Busqueda Avanzada is loading...");
//~ cuando seleciona el periodo
$("#periodo_select").change(function() {
    $('#ListaProyectoDiferidos').html('');
    $('#ListaProyectoValoracionDiferidos').html('');
    $("#estado_select").val('');
    $("#entidad_select").val('');
    //~ titulo de la grafica
    var periodo_name = $("#periodo_select option:selected").text()
    $("#titulo_estadisticas").html('<h1>Periodo Fiscal '+periodo_name+' </h1>');
    var periodo_id=$(this).val();
    //~ INICIO BUSCAR EL CICLO DEL PERIODO
    openerp.jsonRpc('eptEstadisticasBuscarCiclo', 'call', {'periodo_id':periodo_id}).then(function (respuesta) {
                var options='<option value="">Seleccione..</option>'
                $.each(respuesta.ciclos_data,function(index,ciclo){
                    options=options+'<option value='+ciclo.ciclo_id+'>'+ciclo.nombre+'</option>'
                    });
                $("#ciclo_select").html(options);
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
    // FIN DE LA BUSQUEDA DEL CICLO DEL PERIODO
    $(':input[type="hidden"][name="periodo_id"]').val(periodo_id);
    $(':input[type="hidden"][name="ciclo_id"]').val('');
    $(':input[type="hidden"][name="estado_id"]').val('');
    $(':input[type="hidden"][name="entidad_id"]').val('');
    estado_id=$("#estado_select").val();
    if (!estado_id){
        estado_id='0'
        }
     var datos_general={
                'opcion':'general',
                'periodo_id':periodo_id,
                'div':'jpv_Estadistica_Periodo_general',
                'estado_id':estado_id,
                'ciclo_id':'0',
                'entidad_id':'0'}
        $("#jpv_Estadistica_Periodo_general").html('');
        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_general);
    var datos_sectorInv={
                'opcion':'sectorServicio',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'periodo_sector_inversion',
                'estado_id':estado_id,
                'entidad_id':'0'}
    $("#periodo_sector_inversion").html('');
    $("#periodo_sector_inversion").jpv_estadisticas(datos_sectorInv);
    var datos_pryectosDiferidos={
                'opcion':'pryectosDiferidos',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'EptGraficaDiferidos',
                'estado_id':'0',
                'entidad_id':estado_id}
    $("#EptGraficaDiferidos").html('');
    $("#EptGraficaDiferidos").jpv_estadisticas(datos_pryectosDiferidos);
    var datos_proyectosenvaloracion={
                'opcion':'proyectosenvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'EptDictamenesProyectosValoracion',
                'estado_id':'0',
                'entidad_id':estado_id}
        $("#EptDictamenesProyectosValoracion").html('');
        $("#EptDictamenesProyectosValoracion").jpv_estadisticas(datos_proyectosenvaloracion);
    var datos_barramotivosproydiferidosvaloracion={
                'opcion':'barramotivosproydiferidosvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'eptEstadisticasValoracion',
                'estado_id':'0',
                'entidad_id':estado_id}
        $("#eptEstadisticasValoracion").html('');
        $("#eptEstadisticasValoracion").jpv_estadisticas(datos_barramotivosproydiferidosvaloracion);
});



//~ cuando seleciono ciclo
$("#ciclo_select").change(function(){
    $('#ListaProyectoDiferidos').html('');
    $('#ListaProyectoValoracionDiferidos').html('');
    $("#estado_select").val('');
    $("#entidad_select").val('');
    var periodo_name = $("#periodo_select option:selected").text()
    var ciclo_name = $("#ciclo_select option:selected").text()
    var ciclo_text=" "+ciclo_name
    $("#titulo_estadisticas").html('<h1>Periodo Fiscal '+periodo_name+ciclo_text+' </h1>');
    var periodo_id=$('#periodo_select').val();
    var ciclo_id=$(this).val();
    $(':input[type="hidden"][name="periodo_id"]').val(periodo_id);
    $(':input[type="hidden"][name="ciclo_id"]').val(ciclo_id);
    $(':input[type="hidden"][name="estado_id"]').val('');
    $(':input[type="hidden"][name="entidad_id"]').val('');
    estado_id=$("#estado_select").val();
    if (!estado_id){
        estado_id='0'
        }
     var datos_general={
                'opcion':'general',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'jpv_Estadistica_Periodo_general',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#jpv_Estadistica_Periodo_general").html('');
        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_general);
    var datos_sectorInv={
                'opcion':'sectorServicio',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'periodo_sector_inversion',
                'estado_id':estado_id,
                'entidad_id':'0'}
    $("#periodo_sector_inversion").html('');
    $("#periodo_sector_inversion").jpv_estadisticas(datos_sectorInv);
    var datos_pryectosDiferidos={
                'opcion':'pryectosDiferidos',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'EptGraficaDiferidos',
                'estado_id':'0',
                'entidad_id':'0'}
    $("#EptGraficaDiferidos").html('');
    $("#EptGraficaDiferidos").jpv_estadisticas(datos_pryectosDiferidos);
    var datos_proyectosenvaloracion={
                'opcion':'proyectosenvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'EptDictamenesProyectosValoracion',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#EptDictamenesProyectosValoracion").html('');
        $("#EptDictamenesProyectosValoracion").jpv_estadisticas(datos_proyectosenvaloracion);
    var datos_barramotivosproydiferidosvaloracion={
                'opcion':'barramotivosproydiferidosvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'eptEstadisticasValoracion',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#eptEstadisticasValoracion").html('');
        $("#eptEstadisticasValoracion").jpv_estadisticas(datos_barramotivosproydiferidosvaloracion);
    
    });
    
    
    
    
//~ cuando selecciona el estado

$("#estado_select").change(function() {
    $('#ListaProyectoDiferidos').html('');
    $('#ListaProyectoValoracionDiferidos').html('');
    var periodo_id=$("#periodo_select").val();
    var estado_id=$(this).val();
    var ciclo_id=$('#ciclo_select').val();
    $(':input[type="hidden"][name="periodo_id"]').val(periodo_id);
    $(':input[type="hidden"][name="estado_id"]').val(estado_id);
    $(':input[type="hidden"][name="ciclo_id"]').val(ciclo_id);
    $(':input[type="hidden"][name="entidad_id"]').val('');
    //~ buscar municipios
    openerp.jsonRpc('eptEstadisticasBuscarEntidad', 'call', {'estado_id':estado_id,'periodo_id':periodo_id,'ciclo_id':ciclo_id}).then(function (respuesta) {
                var options='<option value="">Seleccione..</option>'
                $.each(respuesta.entidad_data,function(index,causa){
                    options=options+'<option value='+causa.parent_id+'>'+causa.nombre+'</option>'
                    });
                $("#entidad_select").html(options);
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
        //~ titulo de la grafica
                    var periodo_name = $("#periodo_select option:selected").text();
                    var ciclo_name = $("#ciclo_select option:selected").text();
                    var estado_name = $("#estado_select option:selected").text();
                    $("#titulo_estadisticas").html('<h1>Periodo Fiscal: '+periodo_name+' '+ciclo_name+'</h1><h1>'+estado_name+'</h1>');
                    var estado_id=$(this).val();
                    var entidad_id=$('#entidad_select').val();
                     var datos_general={
                                'opcion':'general',
                                'periodo_id':periodo_id,
                                'ciclo_id':ciclo_id,
                                'div':'jpv_Estadistica_Periodo_general',
                                'estado_id':estado_id,
                                'entidad_id':entidad_id}
                        $("#jpv_Estadistica_Periodo_general").html('');
                        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_general);
                    var datos_sectorInv={
                                'opcion':'sectorServicio',
                                'periodo_id':periodo_id,
                                'ciclo_id':ciclo_id,
                                'div':'periodo_sector_inversion',
                                'estado_id':estado_id,
                                'entidad_id':entidad_id}
                    $("#periodo_sector_inversion").html('');
                    $("#periodo_sector_inversion").jpv_estadisticas(datos_sectorInv);
                    var datos_pryectosDiferidos={
                                'opcion':'pryectosDiferidos',
                                'periodo_id':periodo_id,
                                'ciclo_id':ciclo_id,
                                'div':'EptGraficaDiferidos',
                                'estado_id':estado_id,
                                'entidad_id':entidad_id}
                    $("#EptGraficaDiferidos").html('');
                    $("#EptGraficaDiferidos").jpv_estadisticas(datos_pryectosDiferidos);
                    var datos_proyectosenvaloracion={
                                'opcion':'proyectosenvaloracion',
                                'periodo_id':periodo_id,
                                'ciclo_id':ciclo_id,
                                'div':'EptDictamenesProyectosValoracion',
                                'estado_id':estado_id,
                                'entidad_id':entidad_id}
                        $("#EptDictamenesProyectosValoracion").html('');
                        $("#EptDictamenesProyectosValoracion").jpv_estadisticas(datos_proyectosenvaloracion);
                    var datos_barramotivosproydiferidosvaloracion={
                                'opcion':'barramotivosproydiferidosvaloracion',
                                'periodo_id':periodo_id,
                                'ciclo_id':ciclo_id,
                                'div':'eptEstadisticasValoracion',
                                'estado_id':estado_id,
                                'entidad_id':entidad_id}
                        $("#eptEstadisticasValoracion").html('');
                        $("#eptEstadisticasValoracion").jpv_estadisticas(datos_barramotivosproydiferidosvaloracion);
                
                //~ fin de llamar al plugin
});


//~ cuando se selecciona la entidad

$("#entidad_select").change(function() {
    $('#ListaProyectoDiferidos').html('');
    $('#ListaProyectoValoracionDiferidos').html('');
        //~ titulo de la grafica
    var periodo_name = $("#periodo_select option:selected").text();
    var ciclo_name = $("#ciclo_select option:selected").text();
    var estado_name = $("#estado_select option:selected").text();
    var entidad_name = $("#entidad_select option:selected").text();
    $("#titulo_estadisticas").html('<h1>Periodo Fiscal: '+periodo_name+' '+ciclo_name+'</h1><h1>'+estado_name+'</h1><h1>'+entidad_name+'</h1>');
    var periodo_id=$("#periodo_select").val();
    var estado_id=$("#estado_select").val();
    var ciclo_id=$('#ciclo_select').val();
    var entidad_id=$(this).val();
    $(':input[type="hidden"][name="periodo_id"]').val(periodo_id);
    $(':input[type="hidden"][name="ciclo_id"]').val(ciclo_id);
    $(':input[type="hidden"][name="estado_id"]').val(estado_id);
    $(':input[type="hidden"][name="entidad_id"]').val(entidad_id);
    //~ inicio de llama plugin
     var datos_general={
                'opcion':'general',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'jpv_Estadistica_Periodo_general',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
        $("#jpv_Estadistica_Periodo_general").html('');
        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_general);
     var datos_rendicion={
                'opcion':'pryectosRendiciones',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'EptProyectosRendiciones',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
        console.log(estado_id);        
        if (!entidad_id == ''){
        $("#EptProyectosRendiciones").html('');
        $("#ListaProyectosxrendir").html('');
        $(".rowRendiciones").removeClass('hidden');
        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_rendicion);
    }else{
        $(".rowRendiciones").addClass('hidden');
    }       
    var datos_sectorInv={
                'opcion':'sectorServicio',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'periodo_sector_inversion',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
    $("#periodo_sector_inversion").html('');
    $("#periodo_sector_inversion").jpv_estadisticas(datos_sectorInv);
    var datos_pryectosDiferidos={
                'opcion':'pryectosDiferidos',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'EptGraficaDiferidos',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
    $("#EptGraficaDiferidos").html('');
    $("#EptGraficaDiferidos").jpv_estadisticas(datos_pryectosDiferidos);
    var datos_proyectosenvaloracion={
                'opcion':'proyectosenvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'EptDictamenesProyectosValoracion',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
        $("#EptDictamenesProyectosValoracion").html('');
        $("#EptDictamenesProyectosValoracion").jpv_estadisticas(datos_proyectosenvaloracion);
    var datos_barramotivosproydiferidosvaloracion={
                'opcion':'barramotivosproydiferidosvaloracion',
                'periodo_id':periodo_id,
                'ciclo_id':ciclo_id,
                'div':'eptEstadisticasValoracion',
                'estado_id':estado_id,
                'entidad_id':entidad_id}
        $("#eptEstadisticasValoracion").html('');
        $("#eptEstadisticasValoracion").jpv_estadisticas(datos_barramotivosproydiferidosvaloracion);

                //~ fin de llamar al plugin
});

console.debug("[estadistica val] Custom JS for estadistica Busqueda Avanzada is loading...");
});
