# -*- coding: utf-8 -*-
##############################################################################

#~   OpenERP, Open Source Management Solution
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


#~ Modulo Desarrollado por Juventud Productiva ()
#  Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#  Nuestro Correo juventudproductivabicentenaria@gmail.com


##############################################################################

from openerp.osv import fields, osv


class res_users(osv.osv):
    _name = 'res.users'
    _inherit="res.users"
    
    _columns = {
        'activo': fields.boolean('Activo',
                    help='''Este campo desactiva a
                            los usuario de la vista website''', 
                    )
    }
    
    _defaults={'activo':True}

