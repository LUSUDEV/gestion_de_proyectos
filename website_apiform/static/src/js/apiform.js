$(document).ready(function() {

        var input_files = $('input[widget=apiform_image]');
        if (input_files.length>0){
            input_files.each(function(){
                $(this).hide();
               var cargaImagen= new openerp.website.cargaImagen();
               cargaImagen.start(this);
                });
         
        }


});
