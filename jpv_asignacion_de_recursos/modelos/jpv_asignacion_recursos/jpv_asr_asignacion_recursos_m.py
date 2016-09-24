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
#    Modulo Desarrollado por Juventud Productiva (Jose Mancilla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp.http import request
import time

class jpv_asr_rescurso(osv.osv):
    _name='jpv_asr.recurso'
    
    
    _columns = {
        'tipo_cuenta':fields.related('asignacion_de_recurso_line_id',
                    'tipo_cuenta', string='Cuenta', 
                    type='many2one', relation='jpv.tipo_cuentas',
                    help="""Aqui se coloca el tipo de cuenta 
                    a la cual se le asignara los recursos"""),
                            
        'descripcion':fields.related('asignacion_de_recurso_line_id',
                    'descripcion', string='Descripción', type='text',
                    relation='jpv_asr.recurso_general'),
                    
        'estatus':fields.related('asignacion_de_recurso_line_id',
                    'state', string='Status', type='char',
                    relation='jpv_asr.recurso_general'),
            
        'res_partner_id':fields.many2one(
                    'res.partner',
                    'Entidad o Institucion',help="Organizacion a la cual se le va a asignar el monto"
                    ),
                    
        'asignacion_de_recurso_line_id':fields.many2one(
                    'jpv_asr.recurso_general',
                    'Asignacion de recursos',
                    ondelete="cascade"),
        'monto':fields.float('Monto a Asignar'),
        
        'periodo_id':fields.related('asignacion_de_recurso_line_id',
                    'periodo_id', string='Periodo', type='many2one',
                    relation='jpv_plf.periodos',
                    store=True),
        
        'transaccion_id': fields.integer('Identificador de Transacción '),
    }
    
    _sql_constraints = [
        ('recurso_uniq', 'unique (res_partner_id,asignacion_de_recurso_line_id)', 'Alguna de las entidades esta repetida \n o ya tiene monto asignado...\n Por favor verifique e intente nuevamente '),
    ]
   
    def onchange_tipo_cuenta(self, cr, uid, ids, tipo_cuenta, context=None):
        tipo_cuenta=self.pool.get('jpv_asr.recurso_general').tipo_cuenta_id
        partner_ids=[]
        cuentas_obj=self.pool.get('jpv.cuentas')
        cuentas_ids=cuentas_obj.search(cr,uid,[('tipo_cuenta_id','=',tipo_cuenta)])
        cuentas_data=cuentas_obj.browse(cr,uid,cuentas_ids,context)
        for r in cuentas_data:
            partner_ids.append(r.partner_id.id)
        partner_ids=list(set(partner_ids))
        domain = {'res_partner_id':[('id', 'in', partner_ids),
                    ('id','not in',self.pool.get('jpv_asr.recurso_general').list_res_partner_ids)]}
        return {'domain': domain}
   
   
