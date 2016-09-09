  
$(document).ready(function() {
	if($("#container3").length){
		openerp.jsonRpc('/proyecto/consulta/grafica', 'call', {}).then(function (respuesta) {
    Highcharts.setOptions({
        colors: ['#66bb6a', '#d32f2f']
    });
	var options = {
        chart: {
            renderTo: 'container3',
            type: 'column',
        },

        title: {
            text: 'Proyección de Avances ',
            x: -20 //center
        },
        subtitle: {
            text: '2015-2016',
            x: -20
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            title: {
                text: 'Proyeccion Avances'
            },
            plotLines: [{
                value: 0,
                width: 1,

            }]
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    this.x +': % '+ this.y;
            }
        },
   
        plotOptions: {
                series: {
                    colorByPoint: false,
                
                }
            },
        
        series: []
    }

    options.xAxis.categories = ['Avance'];
    	options.series[0] = respuesta.cant_total_financiero;
    	options.series[1] = respuesta.cant_total_fisico;

        chart = new Highcharts.Chart(options);

    
});
}
console.debug('fin de archivo js grafic_3 index');
});
