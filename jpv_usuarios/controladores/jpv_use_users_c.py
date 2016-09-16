# -*- coding: utf-8 -*-

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools

_logger = logging.getLogger(__name__)

class jpv_users(http.Controller):
    
    #~ nombre del la categoria que quiero filtrar
    category_name=['ROLES DE LAS ENTIDADES POLITICO TERRITORIALES']
    #~ nonbres del grupo que quiero filtrar
    not_groups_name=['Alcaldes, Gobernadores o Alcalde Mayor']
    #~ nonbre de lo grupos que quiero controlar [(cant_max,'nombre')]
    #~ lo nombres de grupo que no debe tomar en cuenta
    not_group=['Contact Creation','Employee','Website Comments','Do Not Use Sales Teams']
    #~ cantidad y nombre de los grupos de usuarios controlados para su creación
    control_cant_name_groups=[(1,'Secretario'),(2,'Ingeniero de Obras')]
        
                
    @http.route(
            ['/usuarios'], 
            type='http', auth="user", website=True)
    def users_index(self):
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            user_obj = registry['res.users']
            mi_entidad=self.mi_entidad(uid)
            if mi_entidad['entidad_data']:
                if not base_tools.users_active(uid):
                    return request.redirect(base_tools.LOGIN)
                users_ids = user_obj.search(
                                            cr,
                                            SUPERUSER_ID,
                                            [('id','in',mi_entidad['user_ids'])],
                                            order="id desc",
                                            context=context)
                users_data = user_obj.browse(
                                                cr,
                                                SUPERUSER_ID,
                                                users_ids,
                                                context=context)
                titilo='''Registro de usuarios
                '''+mi_entidad['entidad_data'].name
                datos={'parametros':{
                                'titulo':titilo,
                                'url_boton_crear':'/usuarios/crear',
                                'template':'ept_usuarios.recorrido',
                                'icon_crear':'user',
                                'color_btn_crear':'info',
                                'css':'info',},
                                'users_data':users_data,
                                'groups_user':self.groups_user,
                                'entidad_data':mi_entidad['entidad_data'],
                                'not_groups_name':self.not_groups_name
                                }
                                
                return panel.panel_lista(datos)
            mensaje={
                    'titulo':'Sin EPT',
                    'mensaje':'''Disculpe NO esta asociado a ninguna EPT,
                                Comuníquese con el administrador del sistema''',
                    'volver':'/'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)

            
    def groups_user(self,groups_obj):
        name_group=''
        group_name=['ROLES DE LAS ENTIDADES POLITICO TERRITORIALES']
        groups=base_tools.groups_category(group_name)
        for group in groups_obj:
            if group.id in groups['group_ids']:
                name_group+=group.name+'\n'
        return name_group
        
    @http.route(
            ['/usuarios/<model("res.users"):user>'], 
            type='http', auth="user", website=True)
    def usuario_editar(self,user=None):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        if not base_tools.users_active(uid):
                return request.redirect(base_tools.LOGIN)
        entidad_data=self.mi_entidad(uid)
        groups=base_tools.control_groups_name(
                                        self.category_name,
                                        self.control_cant_name_groups,
                                        entidad_data['user_ids'],
                                        self.not_groups_name)
        #~ en esta variable guardo los id y los nombres de los grupos 
        #~ que si se tomaran en cuenta..
        user_groups=[]
        #~ recorro user (usuario seleccionado) para iterar los grupos que esté 
        #~ tiene asignado y quito los que no quiero que se vean, para 
        #~ luego adicionarselo a -la lista user_groups, que es donde voy a tener
        #~ los grupos permitidos para este usurio
        for u in user:
            for group in u.groups_id:
                if not group.name in self.not_group:
                    user_groups.append((group.id,group.name,True))
        
        #~ recorro los grupo de usuarios que sugún la regla permite y que le queda
        #~ a esta entidas y los que no esten esignados a este usuario los coloco en
        #~ false 
        for idice in range(len(groups['groups'])):
            groups['groups'][idice]=(groups['groups'][idice][0],groups['groups'][idice][1],True)
            if not groups['groups'][idice] in user_groups:
                groups['groups'][idice]=(groups['groups'][idice][0],groups['groups'][idice][1],False)
                
        #~ Aplico teoria de conjunto (union) entre los permisos que tiene este 
        #~ usuario y los que le quedan a la entidad, según las reglas
        groups_union=list(set(groups['groups'])|set(user_groups))
        mi_entidad=self.mi_entidad(uid)
        titilo='''Editar usuario
            '''+mi_entidad['entidad_data'].name
        datos={'parametros':{
                            'titulo':titilo,
                            'url_boton_list':'/usuarios',
                            'template':'ept_usuarios.users_edit',
                            'action':'/usuarios/editar',},
                            'users_data':user,
                            'groups_union':groups_union,
                            }
        return panel.panel_post(datos)
        
    @http.route(
            ['/usuarios/editar'],
            type='json', auth='user', website=True)
    def accion_editar(self,**post):
        ret={}
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        res_users_obj = registry.get('res.users')
        datos_campos=[
                      {'name':'email',
                      'type':'email',
                      'attr':'Correo del Usuario,' },
                      {'name':'in_group_',
                      'type':'checkbox',
                      'attr':'El rol del Usuario,'}
                     ]
        errors=panel.validar().varios_campos(datos_campos,post)
        if len(errors)==0:
            in_groups=panel.dict_keys_startswith(post,'in_group_')
            values={
                'email': post['email'],
                'login': post['email'],
                'image': post['image'],
                }
                
            for in_group in in_groups:
                values[in_group]=True;
            if post['email']!=post['email2']:
                user_id=res_users_obj.search(cr,
                                    SUPERUSER_ID,
                                    [('login','=',post['email'])],
                                    context=context);
            else:
                user_id=[]
            if (len(user_id)==0):
                user_id = res_users_obj.write(
                                        cr,
                                        SUPERUSER_ID,
                                        int(post['iduser']),
                                        values,
                                        context)
            else:
                    ret =  {'modal':{
                            'titulo':'<strong>Error al editar el usuario.</strong>',
                            'cuerpo':'''<h1 class="text-danger" >
                                        El correo
                                        %s ya existe...</h1>
                                        ''' % (post['email']),
                                    },
                            }
                    return ret
        else:
                ret={'error_campos':errors}
                
        ret={'redirect':'/usuarios'}
        return ret
        
    @http.route(
            ['/usuarios/active'], 
            type='json', auth='user', website=True)
    def users_active(self,**post):
            _logger.debug('Incoming data: %s', post)
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            user_obj = registry['res.users']
            active = (True,False)[post['state']==False]
            result=user_obj.write(
                                    cr,
                                    SUPERUSER_ID,
                                    [int(post['id'])], 
                                    {'activo': active })
            ret = {}
            return json.dumps(ret)
        
        
    @http.route(
            ['/usuarios/crear'], 
            type='http', auth='user', website=True)
    def control_groups_name(self):
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            
            entidad_data=self.mi_entidad(uid)
            groups=base_tools.control_groups_name(
                                                self.category_name,
                                                self.control_cant_name_groups,
                                                entidad_data['user_ids'],
                                                self.not_groups_name)
            if groups['groups']:
                mi_entidad=self.mi_entidad(uid)
                titilo='''Registro de usuarios
                '''+mi_entidad['entidad_data'].name
                datos={'parametros':{
                                'titulo':titilo,
                                'url_boton_list':'/usuarios',
                                'template':'ept_usuarios.users_create',
                                'action':'/usuarios/enviar',
                                },
                        'groups_data':groups['groups'],
                                }
                                
                return panel.panel_post(datos)
            mens=''
            for control in self.control_cant_name_groups:
                 mens+='Cantidad de %s permitidos = %s, \n' % (control[1],control[0])
            mensaje={
                    'titulo':'Usuarios máximos permitidos',
                    'mensaje':'Disculpe ya creó los usuarios máximos permitidos'\
                        'permitidos.\n'+mens,
                    'volver':'/usuarios'
                }
            return http.request.website.render('website_apiform.mensaje', mensaje)
        

    @http.route(
            ['/usuarios/enviar'],
            type='json', auth='user', website=True)
    def accion_crear(self,**post):
            ret={}
            registry = http.request.registry
            cr=http.request.cr
            uid=http.request.uid
            context = http.request.context
            res_users_obj = registry.get('res.users')
            ir_action_obj = registry.get('ir.actions.actions')
            datos_campos=[{'name':'name',
                           'type':'text',
                           'attr':'Nombre de usuario,'},
                          {'name':'email',
                          'type':'email',
                          'attr':'Correo del Usuario,' },
                          {'name':'in_group_',
                          'type':'checkbox',
                          'attr':'El rol del Usuario,'}]
            errors=panel.validar().varios_campos(datos_campos,post)
            if(len(errors)==0): 
                in_groups=panel.dict_keys_startswith(post,'in_group_')
               
                value={
                'lang': u'es_VE',
                'tz':'America/Caracas',
                'name':post['name'],
                'email': post['email'],
                'login': post['email'],
                }
                
                for in_group in in_groups:
                        value[in_group]=True;
                if post.has_key('image'):
                    value['image']=post['image'];
                user_id=res_users_obj.search(cr,
                            SUPERUSER_ID,
                            [('login','=',post['email'])],
                            context=context);
                if (len(user_id)==0):
                    user_id = res_users_obj.create(cr, 
                                                    SUPERUSER_ID, 
                                                    value, 
                                                    context=context)
                    data_entidad=self.mi_entidad(uid)
                    if data_entidad['entidad_id']:
                        user_ids=data_entidad['user_ids']
                        user_ids.append(user_id)
                        entidades_obj = registry['ept_ent.entidades']
                        entidades_obj.write(
                                            cr,
                                            SUPERUSER_ID,
                                            data_entidad['entidad_id'],
                                            {'user_ids': [[6, False, user_ids]]},
                                            context)
                else:
                    ret =  {'modal':{
                            'titulo':'<strong>Error al crear el usuario.</strong>',
                            'cuerpo':'''<h1 class="text-danger" >
                                        El Usuario %s con correo
                                        %s ya existe.</h1>
                                        ''' % (post['name'],post['email']),
                                    },
                            }
                    return ret
            else:
                ret={'error_campos':errors}
                return ret
            ret={'redirect':'/usuarios'}
            return ret
            
    @http.route(
        ['/mi_entidad'], 
        type='json', auth="user", website=True)
    def mi_entidad(self,uids):
        if isinstance(uids, (int, long)):
            uids = [uids]
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        ret={}
        entidades_obj = registry['jpv_ent.entidades']
        entidades_ids = entidades_obj.search(
                                        cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uids)],
                                        context=context)
        entidades_data = entidades_obj.browse(
                                        cr,
                                        SUPERUSER_ID,
                                        entidades_ids,
                                        context=context)
        entidad_id=0
        if len(entidades_ids)==1:
            entidad_id=entidades_ids[0]
            
        user_ids=[]
        for entidad in entidades_data:
            for user in entidad.user_ids:
                user_ids.append(user.id)
        ret={'entidad_data':entidades_data,
             'entidad_id':entidad_id,
             'user_ids':user_ids}
        return ret

    @http.route(
            ['/usuario/eliminar'],
            type='json', auth='user', website=True)
    def accion_eliminar(self,**post):
        ret={}
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        res_users_obj = registry.get('res.users')
        if int(post['iduser']):
            res_users_obj.write(
                                cr,
                                SUPERUSER_ID,
                                int(post['iduser']),
                                {'active':False},
                                context)
        ret={'redirect':'/usuarios'}
        return ret



