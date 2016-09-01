# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from openerp.osv import fields, osv


class res_users(osv.osv):
    _name = 'res.users'
    _inherit="res.users"
    
    _columns = {
        'activo': fields.boolean('Activo',
                    help='''Este campo desactiva a
                            los usuario de la vista website''', 
                    )
    }
    
    _defaults={'activo':True}

