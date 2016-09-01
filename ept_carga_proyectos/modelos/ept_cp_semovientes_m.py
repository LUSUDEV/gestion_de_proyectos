# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class ept_cp_semovientes(osv.osv):
    _name = 'ept_cp.semovientes'
    _rec_name = 'especie'
    
    _columns = {
        'especie': fields.char(
                        'Especie',  
                        readonly=False,
                        required=True,   
                        help='Especie Semoviente.'),
        'monto_minimo': fields.float(
                                'Monto',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo que requiere por unidad \
                                    para semovientes.'),
    }
    
class ept_cp_semovientes_grupo_etario(osv.osv):
    _name = 'ept_cp.semovientes_grupo_etario'
    _rec_name = 'grupo_etario'
    
    _columns = {
        'grupo_etario': fields.char(
                        'Grupo Etario',  
                        readonly=False,
                        required=True,   
                        help='Grupo Etario Semoviente.'),
        'especies_id':fields.many2many('ept_cp.semovientes','ept_cp_especie_grupo_rel','grupo_id','especie_id','Especie',readonly=False,required=True, help='Especie a la cual pertenece grupo etario.' )
    }
    
class ept_cp_semovientes_uso(osv.osv):
    _name = 'ept_cp.semovientes_uso'
    _rec_name = 'uso'
    
    _columns = {
        'uso': fields.char(
                        'Uso',  
                        readonly=False,
                        required=True,   
                        help='Uso del Semoviente.'),
        'grupos_id':fields.many2many('ept_cp.semovientes_grupo_etario','ept_cp_grupo_uso_rel','uso_id','grupo_id','Grupo etario',readonly=False,required=True, help='Grupo etario al cual pertenece grupo etario.' )
    }
    
class ept_cp_semovientes_proposito(osv.osv):
    _name = 'ept_cp.semovientes_proposito'
    _rec_name = 'proposito'
    
    _columns = {
        'proposito': fields.char(
                        'Proposito',  
                        readonly=False,
                        required=True,   
                        help='Proposito del Semoviente.'),
        'usos_id':fields.many2many('ept_cp.semovientes_uso','ept_cp_uso_proposito_rel','proposito_id','uso_id','Uso',readonly=False,required=True, help='Uso al cual pertenece grupo etario.' )
    }
