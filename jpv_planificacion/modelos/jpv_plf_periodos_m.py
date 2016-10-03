# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
#    Modulo Desarrollado por Juventud Productiva (Jonathan Reyes)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################
from openerp.osv import fields, osv
from openerp.http import request
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *
from jpv_plf_comunes import * 


class jpv_plf_periodos(osv.osv):
    _name='jpv_plf.periodos'
    _rec_name='periodo_fiscal'
    _description=u"""Estos son los periodos para la gestión de los\
                proyectos de las Entidades"""
                
    def plf_anio_seleccion(self, cursor, user_id, context=None):
        format="%Y"
        anio_actual=date.today()
        anio_ant_2=anio_actual+relativedelta(years=-2)   #quitar despues de migracion
        anio_ant=anio_actual+relativedelta(years=-1)
        anio_prox=anio_actual+relativedelta(years=+1)
        anio_ant_2=anio_ant_2.strftime(format)              #quitardespues de la migracion
        anio_ant=anio_ant.strftime(format)
        anio_actual=anio_actual.strftime(format)
        anio_prox=anio_prox.strftime(format)
        
        return (
            (anio_ant_2,anio_ant_2), #quitar despues de migracion
            (anio_ant,anio_ant),
            (anio_actual,anio_actual),
            (anio_prox,anio_prox))
    def get_select_porcentaje(desde,hasta,rango):
        porc=[]
        
        for i in range(desde,hasta,rango):
            porc.append((str(i),str(i)+'%'))
        return porc

    
    _columns={ 
        'periodo_fiscal':fields.selection(
                    plf_anio_seleccion,
                    'Periodo Fiscal',
                    required=True,
                    help='Seleccione el año del periodo fiscal'),
        'fecha_inicio':fields.date(
                    'Fecha de Inicio',
                    readonly=True,
                    help='Seleccione la fecha de inicio del periodo'),
        'fecha_fin':fields.date(
                    'Fecha Final',
                    readonly=True,
                    help='Seleccione la fecha final del periodo'),
        'porc_manten':fields.selection(
                        get_select_porcentaje(0,105,5),
                        'Porcentaje de Mantenimiento',
                        size=3,
                        required=True,
                        help="""Aqui se coloca el porcentaje de mantenimiento"""),
         'active':fields.boolean(
                    'Activo',
                    help="""Si esta activo el motor lo incluira en la 
                    vista."""),
        'ip_usuario':fields.char(
                    'Ip de usuario',
                    size=15,
                    help='Indica de que ip se esta haciendo'),
        'etapas_ids':fields.one2many(
                        'jpv_plf.etapas',
                        'periodo_id',
                        'Ciclos',
                        help='Ciclos que conformaran el periodo fiscal',
                        ),
    }
    
    _defaults={
        'active':True,
        'ip_usuario' : lambda self,cr,uid,context: request.httprequest.remote_addr,
        'estado' :'borrador',
            }
    _order = "periodo_fiscal desc"
    
    _sql_constraints = [
        ('periodo_fiscal_unico', 'unique (periodo_fiscal)', 'El periodo fiscal ya existe')
    ]
    
    
    def plf_cambiar_estado_evaluacion(self,cr,uid,ids=None,context=None):
        
        hoy=date.today()
        actividad='VALORACIÓN DE PROYECTOS'
        mensaje={
            'title':('Error'),
            'message':('La actividad de '+actividad+' no esta habilitada'),
                }
        list_aviso=[]
        format="%Y"
        anio=hoy.strftime(format)
        proyecto_id=self.search(cr,uid,[('periodo_fiscal','=',anio)])
        for periodo in self.browse(cr,uid,proyecto_id):
            for etapa in periodo.etapas_ids:
                if etapa.state=='activo':
                    for activida in etapa.actividades_etapas_ids:
                        if str(activida.tipo_planificacion_id.nombre_tipo_planificacion)==actividad:
                            fecha_inicio=activida.fecha_inicio.split(' ')[0]
                            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                            fecha_inicio =datetime.date(fecha_inicio)
                            if cmp(hoy,fecha_inicio)==0:
                                list_aviso.append(etapa.id)
                                carga_proyecto_objeto=self.pool.get('jpv_cp.carga_proyecto')
                                carga_proyecto_ids=carga_proyecto_objeto.search(cr,uid,[('ciclo_id','=',etapa.id),('state','=','carga')])
                                carga_proyecto_objeto.write(cr,uid,carga_proyecto_ids,{'state':'evaluacion'},modificacion_interna=0)
                                for ids_proyecto in carga_proyecto_ids:
                                    cp_historial_obj=self.pool.get('jpv_cp.historial_proyecto')
                                    mensaje={
                                        'descripcion':'Su proyecto se encuentra en el proceso de Valoración',
                                        'proyecto_id':ids_proyecto,
                                        }
                                    cp_historial_obj.create(cr,uid,mensaje)
        if len(list_aviso)>0:
            return True
        else:
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'La actividad de '+actividad+' no esta habilitada'))
    
    def plf_validar_nombre_etapa(self, cr, uid, ids, context=None):
        nombre_etapas=[]
        for etapa in self.browse(cr,uid,ids):
            for nombre in etapa.etapas_ids:
                nombre_etapas.append(nombre.nombre)
        nombre_etapa = list(set(nombre_etapas))
        if len(nombre_etapa)!=len(nombre_etapas):
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'El Nombre de la etapa no puede repetirse'))
        return True
        
    def plf_cambiar_state_diferido_cancelado(self, cr, uid, ids, context=None):
        carga_proyecto_objeto=self.pool.get('jpv_cp.carga_proyecto')
        carga_proyecto_ids=carga_proyecto_objeto.search(cr,uid,[('state','=','diferido')])
        carga_proyecto_objeto.write(cr,uid,carga_proyecto_ids,{'state':'negado'},modificacion_interna=0)
        return True
        
        
    _constraints = [
        (plf_validar_nombre_etapa, 'El nombre de la etapa no puede repetirse', 
        ['etapas_ids']), 
        ]


    def plf_fecha_inicio_fin(self, cr, uid, ids, 
                            periodo_fiscal, context=None):
        fechas={}
        if periodo_fiscal:
            fecha_inicio="%s-01-01" % (periodo_fiscal,)
            fecha_fin="%s-12-31" % (periodo_fiscal,)
            
            fechas={
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'etapas_ids':'',
                }
            
            return {
                'value':fechas
                    }
                    
    def plf_control_actividades(self, cr, uid, ids,entidad_id,actividad=None,ciclo_id=None,
                                                    anio=None,context=None):
        actividades=['CARGA DE PROYECTOS',
                    'REPARACIÓN DE PROYECTOS',
                    'EVALUACIÓN DE PROYECTOS']
       
        hoy=date.today()
        if not entidad_id:
            raise osv.except_osv(
                                ('Alerta!'),
                                (u'Debe seleccionar una entidad.'))
        if not actividad:
            actividad='CARGA DE PROYECTOS'
        else:
            if not actividad in actividades:
                raise osv.excjpv_osv(
                                ('Alerta!'),
                                (u'La actividad no existe.'))
        if not anio:
            format="%Y"
            anio=hoy.strftime(format)
        
        mensaje={
            'title':('Error'),
            'message':('La actividad de '+actividad+' no esta habilitada'),
                }
        plf_etapas_objeto=self.pool.get('jpv_plf.etapas')
        if not ciclo_id:
            ciclo_id=False
        
        
        
        if ciclo_id==False:
            plf_etapas_ids=plf_etapas_objeto.search(cr,uid,[
                                                    ('fecha_inicio','<=',hoy),
                                                    ('fecha_fin','>=',hoy),
                                                    ('state','=','activo'),])
        else:
            plf_etapas_ids=plf_etapas_objeto.search(cr,uid,[
                                                    ('id','=',int(ciclo_id)),
                                                    ('fecha_inicio','<=',hoy),
                                                    ('fecha_fin','>=',hoy),
                                                    ('state','=','activo'),])
        
        
        if len(plf_etapas_ids)>0:
            ent_entidades_objeto=self.pool.get('jpv_ent.entidades')
            ent_id=ent_entidades_objeto.search(cr,uid,
                                [('parent_id','=',entidad_id)])
            for id_etapa in plf_etapas_objeto.browse(cr,uid,plf_etapas_ids,
                                                            context=context):
                if id_etapa.rango_accion=='todas':
                    for id_tipo_entidad in id_etapa.tipo_entidades_ids:
                        jpv_datos=ent_entidades_objeto.browse(cr,uid,
                                                              ent_id,
                                                              context=context)
                        if int(id_tipo_entidad)==int(jpv_datos['tipo_entidad_id']):
                            for id_actividad in id_etapa.actividades_etapas_ids:
                                if actividad==id_actividad.tipo_planificacion_id.nombre_tipo_planificacion:
                                    fecha_inicio=id_actividad.fecha_inicio.split(' ')[0]
                                    fecha_fin=id_actividad.fecha_fin.split(' ')[0]
                                    fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                                    fecha_inicio =datetime.date(fecha_inicio)
                                    fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d')
                                    fecha_fin=datetime.date(fecha_fin)
                                    if (cmp(fecha_inicio,hoy)==-1 and \
                                                cmp(hoy,fecha_fin)==-1) or \
                                               (cmp(fecha_inicio,hoy)==0) or \
                                               (cmp(hoy,fecha_fin)==0):
                                        periodo={
                                                'periodo':id_etapa.periodo_id,
                                                'codigo':id_etapa.codigo,
                                                'ciclo':id_etapa.id,  
                                                }
                                        return periodo
                else:
                    for id_entidad in id_etapa.entidades_ids:
                        if int(id_entidad.parent_id)==int(entidad_id):
                            for id_actividad in id_etapa.actividades_etapas_ids:
                                if actividad==id_actividad.tipo_planificacion_id.nombre_tipo_planificacion:
                                    fecha_inicio=id_actividad.fecha_inicio.split(' ')[0]
                                    fecha_fin=id_actividad.fecha_fin.split(' ')[0]
                                    fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                                    fecha_inicio =datetime.date(fecha_inicio)
                                    fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d')
                                    fecha_fin=datetime.date(fecha_fin)
                                    if (cmp(fecha_inicio,hoy)==-1 and \
                                                cmp(hoy,fecha_fin)==-1) or \
                                               (cmp(fecha_inicio,hoy)==0) or \
                                               (cmp(hoy,fecha_fin)==0):
                                        periodo={
                                                'periodo':id_etapa.periodo_id,
                                                'codigo':id_etapa.codigo,
                                                'ciclo':id_etapa.id,   
                                                }
                                        return periodo
        return mensaje
            
    
    def registro_crom_periodo(self,cr,uid,ids,periodo_id):
        cron_objeto=self.pool.get('ir.cron')
        crom_ids=cron_objeto.search(cr,uid,[('periodo_fiscal','=',str(periodo_id))])
        if len(crom_ids)>0:
            cron_objeto.unlink(cr,uid,crom_ids)
        for periodo in self.browse(cr,uid,ids):
            for etapa in periodo.etapas_ids:
                for actividades in etapa.actividades_etapas_ids:
                    if  actividades.tipo_planificacion_id.nombre_tipo_planificacion=='VALORACIÓN DE PROYECTOS':
                        cron={
                            'name':'Cambio de estatus carga-valoración '+str(actividades.id),
                            'user_id':1,
                            'priority':0,
                            'interval_number':1,
                            'interval_type':'days',
                            'nextcall':actividades.fecha_inicio,
                            'numbercall':1,
                            'doall':True,
                            'model':'jpv_plf.periodos',
                            'function':'plf_cambiar_estado_evaluacion',
                            'args':(),
                            'periodo_fiscal':ids,
                            }
                        
                        cron_objeto.create(cr,uid,cron)
        return True
    
    def write (self,cr,uid,ids,vals,context=None):
        modificacion=super(jpv_plf_periodos, self).write(cr, uid, ids,vals,context=context)
        for periodo in self.browse(cr,uid,ids):
            self.registro_crom_periodo(cr,uid,ids,periodo.id)
        return True
    
    def create(self,cr,uid,vals,context=None):
        fechas=self.plf_fecha_inicio_fin(cr, uid,[], 
                                        vals['periodo_fiscal'],
                                        context).values()[0]
        periodo_id=super(jpv_plf_periodos, self).create(cr, uid, vals, 
                                                      context=context)
        self.write(cr,uid,periodo_id,fechas,context=context)
        for periodo in self.browse(cr,uid,periodo_id):
            self.registro_crom_periodo(cr,uid,periodo_id,periodo.id)
        return periodo_id
    
class ir_cron(osv.osv):
    
    _inherit= "ir.cron"
    
    _columns={ 
        'periodo_fiscal':fields.char(
                    'Periodo Fiscal',
                    required=False,
                    help='Indique el periodo fiscal para el que desea registrar la actividad automatizada'),
    }
