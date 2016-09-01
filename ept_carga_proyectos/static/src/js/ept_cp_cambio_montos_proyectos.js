$(document).ready(function () {
    
        $('.cambio_monto').live('click', function (event){
            var monto_disponible=$('p#monto_disponible').text()
            var monto_actual=$('#monto_proyecto').val()
            var monto_cambio=$('#monto_proyecto_cambio').val()
            
            var accion=$(this).attr('id');
            
            if (parseFloat(monto_cambio)!=0.00){
                 
                 monto_disponible=monto_disponible.split(',')
                entero_monto_disp=monto_disponible[0].split('.')
                decimal_monto_disp=monto_disponible[1]
                monto_disp=entero_monto_disp.join('')
                monto_disp=monto_disp+'.'+decimal_monto_disp
                
                monto_actual=monto_actual.split(',')
                entero_monto_act=monto_actual[0].split('.')
                decimal_monto_act=monto_actual[1]
                monto_actual=entero_monto_act.join('')
                monto_actual=monto_actual+'.'+decimal_monto_act
                
                monto_cambio=monto_cambio.split(',')
                entero_monto_camb=monto_cambio[0].split('.')
                decimal_monto_camb=monto_cambio[1]
                monto_camb=entero_monto_camb.join('')
                monto_cambio=monto_camb+'.'+decimal_monto_camb
                
                var monto_rendido=$('#monto_rendido').val()
                var monto_viejo=$('#monto_proyecto_2').val()
                
                monto_viejo=monto_viejo.split(',')
                entero_monto_viejo=monto_viejo[0].split('.')
                decimal_monto_viejo=monto_viejo[1]
                monto_viejo=entero_monto_viejo.join('')
                monto_viejo=monto_viejo+'.'+decimal_monto_viejo
                
                monto_rendido=monto_rendido.split(',')
                entero_monto_rendido=monto_rendido[0].split('.')
                decimal_monto_rendido=monto_rendido[1]
                monto_rendido=entero_monto_rendido.join('')
                monto_rendido=monto_rendido+'.'+decimal_monto_rendido
                
                
                if (accion=='aumento_monto'){
                    monto_nuevo=parseFloat(monto_actual)+parseFloat(monto_cambio)
                    }
                else{
                    if (accion=='restaurar_monto'){
                        $('#monto_proyecto_cambio').val('0.00')
                        monto_nuevo=monto_viejo
                    }else{
                        monto_nuevo=parseFloat(monto_actual)-parseFloat(monto_cambio)
                        }
                    }
                    
                
                if (accion=='aumento_monto'){
                
                    if(parseFloat(monto_disp)<parseFloat(monto_cambio)){
                        cuerpo='El monto que desea asignar a su proyecto no esta disponible en la cuenta asignada'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Error!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#monto_proyecto_cambio').val('0.00');
                    }
                    else{
                        
                        if (parseFloat(monto_nuevo)<0.00){
                        cuerpo='El monto debe ser mayor a 0.00'
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Error!</strong>')
                        $('#AJAX_Modal').modal('show');
                        $('#monto_proyecto_cambio').val('0.00');
                        $('#monto_proyecto_vista').val(monto_viejo);
                        
                        }else{
                        
                            if(parseFloat(monto_nuevo)<parseFloat(monto_rendido)){
                                cuerpo='El monto no debe estar por debajo del monto declarado'
                                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                                $('.titulo').html('<strong>Error!</strong>')
                                $('#AJAX_Modal').modal('show');
                                $('#monto_proyecto_cambio').val('0.00');
                                $('#monto_proyecto_vista').val(monto_viejo);
                            }else{
                                monto_nuevo=String(monto_nuevo).replace('.',',')
                                $('#monto_proyecto').val(monto_nuevo)
                                $('#monto_proyecto_vista').val(monto_nuevo)
                                }
                        }}
                    }else{
                        
                        
                        
                        
                        if(parseFloat(monto_nuevo)<parseFloat(monto_rendido)){
                                cuerpo='El monto no debe estar por debajo del monto declarado'
                                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                                $('.titulo').html('<strong>Error!</strong>')
                                $('#AJAX_Modal').modal('show');
                                $('#monto_proyecto_cambio').val('0.00');
                                $('#monto_proyecto_vista').val(monto_viejo);
                        }else{
                            monto_nuevo=String(monto_nuevo).replace('.',',')
                            $('#monto_proyecto').val(monto_nuevo)
                            $('#monto_proyecto_vista').val(monto_nuevo)
                            }
                        }
                 
                 }
            
            
            
                
            });
            
});
    
                
