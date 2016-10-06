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

#~ Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

{
    'name': "Valoracion de Proyectos - Sistema para la carga, valoración y rendición de proyectos",
    'summary': "Con este módulo se valoran los proyectos",
    'description': """
""",
    'author': "Juventud Productiva Bcentenaria",
    'website': "",

    'category': '',
    'version': '0.1',
    'depends': ['base','base_setup','jpv_conf_valoracion','jpv_carga_proyectos','jpv_firma_cartas','jpv_entidades'],
    'data': [
        'vistas/jpv_eva_valoracion_proyectos_v.xml',
        'vistas/jpv_val_asignacion_valoracion_v.xml',
        'vistas/jpv_val_status_valoracion_v.xml',
        'vistas/template_valoracion.xml',
        'vistas/jpv_va_valoracion_resultados_v.xml',
        'wizard/jpv_val_valoracion_directiva_v.xml',
        'vistas/report_carta_valoracion_r.xml',
        'vistas/jpv_val_menu_live_h.xml',
        'reportes/jpv_val_cartas_rv.xml',
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
        #~ 'seguridad/jpv_val_asignaciones_f.xml',
        'datos/template_mail.xml'
    ],
    'demo': [
    ],
    'tests': [
    ],
    'qweb': [
        'static/src/xml/mail.xml'
        ]
}
