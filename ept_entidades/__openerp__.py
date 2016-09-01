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
    'name': 'CFG Entidades Político Territorial - Sistema de Plan de Inversión',
    'version': '1.0',
    'depends': ['base','base_setup','ept_usuarios','web_fields_masks','web_hide_duplicate','users_only_groups'],
    'author': 'Jueventud Productiva Bicentenaria (Víctor Davila)',
    'category': '',
    'description': """
    Modulo de Registro de las Entidades 
    (Alcaldias, Alcaldia Mayor o Gobernaciones)
    pertenecientes al Concejo Federal de Gobierno
    """,
    'update_xml': [],
    "data" : [
        'seguridad/ept_ent_f.xml',
        'vistas/ept_direccion/ept_ent_redis_v.xml',
        'vistas/ept_direccion/ept_ent_estados_v.xml',
        'vistas/ept_direccion/ept_ent_municipios_v.xml',
        'vistas/ept_direccion/ept_ent_parroquias_v.xml',
        'vistas/ept_entidad/ept_ent_entidad_v.xml',
        'vistas/ept_direccion/ept_ent_husos_v.xml',
        'vistas/ept_tipo_entidad/ept_ent_tipo_entidades_v.xml',
        'seguridad/group_coor_ures/ir.model.access.csv',
        'seguridad/group_ent_pt/ir.model.access.csv',
        'seguridad/group_ent_pts/ir.model.access.csv',
        'seguridad/group_ent_ptio/ir.model.access.csv',
        'seguridad/group_ger_csa/ir.model.access.csv',
        'seguridad/group_ger_csc/ir.model.access.csv',
        'seguridad/group_ger_csg/ir.model.access.csv',
        'seguridad/group_ger_inf/ir.model.access.csv',
        'seguridad/group_ger_ppeg/ir.model.access.csv',
        'seguridad/group_ger_ppec/ir.model.access.csv',
        'seguridad/group_ger_ppea/ir.model.access.csv',
        'seguridad/group_ger_tpa/ir.model.access.csv',
        'seguridad/group_ger_tpc/ir.model.access.csv',
        'seguridad/group_ger_tpg/ir.model.access.csv',
        'seguridad/group_ger_varias/ir.model.access.csv',
        'seguridad/group_ggu_ures/ir.model.access.csv',
        'seguridad/group_jun_dir/ir.model.access.csv',
        'seguridad/group_jun_dir_sec/ir.model.access.csv',
        'seguridad/group_ger_fcto/ir.model.access.csv',
        'seguridad/group_sec_fcto/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
