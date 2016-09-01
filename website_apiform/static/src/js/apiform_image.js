$(document).ready(function () {
   
    'use strict';
    console.debug("[apiform_file] Custom JS for apiform_panel is loading...");

    var cont=0;
    var website = openerp.website,
    qweb = openerp.qweb;
   
    website.add_template_file('/website_apiform/static/src/xml/apiform_imagen.xml');
    website.cargaImagen = openerp.Widget.extend({
        template: 'cargaImagen',
        base646:'lolol',
        placeholder: "/website_apiform/static/src/images/3d_user.png",
        MAIN_TEMPLATE : '<a><div class="ejemplo_img" >\n' +
        '<img\n' +
                'css="story-small"\n' +
                'src="defaults.src"\n' +
                'height="defaults.height"\n' +
                'width="defaults.width"\n' +
                'id="defaults.id" />\n' +
        '   <div class="ejemplo_img_cont" style="top: defaults.top ; height: _height;width:_width ">\n' +
        '       <div class="oe_form_field_image_controls oe_edit_only">\n' +
        '       <i class="fa fa-pencil fa-1g pull-left col-md-offset-1 oe_form_binary_file_edit" id="defaults.id_file" title="Edit" />\n' +
        '       <i class="fa fa-trash-o fa-1g col-md-offset-5 oe_form_binary_file_clear"  id="defaults.id" title="Clear" />\n' +
        '       </div>\n' +
        '   </div>\n' +
        '</div></a>',
        start: function (input_file) {
            if(input_file.placeholder){
                this.placeholder=input_file.placeholder;
                }
            var self = this;
            if( ! window.FileReader ) {
                console.log('no soporta')
                alert('ERROR Disculpe: Usted debe actualizar su navegado \
                        para que el sistema funcione....');
                    return; // No soportado
                }
                if(input_file.type=='file'){
                    var defaults = self.val_defaults(input_file);
                    var TEMPLATE;
                    try {
                        TEMPLATE=qweb.render("apiform_imagen", {'defaults': defaults});
                        
                        }catch(e){
                    TEMPLATE=self.MAIN_TEMPLATE.replace('defaults.src',defaults.src).
                            replace('defaults.height', defaults.height).
                            replace('_height', defaults.height).
                            replace('defaults.top', defaults.height).
                            replace('defaults.width', defaults.width).
                            replace('_width', defaults.width).
                            replace('defaults.id', defaults.id).
                            replace('defaults.namehidden', defaults.namehidden).
                            replace('defaults.id_file', defaults.id_file)
                        }
                    $(input_file).after(TEMPLATE);
                    self.settings = $.extend({}, defaults);
                    self.do_render(self,input_file);
                    $(input_file).hide();
                    }
            },
        do_render: function(self,input_file) {
            $(".ejemplo_img").mouseenter(function() {
            var height=$(this).children('img').attr('height');
            height=height.replace('px','');
            height=height.replace('%','');
            var _top=(54*parseInt(height))/100
            console.log(_top);
            $(".ejemplo_img_cont", this).stop().animate({ top:_top+'px' },{ queue:false, duration:300 });  
            });  
            $(".ejemplo_img").mouseleave(function() {
                  var height=$(this).children('img').attr('height');
                  var width=$(this).children('img').attr('width');
                $(".ejemplo_img_cont", this).stop().animate({ top:height },{ queue:false, duration:300 });  
            });
            $('.oe_form_binary_file_edit').click(function(e){
                  if(input_file.id==$(this).attr('id')){
                  $('#'+input_file.id).click();
                  $('#'+input_file.id).change(function() {
                      $('#id_enviar').hide();
                      self.readImage(this,self);
                      $('#id_enviar').show();
                  });
                  }
                 
                     });
            $('.oe_form_binary_file_clear').click(function(){
                 
                 var id=$(input_file).attr('name')
                 $('#'+id).attr( "src", self.placeholder);
                 $('#'+input_file.id).val('');
                 $('#'+input_file.id).attr("src",'');
                 console.log(input_file);
                 console.log(input_file);
                })
            
            },
        readImage: function(input) {
            var self=this;
            var return_base64;
            if ( input.files && input.files[0] ) {
                var FR= new FileReader();
               FR.onload = function(e) {
                    var id=input.name;
                    return_base64=e.target.result;
                    var base64=e.target.result;
                    var defaults=self.val_defaults(input)
                    base64=base64.split(',')
                    var width=defaults.width.replace('px','');
                    var height=defaults.height.replace('px','');
                    width=width.replace('%','');
                    height=height.replace('%','');
                    if(base64[0]=='data:application/pdf;base64'){
                        $('#'+id).attr( "src", '/website_apiform/static/src/images/pdf.png');
                            $(input).attr('src',return_base64);
                    }else{
                    if(!$(input).attr('transform-size')){
                        $('#'+id).attr( "src", return_base64 );
                        $(input).attr('src',return_base64);
                    }else{
                        openerp.jsonRpc("/website_apiform/apiform_image/base64_size", 'call', {
                        'image_base64': base64[1],
                        'width': width,
                        'height': height}).then(function(res){
                             $('#'+id).attr( "src", res[0].base64 );
                             $(input).attr('src',res[0].base64);
                            });
                    }
                    }
                   
                };
                console.log('input.files[0]')       
                        
                FR.readAsDataURL(input.files[0]);
                }
              
            },
        val_defaults:function(input){
            var height= $(input).attr('height');
            if (!height){
               height= '128px';
               $(input).attr({'height':height});
                } 
            var id_file= $(input).attr('id');
            if (!id_file){
               id_file= 'id_file'+cont;
                $(input).attr({'id':id_file});
                } 
            var width= $(input).attr('width');
            if (!width){
               width= '128px';
               $(input).attr({'width':width});
                } 
            var src= $(input).attr('src');
            if (!src){
               src= this.placeholder;
                }else{
                    src='data:image/png;base64,'+src
                    $(input).attr('src',src);
                    } 
            var id= $(input).attr('name');
            if (!id){
               id= 'idname'+cont;
               $(input).attr({'name':id});
                }
            var namehidden='hidden_'+id;
            
            
            return {'height':height,
                    'width':width,
                    'src':src,
                    'id':id,
                    'namehidden':namehidden,
                    'id_file':id_file
                    }
            },
        
        
        });
        
        
        
                 $('.js_file_apiform').on('fileloaded', function(evento, archivo, previewId, indice, lector){
                    var name =$(this).attr('name');
                    var input=this;
                    var file_name=archivo.name;
                    var preview_id=previewId
                    var type=archivo.type
                    var FR= new FileReader();
                    var file_size=parseInt(archivo.size)/1024;
                    FR.onload = function(e) {
                        if (type.split('/')[0] == 'image'){
                        if (file_size > 100){
                                $('.titulo').html('<strong>Error en carga de imagen<br></strong>');
                                $('.cuerpo').html('<strong class="text-danger">Disculpe la imagen debe tener un peso menor a 100kbs</strong>');
                                $('#AJAX_Modal').modal('show');
                                $(input).fileinput('clear');
                                return false
                            }
                            }
                        else{
                        if (file_size > 200){
                                $('.titulo').html('<strong>Error en carga de imagen<br></strong>');
                                $('.cuerpo').html('<strong class="text-danger">Disculpe el archivo debe tener un peso menor a 200kbs</strong>');
                                $('#AJAX_Modal').modal('show');
                                $(input).fileinput('clear');
                                return false
                            }
                            }
                            //~ openerp.jsonRpc("/website_apiform/apiform_image/base64_size", 'call', {
                            //~ 'image_base64': e.target.result.split(',')[1],
                            //~ 'width': 400,
                            //~ 'height': 400}).then(function(res){
                             //~ $(input).after('<input type="hidden" value="'+res[0].base64+';'+file_name+
                           //~ '" file-name="'+file_name+'" preview-id="'+preview_id+'" input-file-name="'+name+
                           //~ '" name="'+name+'-'+$('input[input-file-name="'+name+'"]').length+'-'+file_name+'" />');
                            //~ });
                        //~ }else{
                             $(input).after('<input type="hidden" value="'+e.target.result+';'+file_name+
                           '" file-name="'+file_name+'" preview-id="'+preview_id+'" input-file-name="'+name+
                           '" name="'+name+'-'+$('input[input-file-name="'+name+'"]').length+'-'+file_name+'" />');
                            //~ }
                           }
                    FR.readAsDataURL(archivo);
                    });
                 
                 $('.js_file_apiform_proyecto').on('fileloaded', function(evento, archivo, previewId, indice, lector){
                    var name =$(this).attr('name');
                    var input=this;
                    var file_name=archivo.name;
                    var preview_id=previewId
                    var type=archivo.type
                    var FR= new FileReader();
                    var file_size=parseInt(archivo.size)/1024;
                    FR.onload = function(e) {
                        if (type.split('/')[0] == 'image'){
                        if (file_size > 400){
                                $('.titulo').html('<strong>Error en carga de imagen<br></strong>');
                                $('.cuerpo').html('<strong class="text-danger">Disculpe la imagen debe tener un peso menor a 400kbs</strong>');
                                $('#AJAX_Modal').modal('show');
                                $(input).fileinput('clear');
                                return false
                            }
                            }
                        else{
                        if (file_size > 400){
                                $('.titulo').html('<strong>Error en carga de imagen<br></strong>');
                                $('.cuerpo').html('<strong class="text-danger">Disculpe el archivo debe tener un peso menor a 400kbs</strong>');
                                $('#AJAX_Modal').modal('show');
                                $(input).fileinput('clear');
                                return false
                            }
                            }
                            //~ openerp.jsonRpc("/website_apiform/apiform_image/base64_size", 'call', {
                            //~ 'image_base64': e.target.result.split(',')[1],
                            //~ 'width': 400,
                            //~ 'height': 400}).then(function(res){
                             //~ $(input).after('<input type="hidden" value="'+res[0].base64+';'+file_name+
                           //~ '" file-name="'+file_name+'" preview-id="'+preview_id+'" input-file-name="'+name+
                           //~ '" name="'+name+'-'+$('input[input-file-name="'+name+'"]').length+'-'+file_name+'" />');
                            //~ });
                        //~ }else{
                             $(input).after('<input type="hidden" value="'+e.target.result+';'+file_name+
                           '" file-name="'+file_name+'" preview-id="'+preview_id+'" input-file-name="'+name+
                           '" name="'+name+'-'+$('input[input-file-name="'+name+'"]').length+'-'+file_name+'" />');
                            //~ }
                           }
                    FR.readAsDataURL(archivo);
                    });
                    
                
                
                $('.js_file_apiform_proyecto').on('filecleared', function(event) {
                    $('input[input-file-name="'+this.name+'"]').remove();
                });
                
                $('.js_file_apiform').on('filecleared', function(event) {
                    $('input[input-file-name="'+this.name+'"]').remove();
                });
                
                $('.kv-file-remove').live('click', function(event) {
                    if($(this).parent().parent().parent().parent().find('object[file_id]').length){
                        var file_id=$(this).parent().parent().parent().parent().find('object[file_id]').attr('file_id');
                        $('input[file_id="'+file_id+'"]').remove();
                        $(this).parent().parent().parent().parent().remove();
                        }
                        else{ 
                            if ($(this).parent().parent().parent().parent().find('img[file_id]').length){
                                var file_id=$(this).parent().parent().parent().parent().find('img[file_id]').attr('file_id');
                                $('input[file_id="'+file_id+'"]').remove();
                                $(this).parent().parent().parent().parent().remove();
                                }
                            else{
                                $('input[preview-id="'+$(this).parent().parent().parent().parent()[0].id+'"]').remove();
                                }
                            }
                    
                    
                });


        console.debug("[apiform_file] Custom JS for apiform_panel is loading...");

});
