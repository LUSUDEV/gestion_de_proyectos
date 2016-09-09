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
#############################################################################

from openerp.osv import fields, osv
from openerp.http import request

class jpv_ent_tipo_entidades(osv.osv):
    _name = 'jpv_ent.tipo_entidades'
    _description = "Registro de los Tipos\
                    de Entidades"
    
    
    _columns = {
        'name':fields.char(
                    'Nombre del Tipo de Entidad ',
                     size=50,
                     required=True,
                     help='Nombre que lleva el Tipo de Entidad'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
    }
    
    _defaults = {
        'active':True,
    }
