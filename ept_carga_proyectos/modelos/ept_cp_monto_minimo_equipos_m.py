# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class ept_cp_montos_minimos_equipos(osv.osv):
    _name = 'ept_cp.montos_minimos_equipos'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del equipo.'),
        'monto_minimo': fields.float(
                                'Monto',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo que requiere por unidad \
                                    para este equipo.'),
    }
