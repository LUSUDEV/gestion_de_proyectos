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

    'name': 'CFG Carga de Proyectos -Sistema de Plan de Inversión', 
    'version': '1.0',
    'depends': ['base_setup','ept_usuarios','ept_entidades','ept_cuentas','ept_planificacion'],
    'author': 'Juventud Productiva Bicentenaria',
    'category': '',
    'description': """
    """,
    'update_xml': [],
    "data" : [
        'vistas/ept_cp_tipo_sectores_v.xml',
        'vistas/ept_cp_carga_proyectos_v.xml',
        'vistas/ept_cp_carga_proyecto_s.xml',
        'vistas/ept_cp_carga_proyecto_secuencia.xml',
        'vistas/ept_cp_monto_minimo_construccion_v.xml',
        'vistas/ept_cp_monto_minimo_equipos_v.xml',
        'vistas/ept_cp_monto_minimo_maquinaria_v.xml',
        'vistas/ept_cp_monto_minimo_vehiculo_v.xml',
        'vistas/ept_cp_monto_minimo_materiales_consumo_v.xml',
        'vistas/ept_cp_carga_proyecto_template.xml',
        'vistas/ept_cp_crear_proyecto_template.xml',
        'vistas/ept_cp_mostrar_proyecto_template.xml',
        'vistas/ept_cp_editar_proyecto_template.xml',
        'vistas/ept_cp_semoviente_v.xml',
        'vistas/ept_cp_template_consultar.xml',
        'wizard/ept_negar_diferidos_proyectos_w.xml',
        'vistas/report_carta_cambio_monto_r.xml',
        'reportes/ept_cp_cartas_rv.xml',
        'reportes/ept_cp_ficha_proyecto_rv.xml',
        'vistas/report_ficha_proyecto_r.xml',
        'seguridad/group_coor_ures/ir.model.access.csv',
        'seguridad/group_ent_pt/ir.model.access.csv',
        'seguridad/group_ent_ptio/ir.model.access.csv',
        'seguridad/group_ent_pts/ir.model.access.csv',
        'seguridad/group_ger_csa/ir.model.access.csv',
        'seguridad/group_ger_csc/ir.model.access.csv',
        'seguridad/group_ger_csg/ir.model.access.csv',
        'seguridad/group_ger_fcto/ir.model.access.csv',
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
        'seguridad/group_sec_fcto/ir.model.access.csv',
        'seguridad/group_gere_ures/ir.model.access.csv',
        'vistas/ept_cp_estadisticas_v.xml',
        'seguridad/ept_proyectos_f.xml',
        ],
    'installable': True,
    'auto_install': False,
}
