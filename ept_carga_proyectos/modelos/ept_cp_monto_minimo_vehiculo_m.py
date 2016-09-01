# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class ept_cp_montos_minimos_vehiculo(osv.osv):
    _name = 'ept_cp.montos_minimos_vehiculo'
    _rec_name = 'uso_id'
    
    _columns = {
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_vehiculo_uso', 
                                'Uso', 
                                required=True, 
                                help=''),
        'caracteristicas_id': fields.many2one(
                                    'ept_cp.montos_minimos_vehiculo_caracteristicas', 
                                    'Caracteristica', 
                                    required=True, 
                                    help=''),
        'tipo_id': fields.many2one(
                                'ept_cp.montos_minimos_vehiculo_tipo', 
                                'Tipo', 
                                required=True, 
                                help=''),
        'monto_minimo': fields.float(
                                'Monto',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo que requiere por unidad \
                                    para este vehículo.'),
    }
    
    
    
class ept_cp_montos_minimos_vehiculo_tipo(osv.osv):
    _name = 'ept_cp.montos_minimos_vehiculo_tipo'
    _rec_name = 'tipo'
    
    _columns = {
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_vehiculo_uso', 
                                'Uso', 
                                required=True, 
                                help=''),
        'caracteristicas_id': fields.many2one(
                                    'ept_cp.montos_minimos_vehiculo_caracteristicas', 
                                    'Caracteristica', 
                                    required=True, 
                                    help=''),
        'tipo': fields.char(
                        'Caracteristicas',  
                        readonly=False,
                        required=True,   
                        help='Tipo de vehiculo.'),
    }
    
class ept_cp_montos_minimos_vehiculo_caracteristicas(osv.osv):
    _name = 'ept_cp.montos_minimos_vehiculo_caracteristicas'
    _rec_name = 'caracteristicas'
    
    _columns = {
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_vehiculo_uso', 
                                'Uso', 
                                required=True, 
                                help=''),
        'caracteristicas': fields.char(
                        'Caracteristicas',  
                        readonly=False,
                        required=True,   
                        help='Caracteristicas del vehiculo.'),
    }
    
    
class ept_cp_montos_minimos_vehiculo_uso(osv.osv):
    _name = 'ept_cp.montos_minimos_vehiculo_uso'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del vehiculo.'),
    }
