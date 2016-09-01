# -*- coding: utf-8 -*-

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import datetime, date, time, timedelta

from openerp.addons.ept_rendicion.controladores import ept_rnd_rendicion_c
self_rendicion=ept_rnd_rendicion_c.rendicion()
_logger = logging.getLogger(__name__)

class ept_cp_carga_proyecto_controlador(http.Controller):
    
    def instanciar_objetos(self,objeto,parametro):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        objeto = registry.get(objeto)
        ids = objeto.search(cr,SUPERUSER_ID,parametro,context=context)
        data = objeto.browse(cr,SUPERUSER_ID,ids,context=context)
        return data
        
    def campos_solo_lectura(self,id_proyecto,ciclo_id,campo):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry.get('ept_plf.periodos')
        carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(id_proyecto)),])
        
        campo_migracion=['obra_civil','equipos','maquinaria','materiales_consumo','vehiculos','tipo_obra','cantidad_estimada_obra','unidad_medicion_obra',
                          'equipos_ids','maquinaria_ids','materiales_ids','vehiculos_ids']
        
        #~ quitar despues de la migracion
       
        #~ if len(carga_proyecto_data['foto_id'])==0:
            #~ if campo in campo_migracion:
                #~ disabled=''
                #~ return disabled
        #~ 
        #~ if carga_proyecto_data['avance']==False and carga_proyecto_data['periodo_id'].periodo_fiscal==str(2015) and carga_proyecto_data['proyect_mantenimiento']==False:
            #~ if campo in campo_migracion:
                #~ disabled=''
                #~ return disabled
            #~ else:
                #~ disabled='disabled'
                #~ return disabled
        #~ if carga_proyecto_data['avance']==False and carga_proyecto_data['periodo_id'].periodo_fiscal==str(2015) and carga_proyecto_data['proyect_mantenimiento']==True:
            #~ disabled='disabled'
            #~ return disabled
            #~ 
        #~ if carga_proyecto_data['avance']==True and carga_proyecto_data['periodo_id'].periodo_fiscal==str(2015) and carga_proyecto_data['proyect_mantenimiento']==False:
            #~ disabled='disabled'
            #~ return disabled
            #~ 
        #~ if carga_proyecto_data['avance']==True and carga_proyecto_data['periodo_id'].periodo_fiscal==str(2015) and carga_proyecto_data['proyect_mantenimiento']==True:
            #~ disabled='disabled'
            #~ return disabled
        
        
        disabled=''
        if carga_proyecto_data['state']=='carga':
            disabled=''
        if carga_proyecto_data['state']=='negado' or carga_proyecto_data['state']=='cancelado' or carga_proyecto_data['state']=='evaluacion' or carga_proyecto_data['state']=='culminado':
            disabled='disabled'
        if carga_proyecto_data['state']=='aprobado' or carga_proyecto_data['state']=='diferido':
            actividad='REPARACIÓN DE PROYECTOS'
            reparacion=periodos_obj.plf_control_actividades(cr, uid, [],int(carga_proyecto_data['partner_id']),actividad,int(ciclo_id))
            if 'periodo' in reparacion.keys():
                disabled=''
            else:
                disabled='disabled'
            if campo=='monto_proyecto':
                disabled=''
                return
            if carga_proyecto_data['avance']==True:
                disabled='disabled'
            #~ solicitudes_obj = registry.get('ept_cp.solicitud_editar_campos')
            #~ solicitudes_ids = solicitudes_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',int(id_proyecto)),('state','=','aprobado')],context=context)
            #~ solicitudes_data=solicitudes_obj.browse(cr,SUPERUSER_ID,solicitudes_ids,context=context)
            #~ if len (solicitudes_ids):
                #~ for id_campo in solicitudes_data['campos_ids']:
                    #~ if str(id_campo.name)==(campo):
                        #~ disabled=''
        return disabled
    
    def ocultar_boton_crear(self,partner_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        hoy=date.today()
        format="%Y"
        periodos_obj = registry.get('ept_plf.periodos')
        anio=hoy.strftime(format)
        actividad="CARGA DE PROYECTOS"
        entidades_data=self.instanciar_objetos('ept_ent.entidades',[('parent_id','=',int(partner_id)),])
        carga=periodos_obj.plf_control_actividades(cr, uid, [],int(partner_id),actividad,None,anio)
        if 'periodo' in carga.keys():
            if entidades_data['cargar_proyectos']==True:
                return ''
            else:
                return 'hidden'
        else:
            return 'hidden'
            
    def ocultar_boton_editar(self,partner_id,ciclo,state,proyecto_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry.get('ept_plf.periodos')
        actividad="REPARACIÓN DE PROYECTOS"
        
        carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),])
        
        entidades_data=self.instanciar_objetos('ept_ent.entidades',[('parent_id','=',int(partner_id)),])
        list_user=[]
        for usuario in entidades_data['user_ids']:
            if usuario.id==uid:
                list_user.append(usuario.id)
        if len(list_user)==0:
            hidden='hidden'
            return hidden
        
        if len(carga_proyecto_data['foto_id'])==0:
            hidden=''
            return hidden
        
        
        #~ if carga_proyecto_data['avance']==True and carga_proyecto_data['periodo_id'].periodo_fiscal==str(2015):
            #~ return 'hidden'
        
        
        reparacion=periodos_obj.plf_control_actividades(cr, uid, [],int(partner_id),actividad,int(ciclo))
        if state=='carga':
            return ''
        if 'periodo' in reparacion.keys():
            return ''
        else:
            if state=='aprobado' or state=='diferido':
                return ''
            else:
                return 'hidden' 
                
    def ocultar_boton_aumento(self,proyecto_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),])
        return True
    
    def ocultar_elementos(self,id_proyecto,campo):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        #~ para la migracion
        carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(id_proyecto)),('editar_migracion','=','True')])
        
        if len(carga_proyecto_data)==1:
            hidden=''
            return hidden
        
        periodos_obj = registry.get('ept_plf.periodos')
        carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(id_proyecto))])
        hidden=''
        if carga_proyecto_data['state']=='carga':
            hidden=''
        if carga_proyecto_data['state']=='negado' or carga_proyecto_data['state']=='cancelado' or carga_proyecto_data['state']=='evaluacion':
            hidden='hidden'
        if carga_proyecto_data['state']=='aprobado' or carga_proyecto_data['state']=='diferido':
            actividad='REPARACIÓN DE PROYECTOS'
            reparacion=periodos_obj.plf_control_actividades(cr, uid, [],int(carga_proyecto_data['partner_id']),actividad,)
            if 'periodo' in reparacion.keys():
                hidden=''
            else:
                hidden='hidden'
        return hidden
    
    def ocultar_proyecto_editado(self,proyecto_id):
        proyecto_data=self.instanciar_objetos('ept_mig.proyectos_migrados',[('proyectos_id','=',int(proyecto_id)),('actualizado','=',True)])
        if len(proyecto_data)==1:
            url='/ept_carga_proyectos/static/src/img/agt_action_success .png'
            return url
        else:
            return
    
    @http.route(['/proyecto'], 
            type='http', auth="user", website=True)
    def carga_proyecto(self):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        datos={}
        entidades_obj = registry.get('ept_ent.entidades')
        proyectos_migrados_obj = registry.get('ept_mig.proyectos_migrados')
        entidades_ids = entidades_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uid)],
                                        context=context)
        if len(entidades_ids)==1:
            ept_carga_proyecto=registry.get('ept_cp.carga_proyecto')
            entidades_data = entidades_obj.browse(
                                                cr,
                                                SUPERUSER_ID,
                                                entidades_ids,
                                                context=context)
            
            gobernacion='false'
            alcaldia='false'
            dict_montos_asoci={}
            partner_asociados_data=[]
            alcaldias_asociadas={}
            if entidades_data['tipo_entidad_id'].name=='GOBERNACIÓN':
                gobernacion="gobernacion"
                list_alcaldia=[]
                for alcaldia in entidades_data['entidades_ids']:
                    list_alcaldia.append(int(alcaldia.parent_id))
                
                partner_asociados_data=self.instanciar_objetos('res.partner',[('id','in',list_alcaldia)],)
            proyectos_gobenacion_data=[]
            if entidades_data['tipo_entidad_id'].name=='ALCALDÍA':
                alcaldia="alcaldia"
                for est in entidades_data['estado_ids']:
                    estado=est[0].id
                for mun in entidades_data['municipio_ids']:
                    municipio=mun[0].id
                proyectos_gobenacion_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('estado_id','=',int(estado)),('municipio_id','=',int(municipio)),('state','=','aprobado'),('partner_id','!=',int(entidades_data['parent_id']))])
                
                for proyecto in proyectos_gobenacion_data:
                    monto_aso='%.2f' % proyecto.monto_proyecto
                    monto_proyecto_aso=str(monto_aso).replace('.',',')
                    dict_montos_asoci[proyecto.id]=monto_proyecto_aso

                #~ proyectos_alcaldias_ids=ept_carga_proyecto.search(cr,uid,[('partner_id','in',list_alcaldia),('state','=','aprobado')])
                #~ proyectos_alcaldias_asociadas_data=ept_carga_proyecto.browse(cr,uid,proyectos_alcaldias_ids)
                #~ for alc_asoci in proyectos_alcaldias_asociadas_data:
                    #~ monto_aso='%.2f' % alc_asoci.monto_proyecto
                    #~ monto_proyecto_aso=str(monto_aso).replace('.',',')
                    #~ dict_montos_asoci[alc_asoci.id]=monto_proyecto_aso
            dict_montos={}
            proyectos_ids= proyectos_migrados_obj.comprobar_actualizacion_ids(cr,SUPERUSER_ID,[],context,entidades_data)
            mensaje_migrados=''
            rendir=True
            if  proyectos_ids:
                rendir=False
                mensaje_migrados=  u"¡Alerta! Para cargar proyectos de este periodo usted debe: \n "\
                                    "1 - REGISTRAR LAS METAS de los proyectos que están en la siguiente lista. \n"\
                                    " 2 - Debe hacer los avances correspondientes para dichos proyectos."
            if not proyectos_ids:
                proyectos_ids=ept_carga_proyecto.search(cr,uid,[('partner_id','=',int(entidades_data['parent_id']))],limit=30)
            carga_proyecto_data=ept_carga_proyecto.browse(cr,uid,proyectos_ids)
            proyectos_ids=[]
            for id_proyecto in carga_proyecto_data:
                proyectos_ids.append(id_proyecto.id)
                monto_proyecto='%.2f' % id_proyecto.monto_proyecto
                monto_proyecto=str(monto_proyecto).replace('.',',')
                dict_montos[id_proyecto.id]=monto_proyecto
            partner=int(entidades_data['parent_id'])

            datos={'parametros':{
                            'titulo':'Proyectos '+entidades_data['name'],
                            'template':'ept_carga_proyectos.proyecto_template',
                            },
                            'carga_proyecto_data':carga_proyecto_data,
                            'proyectos_ids':proyectos_ids,
                            'dict_montos':dict_montos,
                            'dict_montos_asoci':dict_montos_asoci,
                            'self':ept_rnd_rendicion_c.rendicion(),
                            'ocultar_boton_crear':self.ocultar_boton_crear,
                            #~ 'proyectos_alcaldias_asociadas_data':proyectos_alcaldias_asociadas_data,
                            'partner_asociados_data':partner_asociados_data,
                            'proyectos_gobenacion_data':proyectos_gobenacion_data,
                            #~ 'dict_montos_asoci':dict_montos_asoci,
                            'partner_id':partner,
                            'gobernacion':gobernacion,
                            'alcaldia':alcaldia,
                            'mensaje_migrados':mensaje_migrados,
                            'rendir':rendir,
                            'ocultar_proyecto_editado':self.ocultar_proyecto_editado,
                            'domain':"proyecto"
                            }
            return panel.panel_lista(datos)
            
        mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
        
    @http.route(['/proyecto/lectura/<int:proyecto_id>'], type='http', auth="user", website=True)
    def proyectos_solo_lectura(self,proyecto_id):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        entidades_obj = registry.get('ept_ent.entidades')
        entidades_ids = entidades_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uid)],
                                        context=context)
        entidades_data=entidades_obj.browse(cr,uid,entidades_ids)
        entidad=str(entidades_data['name'])
        ept_carga_proyecto=registry.get('ept_cp.carga_proyecto')  #agrgar cambio
        acceso=False
        if len(entidades_ids)==1:
            carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),('partner_id','=',int(entidades_data['parent_id']))])
            if len(carga_proyecto_data)>0:
                acceso=True
            if entidades_data['tipo_entidad_id']['name']=='GOBERNACIÓN':
                list_alcaldia=[]
                for alcaldia in entidades_data['entidades_ids']:
                    list_alcaldia.append(int(alcaldia.parent_id))
                proyectos_alcaldias_ids=ept_carga_proyecto.search(cr,uid,[('partner_id','in',list_alcaldia)])
                proyectos_alcaldias_asociadas_data=ept_carga_proyecto.browse(cr,uid,proyectos_alcaldias_ids)
                list_alcaldia_id=[]
                for i in proyectos_alcaldias_asociadas_data:
                    list_alcaldia_id.append(int(i))
                if int(proyecto_id) in list_alcaldia_id:
                    acceso=True
                    #~ carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),],)
                    #~ entidad=carga_proyecto_data['partner_id'].name
            
            
            
            if entidades_data['tipo_entidad_id']['name']=='ALCALDÍA':
                list_proyec_gobern=[]
                for est in entidades_data['estado_ids']:
                    estado=est[0].id
                for mun in entidades_data['municipio_ids']:
                    municipio=mun[0].id
                proyectos_gobenacion_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('estado_id','=',int(estado)),('municipio_id','=',int(municipio)),('state','=','aprobado')])
                for proyecto in proyectos_gobenacion_data:
                    list_proyec_gobern.append(int(proyecto))
                if int(proyecto_id) in list_proyec_gobern:
                    acceso=True
            carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),],)
            entidad=carga_proyecto_data['partner_id'].name
            if acceso==True:
                
                
                rendicion_obj=registry['ept_rnd.rendicion']
                rendicion_id=rendicion_obj.search(cr,SUPERUSER_ID,[('proyecto_id','=',int(proyecto_id))])
                rendicion_data=[]
                if len(rendicion_id):
                    rendicion_data=rendicion_obj.browse(cr,SUPERUSER_ID,rendicion_id)
                partner=int(entidades_data['parent_id'])
                dict_montos={}  
                for id_proyecto in carga_proyecto_data:
                    monto_proyecto='%.2f' % id_proyecto.monto_proyecto
                    monto_proyecto=str(monto_proyecto).replace('.',',')
                    dict_montos[id_proyecto.id]=monto_proyecto
                datos={'parametros':{
                                'titulo':'Proyecto '+str(entidad),
                                'template':'ept_carga_proyectos.proyecto_vista_solo_lectura',
                                'url_boton_list':'/proyecto',
                                'remover_btn_enviar':'si',
                                'id_form':'form3',
                                },
                                'partner':str(partner),
                                'carga_proyecto_data':carga_proyecto_data,
                                'dict_montos':dict_montos,
                                'ocultar_boton_crear':self.ocultar_boton_crear,
                                'ocultar_boton_editar':self.ocultar_boton_editar,
                                'rendicion_data':rendicion_data,
                                'self':self_rendicion
                                    }
                return panel.panel_post(datos)
            else:
                mensaje={
                        'titulo':'Aviso!',
                        'mensaje':'''Disculpe, Este proyecto no pertenece a la entidad a la cual usted esta asociado,
                                    Comuníquese con el administrador del sistema''',
                        'volver':'/'
                    }
        else:
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
        
    @http.route(['/proyecto/editar/<int:proyecto_id>'], type='http', auth="user", website=True)
    def proyecto_editar(self,proyecto_id):
        
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        entidades_obj = registry.get('ept_ent.entidades')
        entidades_ids = entidades_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uid)],
                                        context=context)
        entidades_data=self.instanciar_objetos('ept_ent.entidades',[('user_ids','in',uid)])
        if len(entidades_ids)==1:
        
            carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
            
            carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(proyecto_id)),('partner_id','=',int(entidades_data['parent_id']))])
            
            if len(carga_proyecto_data)>0:
                tipo_sectores_data=self.instanciar_objetos('ept_cp.tipo_sectores',[('parent_id','=',False)])
                
                categoria_data=self.instanciar_objetos('ept_cp.tipo_sectores',[('parent_id','=',int(carga_proyecto_data['tipo_sector_id']))])
                
                subcategoria_data=self.instanciar_objetos('ept_cp.tipo_sectores',[('parent_id','=',int(carga_proyecto_data['categoria_id']))])
                
                partner=int(entidades_data['parent_id'])
                
                cuenta_data=self.instanciar_objetos('ept.cuentas',[('tipo_cuenta_id.name','=','PLAN DE INVERSIÓN'),('partner_id','=',int(partner))])
                
                equipos_data=self.instanciar_objetos('ept_cp.montos_minimos_equipos',[])
                
                maquinaria_data=self.instanciar_objetos('ept_cp.montos_minimos_maquinaria',[])
                
                vehiculo_uso_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_uso',[])
                
                vehiculo_caract_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_caracteristicas',[])
                
                vehiculo_tipo_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_tipo',[])
                
                material_data=self.instanciar_objetos('ept_cp.montos_minimos_materiales_consumo',[])
                
                semoviente_data=self.instanciar_objetos('ept_cp.semovientes',[])
                
                semoviente_grupo_data=self.instanciar_objetos('ept_cp.semovientes_grupo_etario',[])
                
                semoviente_uso_data=self.instanciar_objetos('ept_cp.semovientes_uso',[])
                
                semoviente_proposito_data=self.instanciar_objetos('ept_cp.semovientes_proposito',[])
                
                unidad=carga_proyecto_obj.cp_filtrar_unidades_medidas (cr, uid, 
                                                                            [], 
                                    int(carga_proyecto_data['subcategoria_id']),
                                    str(carga_proyecto_data['tipo_obra']))
                unidad= unidad.values()[0]
                unidad=unidad[0]
                unidades_data=self.instanciar_objetos('ept_cp.unidades_obra_civil',[('id','in',unidad[2])])
                
                fecha_inicio=carga_proyecto_data['fecha_inicio'].split('-')
                fecha_inicio=fecha_inicio[2]+'-'+fecha_inicio[1]+'-'+fecha_inicio[0]
                fecha_fin=carga_proyecto_data['fecha_fin'].split('-')
                fecha_fin=fecha_fin[2]+'-'+fecha_fin[1]+'-'+fecha_fin[0]
                
                monto_proyecto=carga_proyecto_data['monto_proyecto']
                monto_proyecto=str(monto_proyecto).split('.')
                if len(monto_proyecto[1])==1:
                    monto_proyecto=monto_proyecto[0]+','+monto_proyecto[1]+'0'
                else:
                    monto_proyecto=monto_proyecto[0]+','+monto_proyecto[1]
                monto=carga_proyecto_obj.cp_monto_disponible(cr,uid,[],cuenta_data['id'],context=None)
                monto=monto.values()[0].values()[0]
                monto='%.2f' % monto
                monto_total=str(monto).replace('.',',')
                entidad_datos=carga_proyecto_obj.cp_filtro_estados(cr,uid,[],
                                            int(carga_proyecto_data['partner_id']),context)
                estado_data=entidad_datos.values()[0].values()[0]
                estado_data=estado_data[0]
                estado_data=estado_data[2]
                estado_data=self.instanciar_objetos('ept_ent.estados',[('id','in',estado_data)])
                
                municipios_datos=carga_proyecto_obj.cp_filtro_municipios(
                                        cr,uid,[],
                                        int(carga_proyecto_data['partner_id']),
                                        int(carga_proyecto_data['estado_id']),
                                        'campo',context)
                municipios_datos=municipios_datos.values()[0].values()[2]
                municipios_datos=municipios_datos[0]
                municipios_datos=municipios_datos[2]
                municipio_data=self.instanciar_objetos('ept_ent.municipios',[('id','in',municipios_datos)])
                
                parroquia_data=self.instanciar_objetos('ept_ent.parroquias',[('municipio_id','=',int(carga_proyecto_data['municipio_id']),)])
                
                id_huso=carga_proyecto_obj.cp_filtro_municipios(cr,uid,[],int(carga_proyecto_data['partner_id']),int(carga_proyecto_data['estado_id']),'campo')
                id_huso=id_huso['domain']
                id_huso=id_huso['huso_id'][0]
                id_huso=id_huso[2]
                huso_data=self.instanciar_objetos('ept_ent.husos',[('id','in',id_huso)],)
                
                monto_manteni_disp=self.calculo_monto_mantenimiento(int(carga_proyecto_data['periodo_id']),int(carga_proyecto_data['partner_id']))
                monto_manteni_disp=str(monto_manteni_disp).replace('.',',')
                
                rendicion_data=self.instanciar_objetos('ept_rnd.rendicion',[('proyecto_id','=',int(proyecto_id),)])
                
                monto_rendido=rendicion_data['monto_gastado']
                if monto_rendido==False:
                    monto_rendido='0,00'
                
                datos={'parametros':{
                                'titulo':'Proyecto '+str(entidades_data['name']),
                                'template':'ept_carga_proyectos.proyecto_vista_editar',
                                'url_boton_list':'/proyecto',
                                'id_form':'form2',
                                'remover_btn_enviar':'si',
                                'action':'/proyecto/editar/guardar',
                                },
                                'partner':str(partner),
                                'carga_proyecto_data':carga_proyecto_data,
                                'tipo_sectores_data':tipo_sectores_data,
                                'monto_total':monto_total,
                                'monto_proyecto':monto_proyecto,
                                'fecha_inicio':fecha_inicio,
                                'fecha_fin':fecha_fin,
                                'categoria_data':categoria_data,
                                'subcategoria_data':subcategoria_data,
                                'unidades_data':unidades_data,
                                'equipos_data':equipos_data,
                                'maquinaria_data':maquinaria_data,
                                'vehiculo_uso_data':vehiculo_uso_data,
                                'vehiculo_caract_data':vehiculo_caract_data,
                                'vehiculo_tipo_data':vehiculo_tipo_data,
                                'material_data':material_data,
                                'semoviente_data':semoviente_data,
                                'semoviente_grupo_data':semoviente_grupo_data,
                                'semoviente_uso_data':semoviente_uso_data,
                                'semoviente_proposito_data':semoviente_proposito_data,
                                'estado_data':estado_data,
                                'municipio_data':municipio_data,
                                'parroquia_data':parroquia_data,
                                'huso_data':huso_data,
                                'campos_solo_lectura':self.campos_solo_lectura,
                                'ocultar_boton_aumento':self.ocultar_boton_aumento,
                                'ocultar_elementos':self.ocultar_elementos,
                                'monto_manteni_disp':monto_manteni_disp,
                                'monto_rendido':monto_rendido,
                                    }
                return panel.panel_post(datos)
            else:
                mensaje={
                        'titulo':'Aviso!',
                        'mensaje':'''Disculpe, Este proyecto no pertenece a la entidad a la cual usted esta asociado,
                                    Comuníquese con el administrador del sistema''',
                        'volver':'/'
                    }
        else:
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
    
    @http.route(['/proyecto/crear'], 
            type='http', auth="user", website=True)    
    def crear_proyecto(self):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        
        entidades_obj = registry.get('ept_ent.entidades')
        entidades_ids = entidades_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uid)],
                                        context=context)
        if len(entidades_ids)==1:
            entidades_data = entidades_obj.browse(
                                                    cr,
                                                    SUPERUSER_ID,
                                                    entidades_ids,
                                                    context=context)
            plf_periodos_objeto=registry.get('ept_plf.periodos')
            actividad='CARGA DE PROYECTOS'
            autorizacion_fechas=plf_periodos_objeto.plf_control_actividades(
                                                                         cr, 
                                                                    uid, [],
                                                    int(entidades_data['parent_id']),
                                                                 actividad,)
            if 'message' not in autorizacion_fechas.keys():
                periodo_id=int(autorizacion_fechas['periodo'])
                tipo_sectores_data=self.instanciar_objetos('ept_cp.tipo_sectores',[('parent_id','=',False)])
                
                categ_subca_data=self.instanciar_objetos('ept_cp.tipo_sectores',[])
                
                partner_data=self.instanciar_objetos('res.partner',[('id','=',int(entidades_data['parent_id']))])
                
                cuenta_data=self.instanciar_objetos('ept.cuentas',[('tipo_cuenta_id.name','=','PLAN DE INVERSIÓN'),('partner_id','=',int(partner_data['id']))])
                
                equipos_data=self.instanciar_objetos('ept_cp.montos_minimos_equipos',[])

                maquinaria_data=self.instanciar_objetos('ept_cp.montos_minimos_maquinaria',[])
                
                vehiculo_uso_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_uso',[])
                
                material_data=self.instanciar_objetos('ept_cp.montos_minimos_materiales_consumo',[])
                
                semoviente_data=self.instanciar_objetos('ept_cp.semovientes',[])
                
                carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
                
                monto=carga_proyecto_obj.cp_monto_disponible(cr,uid,[],cuenta_data['id'],context=None)
                monto=monto.values()[0].values()[0]
                if monto!=False:
                    monto='%.2f' % monto
                    monto=str(monto).split('.')
                    monto_total=monto[0]+','+monto[1]
                else:
                    mensaje={
                    'titulo':'Error!',
                    'mensaje':'''No tiene asignado recursos para este Periodo Fiscal,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/proyecto'
                        }
                    return http.request.website.render('website_apiform.mensaje', mensaje)
                entidad_datos=carga_proyecto_obj.cp_filtro_estados(cr,uid,[],
                                                             int(entidades_data['parent_id']),context)
                estado_data=entidad_datos.values()[0].values()[0]
                estado_data=estado_data[0]
                estado_data=estado_data[2]
                
                estado_data=self.instanciar_objetos('ept_ent.estados',[('id','in',estado_data)])
                
                monto_manteni_disp=self.calculo_monto_mantenimiento(int(periodo_id),int(partner_data['id']))
                monto_manteni_disp=str(monto_manteni_disp).replace('.',',')
                
                datos={'parametros':{
                            'titulo':'Registrar Proyecto '+partner_data['name'],
                            'template':'ept_carga_proyectos.registrar_proyecto_template',
                            'url_boton_list':'/proyecto',
                            'css':'info',
                            'id_form':'formcrearproyecto',
                            'id_enviar':'enviar_proyecto',
                            'action':'/proyecto/crear/guardar',
                            },
                            'partner_data':partner_data,
                            'cuenta_data':cuenta_data,
                            'monto_total':monto_total,
                            'tipo_sectores_data':tipo_sectores_data,
                            'categ_subca_data':categ_subca_data,
                            'estado_data':estado_data,
                            'equipos_data':equipos_data,
                            'maquinaria_data':maquinaria_data,
                            'vehiculo_uso_data':vehiculo_uso_data,
                            'material_data':material_data,
                            'semoviente_data':semoviente_data,
                            'periodo_id':periodo_id,
                            'monto_manteni_disp':monto_manteni_disp,
                            
                            }
                return panel.panel_post(datos)
            else:
                mensaje={
                    'titulo':'Sin permiso de carga de proyectos',
                    'mensaje':'''NO esta habilitada la opción de cargar proyectos,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/proyecto'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
                
        mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
        return http.request.website.render('website_apiform.mensaje', mensaje)
        
        
    @http.route('/proyecto/crear/categoria',type='json', auth="public", website=True)
    def buscar_categoria(self,id, **kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        ids_categ = []
        name_categ = []
        
        categ_data=self.instanciar_objetos('ept_cp.tipo_sectores',[('parent_id','=',int(id))])
        for ids in categ_data:
            name_categ.append(ids.name) 
            ids_categ.append(ids.id)
        valores=[]
        valores.append(name_categ)
        valores.append(ids_categ)
        return  valores
        
    @http.route('/proyecto/crear/municipio',type='json', auth="public", website=True)
    def buscar_municipios(self,id_estado,id_entidad,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        municipios_datos=carga_proyecto_obj.cp_filtro_municipios(
                                                        cr,uid,[],
                                                        int(id_entidad),
                                                        int(id_estado),
                                                        'campo',context)
        municipios_datos=municipios_datos.values()[0].values()[2]
        municipios_datos=municipios_datos[0]
        municipios_datos=municipios_datos[2]
        
        municipio_data=self.instanciar_objetos('ept_ent.municipios',[('id','in',municipios_datos)])
        
        name_municipio=[]
        ids_municipio=[]
        valores=[]
        for i in municipio_data:
            name_municipio.append(i.municipio) 
            ids_municipio.append(i.id)
        valores.append(name_municipio)
        valores.append(ids_municipio)
        return  valores
    
    
    @http.route('/proyecto/alcaldias_asociadas',type='json', auth="public", website=True)
    def buscar_proyectos_asociados(self,id_partner,**kw):
        list_proyect=[]
        list_proyectos_asociados=[]
        proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('partner_id','=',int(id_partner)),('state','=','aprobado')])
        for proyecto in proyecto_data:
            list_proyect.append(proyecto.correlativo)
            list_proyect.append(proyecto.nombre_proyecto)
            monto='%.2f' % proyecto.monto_proyecto
            monto_proyecto_aso=str(monto).replace('.',',')
            list_proyect.append(monto_proyecto_aso)
            list_proyect.append(proyecto.state)
            list_proyect.append(proyecto.id)
            list_proyectos_asociados.append(list_proyect)
            list_proyect=[]
        return  list_proyectos_asociados
    
    
    @http.route('/proyecto/crear/parroquia',type='json', auth="public", website=True)
    def buscar_parroquias(self,id_municipio,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        
        parroquia_data=self.instanciar_objetos('ept_ent.parroquias',[('municipio_id','=',int(id_municipio))])
        
        name_parroquia=[]
        ids_parroquia=[]
        valores=[]
        for i in parroquia_data:
            name_parroquia.append(i.parroquia) 
            ids_parroquia.append(i.id)
        valores.append(name_parroquia)
        valores.append(ids_parroquia)
        return  valores
        
        
    @http.route('/proyecto/crear/caracateristica_vehiculo',type='json', auth="public", website=True)
    def buscar_caracteristica_vehiculo(self,id_uso,**kw):
        
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        
        vehiculo_caract_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_caracteristicas',[('uso_id','=',int(id_uso))])
        
        name_caracteristica=[]
        ids_caracteristica=[]
        valores=[]
        for i in vehiculo_caract_data:
            name_caracteristica.append(i.caracteristicas) 
            ids_caracteristica.append(i.id)
        valores.append(name_caracteristica)
        valores.append(ids_caracteristica)
        
        return  valores
        
    @http.route('/proyecto/crear/tipo_vehiculo',type='json', auth="public", website=True)
    def buscar_tipo_vehiculo(self,id_tipo,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        
        vehiculo_tipo_data=self.instanciar_objetos('ept_cp.montos_minimos_vehiculo_tipo',[('caracteristicas_id','=',int(id_tipo))])

        name_tipo=[]
        ids_tipo=[]
        valores=[]
        for i in vehiculo_tipo_data:
            name_tipo.append(i.tipo) 
            ids_tipo.append(i.id)
        valores.append(name_tipo)
        valores.append(ids_tipo)
        return  valores
        
        
    @http.route('/proyecto/crear/grupo_semoviente',type='json', auth="public", website=True)
    def buscar_grupo_semoviente(self,id_tipo,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        semoviente_data_data=[]
        if id_tipo!='':
            semoviente_data_data=self.instanciar_objetos('ept_cp.semovientes_grupo_etario',[('especies_id','=',int(id_tipo))])
        name_grupo=[]
        ids_grupo=[]
        valores=[]
        for i in semoviente_data_data:
            name_grupo.append(i.grupo_etario) 
            ids_grupo.append(i.id)
        valores.append(name_grupo)
        valores.append(ids_grupo)
        return  valores
        
    @http.route('/proyecto/crear/uso_semoviente',type='json', auth="public", website=True)
    def buscar_uso_semoviente(self,id_tipo,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        semoviente_uso_data=[]
        if id_tipo!='':
            semoviente_uso_data=self.instanciar_objetos('ept_cp.semovientes_uso',[('grupos_id','=',int(id_tipo))])
        name_uso=[]
        ids_uso=[]
        valores=[]
        for i in semoviente_uso_data:
            name_uso.append(i.uso) 
            ids_uso.append(i.id)
        valores.append(name_uso)
        valores.append(ids_uso)
        return  valores
        
    @http.route('/proyecto/crear/proposito_semoviente',type='json', auth="public", website=True)
    def buscar_proposito_semoviente(self,id_tipo,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        semoviente_proposito_data=[]
        if id_tipo!='':
            semoviente_proposito_data=self.instanciar_objetos('ept_cp.semovientes_proposito',[('usos_id','=',int(id_tipo))])
        name_proposito=[]
        ids_proposito=[]
        valores=[]
        for i in semoviente_proposito_data:
            name_proposito.append(i.proposito) 
            ids_proposito.append(i.id)
        valores.append(name_proposito)
        valores.append(ids_proposito)
        return  valores
        
        
    @http.route('/proyecto/crear/validar_aval',type='json', auth="public", website=True)
    def validar_aval(self,tipo_obra,subacategoria,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        
        aval=carga_proyecto_obj.cp_validar_requerimiento_aval(cr, uid, 
                                                                    [],
                                                    int(subacategoria),
                                                             tipo_obra, 
                                                               context)
        aval=aval.values()[2].values()[0]
        if aval==True:
            return True
        else:
            return False
            
    @http.route('/proyecto/crear/unidad',type='json', auth="public", website=True)
    def filtrar_unidad(self,tipo_obra,subacategoria,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        
        unidad=carga_proyecto_obj.cp_filtrar_unidades_medidas (cr, uid, [], int(subacategoria),str(tipo_obra))
        unidad= unidad.values()[0]
        unidad=unidad[0]
        
        unidades_data=self.instanciar_objetos('ept_cp.unidades_obra_civil',[('id','in',unidad[2])])
        
        name_unidad=[]
        ids_unidad=[]
        valores=[]
        for uni in unidades_data:
            name_unidad.append(uni.unidad) 
            ids_unidad.append(uni.id)
        valores.append(name_unidad)
        valores.append(ids_unidad)
        return  valores
        
    @http.route('/proyecto/filtrarhuso',type='json', auth="public", website=True)
    def filtrar_huso(self,id_estado,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        
        estado_datos=self.instanciar_objetos('ept_ent.estados',[('id','=',int(id_estado))])

        valores_h=[]
        list_id_huso=[]
        list_name_huso=[]
                
        for h in estado_datos['husos_ids']:
            list_id_huso.append(int(h))
        
        husos_datos=self.instanciar_objetos('ept_ent.husos',[('id','in',list_id_huso)])
    
        list_id=[]
        for hu in husos_datos:
            list_id.append(hu.id)
            list_name_huso.append(hu.huso)
            
        valores_h.append(list_name_huso)
        valores_h.append(list_id_huso)
        return  valores_h
            
    @http.route('/proyecto/duracionproyecto',type='json', auth="public", website=True)
    def duracion_proyecto(self,fecha_inicio,fecha_fin,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        fecha_inicio=fecha_inicio.split(' ')[0]
        fecha_fin=fecha_fin.split(' ')[0]
        duracion=carga_proyecto_obj.cp_validar_fechas_proyecto(cr,uid,[],fecha_inicio,fecha_fin,)
        duracion=duracion.values()[0].values()[0]
        
        return duracion
    
    @http.route('/proyecto/fecha',type='json', auth="public", website=True)
    def fecha_servidor(self,**kw):
        fecha=str(date.today())
        return fecha
    
    @http.route('/proyecto/solicitud_cambio',type='json', auth="public", website=True)
    def buscar_solicitud_cambio(self,id_proyecto,**km):
        solicitud_data=self.instanciar_objetos('ept_cp.solicitud_cambios',[('proyecto_id','=',int(id_proyecto)),('state','=','enviado')])
        dicts={}
        list_cambios=[]
        for records in solicitud_data:
            list_cambios.append(records.id)
            for campos in records.campos_solicitud_ids:
                if campos.tipo_campo=='char':
                    dicts={'char_viejo': campos.char_viejo, 'char_nuevo':campos.char_nuevo, 'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='integer':
                    dicts={'integer_viejo': campos.integer_viejo, 'integer_nuevo':campos.integer_nuevo,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='float':
                    dicts={'float_viejo': campos.float_viejo, 'float_nuevo':campos.float_nuevo,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='text':
                    dicts={'text_viejo': campos.text_viejo, 'text_nuevo':campos.text_nuevo,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='date':
                    dicts={'date_viejo': campos.date_viejo, 'date_nuevo':campos.date_nuevo,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='datetime':
                    dicts={'datetime_viejo': campos.datetime_viejo, 'datetime_nuevo':campos.datetime_nuevo,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='estado_id':
                    dicts={'estado_id_viejo': campos.estado_id_viejo.estado, 'estado_id_nuevo':campos.estado_id_nuevo.estado,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='municipio_id':
                    dicts={'municipio_id_viejo': campos.municipio_id_viejo.municipio, 'municipio_id_nuevo':campos.municipio_id_nuevo.municipio,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='parroquia_id':
                    dicts={'parroquia_id_viejo': campos.parroquia_id_viejo.parroquia, 'parroquia_id_nuevo':campos.parroquia_id_nuevo.parroquia,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='huso_id':
                    dicts={'huso_id_viejo': campos.huso_id_viejo.huso, 'huso_id_nuevo':campos.huso_id_nuevo.huso,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
                if campos.tipo_campo=='husof_id':
                    dicts={'husof_id_viejo': campos.husof_id_viejo.huso, 'husof_id_nuevo':campos.husof_id_nuevo.huso,'tipo_campo':campos.tipo_campo,'campo':campos.campo_id.field_description}
                    list_cambios.append(dicts)
                    dicts={}
        
        return list_cambios
    
    
    @http.route('/proyecto/calculo/monto_mantenimiento',type='json', auth="public", website=True)
    def calculo_monto_mantenimiento(self,periodo_id,entidad_id,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        entidades_data=self.instanciar_objetos('ept_ent.entidades',[('parent_id','=',int(entidad_id))])
        monto_disponible=entidades_data['monto_disp_mantenimiento']
        monto_disponible='%.2f' % monto_disponible
        return monto_disponible
    
    @http.route('/proyecto/cancelar',type='json', auth="public", website=True)
    def cancelar_proyecto(self,proyecto_id, **kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        proyecto_obj = registry.get('ept_cp.carga_proyecto')
        historial_proyecto_obj = registry.get('ept_cp.historial_proyecto')
        cuenta_obj = registry.get('ept.movimientos_cuentas')
        proyecto_data=proyecto_obj.browse(cr,uid,int(proyecto_id))
        if proyecto_data['state']!='cancelado':
            for proyecto in proyecto_data:
                movimiento_id=cuenta_obj.movimiento_ingreso(
                                                        cr,uid,
                                                        int(proyecto.cuenta_id),
                                                        proyecto.monto_proyecto,
                                                        'Cancelación de proyecto',
                                                        proyecto.correlativo,
                                                        'ept_cp.carga_proyecto',
                                                        proyecto.id,
                                                        int(proyecto.periodo_id),
                                                        int(proyecto.partner_id),
                                                        proyecto.proyect_mantenimiento,
                                                        float(proyecto.monto_proyecto))
            valores={
                'movimiento_ids':[[6, False, [movimiento_id['movimiento_id_ingreso']]]],
                'state':'cancelado',
                'monto_tomado_mantenimiento':0.00,
                }
            modificar_state=proyecto_obj.write(cr,uid,int(proyecto_id),valores,0)
            historial={
                'proyecto_id':int(proyecto_id),
                'descripcion':'Usted ha cancelado el proyecto '+proyecto_data['correlativo']
                }
            historial_proyecto_obj.create(cr,uid,historial)
            if modificar_state==True:
                return  True
            else:
                return False
          
    @http.route('/proyecto/coordenadas',type='json', auth="public", website=True)
    def validar_doble_coordenadas(self,ids_sub,**kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        
        coordenada=carga_proyecto_obj.cp_subcaterogia(cr, uid, 
                                                            [],
                                                  int(ids_sub),)
        coordenada=coordenada.values()[0]
        coordenada=coordenada['coordenada']
        if coordenada==True:
            return True
        else:
            return False
            
    def validar_proyecto_mantenimiento(self,ids,periodo_id,res_partner,monto):
        entidades_data=self.instanciar_objetos('ept_ent.entidades',[('parent_id','=',int(res_partner))])
        monto_disponible=entidades_data['monto_disp_mantenimiento']
        monto_disponible='%.2f' % monto_disponible
        ret=1
        if float(monto_disponible)<float(monto):
            ret =  {'modal':{
                    'titulo':'<strong>Error!</strong>',
                    'cuerpo':'''<h4 class="text-danger" >
                                Este proyecto sobrepasa el monto maximo para proyectos de mantenimiento.
                                </h4>
                                ''',
                        },
                }
            return ret
        return ret
        
    @http.route(['/descargar/ficha_proyecto/<model("fnz_clc.conciliacion_bancaria"):proyecto_data>'],
                type='http', auth='user', website=True)
    def descargar_ficha_proyecto(self,proyecto_data, **post):
        cr, uid, context = request.cr, request.uid, request.context
        registry = http.request.registry
        reportname='ept_carga_proyectos.ficha_proyecto_qweb'
        coordenadas='1. Coordenada Norte: '+str(proyecto_data.coord_norte)+' Coordenada Este: '+str(proyecto_data.coord_este)
        coordenadasf='2. Coordenada Norte: '+str(proyecto_data.coord_norte_f)+' Coordenada Este: '+str(proyecto_data.coord_este_f)
        periodo_fiscal= proyecto_data.periodo_id.periodo_fiscal+' ('+proyecto_data.ciclo_id.nombre+')'
        hoy=date.today()
        entidades_obj = registry.get('ept_ent.entidades')
        entidades_id=entidades_obj.search(cr,uid,[('parent_id','=',int(proyecto_data['partner_id']))])
        entidades_data=entidades_obj.browse(cr,uid,entidades_id)
        nombre=''
        for user in entidades_data['user_ids']:
            for group in user.groups_id:
                if group.name=='Alcaldes, Gobernadores o Alcalde Mayor':
                    nombre=user.name
        
        print proyecto_data['semoviente_ids']
        print proyecto_data['vehiculos_ids']
        print proyecto_data['maquinaria_ids']
        print proyecto_data['materiales_ids']
        print proyecto_data['equipos_ids']
        
        valores={
            'correlativo':proyecto_data.correlativo,
            'nombre_proyecto':proyecto_data.nombre_proyecto,
            'descripcion_proyecto':proyecto_data.descripcion_proyecto,
            'periodo_fiscal':periodo_fiscal,
            'tipo_sector':proyecto_data.tipo_sector_id.name,
            'categoria':proyecto_data.categoria_id.name,
            'subcategoria':proyecto_data.subcategoria_id.name,
            'estado':proyecto_data.estado_id.estado,
            'municipio':proyecto_data.municipio_id.municipio,
            'parroquia':proyecto_data.parroquia_id.parroquia,
            'proyecto_data':proyecto_data,
            'coordenadas':coordenadas,
            'coordenadasf':coordenadasf,
            'hoy':hoy,
            'nombre':nombre,
            }
        pdf = request.registry['report'].get_pdf(cr, uid, proyecto_data, reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % proyecto_data.correlativo)
        return response
  
    @http.route('/proyecto/crear/guardar',type='json', auth="public", website=True)
    def guardar_proyecto(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        datos_campos=[]
        proyecto_id=''
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        lista_booleanos=['proyect_mantenimiento','obra_civil','equipos','maquinaria','materiales_consumo','vehiculos','semovientes']
        list_boole_activo=[]
       
        for booleano in lista_booleanos:
            if booleano in post.keys():
                
                list_boole_activo.append(booleano)
        if len (list_boole_activo)<1:
            ret =  {'modal':{
                        'titulo':'<strong>Aviso!</strong>',
                        'cuerpo':'''<h4 class="text-danger" >
                                   Debe seleccionar al menos una caracteristicas para el proyecto a registrar
                                    </h4>
                                    ''',
                                },
                            }
            return ret
        monto=post['monto_proyecto'].split(',')
        decimal='00'
        if len(monto)>1:
            decimal=monto[1]
        entero=monto[0].split('.')
        if len(entero)>1:
            entero=''.join(entero)
        else:
            entero=entero[0]
        monto_proyecto=str(entero)+'.'+str(decimal)
        monto_proyecto=float(monto_proyecto)
        if float(monto_proyecto)<1:
            ret =  {'modal':{
                        'titulo':'<strong>Error!</strong>',
                        'cuerpo':'''<h4 class="text-danger" >
                                    El monto a registrar para el proyecto debe ser mayor a 0.00
                                    </h4>
                                    ''',
                                },
                            }
            return ret
        cuentas_datos=self.instanciar_objetos('ept.cuentas',[('id','=',int(post['cuenta_id']))])
        if float(monto_proyecto)>cuentas_datos['monto_actual']:
            ret =  {'modal':{
                        'titulo':'<strong>Error!</strong>',
                        'cuerpo':'''<h4 class="text-danger" >
                                    El monto que desea asignar a su proyecto no esta disponible en la cuenta asignada
                                    </h4>
                                    ''',
                            },
                    }
            return ret
        plf_periodos_objeto=registry.get('ept_plf.periodos')
        actividad='CARGA DE PROYECTOS'
        autorizacion_fechas=plf_periodos_objeto.plf_control_actividades(
                                                                     cr, 
                                                                uid, [],
                                                int(post['partner_id']),
                                                             actividad,)
        if autorizacion_fechas.keys()[0]=='periodo':
            periodo=int(autorizacion_fechas['periodo'][0])
        if autorizacion_fechas.keys()[0]!='periodo':
            ret =  {'modal':{
                        'titulo':'<strong>Error!</strong>',
                        'cuerpo':'''<h4 class="text-danger" >
                                    La carga de proyecto no esta habilitada para la fecha de hoy.
                                    </h4>
                                    ''',
                                },
                            }
            return ret
        else:
            if 'proyect_mantenimiento' in post.keys() :
                ret=self.validar_proyecto_mantenimiento([],periodo,int(post['partner_id']),monto_proyecto)
                if ret!=1:
                    return ret
        datos_campos=[
                      {'name':'nombre_proyecto',
                      'type':'text',
                      'attr':'Nombre del Proyecto,' },
                      {'name':'descripcion_proyecto',
                      'type':'text',
                      'attr':'Descripción del Proyecto,' },
                      {'name':'fecha_inicio',
                      'type':'text',
                      'attr':'Fecha de Inicio,' },
                      {'name':'fecha_fin',
                      'type':'text',
                      'attr':'Fecha de Fin,' },
                      {'name':'monto_proyecto',
                      'type':'text',
                      'attr':'Monto del Proyecto,' },
                      {'name':'tipo_sector_id',
                      'type':'text',
                      'attr':'Tipo de Sector,' },
                      {'name':'categoria_id',
                      'type':'text',
                      'attr':'Categoria,' },
                      {'name':'subcategoria_id',
                      'type':'text',
                      'attr':'Subcategoria,' },
                      {'name':'benef_masculino',
                      'type':'number',
                      'attr':'Beneficiarios Masculinos,' },
                      {'name':'benef_femenino',
                      'type':'number',
                      'attr':'Beneficiarios Femeninos,' },
                      {'name':'empleo_direct_masculino',
                      'type':'number',
                      'attr':'Empleo Directo Masculino,' },
                      {'name':'empleo_direct_femenino',
                      'type':'number',
                      'attr':'Empleo Directo Femenino,' },
                      {'name':'empleo_indirect_masculino',
                      'type':'number',
                      'attr':'Empleo Indirecto Masculino,' },
                      {'name':'empleo_indirect_femenino',
                      'type':'number',
                      'attr':'Empleo Indirecto Femenino,' },
                      {'name':'estado_id',
                      'type':'number',
                      'attr':'Estado,' },
                      {'name':'total_benef',
                      'type':'number',
                      'cantidad_min':1,
                      'attr':'Total de Beneficiarios,' },
                      {'name':'empleo_direct_total',
                      'type':'number',
                      'cantidad_min':1,
                      'attr':'Total Empleos Directos,' },
                      {'name':'empleo_indirect_total',
                      'type':'number',
                      'cantidad_min':1,
                      'attr':'Total Empleos Indirectos,' },
                      {'name':'municipio_id',
                      'type':'text',
                      'attr':'Municipio,' },
                      {'name':'parroquia_id',
                      'type':'text',
                      'attr':'Parroquia,' },
                      {'name':'huso_id',
                      'type':'text',
                      'attr':'Huso Inicial,' },
                      {'name':'coord_este',
                      'type':'number',
                      'cantidad_max':999999,
                      'attr':'Coordenadas Este Inicial,' },
                      {'name':'coord_norte',
                      'type':'number',
                      'cantidad_max':1999999,
                      'attr':'Coordenadas Norte Norte,' },
                      {'name':'sector',
                      'type':'text',
                      'attr':'Sector,' },
                     ]
        campo_aval_id=False
        list_aval=[]
        if 'aval' in post.keys() :
            campo_aval=panel.dict_keys_startswith(post,'aval_ids')
            campo_aval=campo_aval.keys()
            if len(campo_aval)==1:
                campo_aval_id=campo_aval[0]
            else:
                campo_aval_id=False
        list_files=[]
        campo_foto=panel.dict_keys_startswith(post,'foto_id')
        campo_foto=campo_foto.keys()
        if len(campo_foto)>=1:
            campo_foto_id=campo_foto[0]
        else:
            campo_foto_id='foto_id'
        datos_campos.append(
            {'name':campo_foto_id,
                       'cant':1,
                       'type':'img',
                       'attr':'Fotografía, '}
            )
        if 'obra_civil' in post.keys() :
            datos_campos.append({'name':'tipo_obra',
                                 'type':'radio',
                                 'attr':'Tipo de Obra,'},) 
            datos_campos.append({'name':'cantidad_estimada_obra',
                                 'type':'text',
                                 'attr':'Cantidad,'},)
            datos_campos.append({'name':'unidad_medicion_obra',
                                 'type':'text',
                                 'attr':'Unidad,'},)
        husof_id=''
        coord_este_f=0
        coord_norte_f=0
        coordenada=False
        if 'coordenada' in post.keys() :
            husof_id=post['husof_id'],
            husof_id=husof_id[0]
            coord_este_f=post['coord_este_f'],
            coord_este_f=coord_este_f[0]
            coord_norte_f=post['coord_norte_f'],
            coord_norte_f=coord_norte_f[0]
            coordenada=True
            datos_campos.append({'name':'husof_id',
                                 'type':'text',
                                 'attr':'Huso Final,' },)
            datos_campos.append({'name':'coord_este_f',
                                  'type':'number',
                                  'cantidad_max':999999,
                                  'attr':'Coordenadas Este Final,' },)
            datos_campos.append({'name':'coord_norte_f',
                                  'type':'number',
                                  'cantidad_max':1999999,
                                  'attr':'Coordenadas Norte Final,' },)
                     
        equipos_ids=[]
        equipos=False
        if 'equipos' in post.keys() :
            equipos=True
            equipo=panel.validar().validar_one_2_many(post,'equipo_',datos_campos)
            equipos_ids_p={'uso_id': '', 
                         'cantidad': '', 
                         'tipo':'' }
            equipos_ids=panel.validar().construir_one_2_many(post,'equipo_',equipos_ids_p)
        maquinaria_ids=[]
        maquinarias=False
        if 'maquinaria' in post.keys() :
            maquinarias=True
            maquinaria=panel.validar().validar_one_2_many(post,'maquinaria_',datos_campos)
            maquinarias_ids_p={'uso_id': '', 
                               'cantidad': '', 
                               'tipo': '', 
                                }
            maquinaria_ids=panel.validar().construir_one_2_many(post,'maquinaria_',maquinarias_ids_p)
        vehiculos_ids=[]
        vehiculos=False
        if 'vehiculos' in post.keys() :
            vehiculos=True
            vehiculo=panel.validar().validar_one_2_many(post,'vehiculo_',datos_campos)
            
            vehiculos_ids_p={'uso_id': '', 
                               'tipo_id': '', 
                               'cantidad': '', 
                               'caracteristica_id': '', 
                                }
            
            vehiculos_ids=panel.validar().construir_one_2_many(post,'vehiculo_',vehiculos_ids_p)
        materiales_ids=[]
        materiales=False
        if 'materiales' in post.keys() :
            materiales=True
            materiale=panel.validar().validar_one_2_many(post,'materiales_',datos_campos)
            materiales_ids_p={'uso_id': '', 
                               'cantidad': '', 
                               'tipo': '', 
                                }
            materiales_ids=panel.validar().construir_one_2_many(post,'materiales_',materiales_ids_p)
        semoviente_ids=[]
        semovientes=False
        if 'semovientes' in post.keys() :
            semovientes=True
            semoviente=panel.validar().validar_one_2_many(post,'semovientes_',datos_campos)
            semoviente_ids_p={'uso_id': '', 
                              'proposito_id': '', 
                              'grupo_id': '', 
                              'especie_id': '', 
                              'cantidad': '', 
                             }
            semoviente_ids=panel.validar().construir_one_2_many(post,'semovientes_',semoviente_ids_p)
        errors=panel.validar().varios_campos(datos_campos,post)
        if len(errors)==0:
            if campo_aval_id!=False:
                type_aval_file=post[campo_aval_id].split(';' or ',')[0].split(':')[1]
                data_aval_file=post[campo_aval_id].split(';' or ',')[1].split(',')[1]
                name_aval_file=post[campo_aval_id].split(';' or ',')[2]
                list_aval.append([0,False,{'datas':data_aval_file, 'name':name_aval_file, 'type':'binary', 'mimetype':type_aval_file,'datas_fname':name_aval_file}])
            type_file=post[campo_foto_id].split(';' or ',')[0].split(':')[1]
            data_file=post[campo_foto_id].split(';' or ',')[1].split(',')[1]
            name_file=post[campo_foto_id].split(';' or ',')[2]
            list_files.append([0,False,{'datas':data_file, 'name':name_file, 'type':'binary', 'mimetype':type_file,'datas_fname':name_file}])
            if 'obra_civil' in post.keys() :
                obra_civil=True
                cantidad_estimada_obra=post['cantidad_estimada_obra']
            else:
                obra_civil=False
                cantidad_estimada_obra=0
            if 'aval' in post.keys() :
                aval=True
            else:
                aval=False
            if 'tipo_obra' in post.keys() :
                tipo_obra=post['tipo_obra']
            else:
                tipo_obra=''
            if 'proyect_mantenimiento' in post.keys() :
                proyect_mantenimiento=True
            else:
                proyect_mantenimiento=False
            vals={
                'materiales_consumo': materiales,
                'aval_ids': list_aval,
                'subcategoria_id':int(post['subcategoria_id']),
                'descripcion_proyecto': post['descripcion_proyecto'],
                'equipos': equipos,
                'fecha_fin': post['fecha_fin'],
                'coord_este_f': coord_este_f,
                'benef_masculino': int(post['benef_masculino']),
                'tipo_sector_id':int(post['tipo_sector_id']),
                'municipio_id': int(post['municipio_id']),
                'coordenada': coordenada,
                'vehiculos_ids': vehiculos_ids,
                'nombre_proyecto': post['nombre_proyecto'],
                'empleo_indirect_masculino': int(post['empleo_indirect_masculino']),
                'semoviente_ids': semoviente_ids,
                'partner_id': int(post['partner_id']),
                'create_uid': False,
                'semoviente': semovientes,
                'parroquia_id': int(post['parroquia_id']),
                'empleo_direct_femenino': int(post['empleo_direct_femenino']), 
                'categoria_id':int(post['categoria_id']),
                'obra_civil': obra_civil,
                'vehiculos': vehiculos,
                'coord_norte':int(post['coord_norte']), 
                'aval': aval,
                'fecha_inicio': post['fecha_inicio'], 
                'coord_este': int(post['coord_este']),
                'tipo_obra': tipo_obra,
                'empleo_indirect_femenino': int(post['empleo_indirect_femenino']), 
                'unidad_medicion_obra': post['unidad_medicion_obra'],
                'maquinaria_ids': maquinaria_ids,
                'benef_femenino': int(post['benef_femenino']),
                'empleo_direct_masculino':int(post['empleo_direct_masculino']),
                'foto_id': list_files,
                'proyect_mantenimiento': proyect_mantenimiento,
                'cantidad_estimada_obra': cantidad_estimada_obra,
                'historial_ids': [],
                'estado_id': int(post['estado_id']),
                'maquinaria': maquinarias,
                'husof_id': husof_id,
                'materiales_ids': materiales_ids,
                'huso_id': int(post['huso_id']),
                'monto_proyecto':monto_proyecto,
                'coord_norte_f': coord_norte_f,
                'cuenta_id': int(post['cuenta_id']),
                'equipos_ids':equipos_ids,
                'sector':post['sector']
            }
            proyecto_id=carga_proyecto_obj.create(cr,uid,vals,context=context)
        else:
            ret={'error_campos':errors}
        
        if proyecto_id:
            ret={'redirect':'/proyecto/lectura/%s' % (proyecto_id)}
        return ret
        
    @http.route('/proyecto/editar/guardar',type='json', auth="public", website=True)
    def guardar_edicion_proyecto(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        carga_proyecto_obj = registry.get('ept_cp.carga_proyecto')
        dict_editar_principal=post['post_principal']
        dict_editar_auxiliar=post['post_auxiliar']
        lista_booleanos=['proyect_mantenimiento','obra_civil','equipos','maquinaria','materiales_consumo','vehiculos','semoviente']
        list_boole_activo=[]
        for booleano in lista_booleanos:
            if booleano in dict_editar_principal.keys():
                list_boole_activo.append(booleano)
        
        
        monto=dict_editar_principal['monto_proyecto'].split(',')
        decimal='00'
        if len(monto)>1:
            decimal=monto[1]
        entero=monto[0].split('.')
        if len(entero)>1:
            entero=''.join(entero)
        else:
            entero=entero[0]
        monto_proyecto=str(entero)+'.'+str(decimal)
        monto_proyecto=float(monto_proyecto)
        monto_proyecto='%.2f' % monto_proyecto
        
        monto_aux=dict_editar_auxiliar['monto_proyecto'].split(',')
        decimal_aux='00'
        if len(monto_aux)>1:
            decimal_aux=decimal_aux[1]
        entero_aux=decimal_aux[0].split('.')
        if len(entero_aux)>1:
            entero_aux=''.join(entero_aux)
        else:
            entero_aux=entero_aux[0]
        monto_aux=str(entero_aux)+'.'+str(decimal_aux)
        monto_aux=float(decimal_aux)
        monto_aux='%.2f' % float(monto_aux)
    
        if float(monto_proyecto)<1:
            ret =  {'modal':{
                        'titulo':'<strong>Error!</strong>',
                        'cuerpo':'''<h4 class="text-danger" >
                                    El monto a registrar para el proyecto debe ser mayor a 0.00
                                    </h4>
                                    ''',
                                },
                            }
            return ret
        list_confirm_caract=[]
 
        if len (list_boole_activo)<1: 
            for caracteristicas_confirm in ['semovi_confirm','mater_confirm','vehic_confirm','maqui_confirm','equi_confirm','proyect_manten_confirm','obra_confirm']:
                if caracteristicas_confirm in dict_editar_principal.keys():
                    list_confirm_caract.append(caracteristicas_confirm)
            if len(list_confirm_caract):
                confirm=True
            else:
                ret =  {'modal':{
                            'titulo':'<strong>Aviso!</strong>',
                            'cuerpo':'''<h4 class="text-danger" >
                                       Debe seleccionar al menos una caracteristicas para el proyecto a registrar
                                        </h4>
                                        ''',
                                    },
                                }
                return ret
        vals={}
        edicion=False
        
        dict_claves={
                'subcategoria_id':'',
                'descripcion_proyecto': '',
                'fecha_fin': '',
                'benef_masculino': '',
                'tipo_sector_id':'',
                'municipio_id': '',
                'nombre_proyecto': '',
                'empleo_indirect_masculino': '',
                'partner_id': '',
                'parroquia_id': '',
                'empleo_direct_femenino':'', 
                'categoria_id':'',
                'coord_norte':'', 
                'fecha_inicio':'', 
                'coord_este': '',
                'empleo_indirect_femenino': '', 
                'benef_femenino': '',
                'empleo_direct_masculino':'',
                'estado_id': '',
                'huso_id': '',
                'monto_proyecto':'',
                'cuenta_id':'',
                'duracion_proyec':'',
                'total_benef':'',
                'empleo_direct_total':'',
                'empleo_indirect_total':'',
                'sector':'',
            }
        keys_dc=dict_claves.keys()
        keys_dep=dict_editar_principal.keys()
        keys_dea=dict_editar_auxiliar.keys()
        for dc in keys_dc:
            if dc in keys_dep:
                if dict_editar_principal[dc]!=dict_editar_auxiliar[dc]:
                    if dc=='monto_proyecto':
                        if monto_aux!=monto_proyecto:
                            vals[dc]=monto_proyecto
                    else:
                        vals[dc]=dict_editar_principal[dc]
        datos_campos=[]
        datos_campos.append(
                        {   'name':'fotos_id',
                            'cant':1,
                            'type':'img',
                            'attr':'Fotografía, '}
                        )
        if 'total_benef' in keys_dep:
            datos_campos.append({'name':'total_benef',
                                  'type':'number',
                                  'cantidad_min':1,
                                  'attr':'Total de Beneficiarios,' },)
        if 'empleo_direct_total' in keys_dep:
            datos_campos.append({'name':'empleo_direct_total',
                                  'type':'number',
                                  'cantidad_min':1,
                                  'attr':'Total Empleos Directos,' },)
        if 'empleo_indirect_total' in keys_dep:
            datos_campos.append({'name':'empleo_indirect_total',
                                  'type':'number',
                                  'cantidad_min':1,
                                  'attr':'Total Empleos Indirectos,' },)
        if 'coord_este' in keys_dep:
            datos_campos.append({'name':'coord_este',
                                'type':'number',
                                'cantidad_max':999999,
                                'attr':'Coordenadas Este Inicial,' },)
        if 'coord_norte' in keys_dep:
            datos_campos.append({'name':'coord_norte',
                                  'type':'number',
                                  'cantidad_max':1999999,
                                  'attr':'Coordenadas Norte Norte,' },)
        if 'obra_civil' in keys_dep :
            datos_campos.append({'name':'tipo_obra',
                                 'type':'radio',
                                 'attr':'Tipo de Obra,'},) 
            datos_campos.append({'name':'cantidad_estimada_obra',
                                 'type':'text',
                                 'attr':'Cantidad,'},)
            datos_campos.append({'name':'unidad_medicion_obra',
                                 'type':'text',
                                 'attr':'Unidad,'},)
        
        proyecto_datos=carga_proyecto_obj.browse(cr,uid,int(dict_editar_principal['id']))
        val=[1,2]
        reparacion=carga_proyecto_obj.cp_cambio_state_evaluacion(cr,uid,[],val,int(proyecto_datos['periodo_id']),int(proyecto_datos['ciclo_id']),int(proyecto_datos['partner_id']))
        if 'coordenada' in keys_dep:
            if (proyecto_datos['state']=='diferido' or proyecto_datos['state']=='aprobado') and reparacion!=True:
                print True
            else:
                datos_campos.append({'name':'husof_id',
                                     'type':'text',
                                     'attr':'Huso Final,' },)
                datos_campos.append({'name':'coord_este_f',
                                      'type':'number',
                                      'cantidad_max':999999,
                                      'attr':'Coordenadas Este Final,' },)
                datos_campos.append({'name':'coord_norte_f',
                                      'type':'number',
                                      'cantidad_max':1999999,
                                      'attr':'Coordenadas Norte Final,' },)
                     
        if 'equipos' in keys_dep:
            equipo=panel.validar().validar_one_2_many(dict_editar_principal,'equipo_',datos_campos)
            
        if 'maquinaria' in keys_dep:
            maquinaria=panel.validar().validar_one_2_many(dict_editar_principal,'maquinaria_',datos_campos)

        if 'vehiculos' in keys_dep:
            vehiculo=panel.validar().validar_one_2_many(dict_editar_principal,'vehiculo_',datos_campos)
    
        if 'materiales' in keys_dep:
            materiale=panel.validar().validar_one_2_many(dict_editar_principal,'materiales_',datos_campos)
            
        if 'semoviente' in keys_dep:
            semoviente=panel.validar().validar_one_2_many(dict_editar_principal,'semovientes_',datos_campos)
        
        errors=panel.validar().varios_campos(datos_campos,dict_editar_principal)
        if len(errors)==0:
            list_files_aval=[]
            campo_aval=panel.dict_keys_startswith(dict_editar_principal,'aval_ids')
            campo_aval=campo_aval.keys()
            if campo_aval!=[]:
                edicion_aval=dict_editar_principal[campo_aval[0]].split(';')[2].split('=')[0]
                if edicion_aval!='file_id':
                
                    if len(campo_aval)>=1:
                        campo_aval_id=campo_aval[0]
                        type_file_aval=dict_editar_principal[campo_aval_id].split(';' or ',')[0].split(':')[1]
                        if type_file_aval!='undefined':
                        
                            data_file_aval=dict_editar_principal[campo_aval_id].split(';' or ',')[1].split(',')[1]
                            name_file_aval=dict_editar_principal[campo_aval_id].split(';' or ',')[2]
                            if 'objeto_aval_id' in dict_editar_principal.keys():
                                list_files_aval.append([1,int(dict_editar_principal['objeto_aval_id']),{'datas':data_file_aval, 'name':name_file_aval, 'type':'binary', 'mimetype':type_file_aval,'datas_fname':name_file_aval}])
                            else:
                                list_files_aval.append([0,False,{'datas':data_file_aval, 'name':name_file_aval, 'type':'binary', 'mimetype':type_file_aval,'datas_fname':name_file_aval}])

                            vals['aval_ids']=list_files_aval
                    else:
                        campo_aval_id='aval_ids'
            else:
                carga_proyecto_data=self.instanciar_objetos('ept_cp.carga_proyecto',[('id','=',int(dict_editar_principal['id']))])
                if len(carga_proyecto_data['aval_ids'])>0:
                    list_files_aval.append([2,int(carga_proyecto_data['aval_ids']),{}])
                    vals['aval_ids']=list_files_aval
            list_files=[]
            campo_foto=panel.dict_keys_startswith(dict_editar_principal,'fotos_id')
            campo_foto=campo_foto.keys()
            edicion_foto=dict_editar_principal[campo_foto[0]].split(';')[2].split('=')[0]
            if edicion_foto!='file_id':
                if len(campo_foto)>=1:
                    campo_foto_id=campo_foto[0]
                    type_file=dict_editar_principal[campo_foto_id].split(';' or ',')[0].split(':')[1]
                    if type_file!='undefined':
                    
                        data_file=dict_editar_principal[campo_foto_id].split(';' or ',')[1].split(',')[1]
                        name_file=dict_editar_principal[campo_foto_id].split(';' or ',')[2]
                        if 'objeto_fotos_id' in dict_editar_principal.keys():
                            list_files.append([1,int(dict_editar_principal['objeto_fotos_id']),{'datas':data_file, 'name':name_file, 'type':'binary', 'mimetype':type_file,'datas_fname':name_file}])
                        else:
                            list_files.append([0,False,{'datas':data_file, 'name':name_file, 'type':'binary', 'mimetype':type_file,'datas_fname':name_file}])

                        vals['foto_id']=list_files
                else:
                    campo_foto_id='foto_id'
            
            if 'proyect_mantenimiento' in dict_editar_principal.keys():
                if 'proyect_mantenimiento' not  in dict_editar_auxiliar.keys():
                    vals['proyect_mantenimiento']=True
            else:
                if 'proyect_mantenimiento' in dict_editar_auxiliar.keys():
                    vals['proyect_mantenimiento']=False
            dict_obra={'cantidad_estimada_obra': '','unidad_medicion_obra': ''}
            keys_obra=dict_obra.keys()
            if 'obra_civil' in dict_editar_principal.keys():
                if 'obra_civil' in dict_editar_auxiliar.keys():
                    for ko in keys_obra:
                        if dict_editar_principal[ko]!=dict_editar_auxiliar[ko]:
                            vals[ko]=dict_editar_principal[ko]
                    if dict_editar_principal['tipo_obra']!=dict_editar_auxiliar['tipo_obra2']:
                            vals['tipo_obra']=dict_editar_principal['tipo_obra']
                    if 'aval' in dict_editar_principal.keys():
                        if 'aval' not in dict_editar_auxiliar.keys():
                            vals['aval']=True
                    else:
                        if 'aval' in dict_editar_auxiliar.keys():
                            vals['aval']=False
                else:
                    for ko in keys_obra:
                        vals[ko]=dict_editar_principal[ko]
                    vals['tipo_obra']=dict_editar_principal['tipo_obra']
                    vals['obra_civil']=True
                    if 'aval' in dict_editar_principal.keys():
                        vals['aval']=True
                    else:
                        vals['aval']=False
            else:
                if 'obra_civil' in dict_editar_auxiliar.keys():
                    for ko in keys_obra:
                        vals[ko]=''
                    vals['tipo_obra']=''
                    vals['obra_civil']=False
                    if 'aval' in dict_editar_auxiliar.keys():
                        vals['aval']=False
            equipos_ids_p={'uso_id': '', 'cantidad': '', 'tipo':'' }
            equipos=panel.validar().editar_one2many_booleano(dict_editar_principal,dict_editar_auxiliar,'equipo_',equipos_ids_p,vals,'equipos','equipos_ids')
            maquinarias_ids_p={'uso_id': '', 'cantidad': '', 'tipo': '', }
            maquinaria=panel.validar().editar_one2many_booleano(dict_editar_principal,dict_editar_auxiliar,'maquinaria_',maquinarias_ids_p,vals,'maquinaria','maquinaria_ids')
            vehiculos_ids_p={'uso_id': '','tipo_id': '','cantidad': '','caracteristica_id': '',}
            vehiculos=panel.validar().editar_one2many_booleano(dict_editar_principal,dict_editar_auxiliar,'vehiculo_',vehiculos_ids_p,vals,'vehiculos','vehiculos_ids')
            materiales_ids_p={'uso_id': '', 'cantidad': '', 'tipo': '', }
            materiales=panel.validar().editar_one2many_booleano(dict_editar_principal,dict_editar_auxiliar,'materiale_',materiales_ids_p,vals,'materiales_consumo','materiales_ids')
            semoviente_ids_p={'uso_id': '', 'proposito_id': '', 'grupo_id': '', 'especie_id': '', 'cantidad': '',}
            semoviente=panel.validar().editar_one2many_booleano(dict_editar_principal,dict_editar_auxiliar,'semovientes_',semoviente_ids_p,vals,'semoviente','semoviente_ids')
            dict_coordenada={'husof_id':'', 'coord_este_f': '','coord_norte_f': '',}
            keys_coordenada=dict_coordenada.keys()
            if 'coordenada' in dict_editar_principal.keys():
                if (proyecto_datos['state']=='diferido' or proyecto_datos['state']=='aprobado') and reparacion!=True:
                    print True
                else:
                    for kc in keys_coordenada:
                        if 'coordenada' in dict_editar_auxiliar.keys():
                            if dict_editar_principal[kc]!=dict_editar_auxiliar[kc]:
                                vals[kc]=dict_editar_principal[kc]
                        else:
                            vals[kc]=dict_editar_principal[kc]
                            
                    vals['coordenada']=True
            else:
                if 'coordenada' in dict_editar_auxiliar.keys():
                    for kc in keys_coordenada:
                        vals[kc]=''
                    vals['coordenada']=False
            
            for datos in proyecto_datos:
                if 'proyect_mantenimiento' in dict_editar_principal.keys():
                    if carga_proyecto_data['proyect_mantenimiento']==True:
                        #~ if 'monto_proyecto' in vals.keys() and carga_proyecto_data['proyect_mantenimiento']<vals['monto_proyecto']:
                        if 'monto_proyecto' in vals.keys():
                            print 
                            #~ monto_evaluar=float(carga_proyecto_data['proyect_mantenimiento'])-float(vals['monto_proyecto'])
                            monto_evaluar=abs(float(carga_proyecto_data['monto_proyecto'])-float(vals['monto_proyecto']))
                            ret=self.validar_proyecto_mantenimiento([int(dict_editar_principal['id'])],int(datos.periodo_id),int(datos.partner_id),monto_evaluar,)
                            if ret!=1:
                                return ret
                    else:
                        #~ if 'monto_proyecto' in vals.keys() and carga_proyecto_data['proyect_mantenimiento']<vals['monto_proyecto']:
                        if 'monto_proyecto' in vals.keys():
                            monto_evaluar=abs(float(carga_proyecto_data['monto_proyecto'])-float(vals['monto_proyecto']))
                            ret=self.validar_proyecto_mantenimiento([int(dict_editar_principal['id'])],int(datos.periodo_id),int(datos.partner_id),vals['monto_proyecto'],)
                            if ret!=1:
                                return ret
                        if 'monto_proyecto' not in vals.keys():
                            ret=self.validar_proyecto_mantenimiento([int(dict_editar_principal['id'])],int(datos.periodo_id),int(datos.partner_id),datos.monto_proyecto)
                            if ret!=1:
                                return ret        
                else:
                    if datos.proyect_mantenimiento==True and 'monto_proyecto' in vals.keys():
                        if abs(float(vals['monto_proyecto']) > float(datos.monto_proyecto)):
                            monto_evaluar=abs(float(vals['monto_proyecto'])- float(datos.monto_proyecto))
                            ret=self.validar_proyecto_mantenimiento([int(dict_editar_principal['id'])],int(datos.periodo_id),int(datos.partner_id),monto_evaluar)
                            if ret!=1:
                                return ret
            edicion=carga_proyecto_obj.write(cr,uid,int(dict_editar_principal['id']),vals,1,1)
        else:
            ret={'error_campos':errors}
        if edicion==True:
            ret={'redirect':'/proyecto/lectura/%s' % (int(dict_editar_principal['id']))}
        return ret
     
        
        



    @http.route('/proyecto/aceptar/solicitud_cambio',type='json', auth="public", website=True)
    def aceptar_solicitud_cambio(self, solicitud, **kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        solicitud_obj = registry.get('ept_cp.solicitud_cambios')
        solicitud_campos_obj = registry.get('ept.campos_solicitud_cambio')
        proyectos_obj = registry.get('ept_cp.carga_proyecto')
        cp_historial_obj=registry.get('ept_cp.historial_proyecto')
        solicitud_data= solicitud_obj.browse(cr,uid,int(solicitud))
        vals={}
        list_ids_solicitud=[]
        for sol in solicitud_data:
            proyecto_id=sol['proyecto_id'].id
            for campos in sol.campos_solicitud_ids:
                list_ids_solicitud.append(campos.id)
                if campos.tipo_campo=='char':
                    vals[campos.campo_id.name]=campos.char_nuevo
                if campos.tipo_campo=='integer':
                    vals[campos.campo_id.name]=campos.integer_nuevo
                if campos.tipo_campo=='float':
                    vals[campos.campo_id.name]=campos.float_nuevo
                if campos.tipo_campo=='text':
                    vals[campos.campo_id.name]=campos.text_nuevo
                if campos.tipo_campo=='booelan':
                    vals[campos.campo_id.name]=campos.boolean_nuevo
                if campos.tipo_campo=='date':
                    vals[campos.campo_id.name]=campos.date_nuevo
                if campos.tipo_campo=='datetime':
                    vals[campos.campo_id.name]=campos.datetime_nuevo
                if campos.tipo_campo=='estado_id':
                    vals[campos.campo_id.name]=campos.estado_id_nuevo.id
                if campos.tipo_campo=='municipio_id':
                    vals[campos.campo_id.name]=campos.municipio_id_nuevo.id
                if campos.tipo_campo=='parroquia_id':
                    vals[campos.campo_id.name]=campos.parroquia_id_nuevo.id
                if campos.tipo_campo=='huso_id':
                    vals[campos.campo_id.name]=campos.huso_id_nuevo.id
                if campos.tipo_campo=='husof_id':
                    vals[campos.campo_id.name]=campos.husof_id_nuevo.id
        vals['solicitud_cambio']=False
        self.registro_solicitud_firma_carta_solicitud_cambio(solicitud_data)
        
        solicitud_obj.write(cr,SUPERUSER_ID,int(solicitud),{'state':'aprobado'})
        solicitud_campos_obj.write(cr,SUPERUSER_ID,list_ids_solicitud,{'state':'aprobado'})
        proyectos_obj.write(cr,SUPERUSER_ID,proyecto_id,vals,0)
        vals_solicitud={
            'descripcion':'Usted ha aceptado una solicitud de cambios para su proyecto',
            'proyecto_id': proyecto_id,
            }
        cp_historial_obj.create(cr,SUPERUSER_ID,vals_solicitud,context=context)
        return True
        
        
    @http.route('/proyecto/rechazar/solicitud_cambio',type='json', auth="public", website=True)
    def rechazar_solicitud_cambio(self, solicitud, **kw):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        solicitud_obj = registry.get('ept_cp.solicitud_cambios')
        solicitud_campos_obj = registry.get('ept.campos_solicitud_cambio')
        proyectos_obj = registry.get('ept_cp.carga_proyecto')
        cp_historial_obj=registry.get('ept_cp.historial_proyecto')
        solicitud_data= solicitud_obj.browse(cr,uid,int(solicitud))
        vals={}
        list_ids_solicitud=[]
        for sol in solicitud_data:
            proyecto_id=sol['proyecto_id'].id
            for campos in sol.campos_solicitud_ids:
                list_ids_solicitud.append(campos.id)
        vals['solicitud_cambio']=False
        solicitud_obj.write(cr,SUPERUSER_ID,int(solicitud),{'state':'rechazado'})
        solicitud_campos_obj.write(cr,SUPERUSER_ID,list_ids_solicitud,{'state':'rechazado'})
        proyectos_obj.write(cr,SUPERUSER_ID,proyecto_id,vals,0)
        vals_solicitud={
            'descripcion':'Usted ha rechazado una solicitud de cambios para su proyecto',
            'proyecto_id': proyecto_id,
            }
        cp_historial_obj.create(cr,SUPERUSER_ID,vals_solicitud,context=context)
        return True
    
    
    def registro_solicitud_firma_carta_solicitud_cambio(self,solicitud_data):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
       
        correlativo_carta=registry.get('ir.sequence').get(cr,uid,
                                                    'ept_fir.cartas_x_firmar'),
        
        
        nombre_file=solicitud_data['partner_id']['name']+'_solicitudCambio#'
        
        list_datos_adicionales=[]
        list_datos_adicionales.append([0,False,{'objeto_ratro':'ept_cp.solicitud_cambios', 'objeto_ratro_id':solicitud_data['id'], 'referncia':'',}])
        value_x_firmar={
            'correlativo':correlativo_carta[0],
            'tipo_cartas':'modificación',
            'mensaje':'Su projecto tiene una solicitud de cambio aprobada',
            'referencia':'Carta por solicitud de cambios de la Entidad '+solicitud_data['partner_id']['name'],
            'state':'porfirmar',
            'metodo':'descarga_carta_solicitud_cambio',
            'objeto_ratro_principal':'ept_cp.solicitud_cambios',
            'objeto_principal_id':solicitud_data['id'],
            'objeto_rastro_ids':'ept_cp.carga_proyecto',
            'metodoGenerarCartas':'crear_carta_solicitud_cambio',
            'nombre_file':nombre_file,
            'objeto_rastro_ids':list_datos_adicionales,
            }
        cartas_x_firmar_obj = registry.get('ept_fir.cartas_x_firmar')
        cartas_x_firmar_id=cartas_x_firmar_obj.create(cr,uid,value_x_firmar)
        return True




        
        


        
        
       
            
            
    
    
    
        
       
