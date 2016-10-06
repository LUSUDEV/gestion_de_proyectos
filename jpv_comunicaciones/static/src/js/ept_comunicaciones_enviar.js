$(document).ready(function () {
console.debug("[enviar comunicaciones] Custom JS for comunicaciones is loading...");
$("#EptEnviarComunicaciones").click( function( event ) {
            var comuni=$('#comunicacionCont').val();
            if (comuni.length<3001){
                var gif=$('#img-form1');
                var apiform=$('#form1').apiform_panel();
                var formCont=apiform.context('#form1');
                if (formCont.campovacios=='no'){
                                $.ajax( {
                                  url: '/comunicaciones/enviar',
                                  type: 'http',
                                  data: new FormData($('#form1')[0]),
                                  processData: false,
                                  contentType: false,
                                  type : 'POST',
                                  dataType : 'json',
                                  beforeSend: function( xhr ) {
                                         $('#img-form1').show()
                                         $('#EptEnviarComunicaciones').hide()
                                      }
                                }).done(function(data) {
                                    $('#img-form1').hide()
                                    $('#EptEnviarComunicaciones').show()
                                    cuerpomodal='Comunicación Registrada con el código '+data['correlativo']
                                    $('#form1').find('select').each(function(){
                                        $(this).val('');
                                        });
                                    $('#form1').find('input:text, textarea').each(function(){
                                        $(this).val('');
                                        });
                                    $('.js_jpv_comunicaciones').fileinput('clear');
                                    $('.cuerpo').html('<strong >'+cuerpomodal+'<br></strong>');
                                    $('.titulo').html('<strong class="text-success">Comunicación Registrada</strong>');
                                     $('#AJAX_Modal').modal('show');
                                    });
                }
                }else{
                    var cuerpomodal='El número de caracteres ('+comuni.length+') de la comunición excede el maximo (3000) permitido.'
                    $('.cuerpo').html('<strong class="text-danger">'+cuerpomodal+'</strong>');
                    $('.titulo').html('<strong>Error en el Contenido de la Comunicación.</strong>');
                    $('#AJAX_Modal').modal('show');
                    }
             
             });




console.debug("[enviar comunicaciones] Custom JS for comunicaciones loaded!");
});
