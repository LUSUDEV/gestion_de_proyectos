
$(document).ready(function() {
	if($("#container1").length){
		openerp.jsonRpc('/proyecto/consulta/grafica', 'call', {}).then(function (respuesta) {
	Highcharts.setOptions({
        colors: ['#64b5f6', '#ffee58', '#66bb6a', '#b61342', '#0d47a1', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
    });
	var options = {
        chart: {
            renderTo: 'container1',
            type: 'column',
            marginRight: 130,
            marginBottom: 25
        },
        title: {
            text: ' Graficas de Proyectos',
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
                text: 'Proyección 2015-2016'
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
            x: -10,
            y: 50,
            borderWidth: 0
        },
        series: []
    }

    options.xAxis.categories = ['Proyectos'];
    	options.series[0] = respuesta.cant_proy_aprobados;
    	options.series[1] = respuesta.cant_proy_evaluacion;
    	options.series[2] = respuesta.cant_proy_culminado;
    	options.series[3] = respuesta.cant_proy_cancelado;
    	options.series[4] = respuesta.cant_proy_carga;

        chart = new Highcharts.Chart(options);
        
});
}
console.debug('fin de archivo js grafic_1 index');
});

