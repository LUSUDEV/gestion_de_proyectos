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
    'name': "10) Gestión Comunicaciones Oficiales - Sifipro",
    'summary': "Sistema de Financiamiento de Proyectos ",
    'description': """
""",
    'author': "Juventud Productiva Bcentenaria",
    'website': "",

    'category': '',
    'version': '0.1',
    'depends': ['base','base_setup','mail','jpv_carga_proyectos'],
    'data': [
        'vistas/jpv_com_asuntos_v.xml',
        'vistas/jpv_com_gerencias_v.xml',
        'vistas/template_comunicaciones_vt.xml',
        'vistas/jpv_com_comunicaciones_v.xml',
        'vistas/jpv_com_secuencia.xml',
        'vistas/jpv_com_salida_v.xml',
        'vistas/jpv_com_comuniciones_masivas_v.xml',
        'datos/template_mail.xml',
        'seguridad/group_base_system/ir.model.access.csv',
        'seguridad/group_ent_pt/ir.model.access.csv',
        'seguridad/group_ent_ptio/ir.model.access.csv',
        'seguridad/group_ent_pts/ir.model.access.csv',
        'seguridad/group_ger_csa/ir.model.access.csv',
        'seguridad/group_ger_csc/ir.model.access.csv',
        'seguridad/group_ger_csg/ir.model.access.csv',
        'seguridad/group_ger_inf/ir.model.access.csv',
        'seguridad/group_ger_ppea/ir.model.access.csv',
        'seguridad/group_ger_ppec/ir.model.access.csv',
        'seguridad/group_ger_ppeg/ir.model.access.csv',
        'seguridad/group_ger_tpa/ir.model.access.csv',
        'seguridad/group_ger_tpc/ir.model.access.csv',
        'seguridad/group_ger_tpg/ir.model.access.csv',
        'seguridad/group_ger_varias/ir.model.access.csv',
        'seguridad/group_jun_dir/ir.model.access.csv',
        'seguridad/group_jun_dir_sec/ir.model.access.csv',
        'seguridad/group_jun_dir_ana/ir.model.access.csv',        
    ],
    'demo': [
    ],
    'tests': [
    ],
}
