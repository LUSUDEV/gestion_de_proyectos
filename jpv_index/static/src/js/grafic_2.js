	
	window.onload = function(){
	
	var randon;
	var respuesta=function(){
		if($("#container2").length){
			openerp.jsonRpc('/proyecto/consulta/grafica', 'call', {}).then(function (respuesta) {
				randon=respuesta;
				Morris.Donut({
					element: 'morris-donut-chart',
					colors: ["#B61342", "#EBAA3C", "#4077A0", "#9BC036"],
					data: [
						{label: "Proyectos Sin Iniciar", 	value: [randon.cant_proy_sin_iniciar]},
						{label: "Proyectos Paralizados", 	value: [randon.cant_proy_paralizado]},			
						{label: "Proyectos Culminado", 		value: [randon.cant_proy_culminado_r]},
						{label: "Proyectos En Ejecucion", 	value: [randon.cant_proy_ejecucion]},
							
						],
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
                
       }
   }
    var json_response=respuesta();
    console.debug('fin de archivo js grafic_2 index');
}

	
