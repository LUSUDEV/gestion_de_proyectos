# -*- coding: utf-8 -*-


##############################################################################
#   Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
##############################################################################

{
    'name': "Filtrar lo grupos de roles en la vista view_users_simple_form",
    'summary': "",
    'description':'''
         
        Este módulo tiene como finalidad filtrar lo grupos de roles en la vista
        view_users_simple_form para controlar los grupos que se le desee colocar 
        a los mismos en un determinado formulario.
        
        Cuando se haga una relación a res.users en cualquier objeto y se desee 
        ristringir soló para ciertos grupos... usted debe pasarle por el context 
        la siguiente clave "only_groups_id" con los id o ids que desea controlar. 
                    
        Como usarlo: 
         
             1) en la clase en su .py declare e inicialice una lista global 
              groups_id=[]
               
            2) luego creas este metodo:
                def default_groups(self,cr,uid,name_rols,context=None):
                       res_groups_obj=self.pool.get('res.groups')
                       res_groups_ids=res_groups_obj.search(cr,uid,[('name','in',name_rols)])
                                for group in res_groups_ids:
                                     self.groups_id.append(group)
                                return self.groups_id
                            
                3) su constructor de la clase 'def __init__(self,..)' 
               
                         def __init__(self, pool, cr):
                            init_res = super(ept_ure_ures, self).__init__(pool,
                                                                            cr)
                            name_rols=['Coordinación General UREs']
                            groups_id=self.default_groups(
                                                            cr,
                                                            SUPERUSER_ID,
                                                            name_rols)
                            return init_res
                            
                            
                        
                4) Finalmente en su relación many2may.
                
                        user_ids': fields.many2many(
                    'res.users', 
                    'ept_ure_relacion_ures_users', 
                    'entidad_id', 
                    'entidad_user_id', 
                    'Equipo de la ure',
                    copy=False,
                    domain=[('groups_id', 'in',groups_id)],
                    context={'default_groups_id':groups_id,
                             'only_groups_id':groups_id,},
                    ),
          
''',
    'author': "Juventud Productiva (Felipe Villamizar)",
    'website': "",

    'category': 'Web site',
    'version': '0.1',
    'depends': ['base','base_setup'],
    'data': [
        'vistas/res_users.xml',
        
    ],
    'demo': [
    ],
    'tests': [
    ],
}
