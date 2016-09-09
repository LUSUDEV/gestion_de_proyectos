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
#    Modulo Desarrollado por Juventud Productiva (Victor Davila)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.http import request
from datetime import date
from openerp import SUPERUSER_ID

class jpv_movimientos_cuentas(osv.osv):
    _name='jpv.movimientos_cuentas'
    _description="Registro de Movimientos de Cuentas"
    
    
    def movimiento_ingreso(self,cr,uid,cuenta_id,
                                    valor_ingreso,accion,descripcion,
                                    objeto_rastro,id_rastro,periodo_id,
                                    partner_id=None,context=None):
        
        '''Metódo que se utiliza para pasar los ingresos en movimiento
        esté metódo tiene que recibir por parametros el ID de la cuenta
        el valor a ingresar, una breve descripción el nombre del objeto 
        (el cual se obtiene pasando en los parametros en el orden que le 
        corresponde el self._name )y el ID del registro que registra el 
        movimiento (ejemplo el id del proyecto) se tienen que pasar en este
        mismo orden (cuenta_id,valor_ingreso,descripcion,objeto_rastro,id_rastro,periodo_id)
        dentro el metodo se realiza el calculo de correspondiente al ingreso
        la fecha del registro y la actualizacion del Monto Disponible'''
        valores={}
        resultado_devolver={}
        hoy=date.today()
        saldo_ids=self.search(cr,uid,[('cuenta_id','=',cuenta_id)],
                                limit=1,order="id desc")
        saldo_datos=self.browse(cr,uid,saldo_ids)
        if(valor_ingreso>0):
            resultado=saldo_datos.monto_saldo+valor_ingreso
            valores={
                'name':descripcion,
                'accion':accion,
                'cuenta_id':cuenta_id,
                'fecha_movimiento':hoy,
                'monto_ingreso':valor_ingreso,
                'monto_saldo':resultado,
                'objeto_rastro':objeto_rastro,
                'id_rastro':id_rastro,
                'periodo_id':periodo_id,
                }
            movimiento_id=self.create(cr, uid, valores, context=context)
            cuenta_obj=self.pool.get('jpv.cuentas')
            cuenta_obj.write(cr, uid, [cuenta_id], {'monto_actual': resultado})
            resultado_devolver['movimiento_id_ingreso']=movimiento_id
        else:
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'El monto Ingresado no puede ser Negativo'\
                     'Verifique o comuniquese con el administrador del sistema.'))
        return resultado_devolver

    
    def movimiento_egreso(self,cr,uid,cuenta_id,valor_egreso,accion,descripcion,
                                    objeto_rastro,id_rastro,periodo_id,
                                    partner_id=None,context=None):
        '''Metódo que se utiliza para pasar los egresos en movimiento
        esté metódo tiene que recibir por parametros el ID de la cuenta
        el valor a egresar, una breve descripción el nombre del objeto 
        (el cual se obtiene pasando en los parametros en el orden que le 
        corresponde el self._name )y el ID del registro que registra el 
        movimiento (ejemplo el id del proyecto) se tienen que pasar en este
        mismo orden (cuenta_id,valor_egreso,accion,descripcion,objeto_rastro,
        id_rastro,periodo_id) dentro el metodo se realiza el calculo de correspondiente 
        al egreso teniendo en cuenta que en el mismo se controla si el monto 
        a debitar es mayor al monto actual de igual manera se pasa 
        la fecha del registro y la actualizacion del Monto Disponible'''
        
        valores={}
        resultado_devolver={}
        hoy=date.today()
        saldo_ids=self.search(cr,uid,[('cuenta_id','=',cuenta_id)],limit=1,order="id desc")
        saldo_datos=self.browse(cr,uid,saldo_ids)
        proyecto_obj=self.pool.get('jpv_cp.carga_proyecto')
        proyecto_data=proyecto_obj.browse(cr,uid,id_rastro)
        if (valor_egreso>0):
            if saldo_datos.monto_saldo<valor_egreso:
                raise osv.excjpv_osv(
                        ('Error!'),
                        (u'El monto Ingresado (%s) no puede ser Mayor \
                         al Saldo Disponible (%s)'
                         %(valor_egreso,saldo_datos.monto_saldo)))
            resultado=saldo_datos.monto_saldo-valor_egreso
            valores={
                'name':descripcion,
                'accion':accion,
                'cuenta_id':cuenta_id,
                'fecha_movimiento':hoy,
                'monto_egreso':valor_egreso,
                'monto_saldo':resultado,
                'objeto_rastro':objeto_rastro,
                'id_rastro':id_rastro,
                'periodo_id':periodo_id,
                }
            resultado_mantenimiento_egreso=False
            movimiento_id=self.create(cr, uid, valores, context=context)
            cuenta_obj=self.pool.get('jpv.cuentas')
            cuenta_obj.write(cr, uid, [cuenta_id], {'monto_actual': resultado})
            resultado_devolver['movimiento_id_egreso']=movimiento_id
        else:
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'El monto Ingresado no puede ser Negativo'\
                     'Verifique o comuniquese con el administrador del sistema.'))

        return resultado_devolver
    
    def partner_id_tipo_cuenta_id(self,cr,uid,partner_id,
                                    tipo_cuenta_id,context=None):
        '''Con este metodo obtenemos el ID de la cuenta que posee 
        el partner Este metodo recibe por parametros (partner_id,tipo_cuenta_id)
        en ese mismo orden, de igual manera se controla si el partner elegido 
        no posee cuenta mande un error...'''
        cuenta_obj=self.pool.get('jpv.cuentas')
        cuenta_ids=cuenta_obj.search(cr,uid,
                            [('partner_id','=',partner_id),
                            ('tipo_cuenta_id','=',tipo_cuenta_id)])
        if not cuenta_ids:
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'La entidad o Institución que esta eligiendo, \
                     no poseé cuenta asociada.'))
        return cuenta_ids
    
    def consulta_saldo(self,cr,uid,partner_id,
                                    tipo_cuenta_id,context=None):
        '''Con este metodo obtenemos el Saldo Disponible de la cuenta que posee 
        el partner Este metodo recibe por parametros (partner_id,tipo_cuenta_id)
        en ese mismo orden, de igual manera se controla si el partner elegido 
        no posee cuenta mande un error...'''
        res={}
        cuenta_obj=self.pool.get('jpv.cuentas')
        cuenta_ids=cuenta_obj.search(cr,uid,
                            [('partner_id','=',partner_id),
                            ('tipo_cuenta_id','=',tipo_cuenta_id)])
        if not cuenta_ids:
            raise osv.excjpv_osv(
                    ('Error!'),
                    (u'La entidad o Institución que esta eligiendo, \
                     no poseé cuenta asociada.'))
        monto_actual=cuenta_obj.browse(cr,uid,cuenta_ids).monto_actual
        return monto_actual
    
    def consultar_movimientos(self,cr,uid,cuenta_id,fecha_inicial,
                                        fecha_final,context=None):
        '''Metodo que  se utiliza para consultar un rago de fechas seleccionadas
        donde por parametro debe pasar el ID de la cuenta la fecha desde y 
        una fecha hasta en esté mismo orden (cuenta_id,fecha_inicial,fecha_final)
        este metodo devuelve un diccionario de datos con el recorrido realizado'''
        res={}
        if (cuenta_id):
            cr.execute("SELECT rel.fecha_movimiento,rel.name,rel.accion, rel.cuenta_id,"\
                        "rel.monto_ingreso,rel.monto_egreso, rel.monto_saldo "\
                        "FROM jpv_movimientos_cuentas AS rel "\
                        "WHERE rel.cuenta_id = %s AND rel.fecha_movimiento "\
                        "BETWEEN TO_DATE ('%s', 'yyyy-mm-dd') "\
                        "AND TO_DATE ('%s', 'yyyy-mm-dd') "\
                        "ORDER BY rel.id DESC "\
                        % (str(cuenta_id), fecha_inicial,fecha_final))
            
            res = cr.dictfetchall()
            return res

     
    def eliminar_movimiento(self,cr,uid,cuenta_ids,accion,
                                            descripcion,
                                            periodo_id,context=None):
        '''Metodo que se utiliza para eliminar los movimientos que efectuen errores
        durante el registro masivo por grupo o unitario de un modulo para el 
        ingreso de monto o carga por cualquier asignación, este metodo recibe
        por parametros (cuenta_ids,accion,descripcion,periodo_id) en este mismo orden 
        en este metodo, primero se crean los registros que se van a eliminar
        en un objeto creado para este fin, luego se elimina el o los registros
        que pasen por parametros, en el objeto de crear cuenta'''
        mov_cta_elim_obj=self.pool.get('jpv.movimientos_cuentas_eliminadas')
        cta_elim_valores=[]
        for buscar_ctas_ids in self.browse(cr,uid,cuenta_ids):
            cta_elim_valores={
                'movimiento_cuenta_id':buscar_ctas_ids.id,
                'accion':buscar_ctas_ids.accion+' '+accion,
                'name':buscar_ctas_ids.name+' '+descripcion,
                'fecha_movimiento':buscar_ctas_ids.fecha_movimiento,
                'monto':buscar_ctas_ids.monto_ingreso,
                'objeto_rastro':buscar_ctas_ids.objeto_rastro,
                'id_rastro':buscar_ctas_ids.id_rastro,
                'periodo_id':buscar_ctas_ids.periodo_id,
                }
            mov_cta_elim_obj.create(cr, uid, cta_elim_valores, context=context)
        self.unlink(cr,uid,cuenta_ids,context=context)
        return True

    _columns = {
        'cuenta_id':fields.many2one(
                    'jpv.cuentas',
                    'Cuenta',
                    required=True,
                    ),
        'accion':fields.char(
                    'Acción', 
                    required=True, 
                    ),
        'entidad_id': fields.related(
                    'cuenta_id',
                    'partner_id',
                    'name',
                    type='char',
                    readonly=True,
                    relation="jpv.cuentas",
                    string='Entidad',
                    help='Entidad',
                    ),
        'name':fields.char(
                    'Descripción', 
                    required=True, 
                    ),
        'objeto_rastro':fields.char(
                    'Nombre del Objeto', 
                    ),
        'id_rastro':fields.integer(
                    'ID del Rastro', 
                    ),
        'fecha_movimiento':fields.date(
                    'Fecha', 
                    required=True, 
                    ),
        'monto_ingreso':fields.float(
                    'Créditos',
                    readonly=True,
                    ),
        'monto_egreso':fields.float(
                    'Débitos', 
                    readonly=True,
                    ),
        'monto_saldo':fields.float(
                    'Saldo',
                    readonly=True,
                    ),
        'periodo_id': fields.many2one(
                    'jpv_plf.periodos', 
                    'Periodo', 
                    required=False,
                    help='Periodo en el cual se registro el movimiento',
                    ),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
    }
    _defaults = {
        'active':True,
        'monto_ingreso':0.00,
        'monto_egreso':0.00,
        'monto_saldo':0.00,
    }
    
# objeto creado para realizar automaticamente registros del objeto
# ('jpv.movimientos_cuentas') los cuales van a ser eliminados en un
# instante dado en el registro de movimiento en cuenta
class jpv_movimientos_cuentas_eliminadas(osv.osv):
    _name='jpv.movimientos_cuentas_eliminadas'
    _description="Registro de los Movimientos de Cuentas que se eliminan"
    
    _columns={
        'movimiento_cuenta_id':fields.integer(
                    'Movimiento de la Cuenta',
                    help='Registro del movimiento que se \
                    elimina en cuenta',
                    required=True,
                    ),
        'accion':fields.char(
                    'Acción', 
                    required=True, 
                    ),
        'name':fields.char(
                    'Descripción', 
                    required=True, 
                    ),
        'objeto_rastro':fields.char(
                    'Nombre del Objeto', 
                    ),
        'id_rastro':fields.integer(
                    'ID del Rastro', 
                    ),
        'fecha_movimiento':fields.date(
                    'Fecha', 
                    required=True, 
                    ),
        'periodo_id': fields.many2one(
                    'jpv_plf.periodos', 
                    'Periodo', 
                    required=False,
                    help='Periodo en el cual se registro el movimiento',
                    ),
        'monto':fields.float(
                    'Movimeinto',
                    required=True,
                    ),
    }
