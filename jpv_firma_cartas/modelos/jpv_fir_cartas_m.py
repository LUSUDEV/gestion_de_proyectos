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
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

from openerp.osv import osv, fields



class jpv_fir_cartas_x_firmar(osv.osv):
    _name = 'jpv_fir.cartas_x_firmar'
    _description = "Registro de las cartas por firmar"
    _rec_name= "correlativo"
    
    _columns = {
        'correlativo':fields.char(
                            'correlativo de la Carta',
                            help='Esta es el correlativo asignado a\
                                  la carta proyecto'),
        'tipo_cartas':fields.selection(
                                [('aprobado', 'Proyectos Aprobados'),
                                ('negado', 'Proyectos Negados'),
                                ('diferido', 'Proyectos Diferidos'),
                                ('monto', 'Cambio de Monto'),
                                ('modificación', 'Modificación de Proyecto'),
                                ('cancelación', 'Cancelacion de Proyectos'),
                                ('aprobacion_cemento', 'Aprobación de proyectos por cemento'),
                                ],
                                'Tipos de Cartas',
                                required=True),
                    
        'mensaje':fields.char('Mensaje del historico',required=True),
        
        'referencia':fields.char('Referencia',required=True),
        
        'nombre_file':fields.char('Nombre del Archivo'),
        
        'objeto_ratro_principal':fields.char(
                            'Objeto Rastro Principal',
                            required=True),
        
       'state':fields.selection(
                                [('porfirmar', 'Por firmar'),
                                ('firmado', 'Firmada'),
                                ('porvaloracion', 'Por firma de Valoración'),
                                ('firmadovaloracion', 'Firmada (Valoración)')
                                ],
                                'Estado de la Carta',
                                required=True),
                                
        'objeto_rastro_ids': fields.one2many(
                            'jpv_fir.objeto_rastro',
                            'cartas_x_firmar_id',
                            'Objetos Rastro',
                            required=True),
                            
        'objeto_principal_id':fields.integer(
                                'Objeto Principal Rastro Id',
                                required=True),
                            
        'attachment_id': fields.many2one(
                                'ir.attachment',
                                'Carta'),
                                
        'metodo':fields.char('Metodo a ejecutar, para cargar las cartas'),
        
        'metodoGenerarCartas':fields.char('Metodo a ejecutar,para generar la o las cartas'),
                    
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
                            
    }
    _defaults = {
        'active':True,
    }
    
    _order = 'create_date desc, id desc'

class jpv_fir_objeto_rastro(osv.osv):
    _name = 'jpv_fir.objeto_rastro'
    _description = u"Rastro del objeto de la carta"
    _rec_name= "objeto_ratro"

    _columns={
        'objeto_ratro':fields.char('Objeto Rastro',required=True),
        
        'objeto_ratro_id':fields.integer('Objeto Rastro Id',required=True),
                                
        'cartas_x_firmar_id': fields.many2one(
                                'jpv_fir.cartas_x_firmar',
                                'Carta por firmar'),
                                
        'referncia':fields.char('Refencia Controlador')
        
        }



    
    
        
        

