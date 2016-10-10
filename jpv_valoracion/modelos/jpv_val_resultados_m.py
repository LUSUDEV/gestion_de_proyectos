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
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################


import json
import logging
import base64
from cStringIO import StringIO

import os
import zipfile
from shutil import rmtree
from datetime import date


from openerp.osv import osv, fields
from urlparse import urljoin
from openerp import SUPERUSER_ID

    
class jpv_val_dictamen_valoraciones(osv.osv):
    _name = 'jpv_val.dictamen_valoracion'
    _description = u"Dictamen de las valoraciones,\
                    de los proyecto del Concejo Federal de Gobierno EPT"
    _rec_name= "proyecto_id"
    _order = 'id desc'
    
        
        
    def causa_diferidos_negados(self,cr,uid,proyecto_id,dictamen,context=None):
        mensajes=[]
        if dictamen in ['diferido','negado']:
                dictamen_ids=self.search(
                                        cr,
                                        uid,
                                        [('proyecto_id','=',proyecto_id),
                                        ('dictamen','=',dictamen)])
                dictamen_datos=self.browse(cr,uid,dictamen_ids)
                for dictamen_dato in dictamen_datos:
                    #~ OJO si cambia el tipo de pregunta NO debe apuntar a
                    #~ la posicion 0
                    for resultado in dictamen_dato.resultados_ids:
                        state=resultado[0].resp_texto_siple_id[0].state
                        mensaje=resultado[0].resp_texto_siple_id[0].mensaje
                        if dictamen==state and mensaje:
                            mensajes.append(mensaje)
        return mensajes
        
    def _get_editar_dict_url(self, cr, uid, ids, name, arg, context=None):
        if context and context.get('relative_url'):
            base_url = '/'
        else:
            base_url = self.pool['ir.config_parameter'].get_param(cr, uid, 'web.base.url')
        res = {}
        for dictamen in self.browse(cr, uid, ids, context=context):
            url=''
            if dictamen.tipo_valoracion=='valoracion_coordenadas':
                url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas','valoracion_coordenadas')
            if dictamen.tipo_valoracion=='valoracion_general':
                url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_general','valoracion_general')
            if dictamen.tipo_valoracion=='valCoordenadasUre':
                url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas_ures','valCoordenadasUre')
            if dictamen.id:
                res[dictamen.id] = '<a target="_blank" href="'+urljoin(base_url, url)+'"><button type="button" class="oe_button oe_highlight">Editar Valoracion '+dictamen.proyecto_id.correlativo+'</button></a>'
            if dictamen.tipo_valoracion=='valCoordenadasUre':
                res[dictamen.id] = '<a target="_blank" href="'+urljoin(base_url, url)+'"><button type="button" class="oe_button oe_highlight">Editar Valoracion '+dictamen.proyecto_id.correlativo+'</button></a>'
        return res

    def editar_dict_url_tree(self, cr, uid, ids, context=None):
        dictamen=self.browse(cr, uid, ids, context=context)[0]
        if dictamen.tipo_valoracion=='valoracion_coordenadas':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas','valoracion_coordenadas')
        if dictamen.tipo_valoracion=='valoracion_general':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_general','valoracion_general')
        if dictamen.tipo_valoracion=='valCoordenadasUre':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas_ures','valCoordenadasUre')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new',
        }
        
    #~ 'estatus_valoracion_id':fields.many2one(
                                #~ 'jpv_cp.carga_proyecto',
                                #~ 'Asignación',
                                #~ required=True),
    _columns={
        'asignacion_id':fields.many2one(
                            'jpv_val.asignacion_valoracion',
                            'Asignación',
                            ondelete="restrict"),

        'dictamen':fields.selection(
                                [('aprobado', 'Aprobado'),
                                ('negado', 'Negado'),
                                ('diferido', 'Diferido'),
                                ('sinEfecto', 'Sin Efecto')],
                                'Dictamen de la Valoración',
                                required=True),
                            
        'resultados_ids': fields.one2many(
                            'jpv_val.resultados_valoraciones',
                            'dictamen_id',
                            'Resultados',
                            required=True,
                            ondelete="restrict"),

        
        

        'proyecto_id':fields.many2one(
                            'jpv_cp.carga_proyecto',
                            'Asignación',
                            required=True,
                            ),
                            
                            
        'nombre_ept': fields.related(
                                'proyecto_id',
                                'partner_id',
                                string='Nombre',
                                type="many2one",
                                relation="res.partner",
                                store=True,
                                help="Entidad Politica Territorial",
                                select=True,
                                readonly=True),
        'sub_categoria': fields.related(
                                'proyecto_id',
                                'subcategoria_id',
                                string='Subcategoria',
                                type="many2one",
                                relation="jpv_cp.tipo_sectores",
                                select=True,
                                readonly=True),
                                
        'proyecto_id_status': fields.related(
                                'proyecto_id',
                                'state',
                                string='Estatus',
                                type="char",
                                relation="jpv_cp.carga_proyecto",
                                readonly=True),
                                
        'ciclo_id': fields.related(
                                'proyecto_id',
                                'ciclo_id',
                                string='EPT',
                                type="many2one",
                                relation="jpv_plf.etapas",
                                store=True,
                                help="Ciclo de la Carga",
                                select=True,
                                readonly=True),
                                
        'periodo_id': fields.related(
                                'proyecto_id',
                                'periodo_id',
                                string='EPT',
                                type="many2one",
                                relation="jpv_plf.periodos",
                                store=True,
                                help="Perio de la Carga",
                                select=True,
                                readonly=True),


        'observaciones':fields.text('Observaciones'),

        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
                            
        'tipo_valoracion':fields.selection(
                                [('valoracion_coordenadas', 'Corrdenadas'),
                                ('valoracion_general', 'General'),
                                ('valCoordenadasUre', 'Coordenadas Ures'),],
                                'Tipo de Valoración',
                                required=True),
                                
        'website_url': fields.function(_get_editar_dict_url,
            string="link Editar", type="html"),
            
        'state': fields.selection([
                            ('abierta', 'Abierta'),
                            ('validada', 'Validada'),
                            ], 'Estatus')
        }
        
        
    _defaults = {
        'active': True,
        'state':'abierta',
        }

        
class jpv_val_resultaos_valoraciones(osv.osv):
    _name = 'jpv_val.resultados_valoraciones'
    _description = u"Resultados de las valoraciones,\
                    por proyecto del Concejo Federal de Gobierno EPT"
    _rec_name= "tipo_pregunta"

    _columns={
        'asignacion_id':fields.many2one(
                                'jpv_val.asignacion_valoracion',
                                'Asignación',
                                ondelete="restrict"),
                                
        'pregunta_id': fields.many2one(
                                'jpv_conf.valoracion_preguntas',
                                'Pregunta',
                                ondelete="restrict"),
        
        'dictamen_id':fields.many2one(
                                'jpv_val.dictamen_valoracion',
                                'Dictamen',
                                ondelete="restrict"),

        'tipo_pregunta':fields.selection([
                                ('radio', 'Seleccion simple'),
                                ],
                                'Tipo de Pregunta',required=True),

        'resp_texto_siple_id':fields.many2one(
                                    'jpv_conf.valoracion_items_respueta',
                                    'Respuesta de Seleción Simple',
                                    ondelete="restrict"
                                    ),
        
        }


