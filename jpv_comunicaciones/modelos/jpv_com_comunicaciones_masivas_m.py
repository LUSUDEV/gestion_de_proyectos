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
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import datetime
from openerp.osv import osv, fields

class jpv_com_comunicaciones_masivas(osv.osv):
    _name = 'jpv_com.comunicaciones_masivas'
    _description = u"Envios de Cominicaciones masivas"
    _rec_name= "name"
    _order = 'id desc'
    
    _columns={
        'correlativo': fields.char('Correlativo'),
        'name': fields.char('Asunto', required=True),
        'state':fields.selection([
                                ('borrador', 'Borrador'),
                                ('enviado', 'Enviado'),
                                ('leidos', 'Leído'),
                                ('cancelado', 'Cancelado'),
                                ],
                                'Estatus'),
        'fecha_envio':fields.datetime('Fecha de Envío'),
        'comunicacion': fields.html('Comunicación', required=True),
        'pertner_ids':fields.many2many(
                    'res.partner',
                    'jpv_com_rel_comunicacion_partner',
                    'cominicacion_id',
                    'partner_id',
                    'Destinatarios',
                    ),
                    
                    
        'adjunto_ids': fields.one2many(
                            'jpv_com.adjuntos_masivos',
                            'cominicaciones_id',
                            'Adjunto',
                            ondelete="restrict"),
        'partner_leidos_ids': fields.one2many(
                            'jpv_com.comunicaciones_masivas_leidas',
                            'cominicaciones_id',
                            'Entidades que han leído',),
                            
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        }
        
    _defaults = {
        'active': True,
        'state':'borrador'
        }
        
    def cambio_status_cancelar(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'cancelado'})
        
    def cambio_status_borrador(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'borrador'})
        
    def enviar_mensaje(self,cr,uid,ids,context=None):
        adjuntos=[]
        com_masiva_data=self.browse(cr,uid,ids,context=context)
        for adjunto in com_masiva_data.adjunto_ids:
            adjuntos.append((4,adjunto.attachment_id.id))
        entidad_obj=self.pool.get('jpv_ent.entidades')
        mail_message_obj=self.pool.get('mail.message')
        ir_model_data_obj = self.pool.get('ir.model.data')
        notification_obj=self.pool.get('mail.notification')
        comunicaciones_masivas_leidas_obj=self.pool.get('jpv_com.comunicaciones_masivas_leidas')
        com_masivas_data=self.browse(cr,uid,ids)[0]
        for partner in com_masivas_data.pertner_ids:
            mail_template='email_template_comunicacion_masiva'
            partner_ids=[]
            model=''
            model_id=0
            if partner.cis_entidad:
                model='jpv_ent.entidades'
                entidad_id=entidad_obj.search(cr,uid,[('parent_id','=',partner.id)])
                entidad_data=entidad_obj.browse(cr,uid,entidad_id)
                model_id=entidad_id[0]
                for user in entidad_data.user_ids:
                    partner_ids.append((4,user.partner_id.id))
            
            else:
                mail_template='email_template_comunicacion_masiva_partner'
                model='res.partner'
                model_id=partner.id
                partner_ids.append((4,partner.id))
            ctx={
                'mail_post_autofollow_partner_ids': partner_ids, 
                'default_model': model, 
                'default_res_id':model_id, 
                'mail_read_set_read': False, 
                'mail_post_autofollow': True}
            ctx1={
                    'mail_post_autofollow_partner_ids': partner_ids, 
                    'default_model': model, 
                    'default_res_id':model_id, 
                    'mail_read_set_read': False, 
                    'mail_post_autofollow': True}
            correlativo=com_masiva_data.correlativo
            values={
                'body': correlativo+'<br/><br/>'+com_masiva_data.comunicacion, 
                'model': model, 
                'attachment_ids':adjuntos, 
                'res_id': model_id, 
                'parent_id':False, 
                'subtype_id': False, 
                'author_id': self.pool['res.company'].browse(cr,uid,[1])[0].id, 
                'type': 'notification', 
                'partner_ids':[], 
                'subject': 'Comunicación Oficial '+com_masiva_data.name}
            menssage_id=mail_message_obj.create(cr,uid,values,context=ctx)
            for partner_id in partner_ids:
                value_not={
                    'is_read':False,
                    'starred':False,
                    'partner_id':partner_id[1],
                    'message_id':menssage_id
                    }
                notification_obj.create(cr,uid,value_not)
            try:
                template_id = ir_model_data_obj.get_object_reference(
                                            cr, 
                                            uid, 
                                            'jpv_comunicaciones', 
                                            mail_template)[1]
            except ValueError:
                template_id = False
            ctx = dict()
            ctx.update({
                
                'default_composition_mode': 'email',
                'default_subject': '',
                'default_notified_partner_ids':partner_ids,
                'mark_so_as_sent': True
            })
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template_id, model_id , True, context=ctx)
        self.write(cr,uid,ids,{'state':'enviado','fecha_envio':datetime.datetime.now()})
        masivas_leidas_ids=comunicaciones_masivas_leidas_obj.search(cr,uid,[('cominicaciones_id','in',ids)])
        comunicaciones_masivas_leidas_obj.unlink(cr, uid, masivas_leidas_ids, context=context)
        return
        
    def create(self,cr,uid,vals,context=None):
        print vals
        correlativo=self.pool.get('ir.sequence').get(cr,uid,
                                                    'jpv_com.comunicaciones_masivas')
        vals['correlativo']=correlativo
        salida_id=super(jpv_com_comunicaciones_masivas,self).create(cr,uid,vals,
                                                       context=context)
        return salida_id
        
class jpv_com_adjuntos_masivos(osv.osv):
    _name = 'jpv_com.adjuntos_masivos'
    _description = u"Adjunto de las comunicaciones masivas"
    _rec_name= "cominicaciones_id"
    
    _columns={
        'attachment_id':fields.many2one('ir.attachment','Adjunto',required=True),
        'datas_fname': fields.related(
                            'attachment_id',
                            'datas_fname', 
                            string='Adjunto', 
                            type='char', 
                            relation='ir.attachment', 
                            select=True,
                            store=True),
        'cominicaciones_id': fields.many2one(
                            'jpv_com.comunicaciones_masivas',
                            'Adjuntos Comunicaciones Masivas'),
        }
        
class jpv_com_comunicaciones_masivas_leidas(osv.osv):
    _name = 'jpv_com.comunicaciones_masivas_leidas'
    _description = u"Comunicaciones Masivas Leidas"
    _rec_name= "pertner_id"
    
    _columns={
        'pertner_id':fields.many2one('res.partner','Entidad',required=True),
        'cominicaciones_id': fields.many2one(
                            'jpv_com.comunicaciones_masivas',
                            'Entidades que han leído la comunicaciones'),
        }
