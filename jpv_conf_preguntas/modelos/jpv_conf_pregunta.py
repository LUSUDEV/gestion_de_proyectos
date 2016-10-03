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
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

from openerp.osv import osv, fields

class jpv_conf_obj_rendicion(osv.Model):
    _name = 'jpv_conf.obj_rendicion'
    _description = u'objetos relacionados de la valoración'
    _rec_name = 'model_id'

    _columns = {
        'refencia': fields.char('Referencia del Controlador', required=True),
        
        'model_id': fields.many2one('ir.model', 'Objeto a aplicar',required=False),
        
        'model_parent_id': fields.many2one('ir.model', 'Objeto de Destino',required=False),
        
        'preguntas_ids': fields.one2many('jpv_conf.preguntas',
                                        'obj_rendicion_id', 'Preguntas', copy=True),
            
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
                            
        'advertencia': fields.html('Advertencia'),
        
    }

    _defaults = {
        'active': True,
        }
    
class jpv_conf_pregunta_pregunta(osv.Model):
    _name = 'jpv_conf.preguntas'
    _description = u'Preguntas'
    _rec_name = 'nombre'
    _order = 'sequence,id'

    
    
    _columns = {
        'obj_rendicion_id': fields.many2one('jpv_conf.obj_rendicion', 'Valoración',
            ondelete='cascade'),

        
        'field_ids':fields.many2one(
                                        'ir.model.fields',
                                        'Atributos del Objeto',
                                        required=False
                                        ),
       
        'field_muestra_ids':fields.many2one(
                                        'ir.model.fields',
                                        'Atributo al que Corresponde',
                                        required=False
                                        ),
                                        
                                        
        'nombre': fields.char('Nombre de la Pregunta', required=True),

        'pregunta_id': fields.many2one('jpv_conf.preguntas', 'Pregunta dependiente'),
                                        
        'sequence': fields.integer(string='Sequence'),
        
        'description': fields.html('Descripción'),
        
        'tipo':fields.selection([('titulo', 'Titulo'),
                                ('subtitulo', 'Sub-titulo'),
                                ('textarea', 'Textarea'),
                                ('numerico', 'Numerico'),
                                ('text', 'Campo de Texto'),
                                ('rif', 'Rif'),
                                ('radio', 'Seleccion simple'),
                                ('checkbox', 'Seleccion multiple'),
                                ('date', 'Fecha'),
                                ('select', 'Selection'),
                                ('file', 'Carga de Archivo'),
                                ('img', 'Carga de Imagenes'),
                                ('adquisiciones', 'Adquisiciones'),
                                ('obra', 'Obra Civil'),
                                ],
                                'Tipo de Pregunta'),
                                
                                
        'divs':fields.selection([('1', '1'),
                                ('2', '2'),
                                ('3', '3'),
                                ('4', '4'),
                                ('5', '5'),
                                ('6', '6'),
                                ('7', '7'),
                                ('8', '8'),
                                ('9', '9'),
                                ('10', '10'),
                                ('11', '11'),
                                ('12', '12'),
                                ],
                                'Ocupación del formulario (Divs)'),
                                
                                
        'state':fields.selection([('avance', 'Avance'),
                                ('culminacion', 'Culminación'),
                                ('paralizacion', 'Paralización'),
                                ('cancelacion', 'Cancelación'),
                                ],
                                'Grupo o estado de Preguntas'),

        'cant_files':fields.integer('Cantidad e archivos '),
        # respueatas
        'respuesta_ids': fields.one2many('jpv_conf.items_respueta',
            'pregunta_id', 'Types of answers', copy=True),


        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'dependiente': fields.boolean(
                            'Dependiente',
                            help='Estatus del registro Activado-Desactivado'),
        
        'muestra_continua': fields.boolean('Muestra Continua'),
        
        'condicion_muestra': fields.many2one('jpv_conf.items_respueta', 'Muestra Continua Hasta'),
        
        'dependencias_id':fields.one2many('jpv_conf.dependencia','pregunta_id','Dependencias')
    }

    _defaults = {
        'active': True,
        'divs': '12',
        }
        
    def valoracion_dependiente(self, cr, uid, ids, context=None):
        for items in self.browse(cr,uid,ids):
             if items.pregunta_id.id:
                 self.write(cr,uid,items.pregunta_id.id,{'dependiente':True})
        return True
        
    _constraints = [(
        valoracion_dependiente, 'Verificar si tiene dependencia',
        ['pregunta_id']
            ),]
            
    def limpiar_respuestas(self,cr,uid,ids,pregunta_id,context=None):
        if not pregunta_id:
            return {'value':{'respuesta_ids':[(6, 0, [])]}}


class jpv_conf_pregunta_respuesta(osv.Model):
    _name = 'jpv_conf.items_respueta'
    _rec_name = 'respuesta'
    _order = 'sequence,id'
    _description = 'Respuestas'


    _columns = {
        'respuesta': fields.char("Respuesta",required=True),

        'categoria_id': fields.many2one('jpv_conf.categ_respuesta', 'Categoria',
            ondelete='cascade'),
          
        'tipo_pregunta':fields.related('pregunta_id','tipo',type="char"),   
            
        'pregunta_id': fields.many2one('jpv_conf.preguntas', 'Preguntas',
            ondelete='cascade'),
            
        'dependencia_line':fields.one2many('jpv_conf.dependencia', 'respuesta_id'),
        
        'accion_line':fields.one2many('jpv_conf.accion', 'respuesta_id'),

        'sequence': fields.integer('Label Sequence order'),
        
        'state':fields.selection([('aprobado', 'Aprobao'),
                                ('negado', 'Negado'),
                                ('diferido', 'Diferido'),
                                ],
                                'Estado de Respuesta de Valoración'),
        
    }
    
    _defaults = {
        'sequence': 10,
    }
    
    
    def create(self,cr,uid,values,context=None):
        if 'dependencia_line' in values:
            for i in values['dependencia_line']:
                if i[2] and 'pregunta_id' in i[2]:
                    write_id=self.pool.get('jpv_conf.preguntas').write(cr,uid,i[2]['pregunta_id'],{'dependiente':True})
        create_id=super(jpv_conf_pregunta_respuesta,self).create(cr,uid,values)
        return create_id
    
    def write(self,cr,uid,ids,values,context=None):
        if 'dependencia_line' in values:
            for i in values['dependencia_line']:
                if i[2] and 'pregunta_id' in i[2]:
                    write_id=self.pool.get('jpv_conf.preguntas').write(cr,uid,i[2]['pregunta_id'],{'dependiente':True})
        create_id=super(jpv_conf_pregunta_respuesta,self).write(cr,uid,ids,values)
        return create_id
    
    
class jpv_conf_pregunta_dependencia(osv.Model):
    _name = 'jpv_conf.dependencia'
    _rec_name = 'respuesta_id'
    _order = 'sequence,id'
    _description = 'Respuestas'


    _columns = {
        
        'pregunta_id': fields.many2one('jpv_conf.preguntas', 'Pregunta Dependiente',
            ondelete='cascade'),
            

        'accion_type': fields.selection([('abre', 'Abre'),
                                         ('cierra', 'Cierra')],
                                        'Relacion'),
        
        'respuesta_id':fields.many2one('jpv_conf.items_respueta','Respuesta'),
        
        'sequence': fields.integer(string='Sequence'),
    }
    
    _defaults = {
    
    }


class jpv_conf_pregunta_accion(osv.Model):
    _name = 'jpv_conf.accion'
    _rec_name = 'respuesta_id'
    _order = 'sequence,id'
    _description = 'Respuestas'


    _columns = {
            

        'respuesta_id':fields.many2one('jpv_conf.items_respueta','Respuesta'),
        
        
        'respuesta_accion_id':fields.many2one('jpv_conf.items_respueta','Acciona Respuesta'),
        
        'sequence': fields.integer(string='Sequence'),
    }
    
    _defaults = {
    
    }
    
    
class jpv_conf_pregunta_categ_respuesta(osv.Model):
    _name = 'jpv_conf.categ_respuesta'
    _rec_name = 'name'
    _order = 'sequence,id'
    _description = 'Categorizacion de las Respuestas'


    _columns = {
            

        'name':fields.char('Categoria'),
        
        'sequence': fields.integer(string='Sequence'),
    }
    
    _defaults = {
    
    }



