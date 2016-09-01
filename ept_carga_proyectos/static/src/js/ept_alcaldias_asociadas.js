$(document).ready(function () {
    
   
   
   
   
   //~ Funcion que retorna el valor con en la tabla el estatus esta Cancelado
    function llenarBotonAprobado(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"  ><span class="glyphicon glyphicon-pencil" /> Aprobado</button>'
        return retorno
        }
    function llenarBotonCancelado(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-hand-down"></span> Cancelado</button>'
        return retorno
        }
    //~ Funcion que retorna el valor con en la tabla el estatus esta diferido
    function llenarBotonDiferido(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-refresh"></span> Diferido</button>'
        return retorno
        }
    //~ Funcion que retorna el valor con en la tabla el estatus esta negado
    function llenarBotonNegado(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-remove-circle"></span> Negado</button>'
        return retorno
        }
    //~ Funcion que retorna el valor con en la tabla el estatus esta borrador o carga
    function llenarBotonCarga(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-list-alt"></span> Borrador</button>'
        return retorno
        }
    //~ Funcion que retorna el valor con en la tabla el estatus esta en evaluacion
    function llenarBotonEvaluacion(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-pencil"></span> Evaluación</button>'
        return retorno
        }
    //~ Funcion que retorna el valor con en la tabla el estatus esta en culminado
    function llenarBotonCulminado(){
        var retorno='<button type="button" class="btn btn-xs btn-default btn-block"><span class="glyphicon glyphicon-pencil"></span> Culminado</button>'
        return retorno
        }

    $(function(){
        $('#alcaldias_asociadas').live('click', function (event){
            var id_partner=$(this).val();
            
            $( ".proyectos" ).remove();
            openerp.jsonRpc("/proyecto/alcaldias_asociadas", 'call', {
                'id_partner': id_partner,}).then(function(res){
                    proyectos=res.length
                    tabla="<table class='table table-bordered table-striped mt32 proyectos'><thead><tr><th class='col-md-3'>Código de Proyecto</th><th class='col-md-5'>Nombre del Proyecto</th><th class='col-md-2'>Monto de Proyecto</th><th class='col-md-2'>Estatus</th></tr></thead><tbody>"
                    body=''
                    estatus=''
                    proyec_aux=0
                    if (proyectos>0){
                        while (proyec_aux<proyectos){
                            pro=res[proyec_aux]
                            cont=1
                            for (p in pro){
                                if (cont==1){
                                    switch (pro[3]) {
                                        case 'negado': 
                                        estatus=llenarBotonNegado();
                                            break;
                                        case 'carga': 
                                            estatus=llenarBotonCarga();
                                            break;
                                        case 'evaluacion': 
                                            estatus=llenarBotonEvaluacion();
                                            break;
                                        case 'diferido': 
                                            estatus=llenarBotonDiferido();
                                            break;
                                        case 'cancelado': 
                                            estatus=llenarBotonCancelado();
                                            break;
                                        case 'culminado': 
                                            estatus=llenarBotonCulminado();
                                            break;
                                        case 'aprobado': 
                                            estatus=llenarBotonCulminado();
                                            break;
                                        }
                                    body=body+"<tr><td><a href='/proyecto/lectura/"+pro[4]+"'>"+pro[0]+"</a></td><td >"+pro[1]+"</td><td >"+pro[2]+"</td><td >"+estatus+"</td></tr>"
                                }  
                                cont=cont+1  
                            }
                            proyec_aux=proyec_aux+1
                            }
                       final="</tbody></table>"
                       total=tabla+body+final
                       $( ".here_table" ).append(total);
                    }
                    else{
                        
                        $( ".here_table" ).append('<div id="proyecto_no" class="alert alert-info proyectos"><p>La Alcaldía seleccionada no posee proyectos aprobados.</p></div>');
                        }
                });
        });
    });
    
           
});


