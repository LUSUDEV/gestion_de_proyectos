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
from jpv_plf_comunes import *


class jpv_plf_etapas(osv.osv):
    _name='jpv_plf.etapas'
    _rec_name='nombre'
    _description=u"""Estas son las etapas que conformaran los periodos\
                     para la gestión de los proyectos de las Entidades\
                        """
        
    _columns={
        'nombre':fields.char( 
                    'Nombre del Ciclo',
                    size=80,
                    required=True,
                    help='Describa el nombre del ciclo a registrar'),
        'codigo':fields.char( 
                    'Codigo del Ciclo',
                    size=80,
                    required=False,
                    readonly=True,
                    help='Codigo del ciclo'),
        'fecha_inicio':fields.date(
                    'Fecha de Inicio',
                    required=True,
                    help='Seleccione la fecha de inicio del ciclo'),
        'fecha_fin':fields.date(
                    'Fecha Final',
                    required=True,
                    help='Seleccione la fecha final del ciclo'),
        'rango_accion':fields.selection(
                    [('todas', 'Todas las Entidades'),
                    ('algunas', 'Algunas Entidades')],
                     'Aplicar a:',
                    required=True,
                    help="Seleccione a cuales entidades se desean aplicar \
                    las reglas del ciclo que se esta creando."),
         'active':fields.boolean(
                    'Activo',
                    help="""Si esta activo el motor lo incluira en la 
                    vista."""),
        'periodo_id':fields.many2one(
                    'jpv_plf.periodos',
                    """Periodos""",
                    ondelete='restrict',
                    required=True,),
        'actividades_etapas_ids':fields.one2many(
                                'jpv_plf.actividad_etapas',
                                'etapas_id',
                                'Actividades',
                                 help="Aqui se seleccionaran las actividades\
                                         y las fechas a realizar en cada ciclo",
                                ),
        'tipo_entidades_ids':fields.many2many(
                                'jpv_ent.tipo_entidades',
                                'jpv_plf_etapas_tipo_entidades_rel',
                                'etapa_id',
                                'tipo_entidad_id',
                                'Tipos de Entidades',
                                required=False,
                                help="Seleccione los tipos de entidades a\
                                            los que se le aplicara el ciclo"),
        'entidades_ids': fields.many2many(
                                'jpv_ent.entidades', 
                                'jpv_plf_entidad_etapa_rel', 
                                'etapa_id', 
                                'entidad_id', 
                                'Entidades',
                                copy=False,
                                required=False,
                                help='Aqui se seleccionaran el grupo de \
                                        entidades a las que se le aplicara el ciclo'),
        'state':fields.selection(
                    [('inactivo', 'Inactivo'),
                    ('activo', 'Activo')],
                     'Estaus',
                    help='Aquí se selecciona el estado, si esta activo,\
                                el sistema tomara este ciclo como la\
                             planificacion ṕara todas las actividades.'),
        }
   
   
    _defaults={
        'active':True,
        'state':'inactivo'
            }
            
    
    def plf_activar_etapa(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'activo'},context=context)
    def plf_desactivar_etapa(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'inactivo'},context=context)
    
    def plf_fecha_etapa(self, cr, uid, ids, fecha_inicio, 
                                fecha_fin, context=None):
        fechas={}
        mensaje={}
        if validar_fecha(fecha_inicio, fecha_fin).values()[0]!={}:
            fechas=validar_fecha(fecha_inicio, fecha_fin).values()[1]
            mensaje=validar_fecha(fecha_inicio, fecha_fin).values()[0]
            return {
                'warning':mensaje,
                'value':fechas
                    }
        if fecha_fin:
            fechas={
                'actividades_etapas_ids':''
                }
            return {
                'value':fechas
                    }
        
    def plf_limpiar_fecha_etapa(self, cr, uid, ids, fecha_inicio, context=None):
        fechas={}
        mensaje={}
        if fecha_inicio:
            hoy=date.today()
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_inicio =datetime.date(fecha_inicio)
            if cmp(hoy,fecha_inicio)==1:
                mensaje={
                    'title':('Error de fecha'),
                    'message':('La fecha de inicio no puede ser menor\
                                a la fecha de hoy'),
                    }
                fechas={
                    'fecha_inicio':'',
                    }
            else:
                fechas={
                    'fecha_fin':'',
                    'actividades_etapas_ids':''
                    }
        return {
            'warning':mensaje,
            'value':fechas
                }
            
    def plf_limpiar_rango_accion(self, cr, uid, ids, rango_accion, context=None):
        limpiar={}
        ent_tipo_entidades_objeto=self.pool.get('jpv_ent.tipo_entidades')
        ent_tipo_id=ent_tipo_entidades_objeto.search(cr,uid,[])
        if rango_accion=='todas':
            limpiar={
                'tipo_entidades_ids':[(6, 0,ent_tipo_id)],
                'entidades_ids':''
                }
        else:
            limpiar={
                'tipo_entidades_ids':'',
                'entidades_ids':''
                }
            
        return {
            'value':limpiar
                }
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals:
            lista_2=[]
            lista=vals.keys()
            for i in lista:
                if i!='state':
                    lista_2.append(i)
            if len(lista_2)>=1:
                 vals.update({
                    'state':'inactivo'
                    })
        return super(jpv_plf_etapas, self).write(cr, uid, ids, 
                                                vals, context=context)
    
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'nombre':vals['nombre'].upper()
                })
        etapa_id=super(jpv_plf_etapas, self).create(cr, uid, 
                                                vals, context=context)
        etapa_ids=self.search(cr,uid,[('periodo_id','=',vals['periodo_id'])],
                                                    limit=2,order='id desc')
        etapa_datos=self.browse(cr,uid,etapa_ids)
        if len(etapa_ids)<=1:
            self.write(cr,uid,etapa_id,{'codigo':'C-1'})
        else:
            for c in etapa_datos:
                ant=c.codigo
            p,n=ant.split('-')
            n=int(n)+1
            self.write(cr,uid,etapa_id,{'codigo':'C-'+str(n)})
        return etapa_id
      
        

