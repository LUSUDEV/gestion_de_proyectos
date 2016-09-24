$(document).ready(function () {
                
                
       
       
       //~ mensajes de ayuda para el formulario de carga de proyecto
       
        function informacion_panel(ref){
            var titulo;
            var cuerpo;
           switch(ref) {
                //~ informacion para el panel de nombre y descripcion del proyecto
                  case 'nombre_descripcion':
                    titulo='Nombre y Descripción del Proyecto';
                    cuerpo='<p><strong>Nombre:</strong> es la denominación de la naturaleza del proyecto, debe ser clara, breve,'+
                    'precisa y valido durante toda su vida; respondiendo a un proceso, objeto y localización</p><br/>'+
                    '<strong>Proceso:</strong> como la acción que define la naturaleza de la inversión del proyecto<br/>'+
                    '<strong>Objeto:</strong> se define como materia o motivo del proceso.<br/>'+
                    '<strong>Localización:</strong> la ubicación precisa del proyecto, esta debe contener el nombre de la calle o sector, parroquia, municipio y estado.<br/>'+
                    '<p><strong>Descripción:</strong>corresponde a una descripción general que refleja en qué consiste el proyecto,'+
                    'destacando las características principales. Se deberá detallar las principales características'+
                    ' físicas o de servicios que correspondan al proceso involucrado en el nombre del proyecto</p>';
                    break;
                //~ informacion para el panel de tiempo de ejecución estimado
                  case 'tiempo_ejecucion':
                    titulo='Tiempo de Ejecución Estimado';
                    cuerpo='<p>Se refiere a la fecha de inicio y fin relacionado con la ejecución y culminación del proyecto<br/>'+
                            '<strong>Fecha de Inicio:</strong> la fecha más próxima a la ejecución del proyecto.<br/>'+
                            '<strong>Fecha de Fin:</strong> la fecha más temprana a la culminación del proyecto.</p>';
                    break;
                //~ informacion para el panel de monto del proyecto
                  case 'monto_proyecto':
                    titulo='Monto del proyecto';
                    cuerpo='Debe indicar el Valor Total en moneda nacional que será destinado para la ejecución del proyecto. ';
                    break;
                //~ informacion para el panel de clasificacion de inversión
                  case 'clasificacion':
                    titulo='Clasificación de Inversión'
                    cuerpo='<p>Está referida al sector de inversión, categoría y sub-categoría del proyecto (ver sistema de clasificación de inversión).</p>';
                    break;
                //~ informacion para el panel de proyecto de mantenimiento
                  case 'proyecto_mantenimiento':
                    titulo='Proyecto de Mantenimiento'
                    cuerpo='<p><strong>Mantenimiento:</strong> es el conjunto de acciones continuas y permanentes dirigidas a prever'+
                            ' y asegurar el funcionamiento normal, la eficiencia y la buena presentación de las obras'+
                            ' civil, maquinarias, equipos y vehículos, que se relacionen a la prestación de un servicio'+
                            ' o a la conformación de un proyecto socioproductivo.</p>';
                    break;
                //~ informacion para el panel de caracteristicas generales
                 
                  case 'caracteristicas_generales':
                    titulo='Caracteristicas Generales'
                    cuerpo='<p> Está referida a los aspectos técnicos de obra civil, adquisición de maquinarias,'+
                            ' adquisición de materiales de consumo, adquisición de equipos, adquisición de vehículos,'+
                            ' mantenimiento y semovientes.<br/>'+
                            '<strong>Obra Civil:</strong> Plantea el desarrollo de infraestructuras en el marco de los Sectores de Inversión'+
                            ' (incluye: Construcción Inicial, Ampliación, Rehabilitación o Mejora).<br/>'+
                            '<strong>Construcción Inicial:</strong> acción que comprende la materialización de una obra civil o servicios'+
                            ' que no existe a la fecha; que tiene lugar desde el inicio de la ejecución del proyecto hasta'+
                            ' su puesta en servicio.<br/>'+
                            '<strong>Ampliación:</strong> acción que tiene por objeto aumentar la capacidad de la obra civil o servicio sin'+
                            ' modificación de lo existente.<br/>'+
                            '<strong>Rehabilitación o Mejora:</strong> acción que tiene como objeto el proceso de recuperación de infraestructuras'+
                            ' existentes y aumentar la calidad de una obra civil o un servicio existente.<br/>'+
                            '<strong>Semovientes:</strong> Se refiere a la unidad animal que será adquirida para el predio y el cual está destinado'+
                            '<strong>Cantidad estimada:</strong> son las dimensiones de los movimientos de tierra, estructuras, obras arquitectónicas,'+
                            ' instalaciones eléctricas, instalaciones sanitarias y especiales, obras de servicios y varios presentes en'+
                            ' una obra civil o servicio. <br/>'+
                            '<strong>Unidad de medición:</strong> Es la expresión que sirve de base y permite cuantificar la ejecución de una obra civil'+
                            ' o servicio, se mide comúnmente en  los sistemas legales de medición (metro, kilómetro, hectárea, entre otros).<br/>'+
                            '<strong>Adquisición de Maquinarias:</strong> Comprende la compra de bienes muebles de alto costo unitario y con duración mayor'+
                            ' de un año, destinados a la construcción, industria y sector agropecuario para el proceso de producción y'+
                            ' operatividad de bienes, servicios y son de carácter permanente.<br/><br/>'+
                            '<strong>Nota:</strong> en los ítems correspondientes a maquinaria, equipos, vehículos, materiales de consumo y mantenimiento,'+
                            ' se debe de indicar el Uso, el Tipo y la Cantidad como elementos constantes en este tipo de características'+
                            ' de proyectos. En este sentido se definen a continuación:<br/><br/>'+
                            '<strong>Uso:</strong> hace referencia a la acción y orientación en cuanto a la construcción agropecuaria, de industrias,'+
                            ' servicios básicos y conexos a las actividades productivas.<br/>'+
                            '<strong>Uso:</strong> hace referencia a la acción y orientación en cuanto a la construcción agropecuaria, de industrias,'+
                            ' servicios básicos y conexos a las actividades productivas.<br/>'+
                            '<strong>Tipo:</strong> hace referencia al activo real del dominio público destinado a la construcción, agrícola y pecuaria,'+
                            ' industrias, servicios básicos y conexos a las actividades productivas. <br/>'+
                            '<strong>Cantidad:</strong> Es aquel que se refiere al número de maquinaria(s), equipo(s), materiales de consumo,'+
                            ' servicio(s) y vehículo(s).<br/>'+
                            '<strong>Característica:</strong> es aquella cualidad que determina los tipos de vehículos según su capacidad y uso.<br/>'+
                            '<strong>Adquisición de Materiales de Consumo:</strong> son Artículos que tienen un período corto de uso y durabilidad,'+
                            ' generalmente no mayor de un año, por cuanto tienden a desaparecer al primer uso, muestran un rápido'+
                            ' desgaste o deterioro y experimentan una pérdida posterior, frecuente e inevitable.<br/><br/>'+
                            '<strong>Nota:</strong> los materiales de consumo están limitados a los siguientes usos y los tipos que de ello se deriven.'+
                            ' Los usos ha objeto de inversión son: Alimentos Pecuarios, Productos de Minas, Canteras, Yacimientos,'+
                            ' Cuero, Caucho, Cartón, Papel, Impresos, Químicos y sus derivados, Minerales No Metálicos, Minerales Metálicos'+
                            ' , Madera, Textiles, Vestuario y Útiles Diversos .<br/><br/>'+
                            ' <strong>Adquisición de Equipos:</strong> comprende el conjunto de implementos que se acoplan, pueden ser móviles o fijos'+
                            '  de alto costo unitario y con duración mayor de un año, destinados a la construcción, industria y sector'+
                            ' agropecuario para el proceso de producción y operatividad de bienes, servicios y son de carácter permanente.<br/>'+
                            '<strong>Adquisición de Vehículos:</strong> está referido a indicar la compra de vehículos. Dicha solicitud es única'+
                            ' y va relacionada a un proyecto específico de servicio o socioproductivo. <br/> </p>';
                    break;
                //~ informacion para el panel de beneficiarios del proyecto
                  case 'beneficiarios':
                    titulo='Beneficiarios del Proyecto'
                    cuerpo='<p><strong>Beneficiarios del Proyecto:</strong> esta referido a indicar en términos cuantitativos'+
                            ' de la Población objeto Masculina y Femenina que se va a beneficiar directamente del proyecto. </p>';
                    break;
                //~ informacion para el panel de empleo asociado
                  case 'empleo':
                    titulo='Empleo Asociado'
                    cuerpo='<p>Empleo Asociado al Proyecto: esta referido a indicar en términos cuantitativos'+
                            'la Población objeto Masculina y Femenina se va a beneficiar indirectamente del proyecto.</p>';
                    break;
                //~ informacion para el panel de politica territorial
                  case 'politica_territorial':
                    titulo='Política territorial'
                    cuerpo='se debe colocar el nombre del Estado, Municipio, Parroquia y Sector requeridos. ';
                    break;
                //~ informacion para el panel de geo espacial
                  case 'geo_espacial':
                    titulo='Geo-espacial'
                    cuerpo='<p>debe indicar en coordenadas  universal transversal de Mercator  (UTM) la coordenada'+
                            'Este y Norte, así como el Huso geográfico respectivo del estado o municipio.<br/>'+
                            'Nota: La Coordenada Norte siempre será mayor que la Coordenada Este, salvo en algunas'+
                            'excepciones de ubicaciones geográficas del Estado Amazonas, donde ocurre todo lo contrario.</p>';
                    break;
                //~ informacion para el panel de fotografía
                  case 'fotografia':
                    titulo='Fotografía'
                    cuerpo='Se refiere a colocar una foto que indique el lugar de ejecución del proyecto. ';
                    break;
                }
           
           return {'titulo':titulo,'cuerpo':cuerpo}
           }
       
       $(function(){
            $('#ayudas_informacion').live('click', function (event){
                var informacion=informacion_panel($(this).attr('ref'));
                $('.titulo').html('<strong class="text-info">'+informacion.titulo+'</strong>');
                $('.cuerpo').html(informacion.cuerpo);
                $('#AJAX_Modal').modal('show');
                
            });
        });
                
        
        
        
        
});




           
