$(document).ready(function () {
        $.each( $.find('#tr_ept_scroll_ancho'),function(){
            var tr_ept_mov_ancho=$(this)[0].children;
            var cantidad=tr_ept_mov_ancho.length
            $.each($('.js_tr_ept_scroll_ancho_edit'),function(){
                if ($(this).context.children.length==cantidad){
                    for (i = 0; i < cantidad; i++) { 
                            var ancho=$(tr_ept_mov_ancho[i]).width();
                            $($(this).context.children[i]).width(ancho);
                        }
                    }else{
                        console.log('Error usted debe tener la misma cantidad de th\
                            en la cabecera y la misma cantidad de td en el cuerpo');
                        
                        }
                    
                    });
            });
            
    });
