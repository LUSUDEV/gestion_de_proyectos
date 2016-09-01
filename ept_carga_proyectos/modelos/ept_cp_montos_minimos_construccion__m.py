# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class ept_cp_montos_minimos_construccion(osv.osv):
    _name = 'ept_cp.montos_minimos_construccion'
    _rec_name = 'subcategoria_id'
    
    _columns = {
        'tipo_sector_id':fields.many2one(
                                'ept_cp.tipo_sectores',
                                'Tipo de sector',
                                required=True,
                                help='Tipo de sector al cual pertenece\
                                     el monto minimo a registrar'),
        'categoria_id': fields.many2one(
                                'ept_cp.tipo_sectores', 
                                'Categoría', 
                                required=True, 
                                help='Categoría a la cual pertenece\
                                     el monto minimo a registrar'),
        'subcategoria_id': fields.many2one(
                                    'ept_cp.tipo_sectores', 
                                    'Subcategoría', 
                                    required=True, 
                                    help='Subcategoría a la cual\
                                    pertenece el monto minimo a registrar'),
        'unidades_id':fields.many2one(
                        'ept_cp.unidades_obra_civil',
                        'Unidad de Medida',
                        required=True,
                        help='Tipo de sector al cual pertenece\
                             el proyecto a registrar'),
        'monto_construc': fields.float(
                                'Monto Construcción Inicial',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo de construcción que requiere\
                                 la subcategoria para su ejecución.'),
        'monto_rehabilit': fields.float(
                                'Monto Rehabilitación/Mejora',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo de rehabilitación/mejora que\
                                 requiere la subcategoria para su ejecución.'),
        'monto_ampliac': fields.float(
                                'Monto Ampliación',  
                                readonly=False,
                                required=True,   
                                help='Monto minimo de ampliación que requiere\
                                 la subcategoria para su ejecución.'),
    }
    
    #~ _sql_constraints = [
        #~ ('subcategoria_id_uniq', 'unique (subcategoria_id)', 'Ya existe un \
                            #~ registro de costo minimo para esta subcategoría')
    #~ ]
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
class ept_cp_montos_minimos_construccion(osv.osv):
    _name = 'ept_cp.unidades_obra_civil'
    _rec_name = 'unidad'
    
    _columns = {
        'unidad':fields.char(
                    'Unidad',
                    required=True,
                    help='Unidad de medición para las obras civiles'),
    }
