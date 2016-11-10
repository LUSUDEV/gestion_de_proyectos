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
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.http import request
from openerp import SUPERUSER_ID

class jpv_tipo_cuentas(osv.osv):
    _name = 'jpv.tipo_cuentas'
    _description = "Registro de los Tipos de Cuenta del CFG"
    _rec_name= 'name'
    
    model_partner_id=[]
    def __init__(self, pool, cr):
        init_res = super(jpv_tipo_cuentas, self).__init__(pool, cr)
        #~ self.default_model_partner_id(cr,SUPERUSER_ID)
        name_objeto="name = 'res.partner'"
        cr.execute("select id from ir_model "\
                    "where model = 'res.partner' ;");
        res_objects_ids=cr.fetchall()
        for objeto in res_objects_ids:
            self.model_partner_id.append(objeto[0])
        return init_res
    
    #~ def default_model_partner_id(self,cr,uid,context=None):
        #~ ir_model_obj=self.pool.get('ir.model')
        #~ ir_model_ids=ir_model_obj.search(
                                        #~ cr,
                                        #~ uid,
                                        #~ [('model','=','res.partner')],
                                        #~ context=context)
        #~ for model_id in ir_model_ids:
            #~ self.model_partner_id.append(model_id)
        #~ return self.model_partner_id
    
    def _control_jpv_tipo_field_ids(self, cr, uid, ids, context=None):
        for r in self.browse(cr,uid,ids):
            if not r.jpv_tipo_field_ids:
                raise osv.except_osv(
                        ('Error!'),
                        (u'Debe Seleccionar una opción para\
                         quien será creada la cuenta'))
        return True
        
    _columns = {
        'name':fields.char(
                    'Nombre del Tipo de Cuenta', 
                    required=True,
                    help='Escriba el Nombre del Tipo de Cuenta'),
        'descripcion':fields.text(
                    'Descripción del Tipo de Cuenta',
                    help='Descripción del Tipo de Cuenta'),
        'cis_entidad': fields.boolean(
                            'Entidades',
                            help='Seleccione si el Tipo de Cuenta es para\
                            Entidades'),
        'jpv_tipo_field_ids':fields.many2many(
                    'ir.model.fields',
                    'jpv_rel_tipo_fileds',
                    'entidad_id',
                    'tipo_fields_id',
                    'Relacion Tipo de Cuenta',
                    domain=[('model_id', 'in',model_partner_id),
                            ('ttype','=','boolean'),
                            ('name','like','cis_%')],
                    ),
        'ip':fields.char(
                    'IP',
                     size=15,
                     help='ip del cliente de la petición'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
    }
    _defaults = {
        'active':True,
        'ip':lambda self,cr,uid,context: request.httprequest.remote_addr
    }
    
    _constraints=[
        (_control_jpv_tipo_field_ids, ' ', ['jpv_tipo_field_ids']),
        ]
    
    _sql_constraints=[('name_id_uniq', 'unique (name)', 
                        'El Nombre del Tipo de Cuenta ya existe en la \
                        Base de Datos')]
    
    def asignar_cuenta(self,cr,uid,ids,context=None):
        for valores in self.browse(cr,uid,ids,context=context):
            tipo_cuenta_id=valores.id
        return {
            'name': ('jpv.asignacion_cuentas'),
            'res_model': 'jpv.asignacion_cuentas',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form,tree',
            'view_type': 'form',
            'limit': 80,
            'context': "{   'default_tipo_cuenta_id':%d,\
                            }" % (tipo_cuenta_id),
        }
        
    
