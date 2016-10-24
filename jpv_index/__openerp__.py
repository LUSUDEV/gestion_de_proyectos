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
##############################################################################

{
    'name': "11) JPV Index",
    'summary': "",
    'description': """
""",
    'author': "",
    'website': "Index",

    'category': 'Web site',
    'version': '0.1',
    'depends': ['website'],
    'data': [
        'vista/templates.xml',
        'vista/template1.xml',
        'vista/menu_buzon_mensajeria.xml',
        'vista/menus_documentos.xml',
        'vista/paginas/proyecto.xml',
        'vista/paginas/financiamiento.xml',
        'vista/paginas/estadistica.xml',
        'vista/paginas/home.xml',
        
    ],
    'demo': [
    ],
    'tests': [
    ],
}
