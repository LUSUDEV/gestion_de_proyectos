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


class jpv_cuentas(osv.osv):
    _name = 'jpv.cuentas'
    _description = "Registro de las Cuentas del Concejo Federal de Gobierno"
    _rec_name = 'partner_id'
    
         
    def valor_monto_actual(self, cr, uid, ids, name, arg, context=None):
        res={}
        movimiento_cuenta_obj=self.pool.get('jpv.movimientos_cuentas')
        movimiento_cuenta_ids=movimiento_cuenta_obj.search(
                                                cr,
                                                uid,
                                                [('cuenta_id','in',ids)],
                                                limit=1,order="id desc")
        movimiento_cuenta_datos=movimiento_cuenta_obj.browse(
                                                cr,
                                                uid,
                                                movimiento_cuenta_ids)
        for id in ids:
            res[id]=movimiento_cuenta_datos['monto_saldo']
        return res
    
    _columns = {
        'monto_actual':fields.function(
                    valor_monto_actual,
                    'Monto Disponible',
                    store=True,
                    ),
        'name':fields.char(
                    'Código de la Cuenta', 
                    required=True,
                    readonly=True, 
                    ),
        'tipo_cuenta_id':fields.many2one(
                    'jpv.tipo_cuentas', 
                    'Tipo de Cuenta', 
                    required=True,
                    readonly=True,
                    ),
        'partner_id':fields.many2one(
                    'res.partner', 
                    'Entidad', 
                    required=True,
                    readonly=True,
                    ondelete='cascade'
                    ),
        'movimientos_cuentas_ids':fields.one2many(
                    'jpv.movimientos_cuentas',
                    'cuenta_id',
                    'Movimiento de Cuentas',
                    readonly=True,
                    ),
        'active': fields.boolean(
                            'Activo',
                            readonly=True,
                            help='Estatus del registro Activado-Desactivado'),
    }
    _defaults = {
        'active':True,
    }
    
    _sql_constraints=[( 'tc_p_id_uniq', 'unique (tipo_cuenta_id,partner_id)', 
                        'El tipo de Cuenta para esta Entidad ya Existe')]
    
    def desactivar_cuenta(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {'active':False})
        return {
            'name': 'Cuentas Activas de las jpv',
            'res_model': 'jpv.cuentas',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'limit': 80,
        }
    
    def activar_cuenta(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {'active': True})
        return {
            'name': 'Cuentas Inactivas de las jpv',
            'res_model': 'jpv.cuentas',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'domain': "[('active','=',False)]",
            'limit': 80,
        }
    
    def partner_id_change(self, cr, uid, ids, tipo_cuenta_id,context=None):
        # domain que se entrega al many2one para declarar  
        # el filtro vacio
        domain={'partner_id':[('id','in',[])]}
        # Instanciamos los objetos 
        jpv_tipo_cuentas_obj=self.pool.get('jpv.tipo_cuentas')
        jpv_partner_obj=self.pool.get('res.partner')
        # if creado para controlar una vez hayan
        # pulsado el tipo de cuenta
        if tipo_cuenta_id:
            # Busqueda de tipo de cuenta que necesito realizar la accion
            jpv_tipo_cuentas_ids=jpv_tipo_cuentas_obj.search(
                                                cr,
                                                uid,
                                                [('id','=',tipo_cuenta_id)],
                                                context=context)
            # datos de los atributos los cuales 
            # obtengo de la busqueda anterior
            jpv_tipo_cuentas_data=jpv_tipo_cuentas_obj.browse(
                                                cr,
                                                uid,
                                                jpv_tipo_cuentas_ids)
            re_r=set()
            r=set()
            # recorrido de los datos generados por la busqueda anterior
            for a in jpv_tipo_cuentas_data:
                for field in a.jpv_tipo_field_ids:
                    re_r2=set()
                    res=tuple()
                    # aqui obtenemos los ids de los atributos de res.partner 
                    # los cuales segun el resultado del recorrido anterior 
                    # con el fiel.name este nos filtra
                    # los atributos q sean verdaderos en la tabla 
                    jpv_partner_ids=jpv_partner_obj.search(
                                                    cr,
                                                    uid,
                                                    [(field.name,'=',True)],
                                                    context=context)
                    # se realiza un len(jpv_partner_ids)>0 
                    # para controlar cuando no tenga datos el 
                    # recorrido anterior este no nos de error
                    if len(jpv_partner_ids)>0:
                        # se realiza una consulta con un query para 
                        # consumir menos recursos de la tabla jpv_cuentas 
                        # para que esta nos entregue los registros que 
                        # esten en ella segun el partner y el tipo de cuenta
                        cr.execute('SELECT rel.partner_id '\
                                'FROM jpv_cuentas AS rel '\
                                'WHERE rel.tipo_cuenta_id = %s ' \
                                'AND rel.partner_id in %s ;' \
                                % (str(tipo_cuenta_id), 
                                str(tuple(jpv_partner_ids))))
                        res = cr.fetchall()
                        # variable creada para almacenar los datos
                        re_r3=[]
                        # controlamos que si el resultado anterior es cero 0 
                        # este no nos de error
                        if len(res)>0:
                            # una vez se cumpla esta condicion e ingrese al if
                            # se realiza un recorrido para que este entregue 
                            # a una variable todos los valores que esten en res
                            for a in res:
                                # se adic. el valor del recorrido a la variable
                                re_r3.append(a[0])
                        # se incluye a la variable el valor del recorrido
                        re_r2=set(tuple(re_r3))
                    # se realiza la teoria de conjunto para ir restando valores 
                    # y no repetir partner en la lista que se va a entregar
                    r=set(tuple(jpv_partner_ids))-re_r2
                    # la variable va almacenando los valores que segun el o los
                    # recorridos que realice la entrega anterior
                    re_r= re_r|r
                    # si el resultado esta vacio entra a esta condición para
                    # enviar un alerta (solo informativo)
                    if not re_r:
                        warning={
                            'title':('Alerta!!!'),
                            'message':('''No poseé a quien asignarle esté tipo
                                        de cuentas'''),
                            }
                        return {'warning':warning}
            # se hace el filtro con el domain para asi obtener la lista 
            # correspondiente en el many2many
            domain = {'partner_id': [('id','in',list(re_r))]}
        return {'domain':domain}
    
    def create(self,cr,uid,values,context=None):
        seq=self.pool.get('ir.sequence').get(cr,uid,'jpv.cuentas')
        nombre=values['name']+'-'+seq
        values.update({
            'name':nombre,
            })
        return super(jpv_cuentas,self).create(cr,uid,values,context=context)
        
    
