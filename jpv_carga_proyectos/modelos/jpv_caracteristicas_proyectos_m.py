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
     #~ Modulo Desarrollado por Juventud Productiva (Jonathan Reyes)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
##############################################################################

from openerp.osv import fields, osv

class jpv_cp_equipos_config(osv.osv):
    _name = 'jpv_cp.equipos_config'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del equipo.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }

class jpv_cp_maquinaria_config(osv.osv):
    _name = 'jpv_cp.maquinaria_config'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso de la maquinaria.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
    
class jpv_cp_vehiculo_tipo_config(osv.osv):
    _name = 'jpv_cp.vehiculo_tipo_config'
    _rec_name = 'tipo'
    
    _columns = {
        'uso_id': fields.many2one(
                                'jpv_cp.vehiculo_uso_config', 
                                'Uso', 
                                required=True, 
                                help=''),
        'caracteristicas_id': fields.many2one(
                                    'jpv_cp.vehiculo_caracteristicas_config', 
                                    'Caracteristica', 
                                    required=True, 
                                    help=''),
        'tipo': fields.char(
                        'Tipo',  
                        readonly=False,
                        required=True,   
                        help='Tipo de vehiculo.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
    
class jpv_cp_vehiculo_caracteristicas_config(osv.osv):
    _name = 'jpv_cp.vehiculo_caracteristicas_config'
    _rec_name = 'caracteristicas'
    
    _columns = {
        'uso_id': fields.many2one(
                                'jpv_cp.vehiculo_uso_config', 
                                'Uso', 
                                required=True, 
                                help=''),
        'caracteristicas': fields.char(
                        'Caracteristicas',  
                        readonly=False,
                        required=True,   
                        help='Caracteristicas del vehiculo.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
        
class jpv_cp_vehiculo_uso_config(osv.osv):
    _name = 'jpv_cp.vehiculo_uso_config'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del vehiculo.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }

class jpv_cp_materiales_consumo_config(osv.osv):
    _name = 'jpv_cp.materiales_consumo_config'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del material de consumo.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }

class jpv_cp_construccion_config(osv.osv):
    _name = 'jpv_cp.unidades_obra_civil_config'
    _rec_name = 'unidad'
    
    _columns = {
        'unidad':fields.char(
                    'Unidad',
                    required=True,
                    help='Unidad de medición para las obras civiles'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }

class jpv_cp_construccion_unidades_config(osv.osv):
    _name = 'jpv_cp.construccion_unidades_config'
    _rec_name = 'subcategoria_id'
    
    _columns = {
        'tipo_sector_id':fields.many2one(
                                'jpv_cp.tipo_sectores',
                                'Tipo de sector',
                                required=True,
                                help='Tipo de sector al cual pertenece\
                                     el monto minimo a registrar'),
        'categoria_id': fields.many2one(
                                'jpv_cp.tipo_sectores', 
                                'Categoría', 
                                required=True, 
                                help='Categoría a la cual pertenece\
                                     el monto minimo a registrar'),
        'subcategoria_id': fields.many2one(
                                    'jpv_cp.tipo_sectores', 
                                    'Subcategoría', 
                                    required=True, 
                                    help='Subcategoría a la cual\
                                    pertenece el monto minimo a registrar'),
        'unidades_id':fields.many2one(
                        'jpv_cp.unidades_obra_civil_config',
                        'Unidad de Medida',
                        required=True,
                        help='Tipo de sector al cual pertenece\
                             el proyecto a registrar'),
         'active':fields.boolean('Activo')
        }
    
    _defaults = {
        'active':True,
        }
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}


class jpv_cp_semovientes_config(osv.osv):
    _name = 'jpv_cp.semovientes_config'
    _rec_name = 'especie'
    
    _columns = {
        'especie': fields.char(
                        'Especie',  
                        readonly=False,
                        required=True,   
                        help='Especie Semoviente.'),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
    
class jpv_cp_semovientes_grupo_etario_config(osv.osv):
    _name = 'jpv_cp.semovientes_grupo_etario_config'
    _rec_name = 'grupo_etario'
    
    _columns = {
        'grupo_etario': fields.char(
                        'Grupo Etario',  
                        readonly=False,
                        required=True,   
                        help='Grupo Etario Semoviente.'),
        'especies_id':fields.many2many('jpv_cp.semovientes_config','jpv_cp_especie_grupo_rel','grupo_id','especie_id','Especie',readonly=False,required=True, help='Especie a la cual pertenece grupo etario.' ),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
    
class jpv_cp_semovientes_uso_config(osv.osv):
    _name = 'jpv_cp.semovientes_uso_config'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del Semoviente.'),
        'grupos_id':fields.many2many('jpv_cp.semovientes_grupo_etario_config','jpv_cp_grupo_uso_rel','uso_id','grupo_id','Grupo etario',readonly=False,required=True, help='Grupo etario al cual pertenece grupo etario.' ),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
        
class jpv_cp_semovientes_proposito_config(osv.osv):
    _name = 'jpv_cp.semovientes_proposito_config'
    _rec_name = 'proposito'
    
    _columns = {
        'proposito': fields.char(
                        'Proposito',  
                        readonly=False,
                        required=True,   
                        help='Proposito del Semoviente.'),
        'usos_id':fields.many2many('jpv_cp.semovientes_uso_config','jpv_cp_uso_proposito_rel','proposito_id','uso_id','Uso',readonly=False,required=True, help='Uso al cual pertenece grupo etario.' ),
        'active':fields.boolean('Activo')
    }
    
    _defaults = {
        'active':True,
        }
