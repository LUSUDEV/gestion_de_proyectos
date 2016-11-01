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
    'name': '5) Asignación de Recursos - Sistema para la carga, valoración y rendición de proyectos',
    'version': '1.0',
    'depends': ['base','base_setup','jpv_cuentas'],
    'author': 'Jueventud Productiva Bicentenaria (Jose Daniel Mancilla)',
    'category': '',
    'description': """
    Modulo de Asignacion de Recursos para las Entidades
    """,
    'update_xml': [],
    "data" : [
        'vistas/jpv_asignacion_recursos/jpv_asr_asignacion_recursos_v.xml',
        'wizard/reporte_csv_wizard.xml',
        'vistas/jpv_asignacion_recursos/jpv_asr_asignacion_recursos_general_v.xml',
        'vistas/jpv_asignacion_recursos/template_h.xml',
        'seguridad/group_jun_dir/ir.model.access.csv',
        'seguridad/group_ger_ppeg/ir.model.access.csv',
        'seguridad/group_ger_ppea/ir.model.access.csv',
        'seguridad/group_ger_ppec/ir.model.access.csv',
        'seguridad/group_ent_pt/ir.model.access.csv',
        'seguridad/group_ent_ptio/ir.model.access.csv',
        'seguridad/group_ent_pts/ir.model.access.csv',
        'seguridad/group_ger_csa/ir.model.access.csv',
        'seguridad/group_ger_csc/ir.model.access.csv',
        'seguridad/group_ger_csg/ir.model.access.csv',
        'seguridad/group_ger_inf/ir.model.access.csv',
        'seguridad/group_ger_tpa/ir.model.access.csv',
        'seguridad/group_ger_tpc/ir.model.access.csv',
        'seguridad/group_ger_tpg/ir.model.access.csv',
        'seguridad/group_ger_varias/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
