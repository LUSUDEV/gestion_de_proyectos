# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class ept_cp_montos_minimos_maquinaria(osv.osv):
    _name = 'ept_cp.montos_minimos_maquinaria'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso de la maquinaria.'),
        'monto_minimo': fields.float(
                                'Monto',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo que requiere por unidad \
                                    para esta maquinaria.'),
    }
