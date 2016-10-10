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

from openerp.osv import osv, fields
from openerp import SUPERUSER_ID

    
class jpv_com_comunicaciones(osv.osv):
    _name = 'jpv_com.comunicaciones'
    _description = u"Recepción de Comunicaciones Oficiales"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name= "correlativo"
    _order = 'id desc'

    def _get_attachment_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            res[app_id] = self.pool['ir.attachment'].search_count(
                                            cr, 
                                            uid, 
                                            [('res_model', '=', 'jpv_com.comunicaciones'), ('res_id', '=', app_id)], 
                                            context=context)
        return res
        
    _columns={
        'correlativo': fields.char('Correlativo', required=True),
        'partner_id': fields.many2one('res.partner','Entidad',
                            ondelete="restrict", required=True),
        'users_id': fields.many2one('res.users','Remitente',
                            ondelete="restrict", required=True),
        'asunto_id': fields.many2one('jpv_com.asuntos','Asunto',
                            ondelete="restrict", required=True),
        'comunicacion': fields.text('Comunicación', required=True),
        'attachment_id': fields.many2one(
                                'ir.attachment',
                                'Pdf Adjunto'),
                                
        'datas_fname': fields.related(
                            'attachment_id',
                            'datas_fname', 
                            string='Nombre Adjunto', 
                            type='char', 
                            relation='ir.attachment', 
                            select=True,
                            store=True),
                            
        'mensaje_id': fields.many2one(
                                'mail.message',
                                'Notificacíon'),
        'proyecto_ids':fields.many2many(
                    'jpv_cp.carga_proyecto',
                    'jpv_com_rel_asunto_proyecto',
                    'proyecto_id',
                    'asunto_id',
                    'Asuntos Proyectos',
                    ),
        'gerencia_ids':fields.many2many(
                    'jpv_com.gerencias',
                    'jpv_com_rel_comunicacion_gerecia',
                    'gerencia_id',
                    'comunicacion_id',
                    'Asignar Gerencia',
                    ),
        'grupos_ids':fields.many2many(
                    'res.groups',
                    'jpv_com_rel_comunicacion_grupos',
                    'grupos_id',
                    'comunicacion_id',
                    'Asignar Gerencia',
                    ),
                    
        'user_id': fields.many2one(
                    'res.users', 
                    'Analista Junta Directiva'
                    ),
                    
        'campo_text_ids': fields.one2many(
                            'jpv_com.campos_text',
                            'comunicacion_id',
                            'Campos de texto',
                            ondelete="restrict"),
        'salidas_ids': fields.one2many(
                            'jpv_com.salidas',
                            'comunicacion_id2',
                            'Respuestas',
                            ondelete="restrict"),
        'state':fields.selection([
                                ('proceso', 'En Proceso'),
                                ('procesado', 'Procesado'),
                                ('enviado', 'Enviado'),
                                ('leido', 'Leído'),
                                ('sinrespuesta', 'Sin Respuesta'),
                                ],
                                'Estatus'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
                            
        'attachment_number': fields.function(
                                    _get_attachment_number, 
                                    string='Number of Attachments', 
                                    type="integer"),
        
        
        }
        
    
    
    def action_get_attachment_tree_view(self, cr, uid, ids, context=None):
        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'action_attachment')
        action = self.pool.get(model).read(cr, uid, action_id, context=context)
        action['context'] = {'default_res_model': self._name, 'default_res_id': ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', ids)])
        return action
        
    _defaults = {
        'active': True,
        'state':'proceso'
        }
    
                                                
        
class jpv_com_campos_text(osv.osv):
    _name = 'jpv_com.campos_text'
    _description = u"Compos de textos de los asuntos"
    _rec_name= "campo_texto"
    
    _columns={
        'campo_texto': fields.char('Nombre del Asunto', required=True),
        'asunto_id': fields.many2one('jpv_com.asuntos','Asunto'),
        'comunicacion_id': fields.many2one('jpv_com.comunicaciones','Comunicación'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        }
        
        
    _defaults = {
        'active': True,
        }

class jpv_com_salidas(osv.osv):
    _name='jpv_com.salidas'
    _rec_name='correlativo'
    _description=u'Resuestas de las comunicaciones del cfg'
    
    
    def _default_company(self,cr,uid,ids,context=None):
        return self.pool['res.company'].browse(cr,uid,[1])[0].id
    
    _columns={
        'correlativo': fields.char('Correlativo'),
        
        'asunto_id': fields.many2one('jpv_com.asuntos','Asunto',
                            ondelete="restrict",store=True, required=True),
        'state':fields.selection([
                                ('Borrador', 'Borrador'),
                                ('enviado', 'Enviado'),
                                ],
                                'Estatus'),
                                
        'comunicacion_id2': fields.many2one('jpv_com.comunicaciones','Comunicación'),
        
        'company_id':fields.many2one('res.company', 'Emisor',store=True,readonly=True),
        
        'comunicacion': fields.html('Respuesta', required=True),
        
        'adjunto_ids': fields.one2many(
                            'jpv_com.adjuntos',
                            'salidas_id',
                            'Adjunto',
                            ondelete="restrict"),
                                
        'mensaje_id': fields.many2one(
                                'mail.message',
                                'Notificacíon'),
                                
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        }
        
    _defaults={
        'company_id':_default_company,
        'active':True,
        'state':'Borrador',
        }
    
    
    def enviar_salida(self,cr,uid,ids,context=None):
        ir_attachment_obj=self.pool.get('ir.attachment')
        entidad_obj=self.pool.get('jpv_ent.entidades')
        comunicacion_obj=self.pool.get('jpv_com.comunicaciones')
        notification_obj=self.pool.get('mail.notification')
        mail_message_obj=self.pool.get('mail.message')
        ir_model_data_obj = self.pool.get('ir.model.data')
        salida_data=self.browse(cr,uid,ids)[0]
        comunicacion_data=comunicacion_obj.browse(cr,uid,context['comunicacion_id2'])[0]
        adjuntos=[]
        entidad_id=entidad_obj.search(cr,uid,[('parent_id','=',comunicacion_data.partner_id.id)])
        for adjunto in salida_data.adjunto_ids:
            attachment_id = ir_attachment_obj.write(cr,uid,adjunto.attachment_id.id,{
                'res_model':'jpv_ent.entidades',
                'res_id': entidad_id[0],
                }, context)
            adjuntos.append((4,adjunto.attachment_id.id))
            
     
        ctx={
                'mail_post_autofollow_partner_ids': [(4, comunicacion_data.users_id.partner_id.id)], 
                'default_model': 'jpv_ent.entidades', 
                'default_res_id':entidad_id[0], 
                'mail_read_set_read': False, 
                'mail_post_autofollow': True}
        ctx1={
                'mail_post_autofollow_partner_ids': [(4, comunicacion_data.users_id.partner_id.id)], 
                'default_model': 'jpv_ent.entidades', 
                'default_res_id':entidad_id[0], 
                'mail_read_set_read': False, 
                'mail_post_autofollow': True}
        values={
            'body': salida_data.correlativo+'<br/><br/>'+salida_data.comunicacion, 
            'model': 'jpv_ent.entidades', 
            'attachment_ids':adjuntos, 
            'res_id': entidad_id[0], 
            'parent_id':comunicacion_data.mensaje_id.id, 
            'subtype_id': False, 
            'author_id': self.pool['res.company'].browse(cr,uid,[1])[0].id, 
            'type': 'notification', 
            'partner_ids':[], 
            'subject': False}
        menssage_id=mail_message_obj.create(cr,uid,values,context=ctx)
        value_not={
            'is_read':False,
            'starred':False,
            'partner_id':comunicacion_data.users_id.partner_id.id,
            'message_id':menssage_id
        }
        notification_obj.create(cr,uid,value_not)
        try:
            template_id = ir_model_data_obj.get_object_reference(
                                        cr, 
                                        uid, 
                                        'jpv_comunicaciones', 
                                        'email_template_comunicacion_respuesta')[1]
        except ValueError:
            template_id = False
        ctx = dict()
        ctx.update({
            
            'default_composition_mode': 'email',
            'default_subject': '',
            'default_notified_partner_ids':[comunicacion_data.users_id.partner_id.id],
            'mark_so_as_sent': True
        })
        mail_id = self.pool.get('email.template').send_mail(cr, uid, template_id, entidad_id[0] , True, context=ctx1)
        comunicacion_obj.write(cr,uid,context['comunicacion_id2'],{'state':'enviado'})
        self.write(cr,uid,ids,{'state':'enviado'})
        
        
    def create(self,cr,uid,vals,context=None):
        #~ ir_attachment_obj=self.pool.get('ir.attachment')
        #~ entidad_obj=self.pool.get('jpv_ent.entidades')
        comunicacion_obj=self.pool.get('jpv_com.comunicaciones')
        #~ notification_obj=self.pool.get('mail.notification')
        #~ mail_message_obj=self.pool.get('mail.message')
        #~ ir_model_data_obj = self.pool.get('ir.model.data')
        correlativo=self.pool.get('ir.sequence').get(cr,uid,
                                                    'jpv_com.salidas'),
        vals['correlativo']=correlativo[0]
        salida_id=super(jpv_com_salidas,self).create(cr,uid,vals,
                                                       context=context)
        #~ **************************************
        #~ comunicacion_data=comunicacion_obj.browse(cr,uid,vals['comunicacion_id2'])[0]
        #~ adjuntos=[]
        #~ entidad_id=entidad_obj.search(cr,uid,[('parent_id','=',comunicacion_data.partner_id.id)])
        #~ for adjunto in vals['adjunto_ids']:
            #~ attachment_id = ir_attachment_obj.write(cr,uid,adjunto[2]['attachment_id'],{
                #~ 'res_model':'jpv_ent.entidades',
                #~ 'res_id': entidad_id[0],
                #~ }, context)
            #~ adjuntos.append((4, adjunto[2]['attachment_id']))
            #~ 
     #~ 
        #~ ctx={
                #~ 'mail_post_autofollow_partner_ids': [(4, comunicacion_data.users_id.partner_id.id)], 
                #~ 'default_model': 'jpv_ent.entidades', 
                #~ 'default_res_id':entidad_id[0], 
                #~ 'mail_read_set_read': False, 
                #~ 'mail_post_autofollow': True}
        #~ ctx1={
                #~ 'mail_post_autofollow_partner_ids': [(4, comunicacion_data.users_id.partner_id.id)], 
                #~ 'default_model': 'jpv_ent.entidades', 
                #~ 'default_res_id':entidad_id[0], 
                #~ 'mail_read_set_read': False, 
                #~ 'mail_post_autofollow': True}
        #~ values={
            #~ 'body': vals['correlativo']+'<br/><br/>'+vals['comunicacion'], 
            #~ 'model': 'jpv_ent.entidades', 
            #~ 'attachment_ids':adjuntos, 
            #~ 'res_id': entidad_id[0], 
            #~ 'parent_id':comunicacion_data.mensaje_id.id, 
            #~ 'subtype_id': False, 
            #~ 'author_id': self.pool['res.company'].browse(cr,uid,[1])[0].id, 
            #~ 'type': 'notification', 
            #~ 'partner_ids':[], 
            #~ 'subject': False}
        #~ menssage_id=mail_message_obj.create(cr,uid,values,context=ctx)
        #~ value_not={
            #~ 'is_read':False,
            #~ 'starred':False,
            #~ 'partner_id':comunicacion_data.users_id.partner_id.id,
            #~ 'message_id':menssage_id
        #~ }
        #~ notification_obj.create(cr,uid,value_not)
        #~ try:
            #~ template_id = ir_model_data_obj.get_object_reference(
                                        #~ cr, 
                                        #~ uid, 
                                        #~ 'jpv_comunicaciones', 
                                        #~ 'email_template_comunicacion_respuesta')[1]
        #~ except ValueError:
            #~ template_id = False
        #~ ctx = dict()
        #~ ctx.update({
            #~ 
            #~ 'default_composition_mode': 'email',
            #~ 'default_subject': '',
            #~ 'default_notified_partner_ids':[comunicacion_data.users_id.partner_id.id],
            #~ 'mark_so_as_sent': True
        #~ })
        #~ mail_id = self.pool.get('email.template').send_mail(cr, uid, template_id, entidad_id[0] , True, context=ctx1)
        #~ **********************************************
        comunicacion_obj.write(cr,uid,vals['comunicacion_id2'],{'state':'procesado'})
        return salida_id

class jpv_com_adjuntos(osv.osv):
    _name = 'jpv_com.adjuntos'
    _description = u"Adjunto de las salidas"
    _rec_name= "salidas_id"
    
    _columns={
        'attachment_id':fields.many2one('ir.attachment','Adjunto',required=True),
        'datas': fields.related('attachment_id','datas', string='Adjunto', type='binary', relation='ir.attachment', select=True),
        'datas_fname': fields.related(
                            'attachment_id',
                            'datas_fname', 
                            string='Adjunto', 
                            type='char', 
                            relation='ir.attachment', 
                            select=True,
                            store=True),
        'salidas_id': fields.many2one(
                            'jpv_com.salidas',
                            'Salida'),
        }
    
