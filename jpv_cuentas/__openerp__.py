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

{
    'name': 'Registro de Cuentas y tipos de cuenta - Sistema para la carga, valoración y rendición de proyectos',
    'version': '1.0',
    'depends': ['base_setup','jpv_entidades','jpv_planificacion'],
    'author': 'Jueventud Productiva Bicentenaria (Víctor Davila)',
    'category': '',
    'description': """
    Modulo de Registro de las Cuentas
    
    Modulo de Registro de los Tipos de Cuentas
    
    Modulo de Registro las entidades con las Cuentas
    
    Dentro de estos Módulos se registran todas las cuentas y tipos de cuentas 
    """,
    'update_xml': [],
    "data" : [
        'vistas/jpv_cuentas_v.xml',
        'vistas/jpv_tipo_cuentas_v.xml',
        'vistas/jpv_asignacion_cuentas_v.xml',
        'vistas/template_cuentas.xml',
        'vistas/jpv_cuentas_saldo_ird_t.xml',
        'datos/jpv_cuentas_s.xml'

        #~ 'reportes/jpv_cuenta_saldo_ird_t.xml',
        #~ 'seguridad/group_coor_ures/ir.model.access.csv',
        #~ 'seguridad/group_ggu_ures/ir.model.access.csv',
        #~ 'seguridad/group_ent_pt/ir.model.access.csv',
        #~ 'seguridad/group_ent_ptio/ir.model.access.csv',
        #~ 'seguridad/group_ent_pts/ir.model.access.csv',
        #~ 'seguridad/group_ger_csa/ir.model.access.csv',
        #~ 'seguridad/group_ger_csc/ir.model.access.csv',
        #~ 'seguridad/group_ger_csg/ir.model.access.csv',
        #~ 'seguridad/group_ger_inf/ir.model.access.csv',
        #~ 'seguridad/group_ger_ppea/ir.model.access.csv',
        #~ 'seguridad/group_ger_ppec/ir.model.access.csv',
        #~ 'seguridad/group_ger_ppeg/ir.model.access.csv',
        #~ 'seguridad/group_ger_tpa/ir.model.access.csv',
        #~ 'seguridad/group_ger_tpc/ir.model.access.csv',
        #~ 'seguridad/group_ger_tpg/ir.model.access.csv',
        #~ 'seguridad/group_ger_varias/ir.model.access.csv',
        #~ 'seguridad/group_jun_dir/ir.model.access.csv',
        #~ 'seguridad/group_jun_dir_sec/ir.model.access.csv',
        #~ 'seguridad/group_ger_fcto/ir.model.access.csv',
        #~ 'seguridad/group_sec_fcto/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
