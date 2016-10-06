# -*- coding: utf-8 -*-

import json
import logging
import base64
import csv, operator
from cStringIO import StringIO

import os
import zipfile
from shutil import rmtree
from datetime import date


import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from openerp.addons.web.controllers import main


_logger = logging.getLogger(__name__)

class jpv_cartas_x_firmar(http.Controller):

    
    def _ejecutar_obj_metodo_rastro(self,cr,uid,carta_data,context=None):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        objeto_rastro=carta_data.objeto_ratro_principal
        metodo_rastro=carta_data.metodoGenerarCartas
        try:
            objeto_ratro_obj=registry.get(objeto_rastro)
            metodo = getattr(objeto_ratro_obj,metodo_rastro)
        except AttributeError:
            _logger.warning('Error en el metodo: _distribucion_obj_metodo')
            _logger.warning('El objeto rastro: '+objeto_rastro+' Es Incorrecto... ')
            _logger.warning('Ó el método rastro: '+metodo_rastro+' Es Incorrecto... ')
            return {}
        else:
            return metodo(cr, uid,carta_data,context=context)
    
    
    @http.route(['/cartas_x_firmar/<model("jpv_val_validar_cartas_wizard"):wizard_data>'],
                type='http', auth='user', website=True)
    def descargar_caratas_valoraciones(self,wizard_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        cartas_x_firmar_obj = registry.get('jpv_fir.cartas_x_firmar')
        #~ if not os.path.isdir('/zip/cartas'):
            #~ os.mkdir('/zip/cartas')
        nombre_zip='%s_(%s).zip' % (str(date.today()),str(wizard_data.id))
        ruta_zip='/zip/'+nombre_zip
        if os.path.exists(ruta_zip):
            os.remove(ruta_zip)
        comp_zip = zipfile.ZipFile(ruta_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        for wizard in wizard_data:
            for carta in wizard.cartas_ids:
                carta_data=self._ejecutar_obj_metodo_rastro(cr,uid,carta,context=None)
                codigo=carta['correlativo']
                tipo=carta['tipo_cartas']
                cartas_x_firmar_id=carta['id']
                nombre_file='/zip/'+carta['nombre_file']+'%s#.pdf' % (cartas_x_firmar_id)
                if os.path.exists(nombre_file):
                        os.remove(nombre_file)
                file_tmp = open(nombre_file, "wb",buffering = 0)
                file_tmp.write('¿'+str(cartas_x_firmar_id)+'?\n')
                file_tmp.write(carta_data)
                comp_zip.write(nombre_file)
                file_tmp.close()
                os.remove(nombre_file)
        comp_zip.close()
        reomover_zip = open(ruta_zip, "r")
        data_zip=reomover_zip.read()
        reomover_zip.close()
        os.remove(ruta_zip)
        return request.make_response(data_zip,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_zip)),
                         ('Content-Type', 'application/zip;charset=utf8'),
                         ('Content-Length', len(data_zip))],
                cookies={'fileToken': '212123f4646546'})

        
        
        
       
