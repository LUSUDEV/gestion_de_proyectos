# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from openerp.osv import fields, osv
from openerp.http import request

class ept_ent_husos(osv.osv):
    _name='ept_ent.husos'
    _description='Registro de los Husos'
    _rec_name='huso'
    
    _columns={
        'huso': fields.integer(
                    'Huso', 
                    size=50, 
                    required=True, 
                    help='Nombre  del  Huso'),
            }
    

    
