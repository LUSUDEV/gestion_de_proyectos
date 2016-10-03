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
from openerp.addons.jpv_rendicion.controladores.comunes import *
from openerp.addons.jpv_rendicion.controladores.jpv_rnd_rendicion_c import *


class jpv_rnd_notificaciones_rendicion(osv.osv):
    _name='jpv_rnd.notificaciones_rendicion'
    
   
    
    _columns = {
        'res_partner_id':fields.many2one(
                    'res.partner',
                    'Entidad',help="Entidad",
                    ondelete="cascade"
                    ),
        'rendiciones_vencidas':fields.integer('Rendiciones Vencidas'),
        'rendiciones_vencer':fields.integer('Rendiciones Por vencerse'),
        'rendiciones_vigentes':fields.integer('Rendiciones Actualizadas'),
        'proyectos_sin_rendir':fields.integer('Proyectos Sin Rendir'),
                    
    }
    
    def consulta_rendiciones(self,cr,uid):
        rendicion_obj=self.pool.get('jpv_rnd.rendicion')
        entidades_obj=self.pool.get('jpv_ent.entidades')
        entidades_ids=entidades_obj.search(cr,uid,[])
        entidades_data=entidades_obj.browse(cr,uid,entidades_ids)
        for entidad in entidades_data:
            cr.execute("select eccp.id from jpv_cp_carga_proyecto as eccp inner join jpv_ent_entidades as ee on ee.parent_id=eccp.partner_id"\
                    " where ee.parent_id=%s and eccp.state='aprobado';" % (entidad.parent_id.id));
            proyectos_ids=cr.fetchall()
            proyecto_ids=[]
            for proyecto_id in proyectos_ids:
                proyecto_ids.extend(proyecto_id)
            values={
                'sin_rendicion':[],
                'vigentes':[],
                'por_vencer':[],
                'vencidas':[]
            }
            for id_proyecto in proyecto_ids:
                indicador=rendicion_obj.tiempo_validez_notificacion_get(cr,uid,id_proyecto)
                values[indicador].append(id_proyecto)
            vals={
                'res_partner_id': entidad.parent_id.id,
                'proyectos_sin_rendir': len(values['sin_rendicion']),
                'rendiciones_vigentes': len(values['vigentes']),
                'rendiciones_vencer': len(values['por_vencer']),
                'rendiciones_vencidas': len(values['vencidas']),
            }
            create_id=self.create(cr,uid,vals)
            string=""
            if vals['proyectos_sin_rendir'] > 0:
                string+=("%s proyectos sin rendir," % (vals['proyectos_sin_rendir']))
            if vals['rendiciones_vencidas'] > 0:
                string+=("%s rendiciones vencidas," % (vals['rendiciones_vencidas']))
            if vals['rendiciones_vencer'] > 0:
                string+=("%s rendiciones por vencer," % (vals['rendiciones_vencer']))
            if vals['rendiciones_vigentes'] > 0:
                string+=("%s Rendiciones vigentes" % (vals['rendiciones_vigentes']))
            
            
            body_notificacion=("Para la fecha, tiene "+string)
            mail_message_obj=self.pool.get('mail.message')
            ctx={
                'mail_post_autofollow_partner_ids': [], 
                'default_model': 'jpv_ent.entidades',
                'default_res_id':entidad.id, 
                'mail_read_set_read': True, 
                'mail_post_autofollow': True}
            values_message={
                'body': body_notificacion, 
                'model': 'jpv_ent.entidades',
                'attachment_ids': [], 
                'res_id': entidad.id, 
                'parent_id': False, 
                'subtype_id': False, 
                'author_id': self.pool.get('res.company').browse(cr,uid,[1])[0].id, 
                'type': 'comment', 
                'partner_ids': [entidad.user_ids], 
                'subject': False}
            partner_ids=[]
            for usuario in entidad.user_ids:
                partner_ids.append(usuario.partner_id.id)
            message_id=mail_message_obj.create(cr,uid,values_message,context=ctx)
            for partner in partner_ids:
                vals_notificacion={
                    'is_read': False,
                    'starred': False,
                    'partner_id':partner,
                    'message_id': message_id
                }
                self.pool.get('mail.notification').create(cr,uid,vals_notificacion)
                vals={
                                'create_uid': False, 
                                'name': "Estatus de Rendiciones", 
                                'comunicacion': body_notificacion, 
                                'adjunto_ids': [], 
                                'pertner_ids': [[6, False, [entidad.parent_id]]], 
                                'active': True, 
                                'state': 'enviado', 
                                'fecha_envio': False, 
                                'partner_leidos_ids': []}
                comunicaciones_masivas_obj = self.pool.get('jpv_com.comunicaciones_masivas')
                comunicaciones_masivas_obj.create(cr,SUPERUSER_ID,vals,context=ctx)
        return True
    
    
    
    

    

   
