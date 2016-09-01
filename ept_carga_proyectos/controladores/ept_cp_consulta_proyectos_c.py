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
#    Modulo Desarrollado por Juventud Productiva (Victor Davila)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import date, timedelta
import ept_carga_proyecto_c
from openerp.addons.ept_cuentas.controladores import ept_cuentas_c

_logger = logging.getLogger(__name__)

class ept_cp_consulta_proyectos(http.Controller):
    
    @http.route(
        ['/ept_cp_proyecto_consulta'],
        type='json', auth='user', website=True)
    def consulta_proyectos(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        entidad_id=ept_cuentas_c.ept_cuentas_web().mi_entidad(uid)
        res=[]
        proyectos_obj=registry['ept_cp.carga_proyecto']
        if post['code']==13:
            proyectos_ids = proyectos_obj.search(cr,
                                    SUPERUSER_ID,
                                    ['|',('correlativo','like',post['key']),
                                    ('nombre_proyecto','like',post['key']),
                                    ('partner_id','=',entidad_id['parent_id'])],
                                    context=context)
            proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, proyectos_ids)
            for proyecto in proyectos_data:
                monto_proyecto=str(proyecto.monto_proyecto).replace('.',',')
                monto=monto_proyecto.split(',')
                if len(monto[1])==1:
                    monto_proyecto=monto_proyecto+'0'
                res.append({
                        'id':proyecto.id,
                        'name':proyecto.correlativo,
                        'nombre_proyecto':proyecto.nombre_proyecto,
                        'state':proyecto.state,
                        'monto_proyecto':monto_proyecto,
                        'editar_migracion':proyecto.editar_migracion,})
        else:
            proyectos_ids = proyectos_obj.search(cr,
                                    SUPERUSER_ID,
                                    ['|',('correlativo','like',post['key']),
                                    ('nombre_proyecto','like',post['key']),
                                    ('partner_id','=',entidad_id['parent_id'])],
                                    context=context)
            proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, proyectos_ids)
            for proyecto in proyectos_data:
                monto_proyecto=str(proyecto.monto_proyecto).replace('.',',')
                monto=monto_proyecto.split(',')
                if len(monto[1])==1:
                    monto_proyecto=monto_proyecto+'0'
                res.append({
                        'id':proyecto.id,
                        'name':proyecto.correlativo,
                        'nombre_proyecto':proyecto.nombre_proyecto,
                        'state':proyecto.state,
                        'monto_proyecto':monto_proyecto,
                        'editar_migracion':proyecto.editar_migracion,})
        ret =  {'datos':res,'code': post['code']}
        return ret
        
    @http.route(
        ['/ept_cp_proyecto_consulta/seleccion'],
        type='json', auth='user', website=True)
    def consulta_proyectos_seleccion(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        entidad_id=ept_cuentas_c.ept_cuentas_web().mi_entidad(uid)
        res=[]
        proyectos_rendidos_ids=[]
        proyectos_migrados_obj = registry.get('ept_mig.proyectos_migrados')
        proyectos__edit_ids= proyectos_migrados_obj.comprobar_actualizacion_ids(cr,SUPERUSER_ID,[],context,entidad_id['entidad_data'])
        if not len(proyectos__edit_ids):
            rendir=True
        else:
            rendir=False
        proyectos_obj=registry['ept_cp.carga_proyecto']
        proyectos_ids = proyectos_obj.search(cr,
                                    SUPERUSER_ID,
                                    [('id','=',post['id']),
                                    ('partner_id','=',entidad_id['parent_id'])],
                                    context=context)
        proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, proyectos_ids)
        for proyecto in proyectos_data:
           
            res.append({
                'id':proyecto.id,
                'correlativo':proyecto.correlativo,
                'nombre_proyecto':proyecto.nombre_proyecto,
                'state':proyecto.state,
                'monto_proyecto':proyecto.monto_proyecto,
                'editar_migracion':rendir,
            })
        ret =  {'datos':res,'code': post['id']}
        return ret
    
    @http.route(
        ['/ept_cp_proyecto_consulta/busqueda_avanzada'],
        type='json', auth='user', website=True)
    def consulta_proyectos_busq_avanzada(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        entidad_id=ept_cuentas_c.ept_cuentas_web().mi_entidad(uid)
        proyectos_rendidos_ids=[]
        proyectos_migrados_obj = registry.get('ept_mig.proyectos_migrados')
        proyectos__edit_ids= proyectos_migrados_obj.comprobar_actualizacion_ids(cr,SUPERUSER_ID,[],context,entidad_id['entidad_data'])
        if not len(proyectos__edit_ids):
            rendir=True
        else:
            rendir=False
        res=[]
        where=[('partner_id','=',entidad_id['parent_id'])]
        if post['fecha_inicio'] and post['fecha_fin']=='':
            d,m,a=post['fecha_inicio'].split('-')
            fecha_inicio = date(int(a),int(m),int(d))
            where.append(('fecha_inicio','=',fecha_inicio))
        if post['fecha_fin'] and post['fecha_inicio']=='':
            d,m,a=post['fecha_fin'].split('-')
            fecha_fin = date(int(a),int(m),int(d))
            where.append(('fecha_fin','=',fecha_fin))
        if post['fecha_inicio'] and post['fecha_fin']:
            d,m,a=post['fecha_inicio'].split('-')
            fecha_inicio = date(int(a),int(m),int(d))
            d,m,a=post['fecha_fin'].split('-')
            fecha_fin = date(int(a),int(m),int(d))
            where.append(('fecha_inicio','>=',fecha_inicio))
            where.append(('fecha_inicio','<=',fecha_fin))
        if post['state']:
            where.append(('state','=',post['state']))
        
        if post['monto_proyecto'] and post['monto_proyecto2']=='':
            monto_proyecto=str(post['monto_proyecto']).replace('.','')
            monto_proyecto=monto_proyecto.replace(',','.')
            where.append(('monto_proyecto','=',monto_proyecto))
        
        if post['monto_proyecto2'] and post['monto_proyecto']=='':
            monto_proyecto=str(post['monto_proyecto2']).replace('.','')
            monto_proyecto=monto_proyecto.replace(',','.')
            where.append(('monto_proyecto','=',monto_proyecto))
        
        if post['monto_proyecto'] and post['monto_proyecto2']:
            monto_proyecto=str(post['monto_proyecto']).replace('.','')
            monto_proyecto=monto_proyecto.replace(',','.')
            monto_proyecto2=str(post['monto_proyecto2']).replace('.','')
            monto_proyecto2=monto_proyecto2.replace(',','.')
            where.append(('monto_proyecto','>=',monto_proyecto))
            where.append(('monto_proyecto','<=',monto_proyecto2))
        if post['municipio_id']:
            where.append(('municipio_id','=',post['municipio_id']))
        if post['parroquia_id']:
            where.append(('parroquia_id','=',post['parroquia_id']))
        proyectos_obj=registry['ept_cp.carga_proyecto']
        proyectos_ids = proyectos_obj.search(cr,
                                    SUPERUSER_ID,
                                    where,
                                    context=context)
        proyectos_data=proyectos_obj.browse(cr, SUPERUSER_ID, proyectos_ids)
        if proyectos_data:
            for proyecto in proyectos_data:
               
                 res.append({
                    'id':proyecto.id,
                    'correlativo':proyecto.correlativo,
                    'nombre_proyecto':proyecto.nombre_proyecto,
                    'state':proyecto.state,
                    'monto_proyecto':proyecto.monto_proyecto,
                    'editar_migracion':rendir,
                })
            ret =  {'datos':res}
            return ret
        ret =  {'modal':{
                            'titulo':'<strong>Busqueda sin resultado.</strong>',
                            'cuerpo':'''<h4 class="text-danger" >
                                        La busqueda que realizo no 
                                        obtuvo ningún resultado...</h4>
                                        ''' ,
                                    },
                            }
        return ret
    
    @http.route(
        ['/ept_cp_proyecto_consulta/busqueda_municipios'],
        type='json', auth='user', website=True)
    def consulta_proyectos_busq_municipios(self):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        proyectos_obj=registry['ept_cp.carga_proyecto']
        entidades_obj = registry['ept_ent.entidades']
        entidades_ids = entidades_obj.search(cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uid)],
                                        context=context)
        entidades_data=entidades_obj.browse(cr,
                            SUPERUSER_ID,
                            entidades_ids,
                            context=context).parent_id
        entidad_datos=proyectos_obj.cp_filtro_estados(cr,uid,[],
                                                     entidades_data.id,context)
        estado_data=entidad_datos.values()[0].values()[0]
        estado_data=estado_data[0]
        estado_data=estado_data[2]
        estado_obj = registry.get('ept_ent.estados')
        estado_ids = estado_obj.search(cr,SUPERUSER_ID,
                                                [('id','in',estado_data)],
                                                context=context)
        estado_data = estado_obj.browse(cr,SUPERUSER_ID,estado_ids,
                                                    context=context)
        municipios=[]
        for estados in estado_data:
            valores=ept_carga_proyecto_c.ept_cp_carga_proyecto_controlador().buscar_municipios(int(estados.id),int(entidades_data.id))
            municipios.append(valores)
        return municipios
        
    @http.route(
        ['/ept_cp_proyecto_consulta/busqueda_parroquias'],
        type='json', auth='user', website=True)
    def consulta_proyectos_busq_parroquias(self,municipio_id):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        valores=ept_carga_proyecto_c.ept_cp_carga_proyecto_controlador().buscar_parroquias(municipio_id)
        return valores
