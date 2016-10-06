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


from urlparse import urljoin
import datetime
from urllib import urlencode
from openerp import SUPERUSER_ID
import os
class jpv_ent_entidades(osv.osv): 
    _name = 'jpv_ent.entidades'
    _inherit="jpv_ent.entidades"
    
    def carta_firmada_valoracion(self,cr,uid,carta_data,file_name,file_data,context=None):
        '''Este es el metodo es el que cambia los estado del proyecto una vez
        se cargen las cartas firmadas de las valoraciones de los proyectos,
        le envia un mensaje (notificación) y correo a los usuarios dela ept
        adicionelmente cuando el proyecto sea aprobado verifica y cambia el 
        campo cargar_proyectos.         
        carga_data: Es el browser de jpv_fir.cartas_x_firmar(id,)
        file_data: Es el binario de la carta
        
        Se recomienda una vez guardado la carata a ir_attachment 
        '''
        ir_attachment_obj=self.pool.get('ir.attachment')
        cartas_x_firmar_obj=self.pool.get('jpv_fir.cartas_x_firmar')
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        dictamen_valoracion_obj=self.pool.get('jpv_val.dictamen_valoracion')
        cp_historial_obj=self.pool.get('jpv_cp.historial_proyecto')
        movimientos_cuentas_obj=self.pool.get('ept.movimientos_cuentas')
        ir_model_data_obj = self.pool.get('ir.model.data')
        mail_compose_message = self.pool.get('mail.compose.message')
        mail_message_obj=self.pool.get('mail.message')
        entidad_obj=self.pool.get('jpv_ent.entidades')
        entidad_id=int()
        partner_ids=[]
        mail_template=''
        descripcion='Proyectos Valorados:\n'
        body_notificacion='Carta con los correlativos de los'\
                ' proyectos con estatus '+carta_data.objeto_rastro_ids[0].referncia+'.<br>'
        for objeto_rastro in carta_data.objeto_rastro_ids:
            proyecto_id=int(objeto_rastro.objeto_ratro_id)
            mensajes=[]
            dictamenV=objeto_rastro.referncia
            mensajes=dictamen_valoracion_obj.causa_diferidos_negados(cr,uid,proyecto_id,dictamenV)
            proyecto_datos=carga_proyecto_obj.browse(cr,SUPERUSER_ID,[proyecto_id])[0]
            res_partner_id=proyecto_datos.partner_id.id
            if objeto_rastro.referncia in ['aprobado']:
                mail_template='email_template_valoracion_projectos_jpv_aprobado'
                entidad_id=entidad_obj.search(cr,uid,[('parent_id','=',res_partner_id)])
                entidad_obj.write(cr,uid,entidad_id,{
                                'cargar_proyectos':False}
                                )
            if objeto_rastro.referncia=='diferido':
                mail_template='email_template_valoracion_projectos_jpv_diferido'
            if objeto_rastro.referncia=='negado':
                mail_template='email_template_valoracion_projectos_jpv_negado'
                accion='Proyecto Negado'
                if proyecto_datos.state!='negado':
                    resultado_movimiento=movimientos_cuentas_obj.movimiento_ingreso(
                                                            cr,uid,
                                                            proyecto_datos.cuenta_id.id,
                                                            proyecto_datos.monto_proyecto,
                                                            accion,
                                                            proyecto_datos.correlativo,
                                                            carga_proyecto_obj,
                                                            proyecto_id,
                                                            proyecto_datos.periodo_id.id,
                                                            proyecto_datos.partner_id.id,
                                                            proyecto_datos.proyect_mantenimiento,
                                                            proyecto_datos.monto_proyecto)
                    if proyecto_datos.proyect_mantenimiento==True:
                        carga_proyecto_obj.write(
                                cr,
                                SUPERUSER_ID,
                                proyecto_id,
                                {'monto_tomado_mantenimiento':0},
                                0,
                                context)
                    
            mensajes = ', '.join(mensajes)
            descripcion+=proyecto_datos.correlativo+'. '+mensajes+'\n'
            body_notificacion+="<br><br>"+proyecto_datos.correlativo+'. '+mensajes
            carga_proyecto_obj.write(
                                cr,
                                SUPERUSER_ID,
                                proyecto_id,
                                {'state':objeto_rastro.referncia},
                                0,
                                context)
            referncia=objeto_rastro.referncia
            referncia=referncia.capitalize()+'. '+mensajes
            mensaje={
                'descripcion':referncia,
                'proyecto_id':proyecto_id,
                }
            cp_historial_obj.create(cr,uid,mensaje)
            dictamen_ids=dictamen_valoracion_obj.search(
                                cr,
                                SUPERUSER_ID,
                                [('proyecto_id','=',proyecto_id)])
            dictamen_valoracion_obj.write(
                                        cr,
                                        SUPERUSER_ID,
                                        dictamen_ids,
                                        {'state':'validada'}) # estoy aqui**********************************************************************
        attachment_id = ir_attachment_obj.create(cr,uid,{
            'name': file_name,
            'datas': file_data,
            'datas_fname': file_name,
            'res_model':'jpv_ent.entidades',
            'res_id': int(carta_data.objeto_principal_id),
            'description':descripcion
            }, context)
        cartas_x_firmar_obj.write(
                                cr,
                                uid,
                                carta_data.id,
                                {'attachment_id':attachment_id,
                                'state':'firmadovaloracion'},
                                context)
        #~ envio el menesaje a la entidad
        #~ busco la entidad_id
        entidad_id=entidad_obj.search(cr,uid,[('parent_id','=',res_partner_id)])
        entidad_data=entidad_obj.browse(cr,uid,entidad_id,context=context)[0]
        for usuario in entidad_data.user_ids:
            partner_ids.append(usuario.partner_id.id)
        #~ contenido de la notificación
        ctx={
                'mail_post_autofollow_partner_ids': [], 
                'default_model': 'jpv_ent.entidades', 
                'default_res_id':entidad_id[0], 
                'mail_read_set_read': True, 
                'mail_post_autofollow': True}
        values={
            'body': body_notificacion, 
            'model': 'jpv_ent.entidades', 
            'attachment_ids': [(4, attachment_id)], 
            'res_id': entidad_id[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'comment', 
            'partner_ids': [], 
            'subject': False}
        
        mail_message_obj.create(cr,uid,values,context=ctx)
        #~ envio de correo a la entidad
        try:
            template_id = ir_model_data_obj.get_object_reference(
                                        cr, 
                                        uid, 
                                        'jpv_valoracion', 
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
        mail_id = self.pool.get('email.template').send_mail(cr, uid, template_id, entidad_id[0] , True, context=ctx)
        return
    
    def correos(self,cr,uid,ids,context=None):
        mails=[]
        self_data=self.browse(cr,uid,ids,context=context)[0]
        for usuarios_ept in self_data.user_ids:
            mails.append(usuarios_ept.partner_id.email)
        mails = ', '.join(mails)
        return mails 
    
    def get_access_link(self,cr,uid,ids,context=None):
        datos_url={
            'id':ids[0],
            'view_type':'form',
            'model':'jpv_ent.entidades'
        }
        return "/web#%s" % urlencode(datos_url)
        
        
    
    
class jpv_cp_carga_proyecto(osv.osv): 
    _name = 'jpv_cp.carga_proyecto'
    _inherit="jpv_cp.carga_proyecto"

        
    def dictamen_valoracion(self, cr, uid, ids, field_name, arg, context=None):
        '''campo function que calcula el dictamen de las valoraciones'''
        result = {}
        dictamen_valoracion_obj=self.pool.get('jpv_val.dictamen_valoracion')
        for proyecto in self.browse(cr, uid, ids, context=context):
            sin_dictame='Sin valorar'
            dictamen_ids=[]
            where=[]
            if proyecto.valGeneral==True:
                sin_dictame='Solo General'
            if proyecto.valCoordenadas==True:
                sin_dictame='Solo Coordenadas'
            dictamenes=[sin_dictame]
            if proyecto.valGeneral==True and proyecto.valCoordenadas==True:
                where.append(('tipo_valoracion','in',['valoracion_general','valoracion_coordenadas']))
                where.append(('proyecto_id','=',proyecto.id))
                dictamen_ids=dictamen_valoracion_obj.search(cr,uid,where)
                dictamen_data=dictamen_valoracion_obj.browse(cr,uid,dictamen_ids)
                for resultado in  dictamen_data:
                    dictamenes.append(resultado.dictamen.capitalize())
            if 'Negado' in dictamenes:
                dictamen='Negado'
            elif 'Diferido' in dictamenes:
                dictamen='Diferido'
            elif 'Aprobado' in dictamenes:
                dictamen='Aprobado'
            else:
                dictamen=dictamenes[0]
            self.write(cr, SUPERUSER_ID,proyecto.id,{'dictamengraph':dictamen},0)
            result[proyecto.id]=dictamen
        return result

    _columns = {
        'AsigValCoordenadas': fields.boolean(
                            'Asignación de Valoración de coordenas',
                            help='Si este campo esta tildado, el proyecto\
                                    ya ha sido asignado para la valoración de \
                                    coordenadas'),
                                    
        'valCoordenadasUre': fields.boolean(
                            'Valoracíon de coordenas Ure',
                            help='Sí este campo esta tildado, el proyecto\
                                    ya ha sido valorado las coordenadas desede\
                                    el Ure'),
                                    
        'AsigValGeneral': fields.boolean(
                            'Asignación de Valoracíon General',
                            help='Sí este campo esta tildado, el proyecto\
                                    ya ha sido asignado para la valoración  \
                                    General '),
        'valGeneral': fields.boolean(
                            'Valoracíon General',
                            help='Sí este campo esta tildado, el proyecto\
                                    ya se le hizo la valoración General'),
                                    
        'valCoordenadas': fields.boolean(
                            'Valoración de Coordenadas',
                            help='Sí este campo esta tildado, el proyecto\
                                    ya se le hizo la valoración de coordenadas'),

        'dictamen':fields.function(dictamen_valoracion,
                                            type='char',
                                            string="Status de valoración",
                                            ),
                                                
        'dictamengraph':fields.char("Status de valoración"),
                                
        'valoraciones_ids': fields.one2many(
                                        'jpv_val.dictamen_valoracion',
                                        'proyecto_id',
                                        'Valaraciones'
                                        ),
    
        }

    def valoracion_proyecto_ures(self,cr,uid,ids,context=None):
        url='/valoracion/proyecto/%s/%s/%s' % (ids[0],'valoracion_coordenadas_ures','valCoordenadasUre')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new',
      
        }
        
    _defaults = {
        'AsigValCoordenadas':False,
        'valCoordenadasUre':False,
        'AsigValGeneral':False,
        'valGeneral':False,
        'valCoordenadas':False
        }
    
        
    

class jpv_val_asignacion_valoracion(osv.osv):
    _name = 'jpv_val.asignacion_valoracion'
    _description = u"Asignación de las valoraciones\
                    por proyecto del Concejo Federal de Gobierno"
    _rec_name= "user_id"
    _order = 'fecha_asig desc'
    groups_id=[]
    
    def __init__(self, pool, cr):
        init_res = super(jpv_val_asignacion_valoracion, self).__init__(pool, cr)
        cr.execute(""" select g.id from res_groups as g,
                    ir_module_category as c
                    where c.name = 'ROLES DE LA GERENCIA TÉCNICA DE PROYECTOS'
                    and g.category_id=c.id""");
        res_groups_ids=cr.fetchall()
        for group in res_groups_ids:
            self.groups_id.append(group[0])
        return init_res

    def _get_proyecto_idsg(self, cr, uid, ids, field_name, arg, context=None):
        '''para cargar el mamy2many proyecto_idsg'''
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            proyectos_ids=[]
            for proyect in  record.proyecto_idsg:
                 proyectos_ids.append(proyect.id)
            result[record.id]=proyectos_ids
        return result
        
    def _get_proyecto_idsc(self, cr, uid, ids, field_name, arg, context=None):
        '''para cargar el mamy2many proyecto_idsc'''
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            proyectos_ids=[]
            for proyect in  record.proyecto_idsc:
                 proyectos_ids.append(proyect.id)
            result[record.id]=proyectos_ids
        return result
        
    def _cant_asignaciones_geneales(self, cr, uid, ids, field_name, arg, context=None):
        '''Cantidad de proyectos asignados General'''
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id]=len(record.proyecto_idsg)
        return result
        
    def _cant_asignaciones_coordenadas(self, cr, uid, ids, field_name, arg, context=None):
        '''Cantidad de proyectos asignados por coordenadas'''
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id]=len(record.proyecto_idsc)
        return result

    def _get_valorar_url(self, cr, uid, ids, name, arg, context=None):
        if context and context.get('relative_url'):
            base_url = '/'
        else:
            base_url = self.pool['ir.config_parameter'].get_param(cr, uid, 'web.base.url')
        res = {}
        for asig in self.browse(cr, uid, ids, context=context):
            if (uid==asig.user_id.id):
                res[asig.id] = '<a href="'+urljoin(base_url, "/valoracion/%s/" % asig.id)+'"><button type="button" class="oe_button oe_highlight">Valorar</button></a>'
            else:
                res[asig.id]=''
        return res
        
    _columns = {
        'fecha_asig':fields.datetime('Fecha de Asignacón'),
        'referencia':fields.char('Descripción',required=True),
        
        'proyecto_idsg2': fields.function(_get_proyecto_idsg,
                                            type='many2many',
                                            relation="jpv_cp.carga_proyecto",
                                            string="Projectos generales ocultos"),

        'cant_asig_g':fields.function(_cant_asignaciones_geneales,
                                            type='integer',
                                            string="Generales",
                                            store=True),
        
        'proyecto_idsg':fields.many2many(
                                        'jpv_cp.carga_proyecto', 
                                        'jpv_val_asiganacion_general_rel', 
                                        'proyecto_id', 
                                        'asignaciong_id',
                                        'Proyectos asignar General'),
                    
        'proyecto_idsc2': fields.function(_get_proyecto_idsc,
                                            type='many2many',
                                            relation="jpv_cp.carga_proyecto",
                                            string="Projectos coordenadas ocultos"),

        'cant_asig_c':fields.function(_cant_asignaciones_coordenadas,
                                            type='integer',
                                            string="Coordenadas",
                                            store=True),
                                            
        'dictamen_ids': fields.one2many(
                            'jpv_val.dictamen_valoracion',
                            'asignacion_id',
                            'Voloraciones'),
                            
        'proyecto_idsc':fields.many2many(
                    'jpv_cp.carga_proyecto', 
                    'jpv_val_asiganacion_coordenadas_rel', 
                    'proyecto_id', 
                    'asignacionc_id',
                    'Proyectos asignar Coordenadas'
                    ),
                    
        'tipo_sector_id':fields.many2one(
                                'jpv_cp.tipo_sectores',
                                'Tipo de sector',
                                required=True,
                                help='Tipo de sector al cual pertenece\
                                     el proyecto a asignar'),
                                     
        'categoria_id': fields.many2one(
                                'jpv_cp.tipo_sectores', 
                                'Categoría', 
                                required=True, 
                                help='Categoría a la cual pertenece\
                                     el proyecto a asignar'),
                                     
        'subcategoria_id': fields.many2one(
                                    'jpv_cp.tipo_sectores', 
                                    'Subcategoría', 
                                    required=True, 
                                    help='Subcategoría a la cual\
                                    pertenece el proyecto a asignar'),
                                    
        'mantenimiento': fields.boolean(
                            'Proyecto de Manteniento',
                            help='Sí se pulsa esta opción se listaran\
                                los proyectos de mantenimientos'),
                                    
        'user_id': fields.many2one(
                    'res.users', 
                    'Técnico',
                    copy=False,
                    required=True,
                    domain=[('groups_id', 'in',groups_id)],
                    ),
                    
        'correlativo':fields.char(
                            'Código de la valoración',
                            help='Código unico de la valoración'),

                            
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),

        'website_url': fields.function(_get_valorar_url,
            string="link Valorar", type="html"),

        
        'valoraciones_id': fields.one2many(
                                        'jpv_val.valoraciones',
                                        'asig_valoracion_id',
                                        'Valaraciones',
                                        copy=True,
                                        ),
        'state': fields.selection([
                            ('abierta', 'Abierta'),
                            ('validada', 'Validada'),
                            ], 'Estatus')
                            

    }

    _defaults = {
        'active':True,
        'state':'abierta',
    }

        
    def eliminacion_general(self,cr,uid,ids,proyecto_idsg,proyecto_idsg2,context=None):
        '''Vuelve a poner el proyecto activo para la evaluación de '''
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        proyect_id=set(proyecto_idsg2)-set(proyecto_idsg)
        proyect_id=list(proyect_id)
        
        if len(proyect_id)>0:
            proyecto_data=carga_proyecto_obj.browse(cr,SUPERUSER_ID,proyect_id)[0]
            if proyecto_data.state!='evaluacion':
                raise osv.except_osv(('Error!'),
                                    ('No puede eliminar el proyecto'\
                                    ' %s ya que esta  %s: ' % \
                                    (proyecto_data.correlativo,proyecto_data.state)))
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    proyect_id,
                                    {'AsigValGeneral':False},
                                    0
                                    )
        return {'value':{'proyecto_idsg2':proyecto_idsg}}
                                    
    def eliminacion_coord(self,cr,uid,ids,proyecto_idsc,proyecto_idsc2,context=None):
        '''Vuelve a poner el proyecto activo para evaluar las coordenadas'''
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        proyect_id=set(proyecto_idsc2)-set(proyecto_idsc)
        proyect_id=list(proyect_id)
        if len(proyect_id)>0:
            proyecto_data=carga_proyecto_obj.browse(cr,SUPERUSER_ID,proyect_id)[0]
            if proyecto_data.state!='evaluacion':
                raise osv.except_osv(('Error!'),
                                    ('No puede eliminar el proyecto'\
                                    ' %s ya que esta %s: ' % \
                                    (proyecto_data.correlativo,proyecto_data.state)))
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    proyect_id,
                                    {'AsigValCoordenadas':False},
                                    0
                                    )
        return {'value':{'proyecto_idsc2':proyecto_idsc}}

    def unlink(self, cr, uid, ids, context=None):
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        rigistros=self.browse(cr,uid,ids)
        for datos in rigistros:
            for idsc in datos.proyecto_idsc:
                carga_proyecto_obj.write(
                                cr,
                                SUPERUSER_ID,
                                idsc.id,
                                {'AsigValCoordenadas':False},
                                0
                                )
                
            for idsg in datos.proyecto_idsg:
                carga_proyecto_obj.write(
                                cr,
                                SUPERUSER_ID,
                                idsg.id,
                                {'AsigValGeneral':False},
                                0
                                )
        id_asig=super(jpv_val_asignacion_valoracion, self).unlink(cr, uid, ids, context=context)
        
        return id_asig

    def write(self, cr, uid, ids, values, context=None):
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        if values.has_key('proyecto_idsc'):
            self_data=self.browse(cr,uid,ids,context=context)[0]
            for proyecto in self_data.proyecto_idsc2:
                if proyecto.state!='evaluacion':
                    raise osv.except_osv(('Error!'),
                                    ('No puede eliminar el proyecto'\
                                    ' %s ya que esta %s: ' % \
                                    (proyecto.correlativo,proyecto.state)))
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    values['proyecto_idsc'][0][2],
                                    {'AsigValCoordenadas':True},
                                    0
                                    )
                                    
        if values.has_key('proyecto_idsg'):
            self_data=self.browse(cr,uid,ids,context=context)[0]
            for proyecto in self_data.proyecto_idsg2:
                if proyecto.state!='evaluacion':
                    raise osv.except_osv(('Error!'),
                                    ('No puede eliminar el proyecto'\
                                    ' %s ya que esta %s: ' % \
                                    (proyecto.correlativo,proyecto.state)))
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    values['proyecto_idsg'][0][2],
                                    {'AsigValGeneral':True},
                                    0
                                    )
        id_asig = super(jpv_val_asignacion_valoracion, self).write(cr, uid, ids, values, context)
        return id_asig
        
    def create(self,cr,uid,values,context=None):
        values['fecha_asig']=datetime.datetime.now()
        carga_proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        id_asig=super(jpv_val_asignacion_valoracion,self).create(
                                                    cr,
                                                    uid,
                                                    values,
                                                    context=context)
        if values.has_key('proyecto_idsc') and values['proyecto_idsc'][0][2]:
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    values['proyecto_idsc'][0][2],
                                    {'AsigValCoordenadas':True},
                                    0
                                    )
                                    
        if values.has_key('proyecto_idsg') and values['proyecto_idsg'][0][2]:
            carga_proyecto_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    values['proyecto_idsg'][0][2],
                                    {'AsigValGeneral':True},
                                    0
                                    )
            
        return id_asig

class jpv_val_valoraciones(osv.osv):
    _name = 'jpv_val.valoraciones'
    _description = u"valoraciones de los preyectos"
    _rec_name= "proyecto_id"

    state_project=[('carga', 'Proceso de Carga'),
                            ('evaluacion', 'En Evaluación'),
                            ('diferido', 'Diferido'),
                            ('aprobado', 'Aprobado'),
                            ('negado', 'Negado'),
                            ('cancelado', 'Cancelado')]

    _columns = {
        'proyecto_id':fields.many2one(
                                'jpv_cp.carga_proyecto',
                                'Proyecto',
                                required=True,
                                help='Proyecto evaluados'),
                                
        'state': fields.related('proyecto_id',
                                    'state',
                                    type='char',
                                    relation="jpv_cp.carga_proyecto",
                                    string='Stado',
                                    help='Estado del Proyecto',
                                    select=True,
                                    store=True),
                                
        'asig_valoracion_id': fields.many2one(
                                        'jpv_val.asignacion_valoracion',
                                        'Asignacion de valaraciones'),
            
        'etapas_id':fields.many2one(
                                'jpv_plf.etapas',
                                """Ciclo""",
                                ondelete='cascade',
                                required=True,),
                                
        'tipo': fields.selection([('general', 'General'),
                                         ('coordenadas', 'Cordenadas')],
                                        'Tipo de valoración'),

        }
                                        

        
    
        
        

