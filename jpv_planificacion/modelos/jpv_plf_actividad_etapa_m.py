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
from jpv_plf_comunes import *
from datetime import datetime, date, time, timedelta

class jpv_plf_actividad_etapas(osv.osv):
    _name='jpv_plf.actividad_etapas'
    _rec_name='tipo_planificacion_id'
    _description=u"""Estas son las actividades que se programaran dentro/
                     de las  etapas que conformaran los periodos/
                     para la gestión de los proyectos de las Entidades/"""
    
    
    _columns={ 
        'etapas_id':fields.many2one(
                    'jpv_plf.etapas',
                    """Etapas""",
                    ondelete='cascade',
                    required=True,),
        'tipo_planificacion_id':fields.many2one(
                    'jpv_plf.tipo_planificacion',
                    """Actividades""",
                    required=True,),
        'fecha_inicio':fields.datetime(
                    'Fecha de Inicio',
                    required=True,
                    help='Seleccione la fecha de inicio de la actividad'),
        'fecha_fin':fields.datetime(
                    'Fecha Final',
                    required=True,
                    help='Seleccione la fecha final de la actividad'),
        }
   
    
    def plf_fecha_actividad_etapa(  self, cr, uid, ids, fecha_inicio, 
                                    fecha_fin, fecha_ini_etapa, 
                                    fecha_fin_etapa, context=None):
        fechas={}
        mensaje={}
        if fecha_inicio and fecha_fin:
            fecha_inicio=fecha_inicio.split(' ')[0]
            fecha_fin=fecha_fin.split(' ')[0]
            if validar_fecha(fecha_inicio, fecha_fin).values()[0]!={}:
                fechas=validar_fecha(fecha_inicio, fecha_fin).values()[1]
                mensaje=validar_fecha(fecha_inicio, fecha_fin).values()[0]
                return {
                    'warning':mensaje,
                    'value':fechas
                        }
            if fecha_inicio and fecha_fin:
                fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_inicio =datetime.date(fecha_inicio)
                fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d')
                fecha_fin =datetime.date(fecha_fin)
                fecha_ini_etapa=datetime.strptime(fecha_ini_etapa, '%Y-%m-%d')
                fecha_ini_etapa =datetime.date(fecha_ini_etapa)
                fecha_fin_etapa=datetime.strptime(fecha_fin_etapa, '%Y-%m-%d')
                fecha_fin_etapa =datetime.date(fecha_fin_etapa)
                if cmp(fecha_ini_etapa,fecha_inicio)==1 or cmp(fecha_fin,fecha_fin_etapa)==1:
                    fechas={
                        'fecha_inicio':'',
                        'fecha_fin':'',
                            }
                    mensaje={
                        'title':('Error de fecha'),
                        'message':('Las fechas de la actividad no se encuentran\
                                    dentro del rango de fechas establacido para\
                                    el ciclo '),
                        }
            return {
                'warning':mensaje,
                'value':fechas
                    }
    
    def plf_limpiar_fecha_actividad_etapa(self, cr, uid, ids, 
                                            fecha_inicio, context=None):
        return limpiar_campo_fecha(fecha_inicio)
        
    def plf_tipo_planificacion_id(self, cr, uid, ids, fecha_inicio,
                                    fecha_fin, context=None):
        if not fecha_inicio:
            raise osv.excjpv_osv(('Fechas de la etapa no definida!'), 
                                ('Seleccione una fecha inicial y una\
                                 fecha final.'))
        if not fecha_fin:
            raise osv.excjpv_osv(('Fechas de la etapa no definida!'), 
                                ('Seleccione una fecha inicial y una\
                                 fecha final.'))
        return True
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals:
            lista_2=[]
            lista=vals.keys()
            for i in lista:
                if i!='state':
                    lista_2.append(i)

            if len(lista_2)>=1:
                cp_plf_periodos_objeto=self.pool.get('jpv_plf.etapas')
                etapas_datos=self.browse(cr,uid,ids)
                cp_plf_periodos_objeto.write(cr,uid,
                                            int(etapas_datos['etapas_id']),
                                            {'state':'inactivo'},
                                            context=context)
        return super(jpv_plf_actividad_etapas, self).write(cr, uid, ids, 
                                                vals, context=context)
    
