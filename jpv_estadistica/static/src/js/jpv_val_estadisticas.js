$(document).ready(function () {
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
var cant_proyecto_diferidos=0;
//~ inicio de grafica general
periodo_id=$("#EptgraficaGeneralVal").attr('periodo_id');
estado_id=$("#estado_select").val();
if (!estado_id){
    estado_id='0'
    }
if($("#EptgraficaGeneralVal").length){
        var datos_general={
                'opcion':'general',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'jpv_Estadistica_Periodo_general',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#EptgraficaGeneralVal").jpv_estadisticas(datos_general);
        
        
    }
    //~ Grafica de torta del sector de inversion
if($("#periodo_sector_inversion").length){
        var datos_sectorServicio={
                'opcion':'sectorServicio',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'periodo_sector_inversion',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#periodo_sector_inversion").jpv_estadisticas(datos_sectorServicio);
    }
    //~ inicio de grafica Diferido
    if($("#EptGraficaDiferidos").length){
        var datos_proyectosDiferidos={
                'opcion':'pryectosDiferidos',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'EptGraficaDiferidos',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#periodo_sector_inversion").jpv_estadisticas(datos_proyectosDiferidos);
        
        }
    
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
});
