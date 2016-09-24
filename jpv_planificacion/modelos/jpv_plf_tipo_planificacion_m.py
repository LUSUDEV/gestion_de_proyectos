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
import socket, time

class jpv_plf_tipo_planificacion(osv.osv):
    _name='jpv_plf.tipo_planificacion'
    _rec_name = 'nombre_tipo_planificacion'
    
    _columns={
        'nombre_tipo_planificacion':fields.char( 
                                    'Nombre',
                                    size=50, 
                                    required=True,
                                    help="""Este es el nombre del tipo de\
                                     planificación"""),
        'active':fields.boolean(
                        'Activo',
                        help='Indica si esta o no activo el estado'),
            }
    _defaults={
        'active':True,
            }
    _sql_constraints = [
        ('nombre_tipo_planificacion_unico', 'unique (nombre_tipo_planificacion)',
        'La actividad ya existe')
    ]
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'nombre_tipo_planificacion':vals['nombre_tipo_planificacion'].upper()
                })
        return super(jpv_plf_tipo_planificacion, self).create(cr, uid, vals, 
                                                            context=context)
            
