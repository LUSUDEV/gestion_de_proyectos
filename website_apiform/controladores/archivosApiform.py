# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.controllers import main
from openerp.http import request
import os

#~ Esta clase nos ayudara a todo lorelacionado con los archivos.

class apiform_archivos(http.Controller):
    
    @http.route('/apiform/enlace_descarga_user', auth='user', website=True)
    def descarga_enlace_user(self,modulo,carpeta,nombre_file):
        '''Este metodo nos ayudara a los enlace de descarga de archivos 
        que esten guardados en alguna carpeta de nuestro modulo
        los parametros son los siguientes:
        modulo=nombre del modulo
        carpeta=nombre de la carpeta que esta dentro del modulo donde
        esta el archivo a descargar.
        nombre_file= nombre del archivo a descagar con su extencion,
        Nota: Este metodo se utiliza solo para usuarios del sistema'''
        addons_path = http.addons_manifest[modulo]['addons_path']
        ruta_file=os.path.join(addons_path,modulo,carpeta,nombre_file)
        file = open(ruta_file, "r",buffering = 0)  
        data_file=file.read()
        file.close()  
        return request.make_response(data_file,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_file)),
                         ('Content-Type', 'application/pdf;charset=utf8'),
                         ('Content-Length', len(data_file))],
                cookies={'fileToken': '212123f4646546'})
    
    
    @http.route('/apiform/enlace_descarga_public', auth='public', website=True)
    def descarga_enlace_public(self,modulo,carpeta,nombre_file):
        '''Este metodo nos ayudara a los enlace de descarga de archivos 
        que esten guardados en alguna carpeta de nuestro modulo
        los parametros son los siguientes:
        modulo=nombre del modulo
        carpeta=nombre de la carpeta que esta dentro del modulo donde
        esta el archivo a descargar.
        nombre_file= nombre del archivo a descagar con su extencion,
        Nota: Este metodo es publico'''
        addons_path = http.addons_manifest[modulo]['addons_path']
        ruta_file=os.path.join(addons_path,modulo,carpeta,nombre_file)
        file = open(ruta_file, "r",buffering = 0)  
        data_file=file.read()
        file.close()  
        return request.make_response(data_file,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_file)),
                         ('Content-Type', 'application/pdf;charset=utf8'),
                         ('Content-Length', len(data_file))],
                cookies={'fileToken': '212123f4646546'})
