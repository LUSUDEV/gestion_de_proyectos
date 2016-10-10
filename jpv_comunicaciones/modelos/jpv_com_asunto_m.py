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

from openerp.osv import osv, fields
from urlparse import urljoin
from openerp import SUPERUSER_ID

    
class jpv_com_asuntos(osv.osv):
    _name = 'jpv_com.asuntos'
    _description = u"Configuracion de los asuntos de las comunicaciones"
    _rec_name= "name"
    
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, long):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if context.has_key("default_id"):
                if type(context['default_id'])==int:
                    name=name
            else:
                if record['parent_id']:
                    name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, 
                                         operator='ilike', 
                                         context=None, 
                                         limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, 
                                        limit=limit, context=context)
        if context.has_key("default_id"):
                if type(context['default_id'])==int:
                    ids = self.search(cr, uid, 
                                    [('parent_id','=',context['default_id'])], 
                                    limit=limit, context=context)
                else:
                    ids = self.search(cr, uid, args, 
                                               limit=limit, 
                                               context=context)
        else:
                    ids = self.search(cr, uid, args, 
                                               limit=limit, 
                                               context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
        
    _columns={
        'name': fields.char('Nombre del Asunto', required=True),
        
        'complete_name': fields.function(
                                    _name_get_fnc, 
                                    type="char", 
                                    string='Nombre'),
                                    
        'gerencias_ids':fields.many2many(
                    'jpv_com.gerencias',
                    'jpv_com_rel_asunto_gerencias',
                    'asunto_id',
                    'gerencia_id',
                    'Gerencias asociada',
                    ),
                    
        'proyectos_ids':fields.many2many(
                    'jpv_com.proyectos',
                    'jpv_com_rel_asunto_proyectos',
                    'asunto_id',
                    'proyecto_id',
                    'Plan de Proyectos asociados',
                    ),
                    
        'sequence': fields.integer('Orden de los asuntos'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'tipo_campo':fields.selection([('selection', 'Selección Simple'),
                                ('checkbox', 'Selecion Multiple'),
                                ('text', 'Caja de texto'),
                                ('periodo', 'Seleción de Periodo'),
                                ('proyecto', 'Seleción de Proyecto'),
                                ],
                                'Tipo de campo de la sub-asunto al pulsar'),
        'name_text': fields.char('Nombre de la caja de texto'),
        'parent_id': fields.many2one(
                                'jpv_com.asuntos',
                                'Asunto padre', 
                                select=True, 
                                ondelete='cascade'),
        'child_id': fields.one2many(
                                'jpv_com.asuntos', 
                                'parent_id', 
                                string='Hijo de asunto'),
        'parent_left': fields.integer(
                                'Left Parent', 
                                select=1),
        'parent_right': fields.integer(
                                'Right Parent', 
                                select=1),
        
        }
        
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    
    _defaults = {
        'active': True,
        'sequence': 10,
        }
        
    def write(self, cr, uid, ids, values, context=None):
        id_asunto = super(jpv_com_asuntos, self).write(cr, uid, ids, values, context)
        #~ registros_obj_write=self.pool.get('jpv_movil.registros_obj_write')
        #~ vals={
            #~ 'objeto':self._name,
            #~ 'objeto_id':ids[0]
        #~ }
        #~ registros_obj_write.create(cr,uid,vals,context=context)
        return id_asunto
        
class jpv_com_gerencias(osv.osv):
    _name = 'jpv_com.gerencias'
    _description = u"Configuracion de las gerencias y sus usuarios"
    _rec_name= "gerencia"
    
    _columns={
        'gerencia': fields.char('Nombre de la Gerencia', required=True),
        'res_users_ids':fields.many2many(
                    'res.users',
                    'jpv_com_rel_gerencia_users',
                    'gerencia_id',
                    'users_id',
                    'Usuarios Responsables',
                    ),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        }
        
        
    _defaults = {
        'active': True,
        }
        
class jpv_com_proyectos(osv.osv):
    _name = 'jpv_com.proyectos'
    _description = u"Configuracion del proyecto asociado"
    _rec_name= "proyecto"
    
    _columns={
        'proyecto': fields.char('Nombre del proyecto', required=True),
        'referencia': fields.char('Referencia del Controlador', required=True),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        }
        
        
    _defaults = {
        'active': True,
        }



