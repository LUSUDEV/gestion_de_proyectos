$(document).ready(function () {
    'use strict';
    console.debug("[valorar] Custom JS for valoración is loading...");
    //~ * hay que probar ya que el rrequerimiento inicial fue con puros campos tipo
    //~ radios
    $(".js_val_show").click( function( event ) {
            var proyecto_id=$(this).attr('proyecto_id')
            var tr_id=$(this).attr('tr_id')
            $('.'+tr_id).toggle("swing");
             });

    $.each($('.js_ubicarPregValoracion'),function(index,campo){
            var ref=$(this).attr('ref');
            var tr_id=$(this).attr('tr_id');
            var pregunta_id=$(this).attr('pregunta_id');
            ref=String(ref)
            if ($("."+ref).length>0){
                    var divDestino=$("#"+ref)
                    if(divDestino.attr('mostrar')=='si'){
                        $("."+ref).prependTo("#"+ref);
                        mostrar_preguntas(ref);
                    }else{
                         $(this).html('<p>Este atributo Esta condicionado\
                                ejemplo: Si requiere Aval\
                                <input type="hidden" name="ing-pregunt_'+pregunta_id+'"\
                                 value='+pregunta_id+' /></p>')

                            
                        }
                }
        })
        
    $('.js_respuestaClick').click(function(event) {
            var depen=$(this).attr('depen');
            var tr_id=$(this).attr('tr');
            var id=$(this).attr('id');
            var type=$(this).attr('type');
            $(this).siblings(tr_id);
            if (depen){
            depen=depen.split(' ');
            $.each(depen,function(index,dependencia){
                    dependencia=dependencia.split(' ');
                    dependencia=dependencia[0].split('#');
                    var pregunta=$('#pregunta'+dependencia[0]);
                    if(dependencia[1]=='abre'){
                        pregunta.show();
                        required_campos_v(pregunta);
                        limpiar_campos_v(pregunta);
                        }
                    if(dependencia[1]=='cierra'){
                        hidenCampos_depenCierrar(pregunta)
                        pregunta.hide()
                        Norequired_campos_v(pregunta)
                        }
                });
                }
            //~ dictamen_valoracion(this);
        });

    function limpiar_campos_v(pregunta){
        $(pregunta).find('input:text, textarea').each(function(){
                                        $(this).val('');
                                        });
        $(pregunta).find('input:radio, input:checkbox').each(function(){
                        $(this).removeAttr('checked');
                        $(this).removeAttr('selected');
                        });
        }
        
    function hidenCampos_depenCierrar(pregunta){
        $(pregunta).find('input:text, textarea').each(function(){
                        //~ * Probar 
                        var depen=$(this).attr('depen');
                        if (depen){
                            depen=depen.split(' ');
                         $.each(depen,function(index,dependencia){
                                dependencia=dependencia.split(' ');
                                dependencia=dependencia[0].split('#');
                                var pregunta=$('#pregunta'+dependencia[0]);
                                if(dependencia[1]=='cierra'){
                                    hidenCampos_depenCierrar(pregunta)
                                    pregunta.hide()
                                    Norequired_campos_v(pregunta)
                                    }
                                        });
                                    }
                                        });
        $(pregunta).find('input:radio, input:checkbox').each(function(){
                        var depen=$(this).attr('depen');
                         if (depen){
                            depen=depen.split(' ');
                         $.each(depen,function(index,dependencia){
                                dependencia=dependencia.split(' ');
                                dependencia=dependencia[0].split('#');
                                var pregunta=$('#pregunta'+dependencia[0]);
                                if(dependencia[1]=='cierra'){
                                    hidenCampos_depenCierrar(pregunta)
                                    pregunta.hide()
                                    Norequired_campos_v(pregunta)
                                    }
                                        });
                                    }
                        });
        }
        
        
    function required_campos_v(pregunta){
        $(pregunta).find('input:text, textarea').each(function(){
                            //~ * Probar 
                           $(this).prop('required','required');
                                        });
        $(pregunta).find('input:radio, input:checkbox').each(function(){
                        $(this).prop('required','required');
                        });
        }
        
    function Norequired_campos_v(pregunta){
        $(pregunta).find('input:text, textarea').each(function(){
                            //~ * Probar 
                            $(this).removeAttr('required');
                                        });
        $(pregunta).find('input:radio, input:checkbox').each(function(){
                        $(this).removeAttr('required');
                        });
        }

    function mostrar_preguntas(ref){
        $("."+ref).each(function(){
                        var mostrar=$(this).attr('mostrar');
                        if (mostrar=='Si'){
                            $(this).show();
                            }else{
                            Norequired_campos_v(this);
                                }
                    })
        }

   $(".js_arder_categorias").on("click", function(){
       console.log('asfsafksakfskañfksañl')
       console.log('asfsafksakfskañfksañl')
       console.log('asfsafksakfskañfksañl')
       console.log($("#js_jpv_order_categoria_val"))
  $("#js_jpv_order_categoria_val").sortTable("letter", {column: 4, reverse: false});
  });

    
    
    console.debug("[valorar] Custom JS for valoración loaded!");
});


