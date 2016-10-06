# -*- coding: utf-8 -*-


from cStringIO import StringIO
import os
import zipfile
from shutil import rmtree

from openerp.osv import fields, osv
from openerp.addons.web.http import request
from openerp import http
from openerp.addons.web.controllers import main



class jpv_validar_cartas_wizard_view(osv.TransientModel):
    """
        Este wizard es para validar las cartar a descargar para ser firmadas
    """
    _name = "jpv_val_validar_cartas_wizard"
    _description = "Validar cartas por firmar"


         
    _columns = {
        'cartas_ids':fields.many2many(
                                        'jpv_fir.cartas_x_firmar', 
                                        'jpv_val_validar_cartas_rel', 
                                        'carta_id', 
                                        'valoracion_id',
                                        'Cartas a Validar'),
    }

    def validar_cartas(self, cr, uid, ids, context=None):
        cartas_ids = context.get('active_model') == 'jpv_fir.cartas_x_firmar' and context.get('active_ids')
        if cartas_ids:
            url="/cartas_x_firmar/%s" % ids[0]
      
            return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'self',
            }

    def _default_proyecto_ids(self, cr, uid, context=None):
        if context is None:
            context = {}
        proyecto_model = self.pool['jpv_fir.cartas_x_firmar']
        proyecto_ids = context.get('active_model') == 'jpv_fir.cartas_x_firmar' and context.get('active_ids') or []
        proyecto_data=proyecto_model.browse(cr,uid,proyecto_ids)
        return proyecto_ids

    _defaults = {
        'cartas_ids': _default_proyecto_ids,
        }
