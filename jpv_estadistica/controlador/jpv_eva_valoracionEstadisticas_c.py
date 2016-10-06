# -*- coding: utf-8 -*-

import csv, operator
from openerp.addons.web.controllers import main
from cStringIO import StringIO
from openerp.http import request
from openerp import http,tools, api,SUPERUSER_ID

class jpv_valoracion_estadisticas(http.Controller):
    
    head_csv=['Código','Nombre del Proyecto','Monto','Estado','Motivo']
    condicion=""
    groups_restrict=['Coordinación General UREs']
    logi_restrict={groups_restrict[0]:'ure'}
    
    
    #~ metodo que busca los estados de para la ures
    def filtrar_estados(self):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        user_obj = registry['res.users']
        user_data=user_obj.browse(cr,SUPERUSER_ID,uid)
        estado_ids=[]
        estado_id=0
        restrict=False
        estado_name=''
        for group in user_data.groups_id:
            if group.name in self.groups_restrict:
                if self.logi_restrict[self.groups_restrict[0]]=='ure':
                    for ure in user_data.ures_ids:
                         estado_ids.append(ure.estado_id.id)
                         restrict=True
                         estado_id=estado_ids[0]
        if estado_id:
            estados_obj = registry['jpv_ent.estados']
            estados_data=estados_obj.browse(cr,SUPERUSER_ID,[estado_id])
            estado_name=estados_data.estado
        return {
                'estado_ids':estado_ids,
                'restrict':restrict,
                'estado_id':estado_id,
                'estado_name':estado_name
                }
                
    
    
    #~ ruta de la estadistica para la vista estadistica 
    @http.route(
            ['/eptEstadisticas'], 
            type='http', auth="user", website=True)
    def estadisticas_valoracion(self):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry['jpv_plf.periodos']
        estado_obj = registry['jpv_ent.estados']
        entidades_obj = registry['jpv_ent.entidades']
        periodo_ids=periodos_obj.search(cr,SUPERUSER_ID,[])
        periodo_data=periodos_obj.browse(cr,SUPERUSER_ID,periodo_ids)
        self.filtrar_estados()
        estado_ids=[]
        filtrar_estados=self.filtrar_estados()
        estado_ids=filtrar_estados['estado_ids']
        if not estado_ids:
            estado_ids=estado_obj.search(cr,SUPERUSER_ID,[])
        estado_data=estado_obj.browse(cr,SUPERUSER_ID,estado_ids)
        entidad_ids=entidades_obj.search(cr,SUPERUSER_ID,[])
        entidad_data=entidades_obj.browse(cr,SUPERUSER_ID,entidad_ids)
        periodo_fiscal=periodo_data[0].periodo_fiscal
        periodo_fiscal_id=periodo_data[0].id
        return http.request.website.render(
                        'jpv_estadistica.estadisticas_index', 
                        {'periodo_data':periodo_data,
                        'estado_data':estado_data,
                        'entidad_data':entidad_data,
                        'periodo_fiscal':periodo_fiscal,
                        'periodo_fiscal_id':periodo_fiscal_id,
                        'restrict':filtrar_estados['restrict'],
                        'estado_id':filtrar_estados['estado_id'],
                        'estado_name':filtrar_estados['estado_name']
                        })
                        
    
    #~ ruta para buscar el ciclo según el periodo seleccionado  
    @http.route(
            ['/eptEstadisticasBuscarCiclo'], 
            type='json', auth="user", website=True)
    def Buscar_ciclo(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry['jpv_plf.periodos']
        periodo_data=periodos_obj.browse(cr,SUPERUSER_ID,[int(post['periodo_id'])])
        ciclos_data=[]
        for ciclo in periodo_data.etapas_ids:
                ciclos_data.append({'ciclo_id':ciclo.id,'nombre':ciclo.nombre})
        return {'ciclos_data':ciclos_data}
        
    #~ ruta para buscar las entidades segun el estado que pulse  
    @http.route(
            ['/eptEstadisticasBuscarEntidad'], 
            type='json', auth="user", website=True)
    def Buscar_Entidad_x_estado(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        entidades_obj = registry['jpv_ent.entidades']
        entidad_ids=entidades_obj.search(cr,SUPERUSER_ID,[('estado_id','=',int(post['estado_id']))])
        entidad_data=entidades_obj.browse(cr,SUPERUSER_ID,entidad_ids)
        entidad_resul=[]
        for entidad in entidad_data:
                entidad_resul.append({'parent_id':entidad.parent_id.id,'nombre':entidad.name})
        return {'entidad_data':entidad_resul}
    
                        
      #~ Ruta de grafica de torta de estadistica general, la que tiene de header Total de Proyectos xxx
    @http.route(
            ['/eptEstadisticasPeriodoGereral'], 
            type='json', auth="public", website=True)
    def periodo_general(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not self.condicion:
            condicion=""
            if int(post['periodo_id'])>0:
                condicion=" p.periodo_id = %s and " % post['periodo_id']
            if int(post['ciclo_id'])>0:
                condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
            if int(post['estado_id'])>0:
                condicion=condicion+" p.estado_id=%s and" % post['estado_id']
            if int(post['entidad_id'])>0:
                condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
        else:
            condicion=self.condicion
            
        cr.execute("select sum(case when p.state='carga' then 1 else 0 end) as cargados ,"\
                   " sum(case when p.state='aprobado' then 1 else 0 end) as aprobados, " \
                   " sum(case when p.state='diferido' then 1 else 0 end) as diferidos, " \
                   " sum(case when p.state='negado' then 1 else 0 end) as negados, " \
                   " sum(case when p.state='cancelado' then 1 else 0 end) as cancelados, " \
                   " sum(case when p.state='evaluacion' then 1 else 0 end) as evaluacion, " \
                   " sum(case when p.state='culminado' then 1 else 0 end) as culminados " \
                   "from jpv_cp_carga_proyecto as p where %s active=True " % condicion)
        datos_gererales=cr.dictfetchone()
        self.condicion=""
        return {'datos':datos_gererales}
        
#~ Ruta de grafica de torta de estadistica general, la que tiene de header Total de Proyectos xxx
    @http.route(
            ['/eptEstadisticasPeriodoGereral2'], 
            type='http', auth="public",method="post", website=True)
    def periodo_general2(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        condicion=""
        if int(2)>0:
            condicion=" p.periodo_id=2 and " 
        #~ if int(post['estado_id'])>0:
            #~ condicion=condicion+" p.estado_id=%s and" % post['estado_id']
        #~ if int(post['entidad_id'])>0:
            #~ condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
            
        cr.execute("select sum(case when p.state='carga' then 1 else 0 end) as cargados ,"\
                   " sum(case when p.state='aprobado' then 1 else 0 end) as aprobados, " \
                   " sum(case when p.state='diferido' then 1 else 0 end) as diferidos, " \
                   " sum(case when p.state='negado' then 1 else 0 end) as negados, " \
                   " sum(case when p.state='cancelado' then 1 else 0 end) as cancelados, " \
                   " sum(case when p.state='evaluacion' then 1 else 0 end) as evaluacion, " \
                   " sum(case when p.state='culminado' then 1 else 0 end) as culminados " \
                   "from jpv_cp_carga_proyecto as p where %s active=True " % condicion)
        datos_gererales=cr.dictfetchone()
        return http.request.website.render(
                        'jpv_estadistica.estadisticas_index2', 
                        {'datos':'hola mundo'})
    
    
    #~ Estadistica de la grafica de torta por tipo de sector de inversion 
    
    @http.route(
            ['/eptEstadisticasPeriodoSectorInves'], 
            type='json', auth="user", website=True)
    def periodo_sector_inversion(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not self.condicion:
            condicion=""
            if int(post['periodo_id'])>0:
                condicion=" p.periodo_id=%s and" % post['periodo_id']
            if int(post['ciclo_id'])>0:
                condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
            if int(post['estado_id'])>0:
                condicion=condicion+" p.estado_id=%s and" % post['estado_id']
            if int(post['entidad_id'])>0:
                condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
        else:
            condicion=self.condicion
        cr.execute("select count(p.tipo_sector_id) as total, s.name "\
                        "from jpv_cp_carga_proyecto as p " \
                        "left join jpv_cp_tipo_sectores as s on p.tipo_sector_id=s.id "\
                        "where %s p.active=True "\
                        "group by p.tipo_sector_id, s.name" % condicion)
        datos_sector_inv=cr.dictfetchall()
        self.condicion=""
        return datos_sector_inv
    
    #~ Estadistica de la grafica de torta por Categoria  de inversion
    
    @http.route(
            ['/eptEstadisticasPeriodoCategoria'], 
            type='json', auth="user", website=True)
    def periodo_Categoria(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not self.condicion:
            condicion=""
            if int(post['periodo_id'])>0:
                condicion=" p.periodo_id=%s and" % post['periodo_id']
            if int(post['tipo_sector_id'])>0:
                condicion=" p.tipo_sector_id=%s and" % post['tipo_sector_id']
            if int(post['ciclo_id'])>0:
                condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
            if int(post['estado_id'])>0:
                condicion=condicion+" p.estado_id=%s and" % post['estado_id']
            if int(post['entidad_id'])>0:
                condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
        else:
            condicion=self.condicion
        cr.execute("select categoria_id, categoria,count(categoria_id) as total"\
                " from(select p.categoria_id as categoria_id, s.name as categoria"\
                " from jpv_cp_carga_proyecto as p "\
                " right join jpv_cp_tipo_sectores as s on p.categoria_id=s.id "\
                " where %s p.active=True )"\
                " cantidad_categoria group by categoria_id,categoria"  % condicion) 
                        
        datos_sector_inv=cr.dictfetchall()
        self.condicion=""
        return datos_sector_inv
        
    #~ Estadistica de la grafica de torta por Subategoria  de inversion
    
    @http.route(
            ['/eptEstadisticasPeriodoSubategoria'], 
            type='json', auth="user", website=True)
    def periodo_Subcategoria(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not self.condicion:
            condicion=""
            if int(post['periodo_id'])>0:
                condicion=" p.periodo_id=%s and" % post['periodo_id']
            if int(post['categoria_id'])>0:
                condicion=" p.categoria_id=%s and" % post['categoria_id']
            if int(post['ciclo_id'])>0:
                condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
            if int(post['estado_id'])>0:
                condicion=condicion+" p.estado_id=%s and" % post['estado_id']
            if int(post['entidad_id'])>0:
                condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
        else:
            condicion=self.condicion

        cr.execute("select subcategoria_id, subcategoria,count(subcategoria_id) as total"\
                " from(select p.subcategoria_id as subcategoria_id, s.name as subcategoria"\
                " from jpv_cp_carga_proyecto as p "\
                " right join jpv_cp_tipo_sectores as s on p.subcategoria_id=s.id "\
                " where %s p.active=True )"\
                " cantidad_subcategoria group by subcategoria_id,subcategoria"  % condicion) 
                        
        datos_sector_inv=cr.dictfetchall()
        self.condicion=""
        return datos_sector_inv
        
        #~ Ruta de estadistica de barra de la cantidad de proyectos diferidos   
        
    @http.route(
            ['/eptEstadisticasDiferidos'], 
            type='json', auth="user", website=True)
    def periodo_Diferidos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        dictamen_valoracion_obj=registry['jpv_val.dictamen_valoracion']
        condicion=[('state','=','diferido')]
        if int(post['periodo_id'])>0:
            condicion.append(('periodo_id','=',int(post['periodo_id'])))
        if int(post['ciclo_id'])>0:
            condicion.append(('ciclo_id','=',int(post['ciclo_id'])))
        if int(post['estado_id'])>0:
            condicion.append(('estado_id','=',int(post['estado_id'])))
        if int(post['entidad_id'])>0:
            condicion.append(('partner_id','=',int(post['entidad_id'])))
        proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,condicion)
        cantidad=len(proyecto_ids)
        if (cantidad==1):
            condicion="("+str(proyecto_ids[0])+")"
        else:
            condicion=str(tuple(proyecto_ids))
        if (cantidad>0):
            cr.execute("select pregunta, mensaje, respuesta_id, count(pregunta) " \
                        " from ( select d.id as dictamen_id, r.id,p.nombre as pregunta, " \
                        " ir.respuesta as respuesta, ir.mensaje as mensaje, " \
                        " ir.id as respuesta_id " \
                        " from  jpv_val_dictamen_valoracion as d, "\
                        " jpv_val_resultados_valoraciones as r, "\
                        " jpv_conf_valoracion_preguntas as p, "\
                        " jpv_conf_valoracion_items_respueta as ir "\
                        " where d.proyecto_id in %s and d.dictamen='diferido'"\
                        " and p.id=r.pregunta_id and ir.id=r.resp_texto_siple_id"\
                        " and ir.state='diferido'"\
                        " and d.active=True and r.dictamen_id=d.id) jpv_conf_valoracion_preguntas GROUP BY pregunta,mensaje,respuesta_id " % condicion)
            datos_dictamen=cr.dictfetchall()
        else:
            datos_dictamen="[{'count': 0L,respuesta_id:0l,mensaje:'''}]"
        return {'datos':datos_dictamen,'cantidad':cantidad}
        
        
    #~ datos para la tabla de referencia de lectura de los motivos de las valoraciones
    @http.route(
            ['/eptEstadisticasTablaValoracion'], 
            type='json', auth="user", website=True)
    def Datos_ref_tabla_valoracion(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        preguntas_obj=registry['jpv_conf.valoracion_preguntas']
        pregunta_ids=preguntas_obj.search(cr,SUPERUSER_ID,[
                                ('dependiente','=',False)
                                ])
        pregunta_data=preguntas_obj.browse(cr,SUPERUSER_ID,pregunta_ids)
        datos_tabla={'diferido':{}}
        for pregunta in pregunta_data:
            for respuesta in pregunta.respuesta_ids:
                if respuesta.state=='diferido':
                    mensajes=[]
                    for dependencia in respuesta.dependencia_line:
                        for respuesta_dep in dependencia.pregunta_id.respuesta_ids:
                            if respuesta_dep.state=='diferido' and dependencia.accion_type=="abre":
                                mensajes.append(respuesta_dep.mensaje)
                        datos_tabla['diferido'].update({'Pregunta: '+pregunta.nombre+'<br>Motivo: '+respuesta.mensaje:mensajes})
                if respuesta.state=='aprobado':
                    mensajes=[]
                    for dependencia in respuesta.dependencia_line:
                        for respuesta_dep in dependencia.pregunta_id.respuesta_ids:
                            if respuesta_dep.state=='diferido' and dependencia.accion_type=="abre":
                                mensajes.append(respuesta_dep.mensaje)
                            if dependencia.accion_type=="abre":
                                datos_tabla['diferido'].update({'Pregunta: '+pregunta.nombre:mensajes})
        return datos_tabla
    
        #~ Ruta de los proyectos en valoracion y que estan diferidos (grafica de barra)
    @http.route(
            ['/eptEstadisticasValoracionDiferidos'], 
            type='json', auth="user", website=True)
    def datos_valoracion_diferidos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        dictamen_valoracion_obj=registry['jpv_val.dictamen_valoracion']
        condicion=[('state','=','evaluacion')]
        if int(post['periodo_id'])>0:
            condicion.append(('periodo_id','=',int(post['periodo_id'])))
        if int(post['ciclo_id'])>0:
            condicion.append(('ciclo_id','=',int(post['ciclo_id'])))
        if int(post['estado_id'])>0:
            condicion.append(('estado_id','=',int(post['estado_id'])))
        if int(post['entidad_id'])>0:
            condicion.append(('partner_id','=',int(post['entidad_id'])))
        proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,condicion)
        cantidad=len(proyecto_ids)
        if (cantidad==1):
            condicion="("+str(proyecto_ids[0])+")"
        else:
            condicion=str(tuple(proyecto_ids))
        if (cantidad>0):
            cr.execute("select pregunta, mensaje, respuesta_id, count(pregunta) " \
                        " from ( select d.id as dictamen_id, r.id,p.nombre as pregunta, " \
                        " ir.respuesta as respuesta,ir.mensaje as mensaje, " \
                        " ir.id as respuesta_id " \
                        " from  jpv_val_dictamen_valoracion as d, "\
                        " jpv_val_resultados_valoraciones as r, "\
                        " jpv_conf_valoracion_preguntas as p, "\
                        " jpv_conf_valoracion_items_respueta as ir "\
                        " where d.proyecto_id in %s and d.dictamen='diferido'"\
                        " and p.id=r.pregunta_id and ir.id=r.resp_texto_siple_id"\
                        " and ir.state='diferido' and d.state='abierta'"\
                        " and d.active=True and r.dictamen_id=d.id) jpv_conf_valoracion_preguntas GROUP BY pregunta,mensaje,respuesta_id " % condicion)
            datos_dictamen=cr.dictfetchall()
        else:
            datos_dictamen="[{'count': 0L,respuesta_id:0l,mensaje:'''}]"
            datos_dictamen=[]
        return {'datos':datos_dictamen,'cantidad':len(datos_dictamen)}
        
 #~ Ruta de grafica de torta de estadistica de proyectos en valoracion
    @http.route(
            ['/eptEstadisticasDictamenesProyectosValoracion'], 
            type='json', auth="user", website=True)
    def cant_dictamenes_proyectos_valoracion(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        condicion=[('state','=','evaluacion')]
        if int(post['periodo_id'])>0:
            condicion.append(('periodo_id','=',int(post['periodo_id'])))
        if int(post['ciclo_id'])>0:
            condicion.append(('ciclo_id','=',int(post['ciclo_id'])))
        if int(post['estado_id'])>0:
            condicion.append(('estado_id','=',int(post['estado_id'])))
        if int(post['entidad_id'])>0:
            condicion.append(('partner_id','=',int(post['entidad_id'])))
        proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,condicion)
        cantidad=len(proyecto_ids)
        if (cantidad==1):
            condicion="("+str(proyecto_ids[0])+")"
        else:
            condicion=str(tuple(proyecto_ids))
        if (cantidad>0):
            cr.execute("select d.proyecto_id,d.dictamen "\
                            "from jpv_val_dictamen_valoracion as d "\
                            "where  d.proyecto_id in %s and d.active=true and d.state='abierta' " % condicion)
            
            dictamenes=cr.dictfetchall()
        else:
            dictamenes={}
        #~ print dictamenes
        unir_dictamenes={}
        cant_resultado={'negado':0,'aprobado':0,'diferido':0,'porValorar':0}
        for dictamen in dictamenes:
            if unir_dictamenes.has_key(dictamen['proyecto_id']):
                unir_dictamenes[dictamen['proyecto_id']].update({'dictamen2':dictamen['dictamen']})
                dictamen_list=unir_dictamenes[dictamen['proyecto_id']].values()
                if 'negado' in dictamen_list:
                     cant_resultado['negado']=cant_resultado['negado']+1
                     proyecto_obj.write(cr, SUPERUSER_ID,[int(dictamen['proyecto_id'])],{'dictamengraph':'Negado'},0)
                elif 'diferido' in dictamen_list:
                    cant_resultado['diferido']=cant_resultado['diferido']+1
                    proyecto_obj.write(cr, SUPERUSER_ID,[int(dictamen['proyecto_id'])],{'dictamengraph':'Diferido'},0)
                else:
                    cant_resultado['aprobado']=cant_resultado['aprobado']+1
                    proyecto_obj.write(cr, SUPERUSER_ID,[int(dictamen['proyecto_id'])],{'dictamengraph':'Aprobado'},0)

            else:
                unir_dictamenes[dictamen['proyecto_id']]={'dictamen1':dictamen['dictamen']}
            
        cant_resultado['porValorar']=len(proyecto_ids)-(cant_resultado['negado']+cant_resultado['diferido']+cant_resultado['aprobado'])
        return cant_resultado
        
 #~ Ruta de mostrar la lista de proyectos diferidos
    @http.route(
            ['/EptMostarListaProyectosDiferidos'], 
            type='json', auth="user", website=True)
    def jpv_devolver_datos_proyecto(self,post2=None,**post):
        if not post2==None:
            post=post2
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        respuesta_obj=registry['jpv_conf.valoracion_items_respueta']
        condicion=[('state','=','diferido')]
        if post['estado_id']=='':
            post['estado_id']='0'
        if post['entidad_id']=='':
            post['entidad_id']='0'
        if post['ciclo_id']=='':
            post['ciclo_id']='0'
        if int(post['periodo_id'])>0:
            condicion.append(('periodo_id','=',int(post['periodo_id'])))
        if int(post['ciclo_id'])>0:
            condicion.append(('ciclo_id','=',int(post['ciclo_id'])))
        if int(post['estado_id'])>0:
            condicion.append(('estado_id','=',int(post['estado_id'])))
        if int(post['entidad_id'])>0:
            condicion.append(('partner_id','=',int(post['entidad_id'])))
        proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,condicion)
        dictamenes_datos=[]
        cantidad=len(proyecto_ids)
        if (cantidad==1):
            condicion="("+str(proyecto_ids[0])+")"
        else:
            condicion=str(tuple(proyecto_ids))
        if (cantidad>0):
            cr.execute("select vp.id as pregunta_id,p.id as proyecto_id,vp.nombre as pregunta, "\
                            "ir.mensaje, vp.dependiente,ir.id as respuesta_id, "\
                            "p.nombre_proyecto,r_p.name as entidad,p.correlativo, "\
                            "p.monto_proyecto,e.estado "\
                            "from jpv_val_dictamen_valoracion as d "\
                            "left join jpv_cp_carga_proyecto as p on p.id=d.proyecto_id "\
                            "left join res_partner as r_p on r_p.id=p.partner_id "\
                            "left join jpv_val_resultados_valoraciones as r on r.dictamen_id=d.id "\
                            "left join jpv_conf_valoracion_preguntas as vp on vp.id=r.pregunta_id "\
                            "left join jpv_conf_valoracion_items_respueta as ir on ir.id=r.resp_texto_siple_id "\
                            "left join jpv_ent_estados as e on e.id=p.estado_id "\
                            "where ir.state='diferido'  and d.dictamen='diferido'  "\
                            " and d.active=true and d.proyecto_id in %s order by entidad DESC " % condicion)
            
            dictamenes_datos=cr.dictfetchall()
        else:
            dictamenes={}
        unir_dictamenes={}
        for dictamen in  dictamenes_datos:
            if unir_dictamenes.has_key(dictamen['proyecto_id']):
                if dictamen['dependiente']:
                    unir_dictamenes[dictamen['proyecto_id']].append(dictamen)
                else:
                    respuesta=respuesta_obj.browse(cr,uid,[int(dictamen['respuesta_id'])])
                    adicionar=True
                    for dependencia in respuesta.dependencia_line:
                        if dependencia.accion_type=="abre":
                            adicionar=False
                    if adicionar:
                        unir_dictamenes[dictamen['proyecto_id']].append(dictamen)
            else:
                if dictamen['dependiente']:
                    unir_dictamenes[dictamen['proyecto_id']]=[dictamen]
                else:
                    respuesta=respuesta_obj.browse(cr,uid,[int(dictamen['respuesta_id'])])
                    adicionar=True
                    for dependencia in respuesta.dependencia_line:
                        if dependencia.accion_type=="abre":
                            adicionar=False
                    if adicionar:
                            unir_dictamenes[dictamen['proyecto_id']]=[dictamen]
        return unir_dictamenes

#~ Descargar csv de proyectos con estatus diferido
    @http.route(
            ['/EptDescargarListaProyectosDiferidosCsv'], 
            type='http', auth="user", method="post",website=True)
    def jpv_descargar_csv_diferidos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyectos_csv=self.jpv_devolver_datos_proyecto(post)
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer.writerow([name.encode('utf-8') for name in self.head_csv])
        for proyecto in proyectos_csv:
            motivos=[]
            for motivo in proyectos_csv[proyecto]:
                motivos.append(motivo['mensaje'])
            motivos='\n'.join(motivos)
            row = [
                proyectos_csv[proyecto][0]['correlativo'],
                proyectos_csv[proyecto][0]['entidad'],
                proyectos_csv[proyecto][0]['estado'],
                proyectos_csv[proyecto][0]['monto_proyecto'],
                motivos.strip()
            ]
            writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        nombre_archivo='lista_proyectos_Diferidos.csv'
        return request.make_response(data,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_archivo)),
                         ('Content-Type', 'text/csv;charset=utf8')],
                cookies={'fileToken': '212123f4646546'})

#~ Ruta de mostrar la lista de proyectos en valoracion pero diferidos
    @http.route(
            ['/EptMostarListaProyectosValoracionDiferidos'], 
            type='json', auth="user", website=True)
    def jpv_datos_proyecto_valoaracion_diferidos(self,post2=None,**post):
        if not post2==None:
            post=post2
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyecto_obj=registry['jpv_cp.carga_proyecto']
        respuesta_obj=registry['jpv_conf.valoracion_items_respueta']
        condicion=[('state','=','evaluacion')]
        if post['estado_id']=='':
            post['estado_id']='0'
        if post['entidad_id']=='':
            post['entidad_id']='0'
        if post['ciclo_id']=='':
            post['ciclo_id']='0'
        if int(post['periodo_id'])>0:
            condicion.append(('periodo_id','=',int(post['periodo_id'])))
        if int(post['ciclo_id'])>0:
            condicion.append(('ciclo_id','=',int(post['ciclo_id'])))
        if int(post['estado_id'])>0:
            condicion.append(('estado_id','=',int(post['estado_id'])))
        if int(post['entidad_id'])>0:
            condicion.append(('partner_id','=',int(post['entidad_id'])))
        proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,condicion)
        dictamenes_datos=[]
        cantidad=len(proyecto_ids)
        if (cantidad==1):
            condicion="("+str(proyecto_ids[0])+")"
        else:
            condicion=str(tuple(proyecto_ids))
        if (cantidad>0):
            cr.execute("select vp.id as pregunta_id,p.id as proyecto_id,vp.nombre as pregunta, "\
                            "ir.mensaje, vp.dependiente,ir.id as respuesta_id, "\
                            "p.nombre_proyecto,r_p.name as entidad,p.correlativo, "\
                            "p.monto_proyecto, e.estado "\
                            "from jpv_val_dictamen_valoracion as d "\
                            "left join jpv_cp_carga_proyecto as p on p.id=d.proyecto_id "\
                            "left join res_partner as r_p on r_p.id=p.partner_id "\
                            "left join jpv_val_resultados_valoraciones as r on r.dictamen_id=d.id "\
                            "left join jpv_conf_valoracion_preguntas as vp on vp.id=r.pregunta_id "\
                            "left join jpv_conf_valoracion_items_respueta as ir on ir.id=r.resp_texto_siple_id "\
                            "left join jpv_ent_estados as e on e.id=p.estado_id "\
                            "where ir.state='diferido' and d.state='abierta' and d.dictamen='diferido'  "\
                            " and d.active=true and d.proyecto_id in %s order by entidad DESC " % condicion )
            
            dictamenes_datos=cr.dictfetchall()
        else:
            dictamenes={}
        unir_dictamenes={}
        for dictamen in  dictamenes_datos:
            if unir_dictamenes.has_key(dictamen['proyecto_id']):
                if dictamen['dependiente']:
                    unir_dictamenes[dictamen['proyecto_id']].append(dictamen)
                else:
                    respuesta=respuesta_obj.browse(cr,uid,[int(dictamen['respuesta_id'])])
                    adicionar=True
                    for dependencia in respuesta.dependencia_line:
                        if dependencia.accion_type=="abre":
                            adicionar=False
                    if adicionar:
                        unir_dictamenes[dictamen['proyecto_id']].append(dictamen)
            else:
                if dictamen['dependiente']:
                    unir_dictamenes[dictamen['proyecto_id']]=[dictamen]
                else:
                    respuesta=respuesta_obj.browse(cr,uid,[int(dictamen['respuesta_id'])])
                    adicionar=True
                    for dependencia in respuesta.dependencia_line:
                        if dependencia.accion_type=="abre":
                            adicionar=False
                    if adicionar:
                            unir_dictamenes[dictamen['proyecto_id']]=[dictamen]
        return unir_dictamenes

#~ Descargar csv de proyectos en Valoracion con estatus diferido
    @http.route(
            ['/EptDescargarListaProyectosValoracionDiferidosCsv'], 
            type='http', auth="user", method="post",website=True)
    def jpv_descargar_csv_Valoraciondiferidos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        proyectos_csv=self.jpv_datos_proyecto_valoaracion_diferidos(post)
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer.writerow([name.encode('utf-8') for name in self.head_csv])
        for proyecto in proyectos_csv:
            motivos=[]
            for motivo in proyectos_csv[proyecto]:
                motivos.append(motivo['mensaje'])
            motivos='\n'.join(motivos)
            row = [
                proyectos_csv[proyecto][0]['correlativo'],
                proyectos_csv[proyecto][0]['entidad'],
                proyectos_csv[proyecto][0]['estado'],
                proyectos_csv[proyecto][0]['monto_proyecto'],
                motivos.strip()
            ]
            writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        nombre_archivo='lista_proyectos_Diferidos.csv'
        return request.make_response(data,
                headers=[('Content-Disposition',
                                main.content_disposition(nombre_archivo)),
                         ('Content-Type', 'text/csv;charset=utf8')],
                cookies={'fileToken': '212123f4646546'})
                
#~ se crea este metodo ya que en el dispositivo movil solo se muestra los
#~ estados de aprobado,diferidos,culminados y negados
    def periodo_general_movil(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not self.condicion:
            condicion=""
            if int(post['periodo_id'])>0:
                condicion=" p.periodo_id = %s and " % post['periodo_id']
            if int(post['ciclo_id'])>0:
                condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
            if int(post['estado_id'])>0:
                condicion=condicion+" p.estado_id=%s and" % post['estado_id']
            if int(post['entidad_id'])>0:
                condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
        else:
            condicion=self.condicion
        datos_gererales={}
        cr.execute(" select sum(case when p.state='aprobado'  then 1 else 0 end) as Aprobados, "\
                   " sum(case when p.state='diferido' then 1 else 0 end) as Diferidos, " \
                   " sum(case when p.state='negado' then 1 else 0 end) as Negados, " \
                   " sum(case when p.state='culminado' then 1 else 0 end) as Culminados " \
                   "from jpv_cp_carga_proyecto as p where %s p.active=True " % condicion)
        datos_query=cr.dictfetchone()
        for state in datos_query:
            datos_gererales[state.capitalize()]=datos_query[state]
        self.condicion=""
        return {'datos':datos_gererales}
