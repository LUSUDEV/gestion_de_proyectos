# -*- coding: utf-8 -*-

from openerp.http import request
from openerp import http,tools, api,SUPERUSER_ID
import werkzeug.utils
import werkzeug.wrappers
from openerp.osv import osv
from openerp import http


#~ este metodo recibe los nombre del grupo y las categoria 
#~ que no desea y devuelve los ids con sus nobres y los ids 
def groups_category(group_name,not_category_name=None):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        
        category_obj = registry['ir.module.category']
        groups_obj = registry['res.groups']
        
        if not not_category_name:
            not_category_name={}
            
        category_ids = category_obj.search(
                            cr,
                            SUPERUSER_ID,
                            [('name','in',group_name)],
                            context=context)
        groups_ids = groups_obj.search(
                        cr,
                        SUPERUSER_ID,
                        [('category_id','in',category_ids)],
                        context=context)
        groups_data = groups_obj.browse(
                                        cr,
                                        SUPERUSER_ID,
                                        groups_ids,
                                        context=context)
        groups=[]
        group_ids=[]
        for group in groups_data:
            if not (group.name in  not_category_name):
                groups.append((group.id,group.name))
                group_ids.append(group.id)
                
        return {'groups':groups,'group_ids':group_ids}

#~ este metodo en para controlar la contidad de grupos por categoria de un conjunto
#~ de usuarios.
#~ recibe los siguientes parametros:
#~ el nombre de la categoria category_name=['name1','name2',...],
#~ la cantidad maxima con el nombre control_groups_name=[(2,'name_group'),(4,'name_group'),..]
#~ los ids de los usuarios user_ids=[25,27,29,64]
#~ los nombres de los grupos que no quiero que tome en cuenta not_groups_name=['group_name',..]
#~ devuelve una dicionario con los grupos filtrados

def control_groups_name(category_name,control_groups_name,user_ids,not_groups_name=None):
    if not not_groups_name:
        not_groups_name={}
    registry = http.request.registry
    cr=http.request.cr
    uid=http.request.uid
    context = http.request.context
    res_users_obj = registry.get('res.users')
    groups=groups_category(category_name,not_groups_name)
    res_users_data=res_users_obj.browse(cr,SUPERUSER_ID,user_ids)
    groups_ids=[]
    for user in res_users_data:
        for group in user.groups_id:
            groups_ids.append(group.id)
    for control in control_groups_name:
        for group in groups['groups']:
            cont=0
            if group[1]==control[1]:
                for group_id in groups_ids:
                    if group[0]==group_id:
                        cont+=1
            if cont>=control[0]:
                index=groups['groups'].index(group)
                groups['groups'].pop(index)
                                
    return {'groups':groups['groups']}


LOGIN='/web/login?inactivo=True'
def users_active(user_id):
    print user_id
    registry = http.request.registry
    cr=http.request.cr
    uid=http.request.uid
    context = http.request.context
    res_users_obj = registry.get('res.users')
    res_users_data = res_users_obj.browse(
                            cr,
                            SUPERUSER_ID,
                            [user_id])
    return res_users_data.activo
    
    
