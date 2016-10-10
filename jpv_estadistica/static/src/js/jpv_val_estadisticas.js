$(document).ready(function () {
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
var cant_proyecto_diferidos=0;
//~ inicio de grafica general
periodo_id=$("#jpvgraficaGeneralVal").attr('periodo_id');
estado_id=$("#estado_select").val();
if (!estado_id){
    estado_id='0'
    }
if($("#jpvgraficaGeneralVal").length){
        var datos_general={
                'opcion':'general',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'jpv_Estadistica_Periodo_general',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#jpvgraficaGeneralVal").jpv_estadisticas(datos_general);
        
        
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
    if($("#jpvGraficaDiferidos").length){
        var datos_proyectosDiferidos={
                'opcion':'pryectosDiferidos',
                'periodo_id':periodo_id,
                'ciclo_id':'0',
                'div':'jpvGraficaDiferidos',
                'estado_id':estado_id,
                'entidad_id':'0'}
        $("#periodo_sector_inversion").jpv_estadisticas(datos_proyectosDiferidos);
        
        }
    
console.debug("[estadistica val] Custom JS for estadistica valoración is loading...");
});
