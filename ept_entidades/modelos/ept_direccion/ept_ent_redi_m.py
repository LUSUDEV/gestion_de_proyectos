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

from openerp.osv import fields, osv
from openerp.http import request

class ept_ent_redis(osv.osv):
    _name='ept_ent.redis'
    _description='Registro de REDIS'
    
    _columns = {
        'name': fields.char(
                            'REDI', 
                            size=100, 
                            required=True, 
                            help='Nombre  de la REDI'),
        'codigo': fields.char(
                            'Código', 
                            size=10, 
                            required=True, 
                            help='Código  de  Identificación de la REDI'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'ip':fields.char(
                    'IP',
                     size=15,
                     help='ip del cliente de la petición'),
    }
    
    _defaults = {
        'active':True, 
        'ip':lambda self,cr,uid,context: request.httprequest.remote_addr
    }
    
    
