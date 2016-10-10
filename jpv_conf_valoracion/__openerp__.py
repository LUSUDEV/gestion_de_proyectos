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
#   Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

{
    'name': "Configuración de Preguntas de las Valoraciones  - Sistema para la carga, valoración y rendición de proyectos",
    'summary': "",
    'description': """
""",
    'author': "Juventud Productiva Bcentenaria",
    'website': "",

    'category': '',
    'version': '0.1',
    'depends': ['base','base_setup','jpv_carga_proyectos'],
    'data': [
        'vistas/jpv_conf_obj_valoracion_v.xml',
        'vistas/jpv_conf_preguntas_v.xml',
        'vistas/jpv_conf_respuestas_v.xml',
        'vistas/templates_question_valoracion_tv.xml',
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
