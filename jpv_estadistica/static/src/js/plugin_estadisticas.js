$(document).ready(function () {
    'use strict';
    console.debug("[Estadistica] Custom JS for plugin Estaditica is loading...");
    var jpv_estadisticas = jpv_estadisticas || {};
    var cant_proyecto_diferidos=0;
    jpv_estadisticas.graficas={
        //~ inicio de grafica general
        Tortageneral:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
                if (estado_id==''){
                    estado_id='0'
                    }
                if (entidad_id==''){
                        entidad_id='0'
                        }
                if (ciclo_id==''){
                        ciclo_id='0'
                        }
                var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
                openerp.jsonRpc('eptEstadisticasPeriodoGereral', 'call', datos).then(function (respuesta) {
                cant_proyecto_diferidos=respuesta.datos.diferidos;
                Morris.Donut({
                    element: div,
                    colors: ["#EBAA3C","#B61342" , "#4077A0", "#9BC036", "#290FE8","#58FAD0","#FFFF00"],
                    data: [
                        {label: "Proyectos Borrador", value: [respuesta.datos.cargados]},
                        {label: "Proyectos Aprobados", value: [respuesta.datos.aprobados]},
                        {label: "Proyectos Cancelados", value: [respuesta.datos.cancelados]},
                        {label: "Proyectos Diferidos", value: [respuesta.datos.diferidos]},
                        {label: "Proyectos Valoración", value: [respuesta.datos.evaluacion]},
                        {label: "Proyectos Negados", value: [respuesta.datos.negados]},
                        {label: "Proyectos Culminados", value: [respuesta.datos.culminados]},
                            
                        ],
                    responsive: true,
                    resize: true
                });
                var total=respuesta.datos.cargados+respuesta.datos.aprobados+respuesta.datos.cancelados+respuesta.datos.diferidos+respuesta.datos.negados+respuesta.datos.culminados
                $('#epttotal_general').html('<h4>Total de Proyectos '+total+'</h4>')
            }).fail(function (source, error) {
                       $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                                '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                                '<strong class="text-danger">Debug</strong>'+
                                                '<p>'+error.data.debug+'</p>');
                        $('#AJAXErrorModal').modal('show');
                    });
            
            },
        // ~ inicio de grafica rendiciones
        TortaRendiciones:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
                if (estado_id==''){
                    estado_id='0'
                    }
                if (entidad_id==''){
                        entidad_id='0'
                        }
                if (ciclo_id==''){
                        ciclo_id='0'
                        }
                var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
                openerp.jsonRpc('eptProyectosxRendirEstadistica', 'call', datos).then(function (respuesta) {
				Morris.Donut({
					element: div,
					colors: ["#9BC036","#B61342"],
					data: [
						{label: "Proyectos Actualizados", value: [respuesta.cant_proyectos_actualizados]},
						{label: "Proyectos Por Rendir", value: [respuesta.cant_proyectosXRendir]},
						],
					responsive: true,
					resize: true
				});
                var total=respuesta.cant_proyectos_actualizados+respuesta.cant_proyectosXRendir;
                $('#jpv_proyectos_rendiciones').html('<h4>Total de Proyectos Aprobados '+total+'</h4>')
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
            
            },
             //~ inicio de grafica sector de servicio
        TortaSectorServicio:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
            if (estado_id==''){
                    estado_id='0'
                    }
            if (entidad_id==''){
                    entidad_id='0'
                    }
            if (ciclo_id==''){
                        ciclo_id='0'
                        }
            var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
            openerp.jsonRpc('eptEstadisticasPeriodoSectorInves', 'call', datos).then(function (respuesta) {
                var datos=[];
                $.each(respuesta,function(index,valor){
                    datos.push({label:valor.name,value:valor.total})
                    });
				Morris.Donut({
					element: 'periodo_sector_inversion',
					colors: ["#EBAA3C","#B61342"],
					data: datos,
					responsive: true,
					resize: true
				});
                
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
            
            },
        //~ inicio de barra de proyecto diferidos
        BarraProyectosDiferidos:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
            if (estado_id==''){
                    estado_id='0'
                    }
            if (entidad_id==''){
                    entidad_id='0'
                    }
            if (ciclo_id==''){
                        ciclo_id='0'
                        }
            var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id}
            openerp.jsonRpc('eptEstadisticasDiferidos', 'call',datos).then(function (respuesta) {
                if (respuesta.cantidad>0){
                var total=0
                 var options = {
                chart: {
                    renderTo: div,
                    type: 'column',
                    marginRight: 200,
                    marginBottom: 45
                },
                title: {
                    text: 'Proyectos Diferidos ',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Total '+respuesta.cantidad,
                    x: -20
                },
                xAxis: {
                    categories: []
                },
                yAxis: {
                    title: {
                        text: 'Proyectos Diferidos'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#5C5C61'
                    }]
                },
                tooltip: {
                    formatter: function() {
                            return '<b>'+ this.series.name +'</b><br/>'+
                            this.x +': '+ this.y;
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: 10,
                    y: 20,
                    borderWidth: 1
                },
                series: []
            }

            options.xAxis.categories = ['Diferidos'];
            
                $.each(respuesta['datos'],function(index,datos){
                    options.series.push({'data':[datos.count],
                                               'name':datos.mensaje})
                        
                        }); 
                 console.log(options)
                var chart = new Highcharts.Chart(options);
                
                        }
                    });
                
            },
        
        //~ inicio de proyecto en valoracion torta
        TortaProyectosEnValoracion:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
            if (estado_id==''){
                    estado_id='0'
                    }
            if (entidad_id==''){
                        entidad_id='0'
                        }
            if (ciclo_id==''){
                        ciclo_id='0'
                        }
            var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id};
            openerp.jsonRpc('eptEstadisticasDictamenesProyectosValoracion', 'call', datos).then(function (respuesta) {
                var total=respuesta.porValorar+respuesta.aprobado+respuesta.diferido+respuesta.negado;
                if(total>0){
                cant_proyecto_diferidos=respuesta.diferido
				Morris.Donut({
					element: div,
					colors: ["#EBAA3C","#B61342" , "#4077A0", "#9BC036"],
					data: [
						{label: "Proyectos Por valorar", value: [respuesta.porValorar]},
						{label: "Proyectos Aprobados", value: [respuesta.aprobado]},
						{label: "Proyectos Diferidos", value: [respuesta.diferido]},
						{label: "Proyectos Negados", value: [respuesta.negado]},
							
						],
					responsive: true,
					resize: true
				});
                    }else{
                         $('#'+div).html('');
                        }
                
                $('#epttotal_proyectosValoracion').html('<h4>Total de Proyectos en Valoración '+total+'</h4>');
			}).fail(function (source, error) {
					   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
												'<p>'+error.data.name+': '+error.data.message+'</p>'+
												'<strong class="text-danger">Debug</strong>'+
												'<p>'+error.data.debug+'</p>');
						$('#AJAXErrorModal').modal('show');
					});
            },
        //~ inicio de la grafica de barra los motivos de los proyectos diferidos en la valoracion
        BarraMotivosProyDiferidosValoracion:function(div,periodo_id,ciclo_id,estado_id,entidad_id){
            if (estado_id==''){
                    estado_id='0'
                    }
            if (entidad_id==''){
                    entidad_id='0'
                    }
            if (ciclo_id==''){
                        ciclo_id='0'
                        }
            var datos={'periodo_id':periodo_id,'ciclo_id':ciclo_id,'estado_id':estado_id,'entidad_id':entidad_id};
            openerp.jsonRpc('eptEstadisticasValoracionDiferidos', 'call', datos).then(function (respuesta) {
                if(respuesta.cantidad>0){
                 var total=0
                 var options = {
                chart: {
                    renderTo: div,
                    type: 'column',
                    marginRight: 200,
                    marginBottom: 45
                },
                title: {
                    text: ' Proyectos en  Valoración y Diferidos',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Motivos',
                    x: -20
                },
                xAxis: {
                    categories: []
                },
                yAxis: {
                    title: {
                        text: 'Proyectos en Valoración Diferidos'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#5C5C61'
                    }]
                },
                tooltip: {
                    formatter: function() {
                            return '<b>'+ this.series.name +'</b><br/>'+
                            this.x +': '+ this.y;
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: 10,
                    y: 20,
                    borderWidth: 1
                },
                series: []
            }

            options.xAxis.categories = ['Diferidos'];
            
                $.each(respuesta['datos'],function(index,datos){
                        options.series.push({'data':[datos.count],
                                               'name':datos.mensaje})
                        
                        
                        }); 
                var chart = new Highcharts.Chart(options);
                        }else{
                            $('#'+div).html('');
                            }
                    });
            }
         };
    
               $.fn.jpv_estadisticas = function(datos){
                        var $this = $(this), data = $this.data('jpv_estadisticas');
                        switch(datos.opcion) {
                                case 'general':
                                    return jpv_estadisticas.graficas.Tortageneral(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                case 'sectorServicio':
                                    return jpv_estadisticas.graficas.TortaSectorServicio(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                case 'pryectosDiferidos':
                                    return jpv_estadisticas.graficas.BarraProyectosDiferidos(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                case 'pryectosRendiciones':
                                    return jpv_estadisticas.graficas.TortaRendiciones(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                case 'proyectosenvaloracion':
                                    return jpv_estadisticas.graficas.TortaProyectosEnValoracion(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                case 'barramotivosproydiferidosvaloracion':
                                    return jpv_estadisticas.graficas.BarraMotivosProyDiferidosValoracion(datos.div,datos.periodo_id,datos.ciclo_id,datos.estado_id,datos.entidad_id);
                                    break;
                                default:
                                    return jpv_estadisticas
                            }
        
                        };
                        
            
                
               
    console.debug("[Estadistica] Custom JS for plugin Estaditica is loading...");
});
