# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
#    Modulo Desarrollado por Juventud Productiva (Jose Mancilla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp.http import request
import time
from openerp.addons.ept_rendicion.controladores.comunes import *



class ept_rnd_avance(osv.osv):
    _name='ept_rnd.avance'
    
   
    
    _columns = {
                    
            
        'rendicion_id':fields.many2one(
                    'ept_rnd.rendicion',
                    'Rendicion',help="Rendicion",
                    ondelete="cascade"
                    ),
        
        'proyecto_id': fields.related('rendicion_id','proyecto_id',string='Proyecto', 
                        type='many2one', relation='ept_cp.carga_proyecto',
                        help="""Entidad a la cual esta asociada el proyecto"""),
                    
                    
        'respuestas_line':fields.one2many('ept_rnd.input_line','avance_id','Respuestas'),
    }

    def unlink(self,cr,uid,ids,context=None):
        avance_data=self.browse(cr,uid,ids)
        unlink_id={}
        for avance in avance_data:
            if avance.rendicion_id.state=='culminada':
                raise osv.except_osv(
                    ('Error!'),
                    (u'El Proyecto "%s" ya esta Culminado.\n'\
                    ' No puede eliminar avances en rendiciones de proyectos culminados' % (avance.rendicion_id.proyecto_id.correlativo)))
            else:
                print self
                unlink_id=super(ept_rnd_avance,self).unlink(cr,uid,ids,context)
        return unlink_id 

    
class ept_rnd_input_line(osv.osv):
    _name="ept_rnd.input_line"
    
    
    
    _columns = {
    
        'pregunta_id' : fields.many2one('ept_conf.preguntas', 'Pregunta',ondelete="restrict"),
       
        'avance_id' : fields.many2one('ept_rnd.avance', 'Avance',ondelete="cascade"),
        
        'rendicion_id' : fields.related('avance_id', 'rendicion_id', 
                            string='Rendicion', type='many2one', 
                            relation='ept_rnd.avance', help="""Rendicion"""),
        
        'tipo_pregunta': fields.related('pregunta_id','tipo',string='tipo de pregunta', 
                        type='char', relation='ept_conf.preguntas',
                        help="""Tipo de Pregunta"""),
        
        'respuesta' : fields.char('Respuesta'),
       
        'files' : fields.one2many('ir.attachment', 'input_line_id', 'Archivos'),
    
        'sequence': fields.related('pregunta_id', 'sequence', type='integer' ,string='Sequence'),
    
    
    }

    
class ir_attachment_inherit(osv.osv):
    _inherit='ir.attachment'
    _columns = {
    
       
        'input_line_id' : fields.many2one('ept_rnd.input_line', 'Respuesta', ondelete="cascade"),
        
    
    
    
    }
   
