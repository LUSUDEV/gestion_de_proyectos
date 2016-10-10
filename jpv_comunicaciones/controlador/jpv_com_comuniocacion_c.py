# -*- coding: utf-8 -*-
import json
import base64
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from openerp.addons.jpv_usuarios.controladores import jpv_use_users_c
from werkzeug import secure_filename


class jpv_comunicaciones(http.Controller):

    @http.route(
            ['/jpvcomunicaciones'], 
            type='http', auth="user", website=True)
    def jpvcomunicaciones(self,**post):
            '''este metodo sive para mostrar las valoración asignadas'''
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            user_obj = registry['res.users']
            asuntos_obj = registry['jpv_com.asuntos']
            datos_organizacion=''
            tipo_organizacion=''
            remitente=''
            asuntosData=[]
            referencia=''
            mi_entidad=jpv_use_users_c.jpv_users().mi_entidad(uid)
            if mi_entidad['entidad_data']:
                referencia='entidad'
                datos_organizacion=mi_entidad['entidad_data']
                user_data=user_obj.browse(cr,uid,uid)[0]
                remitente=user_data.name
                tipo_organizacion='Entidad Político Territorial: '
                asunto_ids=asuntos_obj.search(cr,SUPERUSER_ID,[('parent_id','=',False)])
                asunto_data=asuntos_obj.browse(cr,SUPERUSER_ID,asunto_ids)
                for asunto in asunto_data:
                    for plan_proyecto in asunto.proyectos_ids:
                        if plan_proyecto.referencia==referencia:
                            asuntosData.append({
                                                'id':asunto.id,
                                                'asunto':asunto.name,
                                                'tipo_campo':asunto.tipo_campo,
                                                'name_text':asunto.name_text})
                datos={'parametros':{
                                'titulo':'Envío de Comunicación Oficial',
                                'url_boton_list':'/web',
                                'template':'jpv_comunicaciones.envios',
                                'action':'/comunicaciones/enviar',
                                'id_enviar':'jpvEnviarComunicaciones',
                                'nombre_bt_accion':' Enviar'},
                        'datos_organizacion':datos_organizacion,
                        'tipo_organizacion':tipo_organizacion,
                        'referencia':referencia,
                        'remitente':remitente,
                        'asunto_data':asuntosData
                                }
                return panel.panel_post(datos)
            mensaje={
                    'titulo':'Sin Entidad',
                    'mensaje':'''Disculpe NO esta asociado a ninguna Organización,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
            
    @http.route(
            ['/comunicaciones/asuntos'], 
            type='http', auth="user", website=True)
    def jpvcomunicacionesAsuntos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        periodos_obj = registry['jpv_plf.periodos']
        proyecto_obj = registry['jpv_cp.carga_proyecto']
        entidades_obj = registry['jpv_ent.entidades']
        asuntos_obj = registry['jpv_com.asuntos']
        asuntosData=[]
        if post['tipo_campo']=='proyecto':
            entidad_data=entidades_obj.browse(cr,SUPERUSER_ID,int(post['organizacion_id']))[0]
            proyecto_ids=proyecto_obj.search(cr,SUPERUSER_ID,[('partner_id','=',entidad_data.parent_id.id),('periodo_id','=',int(post['asunto_id']))])
            proyecto_data=proyecto_obj.browse(cr,SUPERUSER_ID,proyecto_ids)
            for proyecto in proyecto_data:
                asuntosData.append({
                                    'id':proyecto.id,
                                    'correlativo':proyecto.correlativo,
                                    'name_text':'',
                                    'tipo_campo':''})
        if post['tipo_campo']=='periodo':
            periodos_ids=periodos_obj.search(cr,SUPERUSER_ID,[])
            periodos_data=periodos_obj.browse(cr,SUPERUSER_ID,periodos_ids)
            for periodo in periodos_data:
                asuntosData.append({
                                    'id':periodo.id,
                                    'periodo':periodo.periodo_fiscal,
                                    'name_text':'',
                                    'tipo_campo':'proyecto'})
            
        else:
            asunto_ids=asuntos_obj.search(cr,SUPERUSER_ID,[('parent_id','=',int(post['asunto_id']))])
            asunto_data=asuntos_obj.browse(cr,SUPERUSER_ID,asunto_ids)
            for asunto in asunto_data:
                for plan_proyecto in asunto.proyectos_ids:
                    if plan_proyecto.referencia==post['referencia']:
                        asuntosData.append({
                                            'id':asunto.id,
                                            'asunto':asunto.name,
                                            'name_text':asunto.name_text,
                                            'tipo_campo':asunto.tipo_campo})
        ret = asuntosData
        return json.dumps(ret)
    
    @http.route(
        ['/comunicaciones/enviar'], 
        type='http', auth="user",methods=['POST'], website=True)
    def jpvcomunicacionesEnviar(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        comunicaciones_obj = registry['jpv_com.comunicaciones']
        notification_obj=registry['mail.notification']
        entidades_obj = registry['jpv_ent.entidades']
        mail_message_obj=registry['mail.message']
        users_obj = registry['res.users']
        users_data=users_obj.browse(cr,SUPERUSER_ID,[uid])[0]
        entidad_data=entidades_obj.browse(cr,SUPERUSER_ID,int(post['organizacion_id']))[0]
        file=post["jpv_com_adjunto"]
        #~ proyectos
        proyecto_post_ids=panel.dict_keys_startswith(post,'proyectosadd_')
        proyecto_ids=[]
        for proyecto_id in proyecto_post_ids:
            proyecto_ids.append(int(post[proyecto_id]))
        #~ campos de asunto tipo text
        textSolicitudesPost=[]
        textSolicitudes=panel.dict_keys_startswith(post,'textSolicitud_')
        for text in textSolicitudes:
            asunto_id=text.split('_')
            textSolicitudesPost.append([0,False,{
                'asunto_id':int(asunto_id[1]),
                'campo_texto':post[text],
                'active': True,
                'comunicacion_id': False
                }])
                
        if (post['referencia']=='entidad'):
            correlativo=registry['ir.sequence'].get(cr,uid,
                                                'jpv_com.comunicaciones')
            comunicacion_data={
                'partner_id':entidad_data.parent_id.id,
                'users_id':uid,
                'correlativo':correlativo,
                'asunto_id':int(post['asunto_1']),
                'comunicacion':post['comunicacion'],
                'proyecto_ids':[[6, False, proyecto_ids]],
                'campo_text_ids':textSolicitudesPost
                }
        
        comunicacion_id=comunicaciones_obj.create(cr,SUPERUSER_ID,comunicacion_data)
        #~ contenido de la notificación a la entidad (4, users_data.partner_id.id) (4, users_data.partner_id.id)
        ctx={
                'mail_post_autofollow_partner_ids':[], 
                'default_model': 'jpv_ent.entidades', 
                'default_res_id':int(post['organizacion_id']), 
                'mail_read_set_read': True, 
                'mail_post_autofollow': True}
        
        values={
            'body': post['comunicacion'], 
            'model': 'jpv_ent.entidades', 
            'res_id': int(post['organizacion_id']),
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': users_data.partner_id.id, 
            'type': 'comment', 
            'partner_ids': [], 
            'subject':'Comunicación Oficial '+correlativo}
        if file:
            attachment_obj=registry['ir.attachment']
            attachment_id = attachment_obj.create(cr,SUPERUSER_ID,{
            'name': file.filename,
            'datas': base64.b64encode(file.read()),
            'datas_fname': file.filename,
            'res_model':'jpv_ent.entidades',
            'res_id':int(post['organizacion_id']),
            'mimetype':file.content_type,
            'description':post['comunicacion']
            }, context)
            values['attachment_ids']= [(4, attachment_id)]
            mensaje_id=mail_message_obj.create(cr,SUPERUSER_ID,values,context=ctx)
            comunicaciones_obj.write(cr,SUPERUSER_ID,comunicacion_id,{
                                                'attachment_id':attachment_id,
                                                'mensaje_id':mensaje_id
                                                })
        else:
            mensaje_id=mail_message_obj.create(cr,SUPERUSER_ID,values,context=ctx)
            comunicaciones_obj.write(cr,SUPERUSER_ID,comunicacion_id,{'mensaje_id':mensaje_id})
        value_not={
            'is_read':False,
            'starred':False,
            'partner_id':users_data.partner_id.id,
            'message_id':mensaje_id
            }
        notification_obj.create(cr,uid,value_not)
        ret={'correlativo':correlativo}
        return json.dumps(ret)
        
    @http.route('/jpvconfirmar_comunicaciones',
            type='json', auth="user", website=True)
    def confirmar_comunicaciones(self,**kw):
        comunicaciones={}
        comunicaciones_masivas={}
        ids={}
        comunicaniones_ids=[]
        comunicaniones_masiva_ids=[]
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        entidad_data=jpv_use_users_c.jpv_users().mi_entidad(uid)
        if entidad_data['entidad_id']:
            comunicaciones_obj=registry['jpv_com.comunicaciones']
            comunicaciones_ids=comunicaciones_obj.search(
                                    cr,
                                    SUPERUSER_ID,
                                    [('partner_id','=',entidad_data['entidad_data'].parent_id.id),
                                    ('state','=','enviado')])
            comunicaciones_data=comunicaciones_obj.browse(cr,SUPERUSER_ID,comunicaciones_ids)
            for comunicacion in comunicaciones_data:
                comunicaniones_ids.append(comunicacion.id)
                respuestas={}
                for respuesta in comunicacion.salidas_ids:
                    adjuntohtm=''
                    for adjunto in respuesta.adjunto_ids:
                        adjuntohtm+='''<br/><a target="_blank" href="web/binary/saveas?model=ir.attachment&amp;field=datas&amp;id=%d&amp;filename_field=datas_fname">
                            <img src="/mail/static/src/img/mimetypes/print.png">
                            <div class="oe_name">%s</div>
                            </a><br/>''' % (adjunto.attachment_id.id,adjunto.attachment_id.datas_fname)
                    respuestas[respuesta.id]={
                        'correlativo':respuesta.correlativo,
                        'create_date':respuesta.create_date,
                        'subject':respuesta.mensaje_id.subject,
                        'comunicacion':respuesta.comunicacion,
                        'adjunto':adjuntohtm
                        }
                adjunto='''<a target="_blank" href="web/binary/saveas?model=ir.attachment&amp;field=datas&amp;id=%d&amp;filename_field=datas_fname">
                        <img src="/mail/static/src/img/mimetypes/print.png">
                        <div class="oe_name">%s</div>
                        </a>''' % (comunicacion.attachment_id.id,comunicacion.attachment_id.datas_fname)
                comunicaciones[comunicacion.id]={
                            'correlativo':comunicacion.correlativo,
                            'create_date':comunicacion.create_date,
                            'asunto_name':comunicacion.asunto_id.name,
                            'comunicacion':comunicacion.comunicacion,
                            'respuestas':respuestas,
                            'adjunto':adjunto
                    }
            #~ comunicaciones masivas
            comunicaciones_masivas_obj=registry['jpv_com.comunicaciones_masivas']
            comunicaciones_masivas_ids=comunicaciones_masivas_obj.search(
                                    cr,
                                    SUPERUSER_ID,
                                    [('pertner_ids','=',entidad_data['entidad_data'].parent_id.id),
                                    ('state','=','enviado')])
            comunicaciones_masiva_data=comunicaciones_masivas_obj.browse(cr,SUPERUSER_ID,comunicaciones_masivas_ids)
            for comunicacion in comunicaciones_masiva_data:
                leido=False
                for comunicacion_leida in comunicacion.partner_leidos_ids:
                    if comunicacion_leida.pertner_id.id==entidad_data['entidad_data'].parent_id.id:
                        leido=True
                if not leido:
                    comunicaniones_masiva_ids.append(
                                        {'comunicacion_masiva_id':comunicacion.id,
                                        'partner_id':entidad_data['entidad_data'].parent_id.id})
                    adjuntohtm=''
                    for adjunto in comunicacion.adjunto_ids:
                        adjuntohtm+='''<br/><a target="_blank" href="web/binary/saveas?model=ir.attachment&amp;field=datas&amp;id=%d&amp;filename_field=datas_fname">
                            <img src="/mail/static/src/img/mimetypes/print.png">
                            <div class="oe_name">%s</div>
                            </a><br/>''' % (adjunto.attachment_id.id,adjunto.attachment_id.datas_fname)
                    comunicaciones_masivas[comunicacion.id]={
                            'correlativo':comunicacion.correlativo,
                            'create_date':comunicacion.fecha_envio,
                            'name':comunicacion.name,
                            'comunicacion':comunicacion.comunicacion,
                            'adjunto':adjuntohtm
                        }
            ids['comunicaniones_ids']=comunicaniones_ids
            ids['comunicaniones_masiva_ids']=comunicaniones_masiva_ids
            print comunicaciones_masivas
            return {
                'comunicaciones':comunicaciones,
                'comunicaciones_masivas':comunicaciones_masivas,
                'ids':ids
                }
        return{}
        
    @http.route('/jpvComunicacionesLeidos',
            type='json', auth="user", website=True)
    def confirmar_comunicaciones_leidos(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        comunicacion_obj=registry['jpv_com.comunicaciones']
        comunicaciones_masivas_leidas_obj=registry['jpv_com.comunicaciones_masivas_leidas']
        comunicaciones_masivas_obj=registry['jpv_com.comunicaciones_masivas']
        for id in post['comunicaniones_ids']:
            comunicacion_obj.write(cr,uid,[id],{'state':'leido'})
        for ids in post['comunicaniones_masiva_ids']:
            comunicaciones_masivas_leidas_obj.create(cr,SUPERUSER_ID,{'pertner_id':ids['partner_id'],'cominicaciones_id':ids['comunicacion_masiva_id']})
            comunicacion_masiva_data=comunicaciones_masivas_obj.browse(cr,SUPERUSER_ID,[ids['comunicacion_masiva_id']])[0]
            partner_idsc=[]
            partner_leidos_idsc=[]
            for partner in comunicacion_masiva_data.pertner_ids:
                partner_idsc.append(partner.id)
            for partner_leidos in comunicacion_masiva_data.partner_leidos_ids:
                partner_leidos_idsc.append(partner_leidos.pertner_id.id)
            partner_idsc.sort()
            partner_leidos_idsc.sort()
            if partner_leidos_idsc == partner_idsc:
                comunicaciones_masivas_obj.write(cr,SUPERUSER_ID,[ids['comunicacion_masiva_id']],{'state':'leidos'})
    
   


