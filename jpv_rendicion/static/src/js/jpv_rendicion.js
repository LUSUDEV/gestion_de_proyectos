$(document).ready(function () {
        
        //~ if ($("input[name=tipo_de_ejecucion]").val){$("input[name=tipo_de_ejecucion]").val
            //~ }
    
    $('input[type="checkbox"].rendicion').on('switchChange.bootstrapSwitch', function(event, state) {
        console.log($("input[name=tipo_ejecucion]"));
        if($("input[name=tipo_ejecucion]").data()){
            tipo_ejecucion=$("input[name=tipo_ejecucion]").data().bootstrapSwitch.options.state;
            if(tipo_ejecucion){$("input[name=tipo_de_ejecucion]").val('Contratacion');}
            else{$("input[name=tipo_de_ejecucion]").val('Autogestion');}
        }
        else{
            if ($("input[name=tipo_de_ejecucion]").val()=='Contratacion'){tipo_ejecucion=true}else{tipo_ejecucion=false}
            }
        inicio_administrativo=$("input[name=inicio_administrativo]").data().bootstrapSwitch.options.state;
        if(inicio_administrativo){$("input[name=inicio_administrativo_t]").val('True');}
        else{$("input[name=inicio_administrativo_t]").val('False');}
        if(tipo_ejecucion && inicio_administrativo){
        $("div.etapa").removeClass('hidden');
        $('select[name="etapa_proyecto"]').change();
        }else{
            $("div.etapa").addClass('hidden');
            $("select[name=etapa_proyecto]").val('');
            $("div.otro").addClass('hidden');
            }
    });
    
    $('select[name="etapa_proyecto"]').on('change', function(event) {
        if(event.target.value == 'Otro'){
        $("div.otro").removeClass('hidden');
        }else{
            $("div.otro").addClass('hidden');
            }
    });
    
   
    
    
    
    
    });
