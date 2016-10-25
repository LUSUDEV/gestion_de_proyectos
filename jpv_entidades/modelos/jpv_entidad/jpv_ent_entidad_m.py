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
#    Modulo Desarrollado por Juventud Productiva (Victor Davíla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.http import request
from openerp import SUPERUSER_ID
#~ from openerp.addons.jpv_rendicion.controladores.jpv_rnd_rendicion_c import rendicion

class user(osv.osv):
    _name = 'res.users'
    _inherit="res.users"

    _columns = {
        'entidades_ids': fields.many2many(
                    'jpv_ent.entidades',
                    'jpv_ent_entidad_user_rel',
                    'entidad_user_id',
                    'entidad_id',
                    'Equipo de la Entidad',
                    ),
    }

class partner(osv.osv):
    _name = 'res.partner'
    _inherit="res.partner"

    _columns = {
        'cis_entidad': fields.boolean(
                    'Entidad'
                    ),
        'codigo_onapre': fields.char('Código Onapre',
                    size=15,
                    help='Código de la ONAPRE',
                    ),
        'rif': fields.char(
                    'RIF',
                    size=15,
                    required=True,
                    help='Número del R.I.F. de la Entidad'
                    ),
    }
    _sql_constraints = [
        (   'rif_uniq',
            'unique (rif)',
            'El Numero de RIF ya existe en la Base de Datos'),
    ]


class jpv_ent_entidades(osv.osv):
    _name = 'jpv_ent.entidades'
    _inherits = {'res.partner': 'parent_id'}
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Registro de las Entidades del Consejo Federal de Gobierno"
    _rec_name= "parent_id"

    groups_id=[]
    def __init__(self, pool, cr):
        init_res = super(jpv_ent_entidades, self).__init__(pool, cr)
        names_category="c.name = 'ROLES DE LAS ENTIDADES POLITICO TERRITORIALES'"
        cr.execute("select g.id from res_groups as g,"\
                    "ir_module_category as c "\
                    "where  %s  "\
                    "and g.category_id=c.id;" % (names_category));
        res_groups_ids=cr.fetchall()
        for group in res_groups_ids:
            self.groups_id.append(group[0])
        return init_res


    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image1)) for p in self)
        
    @api.multi
    def get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image1)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image1': tools.image_resize_image_big(value)})

    @api.multi
    def _has_image(self, name, args):
        return dict((p.id, bool(p.image1)) for p in self)

    def _default_venezuela(self,cr,uid,ids,context=None):
        country_obj=self.pool.get('res.country')
        country_id=country_obj.search(  cr,
                                        uid,
                                        [('name','=','Venezuela')],
                                        context=context)
        return country_id[0]

    #~ def validar_roles(self, cr, uid, ids, context=None):
        #~ res_users_obj=self.pool.get('res.users')
        #~ res_entidad_obj=self.pool.get('res.partner')
        #~ arreg = []
        #~ res=[]
        #~ usuarios_ids=[]
        #~ for entidad in self.browse(cr,uid,ids):
            #~ for usuarios in entidad.user_ids:
                #~ usuarios_ids.append(usuarios.id)
                #~ for grupos in usuarios.groups_id:
                    #~ arreg.append(grupos.name)
                    #~ if (grupos.name=='Alcaldes, Gobernadores o Alcalde Mayor' \
                                        #~ and arreg.count(grupos.name)!=1):
                        #~ raise osv.excjpv_osv(('Error !'),
                            #~ ('haz seleccionado dos veces %s' % (grupos.name)))
                    #~ if (grupos.name == 'Secretario' \
                                        #~ and arreg.count(grupos.name)!=1):
                        #~ raise osv.excjpv_osv(('Error !'),
                            #~ ('haz seleccionado dos veces %s' % (grupos.name)))
        #~ res=tuple()
        #~ usuarios_ids=tuple(usuarios_ids)
        #~ if arreg:
            #~ if len(usuarios_ids)==1:
                #~ for usuario_sel in usuarios_ids:
                    #~ usuarios_ids=usuario_sel
                #~ cr.execute('SELECT rel.entidad_id,rel.entidad_user_id '\
                            #~ 'FROM jpv_ent_entidad_user_rel AS rel '\
                            #~ 'WHERE rel.entidad_user_id = %s and ' \
                            #~ 'rel.entidad_id <> %s ;' \
                            #~ % (str(usuarios_ids),ids[0])),
            #~ else:
                #~ cr.execute('SELECT rel.entidad_id,rel.entidad_user_id '\
                            #~ 'FROM jpv_ent_entidad_user_rel AS rel '\
                            #~ 'WHERE rel.entidad_user_id IN %s and ' \
                            #~ 'rel.entidad_id <> %s ;' \
                            #~ % (str(usuarios_ids),ids[0])),
            #~ res = cr.fetchall()
            #~ mensaje=''
            #~ if len(res)>0:
                #~ for e in res:
                    #~ res_entidad_ids=self.search(cr,uid,[('id','=',e[0])])
                    #~ res_entidad_datos=self.browse(cr,uid,res_entidad_ids).name
                    #~ res_users_ids=res_users_obj.search(cr,uid,[('id','=',e[1])])
                    #~ res_users_datos=res_users_obj.browse(cr,uid,res_users_ids).name
                    #~ mensaje=mensaje+' el USUARIO: ' \
                                #~ +res_users_datos \
                                #~ +u' el cual pertence a la ENTIDAD : ' \
                                #~ +res_entidad_datos
                #~ raise osv.excjpv_osv(('Error !'),
                        #~ ('Ha seleccionado %s Verificar Gracias!!!' % (mensaje)))
        #~ return True

    def _get_attachment_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            res[app_id] = self.pool['ir.attachment'].search_count(
                                            cr,
                                            uid,
                                            [('res_model', '=', 'jpv_ent.entidades'), ('res_id', '=', app_id)],
                                            context=context)
        return res

    def _get_comunicaciones_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [('partner_id', '=', entidad_data.parent_id.id)],
                                            context=context)
        return res
        
    def _get_comunicaciones_proceso_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('partner_id', '=', entidad_data.parent_id.id),
                                                ('state', '=', 'proceso'),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_procesadas_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('partner_id', '=', entidad_data.parent_id.id),
                                                ('state', '=', 'procesado'),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_leidas_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('partner_id', '=', entidad_data.parent_id.id),
                                                ('state', '=', 'leido'),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_enviada_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('partner_id', '=', entidad_data.parent_id.id),
                                                ('state', '=', 'enviado'),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_sinrespuesta_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('partner_id', '=', entidad_data.parent_id.id),
                                                ('state', '=', 'sinrespuesta'),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_cfg_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            res[app_id] = self.pool['jpv_com.comunicaciones_masivas'].search_count(
                                            cr,
                                            uid,
                                            [
                                                ('pertner_ids', 'in', [entidad_data.parent_id.id]),
                                                ('state', 'in', ['enviado','leidos']),
                                                ],
                                            context=context)
        return res
        
    def _get_comunicaciones_fcg_enviada_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            comunicaciones_obj=self.pool['jpv_com.comunicaciones_masivas']
            comunicaciones_ids=comunicaciones_obj.search(
                                            cr,
                                            uid,
                                            [
                                                ('pertner_ids', 'in', [entidad_data.parent_id.id]),
                                                ('state', '=', 'enviado')
                                                
                                                ],
                                            context=context)
            comunicaciones_data=comunicaciones_obj.browse(cr,uid,comunicaciones_ids)
            cantidad=len(comunicaciones_ids)
            for comunicacion in comunicaciones_data:
                leida=False
                for leidas in comunicacion.partner_leidos_ids:
                    if leidas.pertner_id.id==entidad_data.parent_id.id:
                        leida=True
                if leida:
                    cantidad-=1
            
            res[app_id] = cantidad
        return res

    def _get_comunicaciones_fcg_leidas_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            entidad_data=self.browse(cr,uid,[app_id])[0]
            comunicaciones_obj=self.pool['jpv_com.comunicaciones_masivas']
            comunicaciones_ids=comunicaciones_obj.search(
                                            cr,
                                            uid,
                                            [
                                                ('pertner_ids', 'in', [entidad_data.parent_id.id]),
                                                ('state', 'in', ['enviado','leidos'])
                                                ],
                                            context=context)
            comunicaciones_data=comunicaciones_obj.browse(cr,uid,comunicaciones_ids)
            cantidad=0
            for comunicacion in comunicaciones_data:
                leida=False
                for leidas in comunicacion.partner_leidos_ids:
                    if leidas.pertner_id.id==entidad_data.parent_id.id:
                        leida=True
                if leida:
                    cantidad+=1
            
            res[app_id] = cantidad
        return res

    def _get_rendicion_proyectos(self, cr, uid, ids, fields, args, context=None):
        res={}
        user_ids=self.search(cr,uid,[('user_ids','in',uid)])
        entidad_data=self.browse(cr,uid,ids)
        for entidad in entidad_data:
            if entidad.id in user_ids :
                proyectos_rendicion_data=rendicion().proyectos_x_rendir_erp({'entidad_id':entidad.parent_id})
                proyectos_aprobados=proyectos_rendicion_data['proyectos_aprobados']
                proyectos_x_rendir=proyectos_rendicion_data['cant_proyectosXRendir']
                proyectos_actualizados=proyectos_rendicion_data['cant_proyectos_actualizados']
                if fields == 'proyectos_aprobados':
                    res[entidad.id]=proyectos_aprobados
                if fields == 'porc_proyectos_x_rendir':
                    res[entidad.id]=proyectos_x_rendir*100/proyectos_aprobados
                if fields == 'porc_proyectos_actualizados':
                    res[entidad.id]=proyectos_actualizados*100/proyectos_aprobados
                if fields == 'proyectos_x_rendir':
                    res[entidad.id]=proyectos_x_rendir
                if fields == 'proyectos_actualizados':
                    res[entidad.id]=proyectos_actualizados
            else:
                res[entidad.id]=0
        return res

    _columns = {
        'parent_id':fields.many2one(
                    'res.partner',
                    'Registro de la Entidad',
                    required=True,
                    ondelete='cascade'
                    ),
        'image1': fields.binary(
                    "Image",
                    help="Este campo contiene la imagen utilizada como avatar\
                    para este contacto , limitado a 1024x1024px"),
        'image_medium': fields.function(
                    _get_image, fnct_inv=_set_image,
                    string="Medium-sized image",
                    type="binary",
                    multi="_get_image",
                    store={
                        'jpv_ent.entidades':
                        (lambda self, cr, uid, ids, c={}: ids, ['image1'], 10),
                        },),
        'image_small': fields.function(
                    _get_image, fnct_inv=_set_image,
                    string="Small-sized image",
                    type="binary",
                    multi="_get_image",
                    store={
                        'jpv_ent.entidades':
                        (lambda self, cr, uid, ids, c={}: ids, ['image1'], 10),
            },),
        'has_image': fields.function(_has_image, type="boolean"),
        #~ 'monto_disp_mantenimiento':fields.float(
                    #~ 'Monto Disponible Mantenimiento',
                     #~ readonly=True,
                     #~ help='Monto que le queda Disponible en la cuenta para \
                     #~ mantenimiento'),
        'ip':fields.char(
                    'IP',
                     size=15,
                     help='ip del cliente de la petición'),

        'tipo_entidad_id':fields.many2one(
                    'jpv_ent.tipo_entidades',
                    'Tipo de Entidad',
                    required=True,
                    help='Tipo de Entidad'),

        'entidades_ids': fields.many2many(
                    'jpv_ent.entidades',
                    'jpv_ent_rel_gob_alcaldias',
                    'gobernacion_id',
                    'alcaldias_id',
                    'Alcaldías de la Gobernación',
                    ),

        'user_ids': fields.many2many(
                    'res.users',
                    'jpv_ent_entidad_user_rel',
                    'entidad_id',
                    'entidad_user_id',
                    'Equipo de la Entidad',
                    domain=[('groups_id', 'in',groups_id)],
                    context={'default_groups_id':groups_id,
                             'only_groups_id':groups_id,},
                    ),

        'redi_ids':fields.many2many(
                    'jpv_ent.redis',
                    'jpv_ent_relacion_ent_redi',
                    'entidad_id',
                    'redi_id',
                    'Relacion REDI'
                    ),

        'estado_ids':fields.many2many(
                    'jpv_ent.estados',
                    'jpv_ent_relacion_ent_estados',
                    'entidad_id',
                    'estados_id',
                    'Relacion Estados'
                    ),

        'municipio_ids':fields.many2many(
                    'jpv_ent.municipios',
                    'jpv_ent_relacion_ent_municipios',
                    'entidad_id',
                    'municipios_id',
                    'Relacion Municipios'
                    ),

        'parroquia_ids':fields.many2many(
                    'jpv_ent.parroquias',
                    'jpv_ent_relacion_ent_parroquias',
                    'entidad_id',
                    'parroquias_id',
                    'Relacion Parroquias'
                    ),

        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),

        'editar': fields.boolean(
                            'Editar Campos Rentringidos',
                            help='''Si este campo esta habilitado,
                                    permite editar campos:
                                    '''),
        #~ 'cargar_proyectos': fields.boolean(
                            #~ 'Cargar Proyectos',
                            #~ help='''Si este campo esta habilitado,
                                    #~ permite que la entidad pueda cargar
                                    #~ proyectos
                                    #~ '''),
        #~ 'attachment_number': fields.function(
                                    #~ _get_attachment_number,
                                    #~ string='Number of Attachments',
                                    #~ type="integer"),

        #~ 'comunicaciones_number': fields.function(
                                    #~ _get_comunicaciones_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
                                    
        #~ 'comunicaciones_proceso_number': fields.function(
                                    #~ _get_comunicaciones_proceso_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
                                    
        #~ 'comunicaciones_procesadas_number': fields.function(
                                    #~ _get_comunicaciones_procesadas_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
        #~ 'comunicaciones_enviada_number': fields.function(
                                    #~ _get_comunicaciones_enviada_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
                                    
        #~ 'comunicaciones_leidas_number': fields.function(
                                    #~ _get_comunicaciones_leidas_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
                                    
        #~ 'comunicaciones_sinrespuesta_number': fields.function(
                                    #~ _get_comunicaciones_sinrespuesta_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
        #~ 'comunicaciones_cfg_number': fields.function(
                                    #~ _get_comunicaciones_cfg_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
        #~ 'comunicaciones_fcg_enviada_number': fields.function(
                                    #~ _get_comunicaciones_fcg_enviada_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
        #~ 'comunicaciones_fcg_leidas_number': fields.function(
                                    #~ _get_comunicaciones_fcg_leidas_number,
                                    #~ string='Número de Comunicaciones',
                                    #~ type="integer"),
        #~ 'proyectos_aprobados': fields.function(
                                    #~ _get_rendicion_proyectos,
                                    #~ string='Número de Proyectos Aprobados',
                                    #~ type="integer"),
        #~ 'proyectos_x_rendir': fields.function(
                                    #~ _get_rendicion_proyectos,
                                    #~ string='Número de Proyectos por rendir',
                                    #~ type="integer"),
        #~ 'proyectos_actualizados': fields.function(
                                    #~ _get_rendicion_proyectos,
                                    #~ string='Número de Proyectos Actualizados',
                                    #~ type="integer"),
        #~ 'porc_proyectos_x_rendir': fields.function(
                                    #~ _get_rendicion_proyectos,
                                    #~ string='Número de Proyectos por rendir',
                                    #~ type="integer"),
        #~ 'porc_proyectos_actualizados': fields.function(
                                    #~ _get_rendicion_proyectos,
                                    #~ string='Número de Proyectos Actualizados',
                                    #~ type="integer"),
    }
    _defaults = {
        'active':True,
        'editar':True,
        #~ 'monto_disp_mantenimiento':0.00,
        'country_id':_default_venezuela,
        'is_company': True,
        'cis_entidad':True,
        'ip':lambda self,cr,uid,context: request.httprequest.remote_addr
    }

    #~ _constraints = [
        #~ (validar_roles, ' ', ['user_ids']),
    #~ ]

    def open_map(self, cr, uid, ids, context=None):
        partner_obj= self.pool.get('res.partner')
        parnert_id=self.browse(cr,uid,ids)
        return partner_obj.open_map(cr,uid,parnert_id.parent_id.id,context)

    @api.multi
    def onchange_type(self, is_company):
        value = {'title': False}
        if is_company:
            value['use_parent_address'] = False
            domain = {'title': [('domain', '=', 'partner')]}
        else:
            domain = {'title': [('domain', '=', 'contact')]}
        return {'value': value, 'domain': domain}

    def limpiar_campos(self,cr,uid,ids,nombre,context=None):
        return self.pool.get('res.partner').limpiar_campos(cr,uid,ids,nombre,context=context)

    def limpiar_campos_ra(self,cr,uid,ids,nombre,context=None):
        res={}
        if nombre=='redi':
            res={
            'estado_ids':'',
            'municipio_ids':'',
            'parroquia_ids':'',

                }
        if nombre=='estado':
            res={
            'municipio_ids':'',
            'parroquia_ids':'',
                }
        if nombre=='municipio':
            res={
            'parroquia_ids':'',
                }
        return {
         'value':res
            }

    #~ def action_get_attachment_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'action_attachment')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ action['context'] = {'default_res_model': self._name, 'default_res_id': ids[0]}
        #~ action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', ids)])
        #~ return action
    #~ inicio acciones de las comunicaciones de las jpv al FCI
    #~ def action_get_comunicaciones_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id)])
        #~ return action
        
    #~ def action_get_comunicacionesSinRespuesta_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id),('state', '=', 'sinrespuesta')])
        #~ return action
        
    #~ def action_get_comunicacionesEnviadas_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id),('state', '=', 'enviado')])
        #~ return action
    #~ def action_get_comunicacionesLeido_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id),('state', '=', 'leido')])
        #~ return action
    #~ def action_get_comunicacionesProcesado_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id),('state', '=', 'procesado')])
        #~ return action
    #~ def action_get_comunicacionesProceso_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('partner_id', '=', entidad_data.parent_id.id),('state', '=', 'proceso')])
        #~ return action
    #~ fin de las aciones de las comunicaciones de las jpv al FCI
    #~ inicio de las acciones de las comunicaciones del FCI a las jpv
    
    #~ def action_get_comunicacionesMasivas_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_masivas_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ action['domain'] = str([('pertner_ids', 'in', [entidad_data.parent_id.id]),('state', 'in', ['enviado','leidos'])])
        #~ return action
        
    #~ def action_get_comunicacionesMasivasEnviadas_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_masivas_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ comunicaciones_obj=self.pool['jpv_com.comunicaciones_masivas']
        #~ comunicaciones_ids=comunicaciones_obj.search(
                                        #~ cr,
                                        #~ uid,
                                        #~ [
                                            #~ ('pertner_ids', 'in', [entidad_data.parent_id.id]),
                                            #~ ('state', '=','enviado')
                                            #~ ],
                                        #~ context=context)
        #~ comunicaciones_data=comunicaciones_obj.browse(cr,uid,comunicaciones_ids)
        #~ comunicacionesMasivas_ids=[]
        #~ for comunicacion in comunicaciones_data:
            #~ leida=False
            #~ for leidas in comunicacion.partner_leidos_ids:
                #~ if leidas.pertner_id.id==entidad_data.parent_id.id:
                    #~ leida=True
            #~ if not leida:
                #~ comunicacionesMasivas_ids.append(comunicacion.id)
        #~ action['domain'] = str([('id', 'in', comunicacionesMasivas_ids)])
        #~ return action
        
    #~ def action_get_comunicacionesMasivasLeidas_tree_view(self, cr, uid, ids, context=None):
        #~ model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jpv_comunicaciones', 'jpv_com_comunicaciones_masivas_action')
        #~ action = self.pool.get(model).read(cr, uid, action_id, context=context)
        #~ entidad_data=self.browse(cr,uid,ids)[0]
        #~ comunicaciones_obj=self.pool['jpv_com.comunicaciones_masivas']
        #~ comunicaciones_ids=comunicaciones_obj.search(
                                        #~ cr,
                                        #~ uid,
                                        #~ [
                                            #~ ('pertner_ids', 'in', [entidad_data.parent_id.id]),
                                            #~ ('state', 'in',['enviado','leidos'])
                                            #~ ],
                                        #~ context=context)
        #~ comunicaciones_data=comunicaciones_obj.browse(cr,uid,comunicaciones_ids)
        #~ comunicacionesMasivas_ids=[]
        #~ for comunicacion in comunicaciones_data:
            #~ leida=False
            #~ for leidas in comunicacion.partner_leidos_ids:
                #~ if leidas.pertner_id.id==entidad_data.parent_id.id:
                    #~ leida=True
            #~ if leida:
                #~ comunicacionesMasivas_ids.append(comunicacion.id)
        #~ action['domain'] = str([('id', 'in', comunicacionesMasivas_ids)])
        #~ return action
        
     #~ fin de las acciones de las comunicaciones del FCI a las jpv
     
    def create(self,cr,uid,values,context=None):
        values.update({
            'editar':False,
            'image':values['image1'],
                    })
        return super(jpv_ent_entidades,self).create(
                                                    cr,
                                                    uid,
                                                    values,
                                                    context=context)

    @api.multi
    def write(self, vals):
        vals['editar']=False
        entidad_id = super(jpv_ent_entidades, self).write(vals)
        return entidad_id
            
