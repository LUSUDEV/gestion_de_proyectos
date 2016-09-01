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
from datetime import datetime, date, time, timedelta
from openerp.addons.ept_rendicion.controladores.comunes import *
from openerp.addons.ept_rendicion.controladores.ept_rnd_rendicion_c import *
from openerp import SUPERUSER_ID



class ept_rnd_cancelacion_proyecto(osv.osv):
    _name='ept_rnd.cancelacion_proyecto'
    _columns = {
                    
            
        'proyecto_id':fields.many2one(
                    'ept_cp.carga_proyecto',
                    'Proyecto',help="Proyecto",
                    ondelete="cascade"
                    ),
        
                    
        'razon':fields.char('Razon por la que cancela el Proyecto'),
        
        'movimiento_id':fields.many2one('ept.movimientos_cuentas','Movimiento')
    }


    def create(self, cr, uid, values, context=None):
        proyecto_data=self.pool.get('ept_cp.carga_proyecto').browse(cr,uid,values['proyecto_id'])
        cancelar=rendicion().cancelar_proyecto_get(proyecto_data.id)
        if not cancelar:
            raise osv.except_osv(
                    ('Error!'),
                    (u'Este Proyecto no se puede cancelar, el avance financiero ha superado el 10% '))
        if not proyecto_data.state == 'cancelado':
            write_state_proyecto=self.pool.get('ept_cp.carga_proyecto').write(cr,
                                                                uid,
                                                                values['proyecto_id'],
                                                                {'state':'cancelado'},0)

            cancel_id=super(ept_rnd_cancelacion_proyecto,self).create(cr,uid,values)
            cancel_data=self.browse(cr,uid,cancel_id)
            monto=cancel_data.proyecto_id.monto_proyecto
            accion='Cancelacion de Proyecto'
            descripcion=cancel_data.proyecto_id.correlativo
            obj_mov_cuentas=self.pool.get('ept.movimientos_cuentas')
            cuenta_id=cancel_data.proyecto_id.cuenta_id.id
            abono_a_cuenta_id=obj_mov_cuentas.movimiento_ingreso(cr,uid,cuenta_id,
                                                                        monto,accion,descripcion,
                                                                        'ept_cp.carga_proyecto',cancel_data.proyecto_id.id,
                                                                        cancel_data.proyecto_id.periodo_id.id,
                                                                        cancel_data.proyecto_id.partner_id.id,
                                                                        cancel_data.proyecto_id.proyect_mantenimiento,
                                                                        monto)
                                                                        
            write_cancel=self.write(cr,uid,cancel_id,{'movimiento_id':abono_a_cuenta_id['movimiento_id_ingreso']})
            if cancel_data.proyecto_id.proyect_mantenimiento:
                                monto_rest_mant=cancel_data.proyecto_id.monto_tomado_mantenimiento - abono_a_cuenta_id['monto_disponible_mantenimiento_ingreso']
                                write_monto_mantenimiento=self.pool.get('ept_cp.carga_proyecto').write(cr,
                                                                    SUPERUSER_ID,
                                                                    cancel_data.proyecto_id.id,
                                                                    {'monto_tomado_mantenimiento':monto_rest_mant},0)
            self.registro_solicitud_firma_carta_cancelacion_proyecto(cr,uid,cancel_data.proyecto_id,cancel_data)
            if write_state_proyecto:
                historial_proyecto_obj=self.pool.get('ept_cp.historial_proyecto')
                historial={
                'proyecto_id':proyecto_data.id,
                'descripcion':'Usted ha cancelado el proyecto '+proyecto_data.correlativo
                }
                historial_proyecto_obj.create(cr,uid,historial)
            return cancel_id
        else:
            raise osv.except_osv(
                    ('Error!'),
                    (u'Este Proyecto ya esta Cancelado'))
            
    
    def registro_solicitud_firma_carta_cancelacion_proyecto(self,cr,uid,proyecto,cancel_data):
        correlativo_carta=self.pool.get('ir.sequence').get(cr,uid,
                                                    'ept_fir.cartas_x_firmar'),
        nombre_file=proyecto.partner_id.name+'_cancelacionproyecto#'
        referencia='referencia'
        list_datos_adicionales=[]
        list_datos_adicionales.append([0,False,{'objeto_ratro':'ept_cp.carga_proyecto', 'objeto_ratro_id':proyecto.id, 'referncia':referencia,}])
        value_x_firmar={
            'correlativo':correlativo_carta[0],
            'tipo_cartas':'cancelación',
            'mensaje':'Su proyecto fue cancelado',
            'referencia':proyecto.partner_id.name+', Carta por cancelacion de proyecto '+proyecto.correlativo,
            'state':'porfirmar',
            'metodo':'carga_carta_cancelacion_proyecto',
            'objeto_ratro_principal':'ept_rnd.cancelacion_proyecto',
            'objeto_principal_id':cancel_data.id,
            'objeto_rastro_ids':'ept_cp.carga_proyecto',
            'metodoGenerarCartas':'crear_carta_cancelacion_proyecto',
            'nombre_file':nombre_file,
            'objeto_rastro_ids':list_datos_adicionales,
            }
        cartas_x_firmar_obj = self.pool.get('ept_fir.cartas_x_firmar')
        cartas_x_firmar_id=cartas_x_firmar_obj.create(cr,uid,value_x_firmar)
        return True

    def crear_carta_cancelacion_proyecto(self,cr,uid,cartaxfirmar_data,context=None):
        reportname='ept_rendicion.cancelacion_proyecto_qweb' 
        proyecto_data=self.pool.get(cartaxfirmar_data.objeto_rastro_ids.objeto_ratro).browse(cr,uid,cartaxfirmar_data.objeto_rastro_ids.objeto_ratro_id) 
        hoy=date.today().strftime("%d-%m-%Y") 
        entidades_obj = self.pool.get('ept_ent.entidades')
        entidades_id=entidades_obj.search(cr,uid,[('parent_id','=',proyecto_data.partner_id.id)])
        entidades_data=entidades_obj.browse(cr,uid,entidades_id) 
        entidad=entidades_data['parent_id']['name'] 
        if entidades_data['tipo_entidad_id'].name=='ALCALDÍA':
            titulo='Alcalde (sa)'
        elif entidades_data['tipo_entidad_id'].name=='GOBERNACIÓN':
            titulo='Gobernador (a)'
        else:
            titulo='Alcalde (sa) Mayor'
        
        for user in entidades_data['user_ids']:
            for group in user.groups_id:
                if group.name=='Alcaldes, Gobernadores o Alcalde Mayor':
                    nombre=user.name
        valores={
                'correlativo':cartaxfirmar_data.correlativo,
                'proyecto_data':proyecto_data,
                'hoy':hoy,
                'nombre':nombre,
                'titulo':titulo,
                'entidad':entidad,
                'get_monto':self.get_monto,
                }
        carta_data = request.registry['report'].get_pdf(cr, uid, [], reportname, data=valores, context=context)
        return carta_data
        
    def get_monto(self,monto):
        monto='{:,.2f}'.format(monto)
        monto=str(monto)
        monto=monto.replace('.',' ')
        monto=monto.replace(',','.')
        monto=monto.replace(' ',',')
        return monto
        
        
    def carga_carta_cancelacion_proyecto(self,cr,uid,carta_data,file_name,file_data,context):
        ir_attachment_obj=self.pool.get('ir.attachment')
        cartas_x_firmar_obj=self.pool.get('ept_fir.cartas_x_firmar')
        cp_historial_obj=self.pool.get('ept_cp.historial_proyecto')
        entidades_obj=self.pool.get('ept_ent.entidades')
        users_obj=self.pool.get('res.users')
        mail_message_obj=self.pool.get('mail.message')
        print 'ksksksksksks'
        print 'ksksksksksks'
        print 'ksksksksksks'
        print 'ksksksksksks'
        for i in carta_data:
            cancel_id=carta_data.objeto_principal_id
            cancelacion_id=self.pool.get('ept_rnd.cancelacion_proyecto').search(cr,uid,[('id','=',cancel_id)])
            if not len(cancelacion_id):
                cancelacion_id=self.pool.get('ept_rnd.cancelacion_proyecto').search(cr,uid,[('proyecto_id','=',cancel_id)])
                write_id_obj=self.pool.get(carta_data._name).write(cr,uid,carta_data.id,{'objeto_principal_id':cancelacion_id[0]})
            cancel_id=cancelacion_id
            cancel_data=self.pool.get('ept_rnd.cancelacion_proyecto').browse(cr,uid,cancel_id)
        proyecto_data=cancel_data.proyecto_id
        partner_id=proyecto_data.partner_id
        entidades_ids=entidades_obj.search(cr,uid,[('parent_id','=',int(partner_id))])
        entidades_data=entidades_obj.browse(cr,uid,entidades_ids)
        usuarios_ids=[]
        for usuarios in entidades_data['user_ids']:
            usuarios_ids.append(int(usuarios))
        users_ids=users_obj.search(cr,uid,[('id','in',usuarios_ids)])
        users_data=users_obj.browse(cr,uid,users_ids)
        partner_ids=[]
        for users in users_data:
            partner_ids.append(int(users['partner_id']))
        attachment_id = ir_attachment_obj.create(cr,uid,{
            'name': file_name,
            'datas': file_data,
            'datas_fname': file_name,
            'res_model':'ept_cp.carga_proyecto',
            'res_id': int(proyecto_data.id),
            'proyecto_carta_id': int(proyecto_data.id),
            'description':'Carta por cancelación del proyecto '+str(proyecto_data['correlativo'])
            }, context)
        cartas_x_firmar_obj.write(
                                cr,
                                uid,
                                carta_data.id,
                                {'attachment_id':attachment_id,
                                'state':'firmado'},
                                context)
        ctx={
                'mail_post_autofollow_partner_ids': [], 
                'default_model': 'ept_ent.entidades', 
                'default_res_id':entidades_ids[0], 
                'mail_read_set_read': True, 
                'mail_post_autofollow': True}
        values={
            'body': 'Cancelación de Proyecto', 
            'model': 'ept_ent.entidades', 
            'attachment_ids': [(4, attachment_id)], 
            'res_id': entidades_ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, partner_ids]], 
            'subject': False}
        mail_message_obj.create(cr,uid,values,context=ctx)
