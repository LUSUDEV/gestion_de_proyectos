# -*- coding: utf-8 -*-


from cStringIO import StringIO
import os
import zipfile
from shutil import rmtree

from openerp.osv import fields, osv
from openerp.addons.web.http import request
from openerp import http
from openerp.addons.web.controllers import main
from openerp import SUPERUSER_ID



class ept_negar_proyectos_diferidos(osv.TransientModel):
    """
        Este wizard es para negar proyectos diferidos.
    """
    _name = "ept.negar_proyectos_diferidos"
    _description = "Negar Proyectos Diferidos"


         
    _columns = {
        'descripcion':fields.char(
                    'Descripción',
                     size=15,
                     required=True),
        'entidades_ids':fields.many2many(
                                        'res.partner', 
                                        'ept_negar_proyecto', 
                                        'negar_id', 
                                        'proyecto_id',
                                        'Entidades'),
        'ciclo_id':fields.many2one('ept_plf.etapas','Ciclo',required=True),
        'diferido_aval':fields.boolean('¿Negar Diferidos por aval?')
    }

    def negar_proyectos(self, cr, uid, ids, context=None):
        list_entidades=[]
        for record in self.browse(cr,uid,ids):
            for id in record.entidades_ids:
                list_entidades.append(id.id)
            if record.diferido_aval==False:
                proyectos_obj=self.pool.get('ept_cp.carga_proyecto')
                proyectos_id=proyectos_obj.search(cr,uid,[('partner_id','in',list_entidades),('ciclo_id','=',record.ciclo_id.id),('state','=','diferido'),])
                proyectos_obj.write(cr,uid,proyectos_id,{'state':'negado'},0)
            else:
                print 'falta averiguar como lleguo a los proyectos con esta condicion.'
        return {
            'name': ('Proyectos'),
            'res_model': 'ept_cp.carga_proyecto',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
        }

    
