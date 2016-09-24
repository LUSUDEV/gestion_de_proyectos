$(document).ready(function () {

    
    
    
    
    openerp.jsonRpc("/proyecto/fecha", 'call', {
            
            }).then(function(res){
                fecha=res.split('-')
                dia=fecha[2]
                mes=fecha[1]
                anio=fecha[0]
                var fecha_actual = String(dia+"-"+mes+"-"+anio);
                
                fecha_actual = new Date(anio,mes-1,dia);
                
                $('#fecha_inicio').datepicker({dateFormat:"dd-mm-yy"});
                $('#fecha_fin').datepicker({dateFormat:"dd-mm-yy"});
                
                $( "#fecha_inicio" ).change(function() {
                    fecha_inicio=$('#fecha_inicio').val();
                    fecha_i=fecha_inicio.split('-')
                    fecha_ini=new Date(fecha_i[2], fecha_i[1] - 1, fecha_i[0]);
                    anio_inicio=fecha_ini.getFullYear()
                    $('#duracion_proyec').val('');
                    $('#duracion_proyecto').text('');
                    $('#fecha_fin').datepicker("setDate",'');
                    
                    console.log(fecha_ini);
                    console.log(fecha_actual);
                    if(fecha_ini < fecha_actual){
                        cuerpo='La fecha de inicio debe ser mayor a la fecha de hoy'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Aviso!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#fecha_inicio').datepicker("setDate",'');
                        }
                    if(parseInt(anio) != parseInt(anio_inicio)){
                        cuerpo='La fecha de inicio del proyecto debe estar comprendida dentro del año fiscal '+anio
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Aviso!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#fecha_inicio').datepicker("setDate",'');
                        }
                }); 
                
                
                
                
                
                
        });
    
    
    
    
    $( "#fecha_fin" ).change(function() {
        fecha_inicio=$('#fecha_inicio').val();
        fecha_fin=$('#fecha_fin').val();
        fecha_i=fecha_inicio.split('-');
        fecha_ini=new Date(fecha_i[2], fecha_i[1] - 1, fecha_i[0]);
        fecha_f=fecha_fin.split('-')
        fecha_fi=new Date(fecha_f[2], fecha_f[1] - 1, fecha_f[0]);
        anio_fin=fecha_fi.getFullYear()
        if (fecha_ini=='Invalid Date'){
            cuerpo='Debe seleccionar la fecha de inicio del proyecto'
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            $('#fecha_fin').datepicker("setDate",'');
            $('#duracion_proyec').val('');
            $('#duracion_proyecto').text('');
        }
        if(fecha_ini>fecha_fi){
            cuerpo='La fecha de fin no debe ser menor a la fecha de inicio del proyecto'
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            $('#fecha_fin').datepicker("setDate",'');
            $('#duracion_proyec').val('');
            $('#duracion_proyecto').text('');
        }
        if(fecha_inicio==fecha_fin){
            cuerpo='La fecha de fin no debe ser igual a la fecha de inicio del proyecto'
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            $('#fecha_fin').datepicker("setDate",'');
            $('#duracion_proyec').val('');
            $('#duracion_proyecto').text('');
        }
        if(anio != anio_fin){
            cuerpo='La fecha final del proyecto debe estar comprendida dentro del año fiscal '+anio
            $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
            $('.titulo').html('<strong>Aviso!</strong>')
            $('#AJAX_Modal').modal('show');
            $('#fecha_fin').datepicker("setDate",'');
            $('#duracion_proyec').val('');
            $('#duracion_proyecto').text('');
            }
        if ((fecha_ini!='Invalid Date') && (fecha_ini<fecha_fi) && (anio == anio_fin) && (fecha_inicio!=fecha_fin)){
            openerp.jsonRpc("/proyecto/duracionproyecto", 'call', {
            'fecha_inicio': fecha_ini,
            'fecha_fin':fecha_fi}).then(function(res){
               $('#duracion_proyec').val(res);
               $('#duracion_proyecto').text(res);
               });
        }
    });
});

