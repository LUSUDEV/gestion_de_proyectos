$(document).ready(function () {
    'use strict';
    console.debug("[export_csv] Custom JS for users is loading...");
    var instance = openerp;
    openerp.web.data_export = {}; 
     $('a.exportar_csv').live('click',function(e) {
         if($('td.oe_list_field_char').length){
             var tr=$('td.oe_list_field_char').parent();
             var partner_ids=[];
             tr.each(function(index){
                partner_ids.push($(this).attr("data-id"));
            });
             openerp.session.get_file({ 
                url: '/asignacion_recursos/exportar',
                data: {partner_ids:partner_ids},
                complete: instance.web.unblockUI,
                 });
             
             $('button.cerrar').click();
         }
         else{
            alert('No hay Entidades o Instituciones seleccionadas');
         }
                
             
             
         });
        
         console.debug("[export_csv] Custom JS for users loaded!");
    });
