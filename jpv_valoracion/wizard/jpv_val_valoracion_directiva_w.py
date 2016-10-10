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
from openerp.addons.jpv_valoracion.controlador import jpv_eva_valoracion_c



class jpv_val_validar_valoraciones_wizard(osv.TransientModel):
    """
        Este wizard es para validar los resultados de la valoraciones
    """
    _name = "jpv_val_validar_valoraciones_wizard"
    _description = "Validar valoraciones"


         
    _columns = {
         'estado_ids':fields.many2many(
                            'jpv_ent.estados',
                            'jpv_val_estado_wizard_validar_rel',
                            'estado_id',
                            'validar_carta_id',
                            'Estado'),
        
        'partner_ids':fields.many2many(
                                        'res.partner', 
                                        'jpv_val_partner_wizard_validar_rel', 
                                        'partner_id', 
                                        'validar_carta_id',
                                        'Entidades'),
        'dictamen':fields.selection(
                                [('Aprobado', 'Aprobado'),
                                ('Negado', 'Negado'),
                                ('Diferido', 'Diferido'),
                                ],
                                'Dictamen de la Valoración'),
        'resumen':fields.html("Rasumen de valoracion",
                                readonly=True,
                                store=False),
        'proyecto_ids':fields.many2many(
                                        'jpv_cp.carga_proyecto', 
                                        'jpv_val_validar_valoraciones_rel', 
                                        'proyecto_id', 
                                        'valoracion_id',
                                        'Proyectos a Validar'),
    }

    def validar_valoracion(self, cr, uid, ids, context=None):
        proyecto_ids = context.get('active_model') == 'jpv_cp.carga_proyecto' and context.get('active_ids')
        validar=self.browse(cr,uid,ids,context=context)
        for proyecto in validar.proyecto_ids:
            dictamen=proyecto.dictamengraph
            if not  dictamen in ["Aprobado","Diferido","Negado"]:
                raise osv.except_osv(
                ('Error!'),
                (u' No se puede procesar la carta \n El proyecto .'+proyecto.correlativo+' Tiene como Dictamen de Valoracion '+dictamen))
            print 'gsdgjsdjg'
            print proyecto.dictamengraph
            print proyecto.id
        if proyecto_ids:
            url="/valoracionept/%s" % ids[0]
            return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'self',
            }

    #~ def _dictamen_valoracion(self, cr, uid, context=None):
        #~ proyecto_model = self.pool['jpv_cp.carga_proyecto']
        #~ proyectos_ids=proyecto_model.search(
                                    #~ cr,
                                    #~ SUPERUSER_ID,
                                    #~ [('state','=','evaluacion')])
        #~ proyecto_data=proyecto_model.browse(cr,uid,proyectos_ids)
        #~ aprobados=0
        #~ negados=0
        #~ diferidos=0
        #~ sin_valorar=0
        #~ solo_genaral=0
        #~ solo_coordenadas=0
        #~ for proyecto in proyecto_data:
            #~ if proyecto.dictamen=='Aprobado':
                #~ aprobados=aprobados+1
            #~ if proyecto.dictamen=='Negado':
                #~ negados=negados+1
            #~ if proyecto.dictamen=='Diferido':
                #~ diferidos=diferidos+1
            #~ if proyecto.dictamen=='Sin valorar':
                #~ sin_valorar=sin_valorar+1
            #~ if proyecto.dictamen=='Solo General':
                #~ solo_genaral=solo_genaral+1
            #~ if proyecto.dictamen=='Solo Coordenadas':
                #~ solo_coordenadas=solo_coordenadas+1   
        #~ table='''<table class="table table-bordered table-striped mt32">
            #~ <thead>
                #~ <tr class="active">
                    #~ <th colspan="7" >
                        #~ <h4 align="center">
                            #~ <b>Resumen de las Valoraciones</b>
                        #~ </h4>
                    #~ </th>
                #~ </tr>
                #~ <tr class="active">
                    #~ <th>Aprobados</th>
                    #~ <th>Diferidos</th>
                    #~ <th>Negados</th>
                    #~ <th>Sin Valorar</th>
                    #~ <th>Solo General</th>
                    #~ <th>Solo Coordenadas</th>
                    #~ <th>Total</th>
                #~ </tr>
            #~ </thead>
            #~ <tbody>
                #~ <tr>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                     #~ <td>%s</td>
                 #~ </tr>
            #~ </tbody>
        #~ </table>''' % (aprobados,
                        #~ diferidos,
                        #~ negados,
                        #~ sin_valorar,
                        #~ solo_genaral,
                        #~ solo_coordenadas,
                        #~ len(proyectos_ids))
        #~ 
        #~ 
        #~ return table
        
    def _default_proyecto_ids(self, cr, uid, context=None):
        if context is None:
            context = {}
        proyecto_model = self.pool['jpv_cp.carga_proyecto']
        proyecto_ids = context.get('active_model') == 'jpv_cp.carga_proyecto' and context.get('active_ids') or []
        print 'proyecto_ids'
        print proyecto_ids
        print proyecto_ids
        print 'proyecto_ids _default_proyecto_ids'
        proyecto_data=proyecto_model.browse(cr,SUPERUSER_ID,proyecto_ids)
        for proyecto in proyecto_data:
            if proyecto.state!='evaluacion':
                proyecto_ids=[]
            if proyecto.dictamen in ['Sin valorar','Solo General','Solo Coordenadas']:
                proyecto_ids=[]
 
        return proyecto_ids

    _defaults = {
        'proyecto_ids': _default_proyecto_ids,
        #~ 'resumen': _dictamen_valoracion,
    }
