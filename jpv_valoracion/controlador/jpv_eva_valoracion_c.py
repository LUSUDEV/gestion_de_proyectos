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
import tempfile
from contextlib import closing


import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from openerp.addons.web.controllers import main


_logger = logging.getLogger(__name__)

class jpv_valoracion(http.Controller):

    head_csv=[      
                    'id',
                    'Código',
                    'Nombre del Proyecto',
                    'Sector',
                    'Categoría',
                    'Subcategoría',
                    'Mantenimiento',
                    'Estado',
                    'Municipio',
                    'Parroquia',
                    'Coordenadas Este Inicio',
                    'Coordenadas Norte Inicio',
                    'Huso Inicial',
                    'Coordenadas Este Final',
                    'Coordenadas Norte Final',
                    'Huso Final']
  
    def destino_referencia(self,field_ids,proyectoid,tr_id):
        ordenar_fields=[]
        ref_destino=''
        for field in field_ids:
            ordenar_fields.append(field.name)
        ordenar_fields=sorted(ordenar_fields)
        for field in ordenar_fields:
            ref_destino=ref_destino+field
        ref_destino=ref_destino+str(proyectoid)+'-'+tr_id
        return ref_destino

    def dependientes_preguntas(self,dependencia_line,proyecto_id):
        depende=""
        for dependecia in dependencia_line:
            for pregunta in dependecia.pregunta_id:
                depende=depende+str(pregunta.id)+'-'+str(proyecto_id)+'#'+dependecia.accion_type+" "
        return depende.strip()

        
        
    @http.route(
            ['/valoracion/<model("jpv_val.asignacion_valoracion"):asig>',
            '/valoracion/<model("jpv_val.asignacion_valoracion"):asig>/<model("jpv_val.dictamen_valoracion"):dictamen>/<string:tipo_asignacion>'], 
            type='http', auth="user", website=True)
    def valoracion_cfg(self,asig=None,dictamen=None,tipo_asignacion=None):
            '''este metodo sive para mostrar las valoración asignadas'''
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            user_obj = registry['res.users']
            conf_val_obj = registry['jpv_conf.objeto_valoracion']
            projecto_obj = registry['jpv_cp.carga_proyecto']
            editar=False
            preguntas=[]
            conf_val_general_ids=conf_val_obj.search(
                                        cr,
                                        uid,
                                        [('refencia','=','valoracion_general')]
                                        )
            ValGeneralData=conf_val_obj.browse(cr,uid,conf_val_general_ids)
            
            ValCoordenadas_ids=conf_val_obj.search(
                                        cr,
                                        uid,
                                        [('refencia','=','valoracion_coordenadas')]
                                        )
                                        
            CoordenadasData=conf_val_obj.browse(cr,uid,ValCoordenadas_ids)
            

            if dictamen!=None:
                editar=True
                if tipo_asignacion=='valoracion_general':
                    dataValoracion=ValGeneralData
                if tipo_asignacion=='valoracion_coordenadas':
                    dataValoracion=CoordenadasData
                for pregunta in dataValoracion.preguntas_ids:
                    dependiente=pregunta.dependiente
                    respuestas=[]
                    for respuesta in pregunta.respuesta_ids:
                        checked=False
                        for resultdo in dictamen.resultados_ids:
                            if respuesta.id==resultdo.resp_texto_siple_id.id:
                                print resultdo.resp_texto_siple_id.id
                                dependiente=False
                                checked=True
                        respuestas.append({
                                        'id':respuesta.id,
                                        'respuesta':respuesta.respuesta,
                                        'state':respuesta.state,
                                        'checked':checked,
                                        'dependencia_line':respuesta.dependencia_line,
                                        })
                    pregunta_data={'id':pregunta.id,
                    'field_ids': pregunta.field_ids,
                    'dependiente': dependiente,
                    'nombre': pregunta.nombre,
                    'tipo': pregunta.tipo,
                    'respuesta_ids': respuestas,
                    }
                    preguntas.append(pregunta_data)
            titulo='Valoraciones Asignadas a '+asig.user_id.name
            proyecto_idg=[]
            for proyecto_id in asig.proyecto_idsg:
                proyecto_idg.append(proyecto_id.id)
            proyecto_idg=projecto_obj.search(cr,uid,[('id','in',proyecto_idg)],order='subcategoria_id desc')
            proyecto_datag=projecto_obj.browse(cr,uid,proyecto_idg)
            proyecto_idc=[]
            for proyecto_id in asig.proyecto_idsc:
                proyecto_idc.append(proyecto_id.id)
            proyecto_idc=projecto_obj.search(cr,uid,[('id','in',proyecto_idc)],order='subcategoria_id desc')
            proyecto_datac=projecto_obj.browse(cr,uid,proyecto_idc)
            datos={'parametros':{
                            'titulo':titulo,
                            'template':'jpv_valoracion.valorar',
                            'icon_crear':'user',
                            'color_btn_crear':'info',
                            'css':'info',},
                            'datos_asig':asig,
                            'cant_general':len(asig.proyecto_idsg),
                            'cant_coordenadas':len(asig.proyecto_idsc),
                            'ValGeneralData':ValGeneralData,
                            'CoordenadasData':CoordenadasData,
                            'proyecto_data_gen':proyecto_datag,
                            'proyecto_data_cor':proyecto_datac,
                            'dependientes_preguntas':self.dependientes_preguntas,
                            'destino_referencia':self.destino_referencia,
                            'dictamen':dictamen,
                            'editar':editar,
                            'preguntas':preguntas

                            }
            return panel.panel_lista(datos)
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)

    @http.route(
            ['/valoracion/formato/<model("jpv_val.asignacion_valoracion"):asig>'], 
            type='http', auth="user", website=True)
    def formato_coordenadas(self,asig=None):
            ''' este metodo es el que genera el formato csv para las
            de coordenadas valoraciones'''
            head_csv=[      
                    'id',
                    'Código',
                    'Nombre del Proyecto',
                    'Sector',
                    'Categoría',
                    'Subcategoría',
                    'Mantenimiento',
                    'Estado',
                    'Municipio',
                    'Parroquia',
                    'Coordenadas Este Inicio',
                    'Coordenadas Norte Inicio',
                    'Huso Inicial',
                    'Coordenadas Este Final',
                    'Coordenadas Norte Final',
                    'Huso Final']
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            conf_val_obj = registry['jpv_conf.objeto_valoracion']
            ValCoordenadas_ids=conf_val_obj.search(
                                        cr,
                                        uid,
                                        [('refencia','=','valoracion_coordenadas')]
                                        )
            CoordenadasData=conf_val_obj.browse(cr,uid,ValCoordenadas_ids)[0]
            fp = StringIO()
            writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
            for pregunta in CoordenadasData.preguntas_ids:
                    head_csv.append(pregunta.nombre)
            head_csv.append('Observaciones')
            writer.writerow([name.encode('utf-8') for name in head_csv])
            for proyecto in asig.proyecto_idsc:
                if proyecto.valCoordenadas==False:
                    row = [
                            proyecto.id,
                            proyecto.correlativo,
                            proyecto.nombre_proyecto,
                            proyecto.tipo_sector_id.name,
                            proyecto.categoria_id.name,
                            proyecto.subcategoria_id.name,
                            proyecto.proyect_mantenimiento,
                            proyecto.estado_id.estado,
                            proyecto.municipio_id.municipio,
                            proyecto.parroquia_id.parroquia,
                            proyecto.coord_este,
                            proyecto.coord_norte,
                            proyecto.huso_id.huso,
                            proyecto.coord_este_f,
                            proyecto.coord_norte_f,
                            proyecto.husof_id.huso
                            ]
                    writer.writerow(row)
            fp.seek(0)
            data = fp.read()
            fp.close()
            nombre_archivo='valoracion_coordenadas'+str(asig.fecha_asig)+str(asig.id)+'.csv'
            return request.make_response(data,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_archivo)),
                         ('Content-Type', 'text/csv;charset=utf8')],
                cookies={'fileToken': '212123f4646546'})
            
    @http.route(
            ['/valoracion/proyecto/<model("jpv_cp.carga_proyecto"):proyecto>/<string:refencia>/<string:tipo_valoracion>',
            '/valoracion/dictamen/<model("jpv_val.dictamen_valoracion"):dictamen>/<model("jpv_cp.carga_proyecto"):proyecto>/<string:refencia>/<string:tipo_valoracion>', 
            '/valoracion/proyectos/<model("jpv_valoraciones_ure"):valoraciones_ure>/<string:refencia>/<string:tipo_valoracion>'], 
            type='http', auth="user", website=True)
    def valoracion_cfg2(self,refencia,tipo_valoracion,proyecto=None,dictamen=None,valoraciones_ure=None):
            ''' Este método es que se usa para valorar, ver o editar una valoración del
            erp a la webdite'''
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            user_obj = registry['res.users']
            conf_val_obj = registry['jpv_conf.objeto_valoracion']
            editar=False
            preguntas=[]
            ValCoordenadas_ids=conf_val_obj.search(
                                        cr,
                                        uid,
                                        [('refencia','=',refencia)]
                                        )
                                        
            dataValoracion=conf_val_obj.browse(cr,uid,ValCoordenadas_ids)
            if valoraciones_ure!=None:
                proyecto=valoraciones_ure[0].proyecto_ids
            if dictamen!=None:
                editar=True
                for pregunta in dataValoracion.preguntas_ids:
                    dependiente=pregunta.dependiente
                    respuestas=[]
                    for respuesta in pregunta.respuesta_ids:
                        checked=False
                        for resultdo in dictamen.resultados_ids:
                            if respuesta.id==resultdo.resp_texto_siple_id.id:
                                dependiente=False
                                checked=True
                        respuestas.append({
                                        'id':respuesta.id,
                                        'respuesta':respuesta.respuesta,
                                        'state':respuesta.state,
                                        'checked':checked,
                                        'dependencia_line':respuesta.dependencia_line,
                                        })
                    pregunta_data={'id':pregunta.id,
                                'field_ids': pregunta.field_ids,
                                'dependiente': dependiente,
                                'nombre': pregunta.nombre,
                                'tipo': pregunta.tipo,
                                'respuesta_ids': respuestas,
                                }
                    preguntas.append(pregunta_data)
            if tipo_valoracion=='valoracion_general':
                titulo='Valoración General' 
            if tipo_valoracion=='valoracion_coordenadas':
                titulo='Valoración Coordenadas Cfg' 
            if tipo_valoracion=='valCoordenadasUre':
                titulo='Valoración Coordenadas Ures' 
            template='jpv_valoracion.valoraciones'
            datos={'parametros':{
                            'titulo':titulo,
                            'template':template,
                            'icon_crear':'user',
                            'color_btn_crear':'info',
                            'css':'info',},
                            'CoordenadasData':dataValoracion,
                            'ValGeneralData':dataValoracion,
                            'dependientes_preguntas':self.dependientes_preguntas,
                            'destino_referencia':self.destino_referencia,
                            'dictamen':dictamen,
                            'editar':editar,
                            'preguntas':preguntas,
                            'proyectos':proyecto,
                            'refencia':refencia,
                            'tipo_valoracion':tipo_valoracion,

                            }
            return panel.panel_lista(datos)
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)

    @http.route(
            ['/jpv_valorar'],
            type='json', auth='user', website=True)
    def guardar_valoraracion(self,postfile=None,**post):
        ''' método para guardar las valoraciones recibe el
        parametro postfile sirve para guardar los registros
        de cada fila del archivo csv, este método valida llamando
        otro metodo validar_resultadosData del jpv_conf.valoracion_preguntas
        para validar las preguntas, tanbien sive para editar las valoracion
        con la siguiente lógica, desactiva la valoracion anterior y crea una
        nueva.'''
        if postfile!=None:
            post=postfile
        asignacion_id=None
        ret={}
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        res_users_obj = registry.get('res.users')
        preguntas_obj = registry.get('jpv_conf.valoracion_preguntas')
        carga_proyecto_obj = registry.get('jpv_cp.carga_proyecto')
        dictamen_valoracion_obj = registry.get('jpv_val.dictamen_valoracion')
        try:
            obj_valoracion_id=int(post['obj_valoracion_id']) 
            proyecto_id=int(post['proyecto_id'])
            tipo_valoracion=post['tipo_valoracion']
        except ValueError:
            print("Error en uno de los campos ocultos de la valoración.")
        preguntas_ids=preguntas_obj.search(
                                    cr,
                                    uid,
                                    [('obj_valoracion_id','=',obj_valoracion_id)])
        pregunta_data=preguntas_obj.browse(cr,uid,preguntas_ids)
        resultado=preguntas_obj.validar_resultadosData(cr,uid,pregunta_data,post)
        if not len(resultado['errors']):
            dictamen=''
            if 'negado' in resultado['dictamen']:
                dictamen='negado'
            elif 'diferido' in resultado['dictamen']:
                dictamen='diferido'
            elif 'aprobado' in resultado['dictamen']:
                dictamen='aprobado'
            elif 'sinEfecto' in resultado['dictamen']:
                dictamen='sinEfecto'
            else:
                menssaje='El metodo validar_resultadosData no devolvio\
                            correctamente los valores:\
                            negado, diferido o aprobado'
                ret =  {'modal':{
                        'titulo':'<strong>Error Logíco de Configuración.</strong>',
                        'cuerpo':'''<h1 class="text-danger" >
                                    %s </h1>
                                    ''' % (menssaje),
                                },
                        }
                return ret
            print 'fdsafasfa'
            print 'fdsafasfa'
            print 'fdsafasfa'
            print 'fdsafasfa'
            print 'fdsafasfa'
            print post
            if not post.has_key('asignacion_id'):
                value={
                    'dictamen':dictamen,
                    'resultados_ids':resultado['resultados_data'],
                    'proyecto_id':proyecto_id,
                    'observaciones':post['observaciones'],
                    'tipo_valoracion':str(tipo_valoracion)
                }
            else:
                value={
                    'asignacion_id':post['asignacion_id'],
                    'dictamen':dictamen,
                    'resultados_ids':resultado['resultados_data'],
                    'proyecto_id':proyecto_id,
                    'observaciones':post['observaciones'],
                    'tipo_valoracion':str(tipo_valoracion)
                }
            
            dictamen_ids=dictamen_valoracion_obj.search(
                                                    cr,
                                                    uid,
                                                    [('proyecto_id','=',proyecto_id),
                                                    ('tipo_valoracion','=',tipo_valoracion)])
            if len(dictamen_ids)>0:
                print 'sfasfasffffffff'
                print 'sfasfasffffffff'
                print 'sfasfasffffffff'
                print dictamen_ids
                dictamen_valoracion_obj.write(cr,uid,dictamen_ids,{'active':False},context)
                dictamen_valoracion_data=dictamen_valoracion_obj.browse(cr,uid,dictamen_ids)[0]
                value['asignacion_id']=dictamen_valoracion_data.asignacion_id.id
            dictamen_id=dictamen_valoracion_obj.create(cr,uid,value,context)
            if dictamen_id:
                if tipo_valoracion=='valoracion_general':
                    atributo='valGeneral'
                if tipo_valoracion=='valoracion_coordenadas':
                    atributo='valCoordenadas'
                if tipo_valoracion=='valCoordenadasUre':
                    atributo='valCoordenadasUre'
                carga_proyecto_obj.write(cr,SUPERUSER_ID,proyecto_id,{atributo:True},0,context)
            menssaje='La valoración se guardo correctamente.'
            ret =  {'modal':{
                    'titulo':'<strong>Registro Exitoso.  </strong>',
                    'cuerpo':'''<h4 class="text-success" >
                                %s</h4>
                                ''' % (menssaje),
                            }
                    }
            return ret
        else:
            ret =  {'error_campos':resultado['errors']}
        return ret

    @http.route(
            ['/jpv_carga_valoracion/csv'],
            type='http', auth='user', website=True)
    def cargar_valoracion_csv(self,**post):
        '''Este metodo carga las valoracion de un archivo csv.
        Esta desarrollado para las valoracion de coordenadas,
        posiblemente tambien funcione para las otras valoraciones
        pero sólo esta probado con pregunta de tipo radio'''
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        conf_val_obj = registry['jpv_conf.objeto_valoracion']
        preguntas_obj = registry.get('jpv_conf.valoracion_preguntas')
        asig_valoracion_obj = registry.get('jpv_val.asignacion_valoracion')
        CoordenadasData=conf_val_obj.browse(cr,uid,int(post['obj_valoracion_id']))[0]
        preguntas_csv=[]
        archivo = csv.DictReader(post['jpv_csv_valoracion'])
        listadicc = list(archivo) 
        rownum = 1
        mensaje=''
        #~ valido la cabecera del arhivo
        if len(listadicc)>0:
            for pregunta in CoordenadasData.preguntas_ids:
                if not listadicc[0].has_key(pregunta.nombre):
                    mensaje+='Nombre de la columna incorrecta: %s' % pregunta.nombre
                preguntas_csv.append({
                                    'nombre':pregunta.nombre,
                                    'tipo':pregunta.tipo,
                                    'id':pregunta.id,
                                    'respuesta_ids':pregunta.respuesta_ids
                                    })
            for head in self.head_csv:
                if not listadicc[0].has_key(head):
                    mensaje='Nombre de columna incorrecta: %s' % head
            
            if mensaje!='':
                ret =  {'modal':{
                'titulo':'<strong>Error de nombre de columna.</strong>',
                'cuerpo':'''<h6 class="text-danger" >
                            %s </h6>
                            ''' % (mensaje),
                        },
                }
                return json.dumps(ret)
        resultado_data=[]
        resultado_errors=[]
        titulo_error1=''
        titulo_error2=''
        titulo_error3=''
        titulo_error4=''
        post_guardar=[]
        #~ para validar si los proyectos correspondiente con la asignacion
        asig_valoracion_data=asig_valoracion_obj.browse(cr,uid,[int(post['asignacion_id'])])
        proyectos_asig_ids=[]
        for asignacion in asig_valoracion_data:
            if post['tipo_valoracion']=='valoracion_coordenadas':
                for id_pryecto in asignacion.proyecto_idsc:
                    proyectos_asig_ids.append(id_pryecto.id)
            if post['tipo_valoracion']=='valoracion_general':
                for id_pryecto in asignacion.proyecto_idsc:
                    proyectos_asig_ids.append(id_pryecto.id)
            if post['tipo_valoracion']=='valoracion_coordenadas_ures':
                for id_pryecto in asignacion.proyecto_idsc:
                    proyectos_asig_ids.append(id_pryecto.id)
        #~ recorro los dato del archivo
        for datos in listadicc:
            rownum+=1
            if not int(datos['id']) in proyectos_asig_ids:
                titulo_error1='- Proyecto no asignado. </br>'
                mensaje+='En la fila: %-8s, %-8s, No corresponde con esta'\
                ' asignación. </br></br>' % (
                                        rownum,
                                        datos['Código'],
                                        )
            post_csv={}
            for pregunta in preguntas_csv:
                #~ emulo el post
                if datos[pregunta['nombre']]!='':
                    post_csv.update({pregunta['tipo']+'-'+str(pregunta['id']):datos[pregunta['nombre']]})
                error=True
                nombre_id=''
                for respuesta in  pregunta['respuesta_ids']:
                    nombre_id+=' %s =  %s '\
                           '</br>' % (respuesta.respuesta,str(respuesta.id))
                    if str(respuesta.id)==str(datos[pregunta['nombre']]):
                        error=False
                        for dependencia in respuesta.dependencia_line:
                            if dependencia.accion_type=='cierra':
                                if datos[dependencia.pregunta_id.nombre]:
                                    titulo_error2='- Inconsistencia. </br>'
                                    mensaje+='En la fila: %s, %s, Inconsistencian de la acción'\
                                            ' de la pregunta. %s con la pregunta.'\
                                            ' %s </br></br>'%(
                                                    rownum,
                                                    datos['Código'],
                                                    pregunta['nombre'],
                                                    dependencia.pregunta_id.nombre
                                                    )
                
                if str(datos[pregunta['nombre']])!='' and error:
                    titulo_error3='- Código de Respuesta Incorrecto. </br>'
                    mensaje+='En la fila: %-8s, %-8s, %-8s , incorecta: %-8s ,'\
                    '</br> Posibles Respuestas:</br> %s </br></br>' % (
                                            rownum,
                                            datos['Código'],
                                            pregunta['nombre'],
                                            datos[pregunta['nombre']],
                                            nombre_id
                                            )
            post_csv.update({
                            'observaciones':datos['Observaciones'],
                            'asignacion_id':post['asignacion_id'],
                            'tipo_valoracion':post['tipo_valoracion'],
                            'proyecto_id':datos['id'],
                            'obj_valoracion_id':post['obj_valoracion_id']
                            })
           
            
                
            resultados=preguntas_obj.validar_resultadosData(cr,uid,CoordenadasData.preguntas_ids,post_csv)
            
            post_guardar.append(post_csv)
            for clave, valor in resultados['errors'].iteritems():
                titulo_error4='- Celda Obligatoria. </br>'
                mensaje+='En la fila %s, %s , %s %s '\
                        '</br></br>'%(str(rownum),datos['Código'],clave,valor)
        if mensaje!='':
            titulo='<h3 class="text-danger"><b> ERROR</b></h3> '
            titulo+=titulo_error1+titulo_error2+titulo_error3+titulo_error4
            mensaje+='</br></br> <h4 class="text-success" >Por favor corrija'\
                    ' y vuelva a subir el archivo</h4>'
            ret =  {'modal':{
                'titulo':'''<strong> %s </strong>
                        ''' % (titulo),
                'cuerpo':'''<h5 class="text-danger" >
                            %s </h5>
                            ''' % (mensaje),
                        },
                }
            return json.dumps(ret)
        #~ una vez verificado que el archivo este correctamente se procede
        #~ a guardar cada valoración.
        for postfile in post_guardar:
            self.guardar_valoraracion(postfile)
        post['jpv_csv_valoracion'].close()
        ret =  {'Exito':{'mensaje':'Todo muy bien'}}
        return json.dumps(ret)

    @http.route(['/valoracionept/<model("jpv_val_validar_valoraciones_wizard"):validar>'],
                type='http', auth='user', website=True)
    def descargar_caratas_valoraciones(self,validar):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        cartas_x_firmar_obj = registry.get('jpv_fir.cartas_x_firmar')
        dictamen_valoracion_obj=registry.get('jpv_val.dictamen_valoracion')
        reportname='jpv_valoracion.resultado_valoracion_qweb'
        docids=[]
        nombre_zip='valoraciones/%s_(%s).zip' % (str(date.today()),str(validar.id))
        if not os.path.exists('valoraciones'):
            os.mkdir("valoraciones",0o755)
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        comp_zip = zipfile.ZipFile(nombre_zip, "w" ,zipfile.ZIP_STORED, allowZip64=True)
        epts={}
        entidad_id=[]
        periodo=str()
        ciclo=str()
        entidad_obj = registry.get('jpv_ent.entidades')
        for proyecto in validar.proyecto_ids:
            periodo=proyecto.periodo_id.periodo_fiscal
            dictameF=proyecto.dictamengraph
            ciclo=proyecto.ciclo_id.nombre
            entidad_id=entidad_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('parent_id','=',proyecto.partner_id.id)]
                                        )
            entidad_data=entidad_obj.browse(cr,uid,entidad_id,context=context)
            for usuario in entidad_data.user_ids:
                for grupo in usuario.groups_id:
                    if grupo.name=='Alcaldes, Gobernadores o Alcalde Mayor':
                        nombre_lider=usuario.name
            clave=proyecto.partner_id.name+'-'+dictameF+'-'+str(entidad_id[0])
            dictamen_m=dictameF
            dictamen_m=dictamen_m.lower()
            razones=dictamen_valoracion_obj.causa_diferidos_negados(cr,uid,proyecto.id,dictamen_m)
            if len(razones):
                razones=' \n '.join(razones)
                
            if epts.has_key(clave):
                epts[clave].append({
                                'correlativo':proyecto.correlativo,
                                'dictamen':dictameF,
                                'id':proyecto.id,
                                'razones':razones,
                                'nombre_lider':nombre_lider
                                })
            else:
                epts.update({clave:[{
                                'correlativo':proyecto.correlativo,
                                'dictamen':dictameF,
                                'id':proyecto.id,
                                'razones':razones,
                                'nombre_lider':nombre_lider
                                }]})
        for ept in epts:
            entidad,dictame,entidad_id=ept.split('-')
            obj_rastro_value=[]
                
            for proyecto in epts[ept]:
                values={
                    'objeto_ratro':'jpv_cp.carga_proyecto',
                    'objeto_ratro_id':proyecto['id'],
                    'referncia':proyecto['dictamen'].lower(),
                    }
                obj_rastro_value.append([0, False,values])
             #~ genero el correlatiivo de la carta
            correlativo_carta=registry.get('ir.sequence').get(cr,uid,
                                                        'jpv_fir.cartas_x_firmar')
            value_x_firmar={
                'correlativo':correlativo_carta,
                'tipo_cartas':dictame.lower(),
                'mensaje':'Su proyecto ha sido %s' % dictame,
                'referencia':'Carta de %s por %s de la Valoración'% (entidad,dictame),
                'state':'porvaloracion',
                'metodo':'carta_firmada_valoracion',
                'objeto_ratro_principal':'jpv_ent.entidades',
                'objeto_principal_id':entidad_id,
                'objeto_rastro_ids':obj_rastro_value
                }
            if len(epts[ept])>1:
                mensaje_dictamen=' que se encuentran'\
                                ' %sS son los siguientes:' % dictame.upper()
            else:
                mensaje_dictamen='que se encuentra'\
                                ' %s es el siguiente:' % dictame.upper()
            valores={
                'correlativo':correlativo_carta,
                'entidad':entidad,
                'cargo_lider':'',
                'proyectos':epts[ept],
                'dictamen':dictame,
                'nombre_lider':proyecto['nombre_lider'],
                'periodo':periodo,
                'ciclo':ciclo,
                'mensaje_dictamen':mensaje_dictamen,
                'fecha':date.today().strftime('%d-%m-%Y'),
                }
            cartas_x_firmar_id=cartas_x_firmar_obj.create(cr,uid,value_x_firmar,context)
            nombre_file='valoraciones/%s_%s#%s#.pdf' % (entidad,dictame,cartas_x_firmar_id)
            if os.path.exists(nombre_file):
                os.remove(nombre_file)
            carta_data = request.registry['report'].get_pdf(cr, uid, docids, reportname, data=valores, context=context)
            file_tmp = open(nombre_file, "wb",buffering = 0)
            file_tmp.write('¿'+str(cartas_x_firmar_id)+'?\n')
            file_tmp.write(carta_data)
            comp_zip.write(nombre_file)
            file_tmp.close()
            os.remove(nombre_file)
        comp_zip.close()
        reomover_zip = open(nombre_zip, "r")
        data_zip=reomover_zip.read()
        reomover_zip.close()
        os.remove(nombre_zip)
        return request.make_response(data_zip,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_zip)),
                         ('Content-Type', 'application/zip;charset=utf8'),
                         ('Content-Length', len(data_zip))],
                cookies={'fileToken': '212123f4646546'})    
    

    
   


