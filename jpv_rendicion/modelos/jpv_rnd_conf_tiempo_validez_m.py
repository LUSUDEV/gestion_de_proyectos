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
#    Modulo Desarrollado por Juventud Productiva (Jose Mancilla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp.http import request
import time
from openerp.addons.jpv_rendicion.controladores.comunes import *



class jpv_rnd_tiempo_validez(osv.osv):
    _name='jpv_rnd.tiempo_validez'
    
   
    
    _columns = {
                    
            
        'dias_validez':fields.integer(
                    'Dias de validez para las rendiciones',
                    ),
        
        'model_id': fields.many2one('ir.model','Modelo al que se le aplicara',
                        help="""Modelo al Cual se le aplicara el tiempo de validez"""),
                    
                    
        'active':fields.boolean('Activo'),
    }

