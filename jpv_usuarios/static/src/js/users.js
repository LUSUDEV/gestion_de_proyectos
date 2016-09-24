$(document).ready(function () {
    'use strict';
    console.debug("[users] Custom JS for users is loading...");
    $(".js_eliminar_user").click( function( event ) {
            var iduser=$(this).attr('iduser');
            var v=$('#'+iduser).apiform_panel();
            var conte=v.context('#'+iduser);
            v.ajax.enviar(conte.destino,conte.datos)
             });
    
    console.debug("[users] Custom JS for users loaded!");
});


