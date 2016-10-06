# -*- coding: utf-8 -*-


from cStringIO import StringIO
import os
import zipfile
from shutil import rmtree
import base64
import logging

from openerp.osv import fields, osv
from openerp.addons.web.http import request
from openerp import http, SUPERUSER_ID
from openerp.addons.web.controllers import main


_logger = logging.getLogger(__name__)

class jpv_fir_carga_cartas_wizard(osv.TransientModel):
    """
        Este wizard es carga las cartas firmadas
    """
    _name = "jpv_fir_carga_cartas_wizard"
    _description = "Cargar las cartas firmadas"
    _order = 'id desc'

         
    _columns = {
        'resumen':fields.html("Rasumen de valoracion",
                                readonly=True,
                                store=False),
        'cartas_x_firmar_ids':fields.many2many('jpv_fir.cartas_x_firmar', 
                                          'jpv_fir_carga_carta_rel', 
                                          'carga_zip_id', 
                                          'cartas_x_firmar_id',
                                          'Cartas',
                                          ),
        'filedata': fields.binary('Archivo o Comprimido',filters='*.zip',required=True),
        'confimado':fields.boolean('Confirmado')
    }

    def validar_zip(self, cr, uid, ids, context=None):
        '''Metodo para validar el contenido de las cartas firmadas 
        .zip antes de cargar o enviar las cartas '''
        nombre_zip='/zip/cartas/validar_zip.zip'
        #~ variable de mensaje html
        resumen='<div class="alert alert-success">'\
                'Correcto el contenido del .zip </div>'
        #~ variables de error
        error_firmar=''
        error_file_corrupto=''
        titulo='Cargar'
        #~ si todo esta bien para que active botton
        confimado=True
        #~ ids de cartas por firmar
        cartas_x_firmar_ids=[]
        #~ creo una carpeta para que si hay error todo se almacene hay..
        if not os.path.isdir('/zip/cartas'):
            os.mkdir('/zip/cartas')
        #~ borro el ultimo validar_zip.zip
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        #~ abro un .zip puente
        zip_tmp = open(nombre_zip, "wb",buffering = 0)
        #~ busco la data del wizard cargado
        data= self.browse(cr,uid,ids,context=context)[0]
        filedata=data.filedata
        #~ decodifico en base64 para poder rescribir el .zip puente
        datazip=base64.b64decode(filedata)
        #~ rescribo el .zip puente
        zip_tmp.write(datazip)
        #~ verifico, desconprimo y recoorro el contenido del .zip
        if zipfile.is_zipfile(nombre_zip):
            unziped = zipfile.ZipFile(nombre_zip, 'r')
            if len(unziped.namelist())>0:
                for file_path in unziped.namelist():
                    fileSplit_=file_path.split('_')
                    if len(fileSplit_)==2:
                        file_content = unziped.read(file_path)
                        #~ busco el id del susudicho.....
                        index_inicial=posicion=file_path.find('o#')
                        index_final=file_path.find('#-')
                        index_inicial=index_inicial+2
                        cartaXfirmar_id=file_path[index_inicial:index_final]
                        #~ valido la fidelidad del archivo
                        if file_path.find(cartaXfirmar_id)==-1:
                            confimado=False
                            file_corrupta = base64.b64encode(file_content)
                            error_file_corrupto+='<div class="alert alert-warning">'\
                            ' '+file_path+'</div>'\
                            '<embed height="200px" width="100%" '\
                            ' src="data:application/pdf;base64,'+file_corrupta+'" />'\
                            '<br/><br/>'
                            resumen='<div class="alert alert-danger">'\
                            'ERROR: Alteración de Archivo.'\
                            '</div> <br/>'+error_file_corrupto
                            titulo='Validar'
                        
                        else:
                            cartas_x_firmar_ids.append(int(cartaXfirmar_id))
                    #~ si el archivo no esta firmado
                    if file_path.find('Firmado')==-1:
                        error_firmar+=file_path+' <br/>'
                        resumen='<div class="alert alert-danger">'\
                            'Error: Falta de Firma.'\
                            '<br/> '+error_firmar+'</div>'
                        confimado=False
                        filedata=''
                        titulo='Validar'
                        cartas_x_firmar_ids=[]
            else:
                resumen='<div class="alert alert-danger">'\
                    'Error: .zip Vacio....</div>'
                titulo='Validar'
                confimado=False
                filedata=''
        else:
            resumen='<div class="alert alert-danger">'\
                    'Error: Extención de archivo Incorrecto,'\
                    ' la extención correcta debe ser .zip</div>'
            titulo='Validar'
            confimado=False
            filedata=''
        zip_tmp.close()
        return {
            'name': (titulo+' Cartas'),
            'res_model': 'jpv_fir_carga_cartas_wizard',
            'type': 'ir.actions.act_window',    
            'view_mode':'form',
            'view_type': 'form',
            'target':'new',
            'context':{
                'default_resumen':resumen,
                'default_cartas_x_firmar_ids':cartas_x_firmar_ids,
                'default_filedata':filedata,
                'default_confimado':confimado}
        }
        
    def cargar_cartas(self, cr, uid, ids, context=None):
        '''Metodo para cargar el contenido de las cartas firmadas 
        .zip antes de cargar o enviar las cartas '''
        nombre_zip='/zip/cartas/validar_zip.zip'
        #~ variable de mensaje html
        resumen='<div class="alert alert-success">'\
                'Exito  Cartas Cargadas.</div>'
        #~ variables de error
        error_firmar=''
        error_file_corrupto=''
        titulo='Cargar'
        #~ si todo esta bien para que active botton
        confimado=False
        #~ ids de cartas por firmar
        cartas_x_firmar_ids=[]
        #~ creo una carpeta para que si hay error todo se almacene hay..
        if not os.path.isdir('/zip/cartas'):
            os.mkdir('/zip/cartas')
        #~ borro el ultimo validar_zip.zip
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        #~ abro un .zip puente
        zip_tmp = open(nombre_zip, "wb",buffering = 0)
        #~ busco la data del wizard cargado
        data= self.browse(cr,uid,ids,context=context)[0]
        filedata=data.filedata
        #~ decodifico en base64 para poder rescribir el .zip puente
        datazip=base64.b64decode(filedata)
        #~ rescribo el .zip puente
        zip_tmp.write(datazip)
        #~ verifico, desconprimo y recoorro el contenido del .zip
        if zipfile.is_zipfile(nombre_zip):
            unziped = zipfile.ZipFile(nombre_zip, 'r')
            for file_path in unziped.namelist():
                fileSplit_=file_path.split('_')
                if len(fileSplit_)==2:
                    file_content = unziped.read(file_path)
                    #~ busco el id del susudicho..... 
                    index_inicial=posicion=file_path.find('o#')
                    index_final=file_path.find('#-')
                    index_inicial=index_inicial+2
                    cartaXfirmar_id=file_path[index_inicial:index_final]
                    #~ valido la fidelidad del archivo
                    if file_path.find(cartaXfirmar_id)==-1:
                        confimado=False
                        file_corrupta = base64.b64encode(file_content)
                        error_file_corrupto+='<div class="alert alert-warning">'\
                        ' '+file_path+'</div>'\
                        '<embed height="200px" width="100%" '\
                        ' src="data:application/pdf;base64,'+file_corrupta+'" />'\
                        '<br/><br/>'
                        resumen='<div class="alert alert-danger">'\
                        'ERROR: Alteración de Archivo.'\
                        '</div> <br/>'+error_file_corrupto
                        titulo='Validar'
                    
                    else:
                        cartas_x_firmar_obj=self.pool.get('jpv_fir.cartas_x_firmar')
                        cartas_x_firmar_data=cartas_x_firmar_obj.browse(cr,uid,[int(cartaXfirmar_id)])[0]
                        for carta in cartas_x_firmar_data:
                                self._distribucion_obj_metodo(
                                                            cr,
                                                            SUPERUSER_ID,
                                                            carta,
                                                            file_path,
                                                            base64.encodestring(file_content)
                                                            
                                                            )
                            
                        cartas_x_firmar_ids.append(int(cartaXfirmar_id))
                        resumen='<div class="alert alert-success">'\
                                'Se han cargado con exito el Contenido'\
                                ' del .zp</div>'
                #~ si el archivo no esta firmado
                if file_path.find('Firmado')==-1:
                    error_firmar+=file_path+' <br/>'
                    resumen='<div class="alert alert-danger">'\
                        'Error: Falta de Firma.'\
                        '<br/> '+error_firmar+'</div>'
                    confimado=False
                    filedata=''
                    titulo='Validar'
        else:
            resumen='<div class="alert alert-danger">'\
                    'Error: Extención de archivo Incorrecto,'\
                    ' la extención correcta debe ser .zip</div>'
            titulo='Validar'
            confimado=False
            filedata=''
        zip_tmp.close()
        return {
            'name': (titulo+' Cartas'),
            'res_model': 'jpv_fir_carga_cartas_wizard',
            'type': 'ir.actions.act_window',    
            'view_mode':'form',
            'view_type': 'form',
            'target':'new',
            'context':{
                'default_resumen':resumen,
                'default_confimado':confimado}
        }
        
    def _distribucion_obj_metodo(self,cr,uid,carta_data,file_name,filedata,context=None):
        objeto_rastro=carta_data.objeto_ratro_principal
        metodo_rastro=carta_data.metodo
        try:
            objeto_ratro_obj=self.pool.get(objeto_rastro)
            metodo = getattr(objeto_ratro_obj,metodo_rastro)
        except AttributeError:
            _logger.warning('Error en el metodo: _distribucion_obj_metodo')
            _logger.warning('El objeto rastro: '+objeto_rastro+' Es Incorrecto... ')
            _logger.warning('Ó el método rastro: '+metodo_rastro+' Es Incorrecto... ')
            return {}
        else:
            return metodo(cr, uid,carta_data,file_name,filedata,context=context)
        
    def _dictamen_valoracion(self, cr, uid, context=None):
        proyecto_model = self.pool['jpv_cp.carga_proyecto']
        proyectos_ids=proyecto_model.search(
                                    cr,
                                    uid,
                                    [('state','=','evaluacion')])
        proyecto_data=proyecto_model.browse(cr,uid,proyectos_ids)
        aprobados=0
        negados=0
        diferidos=0
        sin_valorar=0
        solo_genaral=0
        solo_coordenadas=0
        for proyecto in proyecto_data:
            if proyecto.dictamen=='Aprobado':
                aprobados=aprobados+1
            if proyecto.dictamen=='Negado':
                negados=negados+1
            if proyecto.dictamen=='Diferido':
                diferidos=diferidos+1
            if proyecto.dictamen=='Sin valorar':
                sin_valorar=sin_valorar+1
            if proyecto.dictamen=='Solo General':
                solo_genaral=solo_genaral+1
            if proyecto.dictamen=='Solo Coordenadas':
                solo_coordenadas=solo_coordenadas+1   
        table='''<table class="table table-bordered table-striped mt32">
            <thead>
                <tr class="active">
                    <th colspan="7" >
                        <h4 align="center">
                            <b>Resumen de las Valoraciones</b>
                        </h4>
                    </th>
                </tr>
                <tr class="active">
                    <th>Aprobados</th>
                    <th>Diferidos</th>
                    <th>Negados</th>
                    <th>Sin Valorar</th>
                    <th>Solo General</th>
                    <th>Solo Coordenadas</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                 </tr>
            </tbody>
        </table>''' % (aprobados,
                        diferidos,
                        negados,
                        sin_valorar,
                        solo_genaral,
                        solo_coordenadas,
                        len(proyectos_ids))
        
        
        return table
        
    def _default_proyecto_ids(self, cr, uid, context=None):
        if context is None:
            context = {}
        proyecto_model = self.pool['jpv_cp.carga_proyecto']
        proyecto_ids = context.get('active_model') == 'jpv_cp.carga_proyecto' and context.get('active_ids') or []
        proyecto_data=proyecto_model.browse(cr,uid,proyecto_ids)
        for proyecto in proyecto_data:
            if proyecto.state!='evaluacion':
                proyecto_ids=[]
            if proyecto.dictamen in ['Sin valorar','Solo General','Solo Coordenadas']:
                proyecto_ids=[]
 
        return proyecto_ids

    _defaults = {
        'confimado': False,
    }
