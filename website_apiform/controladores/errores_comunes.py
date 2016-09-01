# -*- coding: utf-8 -*-

from openerp import http
from openerp.addons.website_apiform.controladores import panel

class erroes_help(http.Controller):
    #~ errores comunes de declaraciones
    
    #~ este metodo devuelve un modal informando que 
    #~ no colocó la dirección del action
    @http.route(
                ['/empty_action'],
                type='json', auth='public', website=True)
    def empty_action(self,**post):
        ret = {'modal':{
                            'titulo':'<strong>Error de programación.</strong>',
                            'cuerpo':'''<h5 >
                                        El parametro <b class="text-danger">"action"</b> es obligatorio
                                        y no lo colocó en el diccionario del 
                                        metodo panel_crear(parametros).
                                        Entre los parametro que lleva por
                                        defecto son los
                                        siguientes:</br></br>
                                        %s.</h5>''' % (panel.parametros_crear),
                            }
                }
        return ret
