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

class jpv_asignacion_cuentas(osv.osv):
    _name = 'jpv.asignacion_cuentas'
    _description = u"Asignación de las cuentas con los Partner"
    _rec_name = "tipo_cuenta_id"
    
    def _control_jpv_tipo_cuenta_ids(self, cr, uid, ids, context=None):
        for r in self.browse(cr,uid,ids):
            if not r.jpv_tipo_cuenta_ids:
                raise osv.excjpv_osv(
                        ('Error!'),
                        (u'Debe Seleccionar una opción en la tabla para\
                         quien será creada la cuenta'))
        return True
    
    _columns = {
        'tipo_cuenta_id':fields.many2one(
                    'jpv.tipo_cuentas', 
                    'Tipo de Cuenta',
                    required=True,
                    ),
        'jpv_tipo_cuenta_ids':fields.many2many(
                    'res.partner',
                    'jpv_rel_tipo_cuen_partner',
                    'tipo_cuenta_id',
                    'partner_id',
                    'Relacion Tipo de Cuenta',
                    ),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
    }
    _defaults = {
        'active':True,
    }
    
    _constraints=[
        (_control_jpv_tipo_cuenta_ids, ' ', ['jpv_tipo_cuenta_ids']),
        ]
    
    def tipo_cuenta_id_change(self, cr, uid, ids, tipo_cuenta_id,context=None):
        # domain que se entrega al many2many para entregar el
        # filtro vacio
        domain={'jpv_tipo_cuenta_ids':[('id','in',[])]}
        # Se instancias los objetos de tipos de cuentas 
        # y partner para poder recorrerlos
        jpv_tipo_cuentas_obj=self.pool.get('jpv.tipo_cuentas')
        jpv_partner_obj=self.pool.get('res.partner')
        # if creado para que se ingrese una 
        # vez hayan pulsado el tipo de cuenta
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
            # variable declarada para entrewgar resultados 
            # en el domain una vez haya elegido el tipo de cuenta
            re_r=set()
            r=set()
            # recorrido de los datos generados por la busqueda anterior
            for a in jpv_tipo_cuentas_data:
                # recorrido utilizado para acceder a la 
                # variable jpv_tipo_field_ids y obtener los name
                for field in a.jpv_tipo_field_ids:
                    #variables declaradas en set y tuplas las mismas son 
                    #declaradas para asignarle valores dentro de los recorridos
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
                        if len(jpv_partner_ids)==1:
                            partner_id=0
                            for jpv_partner_sel in jpv_partner_ids:
                                partner_id=jpv_partner_sel
                            cr.execute('SELECT rel.partner_id '\
                                    'FROM jpv_cuentas AS rel '\
                                    'WHERE rel.tipo_cuenta_id = %s ' \
                                    'AND rel.partner_id = %s ;' \
                                    % (str(tipo_cuenta_id), 
                                    str(partner_id)))
                        else:
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
            domain = {'jpv_tipo_cuenta_ids': [('id','in',list(re_r))]}
        return {'domain':domain}
            
    def create(self,cr,uid,values,context=None):
        tipo_cuenta_id=super(jpv_asignacion_cuentas,self).create(
                                                            cr,
                                                            uid,
                                                            values,
                                                            context=context)
        jpv_cuentas_obj=self.pool.get('jpv.cuentas')
        for tipo_cuenta in self.browse(cr,uid,tipo_cuenta_id,context=context):
            jpv_cuentas_vals=[]
            for nom_tpo_cta in tipo_cuenta.jpv_tipo_cuenta_ids:
                jpv_cuentas_vals={
                            'name':tipo_cuenta.tipo_cuenta_id.name, 
                            'tipo_cuenta_id': tipo_cuenta.tipo_cuenta_id.id, 
                            'partner_id': nom_tpo_cta.id, 
                            }
                jpv_cuentas_obj.create(cr,uid,jpv_cuentas_vals,context=context)
        return tipo_cuenta_id
    
    
