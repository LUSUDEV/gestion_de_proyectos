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

class jpv_conf_objeto_valoracion(osv.Model):
    _name = 'jpv_conf.objeto_valoracion'
    _description = u'objetos relacionados de la valoración'
    _rec_name = 'refencia'

    _columns = {
        'refencia': fields.char('Referencia del Controlador', required=True),
        
        'model_id': fields.many2one(
                                    'ir.model',
                                    'Objeto a aplicar',
                                    required=True),
        
        'preguntas_ids': fields.one2many(
                                    'jpv_conf.valoracion_preguntas',
                                    'obj_valoracion_id',
                                    'Preguntas', copy=True),
            
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado')
                }
    
    _sql_constraints = [
        (   'refencia_controlador', 
            'unique (refencia)', 
            'El refencia jpv_conf.objeto_valoracion ya existe en la Base de Datos'),
        ]

    _defaults = {
        'active': True,
        }
    
class jpv_conf_valoracion_pregunta(osv.Model):
    _name = 'jpv_conf.valoracion_preguntas'
    _description = u'Preguntas de la valoración'
    _rec_name = 'nombre'
    _order = 'sequence,id'

    
    _columns = {
        'obj_valoracion_id': fields.many2one(
                                'jpv_conf.objeto_valoracion',
                                'Valoración',
                                ondelete='cascade'),

        
        'field_ids':fields.many2many(
                                'ir.model.fields',
                                'jpv_conf_valoracion_preguntas_rel',
                                'items_id','field_id',
                                'Atributos del Objeto',
                                required=True
                                ),
                                        
        'nombre': fields.char('Nombre de la Pregunta', required=True),

        'pregunta_id': fields.many2one(
                                'jpv_conf.valoracion_preguntas',
                                'Pregunta dependiente'),
                                        
        'sequence': fields.integer(string='Sequence'),
        
        'description': fields.html('Descripción'),
        
        'tipo':fields.selection(
                                [('radio', 'Seleccion simple')],
                                'Tipo de Pregunta',required=True),
        # respueatas
        'respuesta_ids': fields.one2many('jpv_conf.valoracion_items_respueta',
            'pregunta_id', 'Types of answers', copy=True),


        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
                            
        'dependiente': fields.boolean(
                            'Dependiente',
                            help='Estatus del registro Activado-Desactivado'),
        
        'dependencias_id':fields.one2many(
                            'jpv_conf.valoracion_dependencia',
                            'pregunta_id',
                            'Dependencias')    
    }

    _defaults = {
        'active': True,
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

    def validar_resultadosData(self,cr,uid,pregunta_data,post,call=None):
        errors = {}
        resultados_data=[]
        dictamen=[]
        for pregunta in pregunta_data:
            if not post.has_key('ing-pregunt_'+str(pregunta.id)):
                name_repuesta=pregunta.tipo+'-'+str(pregunta.id)
                #~ es obligatoria?
                if not pregunta.dependiente or call==True:
                    #~ existe?
                    if post.has_key(name_repuesta):
                        for respuesta in pregunta.respuesta_ids:
                            if post[name_repuesta]!=None:
                                if post[name_repuesta].isdigit():
                                    if int(post[name_repuesta])==respuesta.id:
                                        dictamen.append(respuesta.state);
                                        #~ la respuesta tiene preguntas dependientes?s
                                        if len(respuesta.dependencia_line)>0:
                                            for pregunta_dep in respuesta.dependencia_line:
                                                #~ la respuesta abre una pregunta?
                                                if pregunta_dep.accion_type=='abre':
                                                    #~ se hace obligatoria la pregunta dependienta con pasarle el call True
                                                    #~ se repite el ciclo
                                                    resultado=self.validar_resultadosData(cr,uid,pregunta_dep.pregunta_id,post,True)
                                                    for state in resultado['dictamen']:
                                                            dictamen.append(state)
                                                    if len(resultado['errors']):
                                                        errors.update(resultado['errors'])
                                                    for resultado in resultado['resultados_data']:
                                                        resultados_data.append(resultado)
                                        if not post.has_key('asignacion_id'):
                                            value={
                                                'tipo_pregunta': pregunta.tipo,
                                                'dictamen_id': False,
                                                'pregunta_id': pregunta.id,
                                                'resp_texto_siple_id': respuesta.id}
                                        else:
                                            value={ 'asignacion_id':post['asignacion_id'],
                                                    'tipo_pregunta': pregunta.tipo,
                                                    'dictamen_id': False,
                                                    'pregunta_id': pregunta.id,
                                                    'resp_texto_siple_id': respuesta.id
                                                    }
                                        resultados_data.append([0, False,value])
                    else:
                        errors.update({pregunta.nombre: ' es obligatorio.'})
        return {'errors':errors,'resultados_data':resultados_data,'dictamen':dictamen}
            
class jpv_conf_valoracion_items_respuesta(osv.Model):
    _name = 'jpv_conf.valoracion_items_respueta'
    _rec_name = 'respuesta'
    _order = 'sequence,id'
    _description = 'Items de respuestas'


    _columns = {
        'respuesta': fields.char("Respuesta",required=True),

        'pregunta_id': fields.many2one(
                                'jpv_conf.valoracion_preguntas',
                                'Preguntas',
                                ondelete='cascade'),
            
        'dependencia_line':fields.one2many(
                                'jpv_conf.valoracion_dependencia',
                                'respuesta_id'),

        'sequence': fields.integer('Label Sequence order'),
        
        'state':fields.selection([('aprobado', 'Aprobado'),
                                ('negado', 'Negado'),
                                ('diferido', 'Diferido'),
                                ('sinEfecto', 'Sin Efecto'),
                                ],
                                'Dictamen de Respuesta de la Valoración'
                                , required=True),
        'mensaje': fields.char("Mensaje"),
        
    }
    
    _defaults = {
        'sequence': 10,
    }
    

    def create(self,cr,uid,values,context=None):
        if 'dependencia_line' in values:
            for i in values['dependencia_line']:
                if i[2] and 'pregunta_id' in i[2]:
                    write_id=self.pool.get('jpv_conf.valoracion_preguntas').write(cr,uid,i[2]['pregunta_id'],{'dependiente':True})
        create_id=super(jpv_conf_valoracion_items_respuesta,self).create(cr,uid,values)
        return create_id
    
    def write(self,cr,uid,ids,values,context=None):
        if 'dependencia_line' in values:
            for i in values['dependencia_line']:
                print i
                if i[2] and 'pregunta_id' in i[2]:
                    write_id=self.pool.get('jpv_conf.valoracion_preguntas').write(cr,uid,i[2]['pregunta_id'],{'dependiente':True})
        write_id=super(jpv_conf_valoracion_items_respuesta,self).write(cr,uid,ids,values)
        return write_id

class jpv_conf_valoracion_pregunta_dependencia(osv.Model):
    _name = 'jpv_conf.valoracion_dependencia'
    _rec_name = 'respuesta_id'
    _order = 'sequence,id'
    _description = 'Preguntas dependientes'


    _columns = {
        
        'pregunta_id': fields.many2one(
                                'jpv_conf.valoracion_preguntas',
                                'Pregunta Dependiente',
                                ondelete='cascade',required=True),
            
        'accion_type': fields.selection([('abre', 'Abre'),
                                         ('cierra', 'Cierra')],
                                        'Relacion',required=True),
        
        'respuesta_id':fields.many2one(
                                'jpv_conf.valoracion_items_respueta',
                                'Respuesta'),
        
        'sequence': fields.integer(string='Sequence'),
    }
    
class jpv_conf_valoracion_pregunta_accion(osv.Model):
    _name = 'valoracion_pregunta_accion'
    _rec_name = 'respuesta_id'
    _order = 'sequence,id'
    _description = 'Acciones de las preguntas de la valoracion'


    _columns = {
            

        'respuesta_id':fields.many2one(
                                'jpv_conf.valoracion_items_respueta',
                                'Respuesta'),
        
        
        'respuesta_accion_id':fields.many2one(
                                'jpv_conf.valoracion_items_respueta',
                                'Acciona Respuesta'),
        
        'sequence': fields.integer(string='Sequence'),
    }

    
