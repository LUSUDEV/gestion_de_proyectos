# -*- coding: utf-8 -*-
import base64
import werkzeug
import werkzeug.urls
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request, STATIC_CACHE
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
from datetime import datetime,date
import time 
import logging
from openerp.addons.website_apiform.controladores import panel, base_tools
from openerp.addons.jpv_usuarios.controladores.jpv_use_users_c import jpv_users as jpv_usuarios
from openerp.addons.jpv_carga_proyectos.controladores import jpv_carga_proyecto_c as ecp
import comunes
import json



logger = logging.getLogger(__name__)



class rendicion(http.Controller):
    
    entidad_id=""
    
    def activar_carga(self,proyecto_id,uid):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        proyecto_id=int(proyecto_id)
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        proyecto_write=proyecto_obj.write(cr,SUPERUSER_ID,proyecto_id,{'avance':True},0)
        proyecto=self.instanciar_objetos('jpv_cp.carga_proyecto',proyecto_id)
        proyectos_data=self.instanciar_objetos('jpv_cp.carga_proyecto',
                                                None,
                                                [('partner_id','=',proyecto.partner_id.id),
                                                ('state','=','aprobado'),
                                                ('avance','=',False)])
        if not len(proyectos_data):
            entidad_data=self.instanciar_objetos('jpv_ent.entidades',
                                                None,
                                                [('parent_id','=',proyecto.partner_id.id)])
            write_entidad=registry['jpv_ent.entidades'].write(cr, SUPERUSER_ID,
                                                entidad_data.id,
                                                {'cargar_proyectos':True})
        else:
            for proyecto in proyectos_data:
                actualizado=self.tiempo_validez_bol_get(proyecto.id)
                if not actualizado:
                    return True
                else:
                    proyecto_write=proyecto_obj.write(cr,SUPERUSER_ID,proyecto_id,{'avance':True},0)    
        entidad_data=self.instanciar_objetos('jpv_ent.entidades',
                                                None,
                                                [('parent_id','=',proyecto.partner_id.id)])
        write_entidad=registry['jpv_ent.entidades'].write(cr, SUPERUSER_ID,
                                                entidad_data.id,
                                                {'cargar_proyectos':True})            
        return True

    @http.route(['/ocultar_boton_crear'], type='json', auth='public', website=True)    
    def ocultar_boton_crear(self,partner_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        hoy=date.today()
        format="%Y"
        periodos_obj = registry.get('jpv_plf.periodos')
        anio=hoy.strftime(format)
        actividad="CARGA DE PROYECTOS"
        carga=periodos_obj.plf_control_actividades(cr, uid, [],int(partner_id),actividad,None,anio)
        if 'periodo' in carga.keys():
            return ''
        else:
            return 'hidden'

    def ocultar_boton_editar(self,partner_id,ciclo,state,proyecto_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry.get('jpv_plf.periodos')
        actividad="REPARACIÓN DE PROYECTOS"
        entidades_data=self.instanciar_objetos('jpv_ent.entidades',[('parent_id','=',int(partner_id)),])
        list_user=[]
        for usuario in entidades_data['user_ids']:
            if usuario.id==uid:
                list_user.append(usuario.id)
        if len(list_user)==0:
            hidden='hidden'
            return hidden
    
    def formato_montos_get(self, monto):
        monto='{:,.2f}'.format(monto)
        monto=str(monto)
        monto=monto.replace('.',' ')
        monto=monto.replace(',','.')
        monto=monto.replace(' ',',')
        return monto
        
        
    def instanciar_objetos(self, objeto_name,objeto_id=None, domain=None, orden=None, limite=None):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        obj=registry[objeto_name]
        if objeto_id == None:
            if domain:
                obj_id=obj.search(cr,SUPERUSER_ID,domain,order=orden,limit=limite)
            else:
                return False
        else:
            obj_id=objeto_id
        obj_data=obj.browse(cr,SUPERUSER_ID,obj_id)
        return obj_data
            
    def rendicion_proyecto_get(self,proyecto_id):
        redicion_data=self.instanciar_objetos('jpv_rnd.rendicion', None,[('proyecto_id','=',proyecto_id)])
        if not len(redicion_data):
            return False
        else:
            return True
            
    def cancelar_proyecto_get(self,proyecto_id):
        redicion_data=self.instanciar_objetos('jpv_rnd.rendicion', None,[('proyecto_id','=',proyecto_id)])
        if not len(redicion_data):
            return True
        else:
            if redicion_data.monto_gastado:
                monto_gastado=redicion_data.monto_gastado
                monto_gastado=monto_gastado.replace(".","")
                monto_gastado=monto_gastado.replace(",",".")
                monto_gastado=float(monto_gastado)
            else:
                monto_gastado = 0.00
            avance_financiero=float((monto_gastado*100)/redicion_data.monto)
            if avance_financiero > 10:
                return False
            else:
                return True
        
    def tiempo_validez_get(self,proyecto_id,uid=None):
        cr, context = http.request.cr, http.request.context
        if not uid:
            uid=http.request.uid
        registry = http.request.registry
        hoy=datetime.today()
        retorno='success'
        entidad_data=jpv_usuarios().mi_entidad(uid)
        proyecto_data=self.instanciar_objetos('jpv_cp.carga_proyecto', proyecto_id)
        tiempo_data=self.instanciar_objetos('jpv_rnd.tiempo_validez', None,[('model_id','=','jpv_rnd.rendicion')])
        fecha_inicio=datetime.strptime(proyecto_data.fecha_inicio,'%Y-%m-%d')
        if fecha_inicio > hoy:
            return retorno
        diferencia_inicio=hoy-fecha_inicio
        diferencia_inicio=diferencia_inicio.days
        if diferencia_inicio < tiempo_data.dias_validez:
            return retorno
        redicion_data=self.instanciar_objetos('jpv_rnd.rendicion', None,[('proyecto_id','=',proyecto_id)])
        #actividad='REPARACIÓN DE PROYECTOS'
        #planificacion_data=registry['jpv_plf.periodos'].plf_control_actividades(cr,SUPERUSER_ID,[],entidad_data['entidad_data'].parent_id.id,actividad)
        
        if not len(redicion_data):
            # if not 'periodo' in planificacion_data:
            self.deshabilitar_carga(proyecto_id)
            return 'danger'
        avance_data=self.instanciar_objetos('jpv_rnd.avance', None,[('rendicion_id','=',redicion_data.id)],'create_date DESC',1)
        if not avance_data.create_date:
            self.deshabilitar_carga(proyecto_id)
            return 'danger'
        fecha_avance=datetime.strptime(avance_data.create_date,'%Y-%m-%d %H:%M:%S')
        diferencia=hoy-fecha_avance
        diferencia=diferencia.days
        if diferencia > tiempo_data.dias_validez:
            # if not 'periodo' in planificacion_data:
            self.deshabilitar_carga(proyecto_id)
            retorno='danger'
        elif diferencia <= tiempo_data.dias_validez and diferencia > tiempo_data.dias_validez*0.80 :
            retorno='warning'
        elif diferencia < tiempo_data.dias_validez*0.80:
            retorno='success'
        return retorno
        
        
    def tiempo_validez_bol_get(self,proyecto_id):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        hoy=datetime.today()
        tiempo_data=self.instanciar_objetos('jpv_rnd.tiempo_validez', None,[('model_id','=','jpv_rnd.rendicion')])
        proyecto_data=self.instanciar_objetos('jpv_cp.carga_proyecto', proyecto_id)
        redicion_data=self.instanciar_objetos('jpv_rnd.rendicion', None,[('proyecto_id','=',proyecto_id)])
        fecha_inicio=datetime.strptime(proyecto_data.fecha_inicio,'%Y-%m-%d')
        retorno=True
        if fecha_inicio > hoy:
            return retorno
        diferencia_inicio=hoy-fecha_inicio
        diferencia_inicio=diferencia_inicio.days
        if diferencia_inicio < tiempo_data.dias_validez:
            return retorno
        if not len(redicion_data):
            self.deshabilitar_carga(proyecto_id)
            return False
        avance_data=self.instanciar_objetos('jpv_rnd.avance', None,[('rendicion_id','=',redicion_data.id)],'create_date DESC',1)
        if not avance_data.create_date:
            self.deshabilitar_carga(proyecto_id)
            return False
        fecha_avance=datetime.strptime(avance_data.create_date,'%Y-%m-%d %H:%M:%S')
        diferencia=hoy-fecha_avance
        diferencia=diferencia.days
        if diferencia > tiempo_data.dias_validez:
            retorno=False
            self.deshabilitar_carga(proyecto_id)
        else:
            retorno=True
        return retorno
        
    def deshabilitar_carga(self,proyecto_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto=self.instanciar_objetos('jpv_cp.carga_proyecto',proyecto_id)
        proyecto_write=registry['jpv_cp.carga_proyecto'].write(cr,SUPERUSER_ID,proyecto_id,{'avance':False},0)
        entidad_data=self.instanciar_objetos('jpv_ent.entidades',
                                                None,
                                                [('parent_id','=',proyecto.partner_id.id)])
        write_entidad=registry['jpv_ent.entidades'].write(cr, SUPERUSER_ID,
                                                entidad_data.id,
                                                {'cargar_proyectos':False})
        return True
        
    def input_line_order(self,data):
        lista=[]
        data=list(data)
        data.sort(comunes.compara)    
        return data
    
    def dependiente_a(self,dependencia):
        string=''
        for i in dependencia:
            string+=str(i.pregunta_id.id)+'#'+i.accion_type+'-'
        return string
    
    
    def accion_answer(self,accion_line):
        string=''
        for i in accion_line:
            string+=str(i.respuesta_accion_id.id)+'-'
        return string
        
        
    def dependencia(self,dependencia_line):
        string=''
        for i in dependencia_line:
            string+=str(i.respuesta_id.id)+'#'+(i.accion_type)+'-'
        return string
        
    def categorias(self,respuestas_ids):
        categorias=[]
        for i in respuestas_ids:
            categorias.append(i.categoria_id)
            categorias=list(set(categorias))
            categorias.sort(comunes.compara)
        return categorias
    
    
    def field_get(self,field,proyecto_data):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        campo=getattr(proyecto_data,field)
        return campo
    
    def get_avance_fisico(self,respuestas_ids,avance_fisico):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        avance_fisico=int(avance_fisico.split('%')[0])
        lista_respuesta=[]
        for rta in respuestas_ids:
            if int(rta.respuesta.split('%')[0]) >= avance_fisico:
                lista_respuesta.append(rta)
        return lista_respuesta
    
    def adquisicion_get(self,model_name):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        list_order=['Especie','Grupo Etario','Uso','Caracteristica','Proposito','Tipo','Cantidad']
        data_ordenada=[]
        ir_model_fields_obj=registry['ir.model.fields']
        fields_ids=ir_model_fields_obj.search(cr,
            SUPERUSER_ID,[('model','=',model_name),
                ('name','not in',
                    ['create_uid','create_date','write_uid','write_date','id','proyecto_id'])])
        fields_data=ir_model_fields_obj.browse(cr,SUPERUSER_ID,fields_ids)
        for i in list_order:
            for r in fields_data:
                if r.field_description==i:
                    data_ordenada.append(r)
        return data_ordenada
        
        
    @http.route(['/ocultar_proyecto_editado'], type='json', auth='public', website=True)    
    def ocultar_proyecto_editado(self,proyecto_id):
        proyecto_data=self.instanciar_objetos('jpv_mig.proyectos_migrados',None,[('proyectos_id','=',int(proyecto_id)),('actualizado','=',True)])
        if len(proyecto_data)==1:
            url='/jpv_carga_proyectos/static/src/img/agt_action_success .png'
            return url
        else:
            return
        
    def construir_one_2_many_r(self,post,pivote,dict_principal):
        
        """Metodo para construir los one2many
           Este metodo recibe como parametros:
           
           - post= diccionarios con los valores de la vista
           - pivote= primer string de las claves del diccionario que representa el elemento comun
           - dict_principal  representa la estructura que se requiere para armar el one2many
           
        """
        datos_campos=panel.dict_keys_startswith(post,pivote)
        datos_filtrados=datos_campos.keys()
        datos_filtrados=datos_campos.keys()
        vals=[]
        datos_dicts=[]
        i=0
        datos_len=len(datos_filtrados)
        while i<=datos_len:
            if len(datos_filtrados)>0:
                dato=datos_filtrados[0].split('_')
                datos_dict=panel.dict_keys_startswith2(datos_campos,dato[-1])
                datos_dicts=datos_dict.keys()
                diccionario={}
                for dds in datos_dicts:
                    if dds.split('-')[3]=='accion':
                        accion=int(datos_campos[dds])
                if accion == 0 or accion == 1:
                    for dd in datos_dicts:
                        if dd.split('-')[3] == 'id':
                            if datos_campos[dd]:
                                obj_id=int(datos_campos[dd])
                            else:
                                obj_id=datos_campos[dd]
                        clave_tem=dd.split('-')
                        for dp in dict_principal:
                            clave_erp=dp.split('_')
                            if clave_tem[4].split('_')[0]==clave_erp[0]:
                                diccionario[dp]=datos_campos[dd]
                elif accion == 4 or accion == 2:
                    for dd in datos_dicts:
                        if dd.split('-')[3] == 'id':
                            obj_id=int(datos_campos[dd])
                            diccionario=False
                                
                    
                datos_filtrados=list(set(datos_filtrados) - set(datos_dicts))
                vals.append([accion,obj_id,diccionario])
            i=i+1
        return vals
        
    def armar_edicion(self, campos_requeridos, post, respuestas_culminacion):
        values={}
        adquisicion_equipos=[]
        adquisicion_vehiculo=[]
        adquisicion_materiales=[]
        adquisicion_maquinaria=[]
        adquisicion_semovientes=[]
        lista_old_rta=[]
        lista_new_rta=[]
        obra_civil={}
        lista_respuesta_line=[]
        for campo in campos_requeridos:
            campo_id=int(campo.split('-')[0])
            tipo_pregunta=campo.split('-')[1]
            if tipo_pregunta == 'adquisiciones':
                adquisicion=campo.split('-')[2]
                if adquisicion == 'jpv_cp.equipos':
                    equipos_ids_p={'uso_id': '', 
                     'cantidad': '', 
                     'tipo':'' }
                    adquisicion_equipos=self.construir_one_2_many_r(post,campo,equipos_ids_p)
                if adquisicion == 'jpv_cp.vehiculo':
                    vehiculo_ids_p={'uso_id': '', 
                     'cantidad': '', 
                     'caracteristica_id': '', 
                     'tipo_id':'' }
                    adquisicion_vehiculo=self.construir_one_2_many_r(post,campo,vehiculo_ids_p)
                if adquisicion == 'jpv_cp.materiales_consumo':
                    materiales_ids_p={'uso_id': '', 
                     'cantidad': '', 
                     'tipo':'' }
                    adquisicion_materiales=self.construir_one_2_many_r(post,campo,materiales_ids_p)
                if adquisicion == 'jpv_cp.maquinaria':
                    maquinaria_ids_p={'uso_id': '', 
                     'cantidad': '', 
                     'tipo':'' }
                    adquisicion_maquinaria=self.construir_one_2_many_r(post,campo,maquinaria_ids_p)
                if adquisicion == 'jpv_cp.semovientes_caracteristicas':
                    semoviente_ids_p={'especie_id': '', 
                     'grupo': '', 
                     'uso': '', 
                     'proposito': '', 
                     'cantidad':'' }
                    adquisicion_semovientes=self.construir_one_2_many_r(post,campo,semoviente_ids_p)
            else:        
                for respuesta in respuestas_culminacion:
                    avance_id=respuesta['avance_id']
                    if respuesta['pregunta_id'] == campo_id:
                        lista_old_rta.append(campo)
                        list_files=[]
                        if tipo_pregunta == 'file' or tipo_pregunta == 'img':
                            list_new_files=[]
                            list_old_files=[]
                            list_conserve_files=[]
                            list_deleted_files=[]
                            files_post=panel.dict_keys_startswith(post,campo)
                            if len(respuesta['files']):
                                for file_post in files_post.keys():
                                    name=files_post[file_post].split(';')[-1]
                                    if name.split('=')[0]=='file_id':
                                        file_id=int(name.split('=')[1])
                                        for _file in respuesta['files']:
                                            if _file['id'] == file_id:
                                                list_old_files.append([4,_file['id'],{}])
                                                list_conserve_files.append(_file['id'])
                                            else:
                                                list_deleted_files.append(_file['id'])
                                    else:
                                        type_file=files_post[file_post].split(';' or ',')[0].split(':')[1]
                                        data_file=files_post[file_post].split(';' or ',')[1].split(',')[1]
                                        list_new_files.append([0,False,{'datas':data_file,
                                                        'name':name,
                                                        'type':'binary',
                                                        'mimetype':type_file,}])
                                        for __file in respuesta['files']:
                                            list_deleted_files.append(__file['id'])
                            list_deleted_files=list(set(list_deleted_files)-set(list_conserve_files))
                            for id_file in list_deleted_files:
                                list_old_files.append([2,id_file,{}])
                            list_files.extend(list_new_files)
                            list_files.extend(list_old_files)
                            lista_respuesta_line.append([1,respuesta['id'],{'files':list_files}])
                        else:
                            lista_respuesta_line.append([1,respuesta['id'],{'respuesta':post[campo]}])
                    else:
                        lista_new_rta.append(campo)
                if len(campo.split('-')) > 2:
                    if campo.split('-')[2] == 'obra':
                        obra_civil[campo.split('-')[3]]=post[campo]
                        obra_civil['obra_civil']=True
                        
        lista_new_rta=list(set(lista_new_rta)-set(lista_old_rta))
        for campo_new in lista_new_rta:
            lista_respuesta_line.append([0, False, {'pregunta_id':int(campo_new.split('-')[0]), 'respuesta': post[campo_new]}])
        lista_respuesta_line.sort()
        avances=[[1,avance_id, {'respuestas_line':lista_respuesta_line}]]
        values={'avances': avances,
            'adquisicion_equipos': adquisicion_equipos,
            'adquisicion_vehiculo': adquisicion_vehiculo,
            'adquisicion_materiales': adquisicion_materiales,
            'adquisicion_maquinaria': adquisicion_maquinaria,
            'adquisicion_semovientes': adquisicion_semovientes,
            'obra_civil': obra_civil,
            'ult_avance': avance_id,
        }
        return values
                    
        
    @http.route(['/rendicion/name_search'], type='http', auth='public', website=True)    
    def name_search(self,model_name,domain=None):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        model_obj=registry[str(model_name)]
        field_data=model_obj.name_search(cr,SUPERUSER_ID,name="",operator="ilike")
        return field_data
    
    
    
    @http.route(['/rendicion'], type='http', auth='public', website=True)
    def index(self, **kwargs):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        entidad_data=jpv_usuarios().mi_entidad(uid)
        dict_montos={}
        if len(entidad_data['entidad_data']):
            proyecto_obj=registry['jpv_cp.carga_proyecto']
            rendicion_obj=registry['jpv_rnd.rendicion']
            mensaje_migrados=""
            proyectosr_ids=proyecto_obj.search(cr,
                                                    SUPERUSER_ID,
                                                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                                                    ('state','=','aprobado')])
            proyectosr_data=proyecto_obj.browse(cr,SUPERUSER_ID,proyectosr_ids)
            proyectos_rendidos_ids=[]
            rendir=True
            for proyecto in proyectosr_data:
                actualizado=self.tiempo_validez_bol_get(proyecto.id)
                if actualizado:
                    proyectos_rendidos_ids.append(proyecto.id)
                else:
                    mensaje_migrados=  u"¡Alerta! Para cargar proyectos de este periodo usted debe \n "\
                    "hacer los avances correspondientes para los siguientes proyectos."
            proyectos_obj=registry['jpv_cp.carga_proyecto']
            proyectos_ids=proyectos_obj.search(cr,SUPERUSER_ID,
                [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                ('state','=','aprobado')])
            # proyectos_data=proyectos_obj.read(cr, SUPERUSER_ID, proyectos_ids,['nombre_proyecto','monto_proyecto','correlativo','state'])
            proyectos_data={}
            for id_proyecto in proyectos_data:
                monto_proyecto=str(id_proyecto['monto_proyecto']).replace('.',',')
                monto=monto_proyecto.split(',')
                if len(monto[1])==1:
                    monto_proyecto=monto_proyecto+'0'
                dict_montos[id_proyecto['id']]=monto_proyecto
            proyectos_data
            datos={'parametros':{
                                'titulo':'Proyectos '+entidad_data['entidad_data'].name,
                                'template':'jpv_carga_proyectos.proyecto_template',
                                'css':'info',},
                    'carga_proyecto_data': proyectos_data,
                    'entidad_data': entidad_data,
                    'proyectos_ids': proyectos_ids,
                    'dict_montos':dict_montos,
                    'self':self,
                    'ocultar_boton_crear':self.ocultar_boton_crear,
                    'dict_montos_asoci':[],
                    'partner_id':entidad_data['entidad_data'].parent_id.id,
                    'partner_asociados_data':[],
                    'proyectos_gobenacion_data':[],
                    'proyectos_alcaldias_asociadas_data':[],
                    'gobernacion':[],
                    'alcaldia':[],
                    'mensaje_migrados':mensaje_migrados,
                    'rendir':rendir,
                    'ocultar_proyecto_editado':self.ocultar_proyecto_editado,
                    'domain':"rendicion"
                                }
                                
            return panel.panel_lista(datos)
        else:
            mensaje={
                    'titulo':'Sin jpv',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)


    @http.route(['/jpv_mostrar_proyectos'], type='json', auth='public', website=True)
    def mostrar_proyectos(self, **kwargs):
        page_limit=kwargs['page_limit']
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        entidad_data=jpv_usuarios().mi_entidad(uid)
        entidad_data['entidad_data_dict']=registry[entidad_data['entidad_data']._name].read(cr,SUPERUSER_ID,entidad_data['entidad_id'])
        dict_montos={}
        if len(entidad_data['entidad_data']):
            proyecto_obj=registry['jpv_cp.carga_proyecto']
            rendicion_obj=registry['jpv_rnd.rendicion']
            mensaje_migrados=""
            proyectosr_ids=proyecto_obj.search(cr,
                                                    SUPERUSER_ID,
                                                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id)])
            proyectosr_data=proyecto_obj.browse(cr,SUPERUSER_ID,proyectosr_ids)
            proyectos_rendidos_ids=[]
            proyectos_migrados_obj = registry.get('jpv_mig.proyectos_migrados')
            proyectos__edit_ids= proyectos_migrados_obj.comprobar_actualizacion_ids(cr,SUPERUSER_ID,[],context,entidad_data['entidad_data'])
            if not len(proyectos__edit_ids):
                rendir=True
            else:
                rendir=False
                
            proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,
                                            [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                                            ('state','=','aprobado'),
                                            ('id','not in',proyectos_rendidos_ids)])
            if len(proyecto_ids):
                mensaje_migrados=  u"¡Alerta! Para cargar proyectos de este periodo usted debe \n "\
                                    "hacer los avances correspondientes para los siguientes proyectos."
            proyectos_obj=registry['jpv_cp.carga_proyecto']
            if kwargs['domain']=='rendicion':
                proyectos_ids=proyectos_obj.search(cr,SUPERUSER_ID,
                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                    ('state','=','aprobado')])
            elif kwargs['domain']=='proyecto':
                proyectos_ids=proyectos_obj.search(cr,SUPERUSER_ID,
                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id)])
            proyectos_data=proyectos_obj.read(cr, SUPERUSER_ID, proyectos_ids[:page_limit])
            for id_proyecto in proyectos_data:
                monto_proyecto=str(id_proyecto['monto_proyecto']).replace('.',',')
                monto=monto_proyecto.split(',')
                if len(monto[1])==1:
                    monto_proyecto=monto_proyecto+'0'
                dict_montos[id_proyecto['id']]=monto_proyecto
            datos={ 'carga_proyecto_data': proyectos_data,
                    'entidad_data': entidad_data['entidad_data_dict'],
                    'proyectos_ids': proyectos_ids,
                    'dict_montos':dict_montos,
                    'self':'/self',
                    'ocultar_boton_crear':'/ocultar_boton_crear',
                    'dict_montos_asoci':[],
                    'partner_id':entidad_data['entidad_data'].parent_id.id,
                    'partner_asociados_data':[],
                    'proyectos_gobenacion_data':[],
                    'proyectos_alcaldias_asociadas_data':[],
                    'gobernacion':[],
                    'alcaldia':[],
                    'mensaje_migrados':mensaje_migrados,
                    'rendir':rendir,
                    'page_limit':page_limit,
                    'ocultar_proyecto_editado':'/ocultar_proyecto_editado'
                                }
                                
            return datos
        else:
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
        
        
    @http.route('/rendicion/busca_respuestas', auth='public', website=True, type='json')
    def busca_respuestas(self, datos_met=None, **datos):
        if not datos_met==None:
            datos=datos_met
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        registry = http.request.registry
        preguntas_ms_ids=[]
        preguntas_mc_ids=[]
        input_line_obj=registry['jpv_rnd.input_line']
        input_line_ids=input_line_obj.search(cr, SUPERUSER_ID,
                                            [('rendicion_id','=',datos['id'])])
        input_line_data=input_line_obj.browse(cr,SUPERUSER_ID,input_line_ids)
        for line in input_line_data:
            if not line.pregunta_id.muestra_continua:
                preguntas_ms_ids.append(line.pregunta_id.id)
            else:
                preguntas_mc_ids.append(line.pregunta_id.id)
        preguntas_ms_ids=list(set(preguntas_ms_ids))
        preguntas_mc_ids=list(set(preguntas_mc_ids))
        ms_ids=[]
        mc_ids=[]
        for i in preguntas_ms_ids:
            ms_ids.extend(input_line_obj.search(cr,SUPERUSER_ID,
                                            [('pregunta_id','=',i),
                                            ('rendicion_id','=',datos['id'])],
                                            order='create_date DESC',limit=1))
        for r in preguntas_mc_ids:
            mc_ids.extend(input_line_obj.search(cr,SUPERUSER_ID,
                                            [('pregunta_id','=',r),
                                            ('rendicion_id','=',datos['id'])],
                                            order='create_date DESC',limit=1))
        ms_data=input_line_obj.browse(cr, SUPERUSER_ID, ms_ids)
        mc_data=input_line_obj.browse(cr, SUPERUSER_ID, mc_ids)
        ms_list=[]
        mc_list=[]
        culminacion_list=[]
        for line in ms_data:
            if line.pregunta_id.state == 'culminacion':
                files_list=[]
                if line.tipo_pregunta == 'file' or line.tipo_pregunta == 'img':
                    for files in line.files:
                        files_list.append({'datas':files.datas,
                                    'id':files.id,
                                    'name':files.name,
                                    'type':files.mimetype
                                    })
                culminacion_list.append({'id':line.id,
                            'avance_id':line.avance_id.id,
                            'pregunta_id':line.pregunta_id.id,
                            'tipo_pregunta':line.tipo_pregunta,
                            'respuesta':line.respuesta,
                            'files':files_list
                            })
            else:
                ms_list.append({'id':line.id,
                            'pregunta_id':line.pregunta_id.id,
                            'tipo_pregunta':line.tipo_pregunta,
                            'respuesta':line.respuesta
                            })
        for lines in mc_data:
            if lines.respuesta == lines.pregunta_id.condicion_muestra.respuesta:
                ms_list.append({'id':lines.id,
                            'pregunta_id':lines.pregunta_id.id,
                            'tipo_pregunta':lines.tipo_pregunta,
                            'respuesta':lines.respuesta
                            })
            elif lines.pregunta_id.state == 'culminacion':
                files_list=[]
                if line.tipo_pregunta == 'file' or line.tipo_pregunta == 'img':
                    for files in line.files:
                        files_list.append({'datas':files.datas,
                                    'name':files.name,
                                    'type':files.mimetype
                                    })
                culminacion_list.append({'id':lines.id,
                            'avance_id':lines.avance_id.id,
                            'pregunta_id':lines.pregunta_id.id,
                            'tipo_pregunta':lines.tipo_pregunta,
                            'respuesta':lines.respuesta,
                            'files':files_list
                            })
            else:
                if lines.pregunta_id.condicion_muestra:
                    mc_list.append({'id':lines.id,
                            'pregunta_id':lines.pregunta_id.id,
                            'tipo_pregunta':lines.tipo_pregunta,
                            'respuesta':lines.respuesta
                            })
                   
                      
        val={'preguntas_ms':ms_list,
            'preguntas_mc':mc_list,
            'preguntas_culminacion':culminacion_list
            }    
        
        return val
        
        
        
        
        
    @http.route('/avance/<int:id_proyecto>/', auth='public', website=True)
    def avance(self, id_proyecto):
        datos={}
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        entidad_data=jpv_usuarios().mi_entidad(uid)
        responsable=[]
        rendicion_question_obj=registry['jpv_conf.obj_rendicion']
        rendicion_question_id=rendicion_question_obj.search(cr,SUPERUSER_ID,[('refencia','=','rendicion')])
        if not len(entidad_data['entidad_data']):
            mensaje={
                    'titulo':'Sin jpv',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        for user in entidad_data['entidad_data'].user_ids:
            for group in user.groups_id:
                if group.name == 'Alcaldes, Gobernadores o Alcalde Mayor':
                    responsable=user
        if not len(responsable):
            mensaje={
                    'titulo':'Sin Representante Asociado',
                    'mensaje':'''Disculpe no tiene Alcalde o Gobernador asociado la entidad''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
            
        if not len(rendicion_question_id):
            mensaje={
                    'titulo':'Sin Cuestionario de Rendiciones',
                    'mensaje':'''Disculpe No Tiene cargada ningun cuestionario en el sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        
            
        rendicion_question_data=rendicion_question_obj.browse(cr,SUPERUSER_ID,rendicion_question_id)
        rendicion_obj=registry['jpv_rnd.rendicion']
        rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',id_proyecto)])
        rendicion_data=[]
        if len(rendicion_id):
            rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
        proyectos_obj=registry['jpv_cp.carga_proyecto']
        proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, id_proyecto)
        if not proyectos_data.state == 'aprobado':
                mensaje={
                    'titulo':'No puede Rendir',
                    'mensaje':'''Disculpe Este proyecto no puede ser rendido,\n no puede rendir proyectos que no esten aprobados''',
                    'volver':'/'
                }
                return http.request.website.render('website_apiform.mensaje', mensaje)
        datos.update({'parametros':{
                            'action':'/avance',
                            'titulo':'Avance',
                            'url_boton_list':'/rendicion',
                            'template':'jpv_rendicion.avance',
                            'css':'success',
                            'id_enviar':'id_guardar_rendicion_jpv',
                            'nombre_bt_accion':'Declarar'
                            },
                'proyectos_data': proyectos_data,
                'entidad_data': entidad_data['entidad_data'],
                'responsable': responsable,
                'rendicion_data':rendicion_data,
                'rendicion_question_data':rendicion_question_data,
                'dependiente': self.dependiente_a,
                'accion_answer': self.accion_answer,
                'dependencia': self.dependencia,
                'categorias_select': self.categorias,
                'field_get': self.field_get,
                'adquisicion_get': self.adquisicion_get,
                'name_search': self.name_search,
                'self': self,
                
                            })
                            
        return panel.panel_post(datos)
    
    
    @http.route('/avance/consultar/<int:id_proyecto>/', auth='public', website=True)
    def avance_consulta(self, id_proyecto):
        datos={}
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        entidad_data=jpv_usuarios().mi_entidad(uid)
        responsable=[]
        for user in entidad_data['entidad_data'].user_ids:
            for group in user.groups_id:
                if group.name == 'Alcaldes, Gobernadores o Alcalde Mayor':
                    responsable=user
        if not len(entidad_data['entidad_data']):
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
            
        rendicion_obj=registry['jpv_rnd.rendicion']
        rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',id_proyecto)])
        rendicion_data=[]
        if len(rendicion_id):
            rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
        proyectos_obj=registry['jpv_cp.carga_proyecto']
        proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, id_proyecto)
        if not proyectos_data.state == 'culminado':
            mensaje={
                    'titulo':'No disponible',
                    'mensaje':'''Disculpe Este proyecto no esta culminado''',
                    'volver':'/'
            }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        if not len(rendicion_data):
            mensaje={
                    'titulo':'No disponible',
                    'mensaje':'''Disculpe este proyecto no tiene avances''',
                    'volver':'/'
            }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        datos.update({'parametros':{
                            'action':'/avance',
                            'titulo':'Avances del proyecto',
                            'url_boton_list':'/proyecto',
                            'template':'jpv_rendicion.consulta',
                            'css':'info',
                            'id_enviar':'id_guardar',
                            'remover_btn_enviar':'si',
                            'nombre_bt_accion':'Declarar'
                            },
                'proyectos_data': proyectos_data,
                'entidad_data': entidad_data['entidad_data'],
                'responsable': responsable,
                'rendicion_data':rendicion_data,
                'self':self,
                            })
                            
        return panel.panel_post(datos)
    
    
    
        
    @http.route('/avance', auth='public', website=True, type='json')
    def avance_enviar(self, **kwargs):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        pregunta_obj=registry['jpv_conf.preguntas']
        campos_requeridos_sf=kwargs['fields_required'].split('#')
        campos_requeridos_sf.pop()
        campos_requeridos_sf=list(set(campos_requeridos_sf))
        campos_requeridos_sf.sort()
        campos_requeridos=[]
        for campos in campos_requeridos_sf:
            if campos.split('-')[1] == 'adquisiciones':
                split_campo=campos.split('-')
                split_campo.pop()
                split_campo.pop()
                campos_requeridos.append(('-').join(split_campo))
            else:
                campos_requeridos.append(campos)
        campos_requeridos=list(set(campos_requeridos))
        campos_requeridos.sort()
        campos=[]
        for i in campos_requeridos:
            if i.split('-')[1] == 'file' or i.split('-')[1] == 'img':
                campos.append({'name':i,
                       'cant':int(i.split('-')[2]),
                       'type':i.split('-')[1],
                       'attr':pregunta_obj.browse(cr,SUPERUSER_ID,int(i.split('-')[0])).nombre+','})
            elif i.split('-')[1] == 'adquisiciones':
                campos_adquisicion=panel.dict_keys_startswith(kwargs,i)
                for campo in campos_adquisicion.keys():
                    fila=int(campo.split('_')[-1])
                    nombre_obj_campo=campo.split('-')[4].split('_')
                    nombre_obj_campo.pop()
                    nombre_obj_campo=('_').join(nombre_obj_campo)
                    if not campo.split('-')[3] == 'id' and not campo.split('-')[3] == 'accion':
                        descripcion_campo=registry[campo.split('-')[2]
                                                    ].fields_get(cr,
                                                                SUPERUSER_ID,
                                                                nombre_obj_campo
                                                                )[nombre_obj_campo]['string']
                        nombre_adquisicion=pregunta_obj.browse(cr,SUPERUSER_ID,int(i.split('-')[0])).nombre
                        descripcion_adquisicion=registry['jpv_cp.carga_proyecto'].fields_get(cr,SUPERUSER_ID,nombre_adquisicion)[nombre_adquisicion]['string']
                        campos.append({'name':campo,
                           'type':campo.split('-')[3],
                           'attr':'En Adquisición de '+descripcion_adquisicion+'s fila '+str(fila)+', el campo '+descripcion_campo+' ',})
            elif i.split('-')[1] == 'numerico':
                monto_minimo=0
                pregunta_data=pregunta_obj.browse(cr,SUPERUSER_ID,int(i.split('-')[0]))
                if pregunta_data.field_muestra_ids and pregunta_data.field_muestra_ids.name=='monto_gastado':
                    rendicion_obj=registry['jpv_rnd.rendicion']
                    rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',int(kwargs['proyecto_id']))])
                    if len(rendicion_id):
                        rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID, rendicion_id)
                        if rendicion_data.monto_gastado:
                            monto_minimo=rendicion_data.monto_gastado
                            monto_minimo=monto_minimo.replace(".","")
                            monto_minimo=monto_minimo.replace(",",".")
                            monto_minimo=float(monto_minimo)
                        monto_maximo=rendicion_data.monto
                    else:
                        proyecto_data=registry['jpv_cp.carga_proyecto'].browse(cr,SUPERUSER_ID, int(kwargs['proyecto_id']))
                        monto_maximo=proyecto_data.monto_proyecto
                campos.append({'name':i,
                       'type':i.split('-')[1],
                       'attr':pregunta_data.nombre+',',
                       'min':monto_minimo,
                       'attr_min':'El monto no debe ser menor al monto gastado',
                       'attr_max':'El monto no debe sobrepasar el monto del proyecto',
                       'min':monto_minimo,
                       'max':monto_maximo})
            else:
                campos.append({'name':i,
                       'type':i.split('-')[1],
                       'attr':pregunta_obj.browse(cr,SUPERUSER_ID,int(i.split('-')[0])).nombre+','})
        errors=panel.validar().varios_campos(campos,kwargs)
        if not len(errors):
            adquisicion_equipos=[]
            adquisicion_vehiculo=[]
            adquisicion_materiales=[]
            adquisicion_maquinaria=[]
            adquisicion_semovientes=[]
            obra_civil={}
            lista_respuesta_line=[]
            avances=[]
            rendicion_obj=registry['jpv_rnd.rendicion']
            rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',int(kwargs['proyecto_id']))])
            datos={}
            datos['id']=rendicion_id
            lista_respuestas=self.busca_respuestas(datos)
            for pregunta in lista_respuestas['preguntas_ms']:
                for campo in campos_requeridos:
                    pregunta_id=int(campo.split('-')[0])
                    if pregunta['pregunta_id'] == pregunta_id:
                        return {'error_campos':{'Existen preguntas que ya han sido contestadas..':'\nPor favor refresque la pagina y vuelva a intentarlo '}}
            if kwargs['edicion']=='True':
                edicion_line=self.armar_edicion(campos_requeridos,kwargs,lista_respuestas['preguntas_culminacion'])
                adquisicion_equipos=edicion_line['adquisicion_equipos']
                adquisicion_vehiculo=edicion_line['adquisicion_vehiculo']
                adquisicion_materiales=edicion_line['adquisicion_materiales']
                adquisicion_maquinaria=edicion_line['adquisicion_maquinaria']
                adquisicion_semovientes=edicion_line['adquisicion_semovientes']
                obra_civil=edicion_line['obra_civil']
                avances=edicion_line['avances']
            else:
                for i in campos_requeridos:
                    if i.split('-')[1] == 'file' or i.split('-')[1] == 'img':
                        files = panel.dict_keys_startswith(kwargs, i)
                        list_files=[]
                        for row in files:
                            type_file=kwargs[row].split(';' or ',')[0].split(':')[1]
                            data_file=kwargs[row].split(';' or ',')[1].split(',')[1]
                            name_file=kwargs[row].split(';' or ',')[2]
                            list_files.append([0,False,{'datas':data_file,
                                                        'name':name_file,
                                                        'type':'binary',
                                                        'mimetype':type_file,}])
                        lista_respuesta_line.append([0,False,{'pregunta_id':int(i.split('-')[0]),
                                                            'respuesta':str(len(list_files))+i.split('-')[1],
                                                            'files':list_files}])
                    elif i.split('-')[1] == 'adquisiciones':
                        if i.split('-')[2] == 'jpv_cp.equipos':
                            equipos_ids_p={'uso_id': '', 
                             'cantidad': '', 
                             'tipo':'' }
                            adquisicion_equipos=self.construir_one_2_many_r(kwargs,i,equipos_ids_p)
                        if i.split('-')[2] == 'jpv_cp.vehiculo':
                            vehiculo_ids_p={'uso_id': '', 
                             'cantidad': '', 
                             'caracteristica_id': '', 
                             'tipo_id':'' }
                            adquisicion_vehiculo=self.construir_one_2_many_r(kwargs,i,vehiculo_ids_p)
                        if i.split('-')[2] == 'jpv_cp.materiales_consumo':
                            materiales_ids_p={'uso_id': '', 
                             'cantidad': '', 
                             'tipo':'' }
                            adquisicion_materiales=self.construir_one_2_many_r(kwargs,i,materiales_ids_p)
                        if i.split('-')[2] == 'jpv_cp.maquinaria':
                            maquinaria_ids_p={'uso_id': '', 
                             'cantidad': '', 
                             'tipo':'' }
                            adquisicion_maquinaria=self.construir_one_2_many_r(kwargs,i,maquinaria_ids_p)
                        if i.split('-')[2] == 'jpv_cp.semovientes_caracteristicas':
                            semoviente_ids_p={'especie_id': '', 
                             'grupo': '', 
                             'uso': '', 
                             'proposito': '', 
                             'cantidad':'' }
                            adquisicion_semovientes=self.construir_one_2_many_r(kwargs,i,semoviente_ids_p)
                    elif len(i.split('-')) > 2:
                        if i.split('-')[2] == 'obra':
                            obra_civil[i.split('-')[3]]=kwargs[i]
                            obra_civil['obra_civil']=True
                    else:
                        lista_respuesta_line.append([0,False,{'pregunta_id':int(i.split('-')[0]), 'respuesta':kwargs[i]}])
                        
                lista_respuesta_line.sort()
            if len(rendicion_id):
                rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID, rendicion_id)
                if not len(avances):
                    for line in rendicion_data.rendicion_line:
                        avances.append([4,line.id,False])
                    avances.append([0,False, {'respuestas_line':lista_respuesta_line}])
                    
                vals={
                'rendicion_line':avances,
                'adquisicion_equipos':adquisicion_equipos,
                'adquisicion_vehiculo':adquisicion_vehiculo,
                'adquisicion_materiales_consumo':adquisicion_materiales,
                'adquisicion_maquinaria':adquisicion_maquinaria,
                'adquisicion_semovientes':adquisicion_semovientes
                }
                vals.update(obra_civil)
                write_id=rendicion_obj.write(cr,SUPERUSER_ID, rendicion_id,vals)
                if kwargs['declarar_culminacion'] == 'True':
                    rend_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
                    if rend_data.state == 'ejecucion':
                        vals={}
                        vals.update({'state':'culminada'})
                        write_state_project=registry['jpv_cp.carga_proyecto'].write(cr,
                                                                SUPERUSER_ID,
                                                                int(kwargs['proyecto_id']),
                                                                {'state':'culminado'},0)
                        monto_gastado=rend_data.monto_gastado
                        monto_gastado=monto_gastado.replace(".","")
                        monto_gastado=monto_gastado.replace(",",".")
                        monto_gastado=float(monto_gastado)
                        if monto_gastado < rend_data.monto:
                            monto_restante=rend_data.monto - monto_gastado
                            accion='Abono de Monto Restante Culminación'
                            descripcion=rend_data.proyecto_id.correlativo
                            obj_mov_cuentas=registry['jpv.movimientos_cuentas']
                            cuenta_id=rend_data.proyecto_id.cuenta_id.id
                            abono_a_cuenta_id=obj_mov_cuentas.movimiento_ingreso(cr,SUPERUSER_ID,cuenta_id,
                                                                        monto_restante,accion,descripcion,
                                                                        'jpv_cp.carga_proyecto',rend_data.proyecto_id.id,
                                                                        rend_data.proyecto_id.periodo_id.id,
                                                                        rend_data.entidad_id.id,
                                                                        )
                            if rend_data.proyecto_id.proyect_mantenimiento:
                                monto_rest_mant=rend_data.proyecto_id.monto_tomado_mantenimiento - abono_a_cuenta_id['monto_disponible_mantenimiento_ingreso']
                                write_monto_mantenimiento=registry['jpv_cp.carga_proyecto'].write(cr,
                                                                    SUPERUSER_ID,
                                                                    rend_data.proyecto_id.id,
                                                                    {'monto_tomado_mantenimiento':monto_rest_mant},0)
                            lista_movimientos=[]
                            for movimiento in rend_data.movimiento_ids:
                                lista_movimientos.append(movimiento.id)
                            lista_movimientos.append(abono_a_cuenta_id['movimiento_id_ingreso'])
                            vals.update({'movimiento_ids': [[6,False,lista_movimientos]]})    
                        write_id=rendicion_obj.write(cr,SUPERUSER_ID, rendicion_id,vals)
                self.activar_carga(kwargs['proyecto_id'],uid)
                
            else:
                vals={
                'proyecto_id':int(kwargs['proyecto_id']),
                'rendicion_line':[[0,False, {'respuestas_line':lista_respuesta_line}]],
                'adquisicion_equipos':adquisicion_equipos,
                'adquisicion_vehiculo':adquisicion_vehiculo,
                'adquisicion_materiales_consumo':adquisicion_materiales,
                'adquisicion_maquinaria':adquisicion_maquinaria,
                'adquisicion_semovientes':adquisicion_semovientes
                }
                vals.update(obra_civil)
                hacer_movimiento=False
                if kwargs['declarar_culminacion'] == 'True':
                    vals.update({'state':'culminada'})
                    write_state_project=registry['jpv_cp.carga_proyecto'].write(cr,
                                                            SUPERUSER_ID,
                                                            int(kwargs['proyecto_id']),
                                                            {'state':'culminado'},0)
                rendicion_id=rendicion_obj.create(cr,SUPERUSER_ID,vals)
                self.activar_carga(kwargs['proyecto_id'],uid)
                if kwargs['declarar_culminacion'] == 'True':
                    rend_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
                    monto_gastado=rend_data.monto_gastado
                    monto_gastado=monto_gastado.replace(".","")
                    monto_gastado=monto_gastado.replace(",",".")
                    monto_gastado=float(monto_gastado)
                    if monto_gastado < rend_data.monto:
                        monto_restante=rend_data.monto - monto_gastado
                        accion='Abono de Monto Restante Culminación'
                        descripcion=rend_data.proyecto_id.correlativo
                        obj_mov_cuentas=registry['jpv.movimientos_cuentas']
                        cuenta_id=rend_data.proyecto_id.cuenta_id.id
                        abono_a_cuenta_id=obj_mov_cuentas.movimiento_ingreso(cr,SUPERUSER_ID,cuenta_id,
                                                                    monto_restante,accion,descripcion,
                                                                    'jpv_cp.carga_proyecto',rend_data.proyecto_id.id,
                                                                    rend_data.proyecto_id.periodo_id.id,
                                                                    rend_data.entidad_id.id,
                                                                    rend_data.proyecto_id.proyect_mantenimiento,
                                                                    rend_data.proyecto_id.monto_proyecto)
                        if rend_data.proyecto_id.proyect_mantenimiento:
                            monto_rest_mant=rend_data.proyecto_id.monto_tomado_mantenimiento - abono_a_cuenta_id['monto_disponible_mantenimiento_ingreso']
                            write_monto_mantenimiento=registry['jpv_cp.carga_proyecto'].write(cr,
                                                                SUPERUSER_ID,
                                                                rend_data.proyecto_id.id,
                                                                {'monto_tomado_mantenimiento':monto_rest_mant},0)
                        write_mov_id=rendicion_obj.write(cr,SUPERUSER_ID,rendicion_id,{'movimiento_ids':[[6,False,[abono_a_cuenta_id['movimiento_id_ingreso']]]]})
        else:
            return{'error_campos':errors}
        rendicion_data_update=rendicion_obj.read(cr,SUPERUSER_ID,rendicion_id)
        return {'redirect':'/rendicion'}
        
        
    
    
    @http.route('/cancelar/<int:id_proyecto>/', auth='public', website=True)
    def cancelar(self, id_proyecto):
        datos={}
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        cancelar_proyecto=self.cancelar_proyecto_get(id_proyecto)
        if cancelar_proyecto:
            entidad_data=jpv_usuarios().mi_entidad(uid)
            for user in entidad_data['entidad_data'].user_ids:
                for group in user.groups_id:
                    if group.name == 'Alcaldes, Gobernadores o Alcalde Mayor':
                        responsable=user
            rendicion_question_obj=registry['jpv_conf.obj_rendicion']
            rendicion_question_id=rendicion_question_obj.search(cr,SUPERUSER_ID,[('refencia','=','cancelacion')])
            rendicion_question_data=rendicion_question_obj.browse(cr,SUPERUSER_ID,rendicion_question_id)
            rendicion_obj=registry['jpv_rnd.rendicion']
            rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',id_proyecto)])
            rendicion_data=[]
            proyectos_obj=registry['jpv_cp.carga_proyecto']
            proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, id_proyecto)
            if not proyectos_data.state == 'aprobado':
                mensaje={
                    'titulo':'No puede Cancelar',
                    'mensaje':'''Disculpe Este proyecto no puede ser cancelado, no esta aprobado''',
                    'volver':'/'
                }
                return http.request.website.render('website_apiform.mensaje', mensaje)
            datos.update({'parametros':{
                                'action':'/cancelar',
                                'titulo':'Cancelar Proyecto',
                                'template':'jpv_rendicion.avance',
                                'id_enviar':'id_guardar_rendicion_jpv',
                                'css':'danger',
                                },
                    'proyectos_data': proyectos_data,
                    'entidad_data': entidad_data['entidad_data'],
                    'rendicion_data':rendicion_data,
                    'rendicion_question_data':rendicion_question_data,
                    'dependiente': self.dependiente_a,
                    'accion_answer': self.accion_answer,
                    'dependencia': self.dependencia,
                    'categorias_select': self.categorias,
                    'field_get': self.field_get,
                    'adquisicion_get': self.adquisicion_get,
                    'name_search': self.name_search,
                    'responsable':responsable,
                    'self': self,
                    
                                })
            return panel.panel_post(datos)
        else:
            mensaje={
                    'titulo':'No puede Cancelar',
                    'mensaje':'''Disculpe Este proyecto no puede ser cancelado''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
    
    @http.route('/cancelar', auth='public', website=True, type='json')
    def cancelar_proyecto(self, **kwargs):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        campos=[]
        pregunta_obj=registry['jpv_conf.preguntas']
        campos_requeridos=kwargs['fields_required'].split('#')
        campos_requeridos.pop()
        for campo in campos_requeridos:
            campos.append({'name':campo,
                       'type':campo.split('-')[1],
                       'attr':pregunta_obj.browse(cr,SUPERUSER_ID,int(campo.split('-')[0])).nombre+','})
        errors=panel.validar().varios_campos(campos,kwargs)
        if not len(errors):
            cancelacion_id=registry['jpv_rnd.cancelacion_proyecto'].create(cr,
                                                            SUPERUSER_ID,
                                                            {'proyecto_id':int(kwargs['proyecto_id']),
                                                            'razon':kwargs[campos_requeridos[-1]]})
        else:
            return {'error_campos':errors}    
        return {'redirect':'/rendicion'} 
        
    @http.route(['/descargar/reporte_ejecucion/<int:id_proyecto>'],
                type='http', auth='user', website=True)
    def descargar_reporte_ejecucion(self,id_proyecto, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='jpv_rendicion.id_template_reporte_ejecucion_qweb_website'
        entidad_data=jpv_usuarios().mi_entidad(uid)
        nombre=''
        rendicion_obj=registry['jpv_rnd.rendicion']
        rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',id_proyecto)])
        rendicion_data=[]
        if len(rendicion_id):
            rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
        valores={
            'rendicion_data':rendicion_data,
            }
        pdf = request.registry['report'].get_pdf(cr, SUPERUSER_ID, rendicion_data, reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % (rendicion_data.proyecto_id.correlativo))
        return response
        
    @http.route(['/self'],type='json', auth='user', website=True)
    def ejecutar_metodo(self,datos):
        values={}
        for metodo in datos:
            metodo_ejec=getattr(self,metodo['metodo'])
            values[metodo['metodo']]=metodo_ejec(metodo['parametros'])
        return values 

    @http.route(['/jpvProyectosVerMas'],type='json', auth='user', website=True)
    def jpv_ver_mas_proyectos(self,**datos):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        inicio=datos['fin']
        fin=inicio+datos['page_limit']
        proyectos_data=registry['jpv_cp.carga_proyecto'].read(cr,uid,datos['lista_proyectos_ids'][inicio:fin])
        values={'inicio':inicio,
                'fin':fin,
                'proyectos_data':proyectos_data
        }
        return values

    @http.route(['/jpvProyectosVerRendir'],type='json', auth='user', website=True)
    def jpv_ver_proyectos_rendir(self,**datos):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        inicio=datos['num']
        fin=datos['fin']
        proyectos_data=registry['jpv_cp.carga_proyecto'].read(cr,uid,datos['lista_proyectos_ids'][inicio:fin])
        values={'inicio':inicio,
                'fin':fin,
                'proyectos_data':proyectos_data
        }
        return values



    def armar_botones_proyectos(self, datos):
        tr=''
        num=datos['num']
        for proyecto in datos['proyectos_data']:
            num=num+1
            tr=tr+'<tr id='+str(proyecto['id'])+' class="jpv_proyecto">'\
                    '<td>'+str(num)+'</td>'\
                    '<td><a href="/proyecto/lectura/'+str(proyecto['id'])+'" >'+proyecto['correlativo']+'</a></td>'\
                    '<td class="limitar_caracteres_'+str(num)+'" align="justify">'+proyecto['nombre_proyecto']+'</td>'\
                    '<td>'+str(self.formato_montos_get(proyecto['monto_proyecto']))+'</td>'\
                    '<td>'+str(self.armar_btn(proyecto['id'],proyecto['state']))+'</td>'\
                  '</tr>'
        return tr

    def armar_btn(self,proyecto_id,state):
        btn=''
        if state=='negado':
            btn='<button type="button"'\
                'class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-remove-circle"/>'\
                ' Negado</button>'
        elif state=='aprobado':
            btn=self.btn_aprobado(proyecto_id)
        elif state=='evaluacion':
            btn='<button type="button" '\
                  'class="btn btn-xs btn-default btn-block">'\
                  '<span class="glyphicon glyphicon-pencil" />'\
                  ' Evaluación</button>'
        elif state=='carga':
            btn='<button type="button" class="btn btn-xs btn-default btn-block"  >'\
                '<span class="glyphicon glyphicon-list-alt" />'\
                ' Borrador</button>'
        elif state=='diferido':
            btn='<button type="button" class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-refresh" />'\
                ' Diferido</button>'
        elif state=='cancelado':
            btn='<button type="button" class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-hand-down" />'\
                ' Cancelado</button>'
        elif state=='culminado':
            btn=self.btn_culminado(proyecto_id)
        return btn

    def btn_aprobado(self,proyecto_id):
        btn=''
        tiempo_validez=self.tiempo_validez_get(proyecto_id)
        cancelar_proyecto=self.cancelar_proyecto_get(proyecto_id)
        reporte_ejecucion=self.rendicion_proyecto_get(proyecto_id)
        btn="""<div class="btn-group" >
                  <button type="button" class="btn btn-xs btn-"""+tiempo_validez+""""><span class="glyphicon glyphicon-check" />Aprobado</button>
                    <button type="button" class="btn btn-xs btn-"""+tiempo_validez+""" dropdown-toggle" data-toggle="dropdown">
                        <span class="caret"></span>
                        <span class="sr-only">Desplegar menú</span>
                    </button>
                     <ul class="dropdown-menu">
                        <li>
                            <a href="/avance/"""+str(proyecto_id)+"""">
                                <h5><span class="glyphicon glyphicon-arrow-right"/>Avance</h5>
                            </a>
                        </li>
                        <li>
                            <a href="/avance/"""+str(proyecto_id)+"""/">
                                <h5><span class="glyphicon glyphicon-ok" />Culminación</h5>
                            </a>
                        </li>"""
        if cancelar_proyecto:
            btn=btn+"""<li><a href="/cancelar/"""+str(proyecto_id)+"""/">
                                <h5><span class="glyphicon glyphicon-remove" />Cancelar</h5>
                            </a>
                        </li>"""
        if reporte_ejecucion:
            btn=btn+"""<li><a href="/descargar/reporte_ejecucion/"""+str(proyecto_id)+"""/">
                                <h5><span class="glyphicon glyphicon-download" />Reporte de Ejecución</h5>
                            </a>
                        </li>"""
        btn=btn+"""</ul>
                 </div>"""

        return btn

    def btn_culminado(self,proyecto_id):
        btn=''
        btn="""<div class="btn-group" >
                  <button type="button" class="btn btn-xs btn-primary"><span class="glyphicon glyphicon-check" />Culminado</button>
                    <button type="button" class="btn btn-xs btn-primary dropdown-toggle" data-toggle="dropdown">
                        <span class="caret"></span>
                        <span class="sr-only">Desplegar menú</span>
                    </button>
                     <ul class="dropdown-menu">
                        <li>
                            <a href="/avance/consultar/"""+str(proyecto_id)+"""">
                                <h5><span class="glyphicon glyphicon-arrow-right"/>Consultar Avances</h5>
                            </a>
                        </li>
                        <li>
                            <a href="/descargar/reporte_ejecucion/"""+str(proyecto_id)+"""/">
                                <h5><span class="glyphicon glyphicon-ok" />Reporte de Ejecución</h5>
                            </a>
                        </li>"""
        btn=btn+"""</ul>
                 </div>"""

        return btn

    def proyectos_x_rendir(self,parametros):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        proyectos_x_rendir=[]
        entidad_data=jpv_usuarios().mi_entidad(uid)
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        proyectosr_ids=proyecto_obj.search(cr,
                                                    SUPERUSER_ID,
                                                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                                                    ('state','=','aprobado')])
        for id_proyecto in proyectosr_ids:
            actualizado=self.tiempo_validez_bol_get(id_proyecto)
            if not actualizado:
                proyectos_x_rendir.append(id_proyecto)
        return proyectos_x_rendir

    @http.route(['/jpvProyectosxRendirListaEstadistica'],type='json', auth='user', website=True)
    def proyectos_x_rendir_lista(self,**parametros):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        proyectos_x_rendir=[]
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        proyectosr_ids=proyecto_obj.search(cr,
                                                    SUPERUSER_ID,
                                                    [('partner_id','=',int(parametros['entidad_id'])),
                                                    ('state','=','aprobado')])
        for id_proyecto in proyectosr_ids:
            actualizado=self.tiempo_validez_bol_get(id_proyecto)
            if not actualizado:
                proyectos_x_rendir.append(id_proyecto)
        proyectos_data=proyecto_obj.read(cr,uid,proyectos_x_rendir,['nombre_proyecto',
                                                                                'correlativo',
                                                                                'monto_proyecto',
                                                                                'state'])
        return proyectos_data

    @http.route(['/jpvProyectosxRendirEstadistica'],type='json', auth='user', website=True)
    def proyectos_x_rendir_c(self,**parametros):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        proyectos_x_rendir=[]
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        if self.entidad_id:
            parametros['entidad_id']=self.entidad_id
        proyectosr_ids=proyecto_obj.search(cr,
                                            SUPERUSER_ID,
                                            [('partner_id','=',int(parametros['entidad_id'])),
                                            ('state','=','aprobado')])
        cantidad_proyectos=len(proyectosr_ids)
        for id_proyecto in proyectosr_ids:
            actualizado=self.tiempo_validez_bol_get(id_proyecto)
            if not actualizado:
                proyectos_x_rendir.append(id_proyecto)
        cantidad_proyectos=len(proyectosr_ids)-len(proyectos_x_rendir)
        self.entidad_id=""
        return {'cant_proyectos_actualizados':cantidad_proyectos,
                'cant_proyectosXRendir':len(proyectos_x_rendir)
        }

    def proyectos_x_rendir_erp(self,parametros):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        proyectos_x_rendir=[]
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        if self.entidad_id:
            parametros['entidad_id']=self.entidad_id
        proyectosr_ids=proyecto_obj.search(cr,
                                            SUPERUSER_ID,
                                            [('partner_id','=',int(parametros['entidad_id'])),
                                            ('state','=','aprobado')])
        cantidad_proyectos=len(proyectosr_ids)
        for id_proyecto in proyectosr_ids:
            actualizado=self.tiempo_validez_bol_get(id_proyecto)
            if not actualizado:
                proyectos_x_rendir.append(id_proyecto)
        cantidad_proyectos=len(proyectosr_ids)-len(proyectos_x_rendir)
        self.entidad_id=""
        return {'proyectos_aprobados':len(proyectosr_ids),
                'cant_proyectos_actualizados':cantidad_proyectos,
                'cant_proyectosXRendir':len(proyectos_x_rendir)
        }

    def proyectos_x_rendir_movil(self,parametros):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        proyectos_x_rendir=[]
        rendicionesxvencer=[]
        proyectos_actualizados=[]
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        if parametros.has_key('periodo'):
            periodo_ids=registry['jpv_plf.periodos'].search(cr,SUPERUSER_ID,[('periodo_fiscal','=',parametros['periodo'])])
        else:
            periodo_ids=registry['jpv_plf.periodos'].search(cr,SUPERUSER_ID,[])
        if self.entidad_id:
            parametros['entidad_id']=self.entidad_id
        proyectosr_ids=proyecto_obj.search(cr,
                                            SUPERUSER_ID,
                                            [('partner_id','=',int(parametros['entidad_id'])),
                                            ('state','=','aprobado'),
                                            ('periodo_id','in',periodo_ids)])
        cantidad_proyectos=len(proyectosr_ids)
        for id_proyecto in proyectosr_ids:
            actualizado=self.tiempo_validez_get(id_proyecto,int(parametros['uid']))
            if actualizado=='danger':
                proyectos_x_rendir.append(id_proyecto)
            elif actualizado=='warning':
                rendicionesxvencer.append(id_proyecto)
            elif actualizado=='success':
                proyectos_actualizados.append(id_proyecto)
        cantidad_proyectos=len(proyectosr_ids)-len(proyectos_x_rendir)
        self.entidad_id=""
        return {'Rendiciones vigentes':len(proyectos_actualizados),
                'Rendiciones vencidas':len(proyectos_x_rendir),
                'Rendiciones por vencer':len(rendicionesxvencer),
                'proyectos_x_rendir_ids':proyectos_x_rendir,
                'rendicionesxvencer_ids':rendicionesxvencer,
                'proyectos_actualizados_ids':proyectos_actualizados
        }


class jpv_carga_proyecto_controlador_inherit(ecp.jpv_cp_carga_proyecto_controlador):
    def armar_btn(self,proyecto_id,state):
        btn=''
        if state=='negado':
            btn='<button type="button"'\
                'class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-remove-circle"/>'\
                ' Negado</button>'
        elif state=='aprobado':
            btn=rendicion().btn_aprobado(proyecto_id)
        elif state=='evaluacion':
            btn='<button type="button" '\
                  'class="btn btn-xs btn-default btn-block">'\
                  '<span class="glyphicon glyphicon-pencil" />'\
                  ' Evaluación</button>'
        elif state=='carga':
            btn='<button type="button" class="btn btn-xs btn-default btn-block"  >'\
                '<span class="glyphicon glyphicon-list-alt" />'\
                ' Borrador</button>'
        elif state=='diferido':
            btn='<button type="button" class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-refresh" />'\
                ' Diferido</button>'
        elif state=='cancelado':
            btn='<button type="button" class="btn btn-xs btn-default btn-block" >'\
                '<span class="glyphicon glyphicon-hand-down" />'\
                ' Cancelado</button>'
        elif state=='culminado':
            btn=rendicion().btn_culminado(proyecto_id)
        return btn

    
