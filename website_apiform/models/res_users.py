# -*- coding: utf-8 -*-
##############################################################################
#
# 
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

from openerp.osv import osv, fields
from openerp.addons.website_apiform.controladores import panel, base_tools

############################################################################
#    Esta clase tiene como finalidad filtrar lo grupos de roles en la vita 
#   view_user_simple_form para controlar los grupos que se le desee colocar 
#   a los mismos en un determinado formulario. 
#   Cuando se haga una relación a res.users en cualquier objeto y se desee 
#   ristringir soló para ciertos grupos... usted debe pasarle por el context
#   la siguiente clave "only_groups_id" con los id o ids que desea controlar. 

# comento los siguientes metodos:
#      
#      adicionar_groups_id => este metodo nos devuelve los ids de los grupos 
#                         pasandole una lista con los nombre del grupo
#                         
#         raise_groups_id: este metodo genera el mensaje de para que el usuario 
#                         sepa cuales son los grupos prmetidos.
#                        
#        default_groups_id: Con este metodo le adiciono a la diccionario vals
#                          vals['groups_id'][0][2].append(group) los grupos
#                          seleccionado y permitidos.
#                          
#        create y write: es donde filamente verifico si cuando registren o 
#                     modifiquen a un usuario tiene una condicion de grupos de 
#                    permisos permitidos.
#                    
#    Como usarlo: 
#         
#             1) en la clase en su .py declare e inicialice una lista global 
#              groups_id=[]
#               
#           2) luego cree este metodo:

                   #def default_groups(self,cr,uid,name_rols,context=None):
                       #res_groups_obj=self.pool.get('res.groups')
                            #res_groups_ids=res_groups_obj.search(cr,uid,[
                                                                    #('name',
                                                                  #'in',
                                                                   #name_rols)
                                                                   #])
                            #for group in res_groups_ids:
                                 #self.groups_id.append(group)
                            #return self.groups_id
                            
                #3) su constructor de la clase 'def __init__(self,..)' 
               
                         #def __init__(self, pool, cr):
                            #init_res = super(ept_ure_ures, self).__init__(pool,
                                                                            #cr)
                            #name_rols=['Coordinación General UREs']
                            #groups_id=self.default_groups(
                                                            #cr,
                                                            #SUPERUSER_ID,
                                                            #name_rols)
                            #return init_res
                            
                            
                        
                #4) Finalmente en su relación many2may.
                
                        #user_ids': fields.many2many(
                    #'res.users', 
                    #'ept_ure_relacion_ures_users', 
                    #'entidad_id', 
                    #'entidad_user_id', 
                    #'Equipo de la ure',
                    #copy=False,
                    #domain=[('groups_id', 'in',groups_id)],
                    #context={'default_groups_id':groups_id,
                             #'only_groups_id':groups_id,},
                    #),
          
############################################################################
class res_users(osv.osv):
    _name = 'res.users'
    _inherit="res.users"
    
    def buscar_groups_id(self, cr, uid,name_rols,context=None):
        res_groups_obj=self.pool.get('res.groups')
        res_groups_ids=res_groups_obj.search(cr,uid,[('name','in',name_rols)])
        return res_groups_ids
        
        
        
    def raise_groups_id(self, cr, uid, context=None):
        grupos=' '
        res_groups_obj=self.pool.get('res.groups')
        groups_data=res_groups_obj.browse(cr,uid,context['only_groups_id'])
        for groups in groups_data:
            grupos+=groups.name+' \n'
        raise osv.except_osv(('Error de asignación grupo'),
            (u'''El grupo que le esta asignando no corresponde con 
            los autorizados para esta interfaz. Por esta enterfaz soló
            puede asignarle los siguientes grupos:\n %s 
            NOTA:Si desea crear un usuario con los grupos que esta asignando,
            debe comunnicarse con el administrador. , ''' % (grupos)))
        return True

    def default_groups_id(self, cr, uid, vals, context=None):
        #~ aplicamos teoria de conjuntos de lo que ponen por defecto
        #~ y lo que el usuario selecciono...
        adicionar=self.buscar_groups_id( cr, uid,['Employee'])
        groups_id= set(vals['groups_id'][0][2])
        default_groups_id= set(context['only_groups_id'])
        union=groups_id & default_groups_id;
        diferencia1= groups_id - default_groups_id;
        diferencia2=diferencia1-set(adicionar)
        if len(diferencia2)>0:
            self.raise_groups_id(cr, uid,context)
        #~ self.raise_groups_id(cr, uid,context)
        for group in adicionar:
            if not group in vals['groups_id'][0][2]:
                vals['groups_id'][0][2].append(group)
        return vals
        
    def create(self, cr, uid, vals, context=None):
        if context.has_key('only_groups_id'):
            vals=self.default_groups_id(cr,uid,vals,context)
        user_id = super(res_users, self).create(cr, uid, vals, context=context)
        return user_id
        
    def write(self, cr, uid, ids, vals, context=None):
        if context.has_key('only_groups_id') and vals.has_key('groups_id'):
            vals=self.default_groups_id(cr,uid,vals,context=context)
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        return res
