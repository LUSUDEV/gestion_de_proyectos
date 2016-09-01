# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import tools, api
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *
from openerp import tools
from openerp.tools.translate import _
from openerp.addons.ept_planificacion.modelos.ept_plf_comunes import *
from openerp.http import request
from openerp import SUPERUSER_ID

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

class ept_cp_carga_proyecto(osv.osv): 
    _name = 'ept_cp.carga_proyecto'
    _rec_name = 'correlativo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Carga de proyectos'
    
    def cp_monto_disponible(self,cr,uid,ids,field_name,arg,context=None):
        monto={}
        for atributos in self.browse(cr,uid,ids):
            cuentas_objeto=self.pool.get('ept.cuentas')
            cuentas_id=cuentas_objeto.search(cr,uid,[('id','=',int(atributos.cuenta_id))])
            cuentas_datos=cuentas_objeto.browse(cr,uid,cuentas_id,context=context)
            monto[atributos.id]=cuentas_datos['monto_actual']
        return monto
        
    def cp_monto_disponible_mantenimiento(self,cr,uid,ids,field_name,arg,context=None):
        monto_mantenimiento={}
        for atributos in self.browse(cr,uid,ids):
            entidades_objeto=self.pool.get('ept_ent.entidades')
            entidades_id=entidades_objeto.search(cr,uid,[('parent_id','=',int(atributos.partner_id))])
            entidades_data=entidades_objeto.browse(cr,uid,entidades_id)
            monto_disponible_mantenimiento=entidades_data['monto_disp_mantenimiento']
            monto_mantenimiento[atributos.id]=monto_disponible_mantenimiento
        return monto_mantenimiento
    
    def cp_partner_defecto(self,cr,uid,ids, context=None):
        ent_entidades_objeto=self.pool.get('ept_ent.entidades')
        ent_id=ent_entidades_objeto.search(cr,uid,[('user_ids','in',uid)])
        ent_datos=ent_entidades_objeto.browse(cr,uid,ent_id,)
        if len (ent_id)>0:
            return ent_datos['parent_id']
    
    def _get_attachment_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            res[app_id] = self.pool['ir.attachment'].search_count(
                                            cr, 
                                            uid, 
                                            [('res_model', '=', 'ept_cp.carga_proyecto'), ('res_id', '=', app_id)], 
                                            context=context)
        return res
    
    _columns = {
        'state': fields.selection([
                            ('carga', 'Proceso de Carga'),
                            ('evaluacion', 'Valoración'),
                            ('diferido', 'Diferido'),
                            ('aprobado', 'Aprobado'),
                            ('negado', 'Negado'),
                            ('cancelado', 'Cancelado'),
                            ('culminado', 'Culminado'),
                            ], 'Estatus', 
                            readonly=True, 
                            copy=False, 
                            help="Estado en el que se encuentra \
                                 actualmente el proyecto cargado.", 
                            select=True),
        'proyect_mantenimiento': fields.boolean('Proyecto de Mantenimiento',
                                    states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                    help='Seleccionar esta opción si desea\
                                        que el proyecto sea de mantenimiento.' ),
        'correlativo':fields.char(
                            'Codificación FCI',
                            help='Esta es el correlativo asignado al\
                                  proyecto'),
        'partner_id': fields.many2one(
                                'res.partner', 
                                'Entidad', 
                                required=False,
                                ondelete='restrict',
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Seleccione  a la cual\
                                      se le cargara el proyecto'),
        'cuenta_id': fields.many2one(
                                'ept.cuentas', 
                                'Cuenta',
                                ondelete='restrict', 
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Seleccione la cuenta de la cual\
                                      se debitara el monto del proyecto\
                                       a registrar'),
        'nombre_proyecto':fields.text(
                                'Nombre del proyecto ', 
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                size=500,  
                                help='Este es el nombre del  proyecto'),
        'descripcion_proyecto':fields.text(
                                    'Descripción del proyecto', 
                                    required=True, size=500,  
                                    states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                    help='Esta es la descripción del\
                                          proyecto'),
        'tipo_sector_id':fields.many2one(
                                'ept_cp.tipo_sectores',
                                'Tipo de sector',
                                ondelete='restrict',
                                required=True,
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Tipo de sector al cual pertenece\
                                     el proyecto a registrar'),
        'categoria_id': fields.many2one(
                                'ept_cp.tipo_sectores', 
                                'Categoría', 
                                ondelete='restrict',
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Categoría a la cual pertenece\
                                     el proyecto a registrar'),
        'subcategoria_id': fields.many2one(
                                    'ept_cp.tipo_sectores', 
                                    'Subcategoría', 
                                    ondelete='restrict',
                                    required=True, 
                                    states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                    help='Subcategoría a la cual\
                                    pertenece el proyecto a registrar'),
        'fecha_inicio':fields.date(
                            'Fecha de Inicio', 
                            required=True, 
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help='Fecha de Inicio del Proyecto'),
        'fecha_fin': fields.date(
                            'Fecha de Fin', 
                            required=True, 
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help='Fecha de Finalización del Proyecto'),
        'monto_disponible':fields.function(
                            cp_monto_disponible,
                            'Monto Disponible',
                            type='float',
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            ),
        'monto_disponible_mantenimiento':fields.function(
                                        cp_monto_disponible_mantenimiento,
                                        'Monto Disponible de Mantenimiento',
                                        type='float',
                                        ),
        'monto_proyecto':fields.float(
                                'Monto del proyecto',  
                                required=True,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Monto total del proyecto a cargar'),
        'monto_tomado_mantenimiento':fields.float(
                                'Monto tomado mantenimiento',  
                                help='Monto tomado del total de mantenimiento'),
        'duracion_proyec': fields.char(
                                'Duración del proyecto',  
                                readonly=True,
                                help='Duración del proyecto'),
        'obra_civil': fields.boolean(
                                    'Obra Civil',
                                    states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                    help=''),
        'tipo_obra': fields.selection([
                            ('construccion', 'Construcción Inicial'),
                            ('ampliacion', 'Ampliación'),
                            ('rehabilitacion', 'Rehabilitación o Mejora'),
                            ], 'Tipo de Obra', 
                            readonly=False,
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            copy=False, 
                            help="Tipo de obra que se realizara mediante\
                                el proyecto a registrar.", 
                            select=True),
        'cantidad_estimada_obra': fields.float(
                                'Cantidad Estimada',  
                                readonly=False,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help=''),
        'unidad_medicion_obra':fields.many2one(
                                        'ept_cp.unidades_obra_civil', 
                                        'Unidad', 
                                        required=False, 
                                        states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                        help=''),
        'equipos': fields.boolean(
                            'Adquisición de Equipos',
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help=''),
        'equipos_ids': fields.one2many(
                                'ept_cp.equipos', 
                                'proyecto_id', 
                                'Equipo', 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Especificaciones de los equipos a\
                                 adquirir mediante el proyecto a registrar'),
        'maquinaria': fields.boolean(
                            'Adquisición de Maquinarias',
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help=''),
        'maquinaria_ids': fields.one2many(
                                'ept_cp.maquinaria', 
                                'proyecto_id', 
                                'Maquinarias', 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Especificaciones de las maquinarias\
                                 a adquirir mediante el proyecto a\
                                  registrar'),
        'materiales_consumo': fields.boolean(
                            'Adquisición de Materiales de Consumo',
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help=''),
        'materiales_ids': fields.one2many(
                                'ept_cp.materiales_consumo', 
                                'proyecto_id', 
                                'Vehiculos', 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Especificaciones de los materiales\
                                 de consumo a adquirir mediante el\
                                  proyecto a registrar'),
        'vehiculos': fields.boolean(
                            'Adquisición de Vehiculos',
                            states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                            help=''),
        'vehiculos_ids': fields.one2many(
                                'ept_cp.vehiculo', 
                                'proyecto_id', 
                                'Vehiculos', 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Especificaciones de los vehiculos\
                                 a adquirir mediante el proyecto a\
                                  registrar'),
        'semoviente': fields.boolean('Semoviente',
                                      states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},  
                                        ),
        'semoviente_ids': fields.one2many(
                                'ept_cp.semovientes_caracteristicas', 
                                'proyecto_id', 
                                'Semovientes', 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Especificaciones de los semovientes\
                                  a adquirir mediante el\
                                  proyecto a registrar'),
        'benef_masculino': fields.integer(
                                'Beneficiarios Masculinos',  
                                readonly=False, 
                                required=True,   
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Beneficiarios masculinos que \
                                    generara el proyecto a registrar'),
        'benef_femenino': fields.integer(
                                'Beneficiarios Femeninos',  
                                readonly=False,
                                required=True,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Beneficiarios femeninos que \
                                    generara el proyecto a registrar'),
        'total_benef': fields.integer(
                                'Total Beneficiarios ',  
                                readonly=True,
                                help='Total de beneficiarios que \
                                    generara el proyecto a \
                                    registrar'),
        'empleo_direct_masculino': fields.integer(
                                'Empleo Directo Masculinos',  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                readonly=False,  
                                required=True,  
                                help='Empleos directos masculinos que \
                                    generara el proyecto a registrar'),
        'empleo_direct_femenino': fields.integer(
                                'Empleo Directo Femeninos',  
                                readonly=False,
                                required=True,   
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Empleos directos femeninos que \
                                    generara el proyecto a registrar'),
        'empleo_direct_total': fields.integer(
                                'Total Empleo Directo',  
                                readonly=True,
                                help='Total de Empleos directos  que \
                                    generara el proyecto a registrar'),
        'empleo_indirect_masculino': fields.integer(
                                'Empleo Indirecto Masculinos',  
                                readonly=False,
                                required=True,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Empleos indirectos masculinos que \
                                    generara el proyecto a registrar'),
        'empleo_indirect_femenino': fields.integer(
                                'Empleo Indirecto Femeninos',  
                                readonly=False, 
                                required=True,   
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Empleos indirectos femeninos que \
                                    generara el proyecto a registrar'),
        'empleo_indirect_total': fields.integer(
                                'Total empleo Indirecto',  
                                readonly=True,  
                                help='Total de Empleos indirectos  que \
                                    generara el proyecto a registrar'),
        'estado_id': fields.many2one(
                                'ept_ent.estados', 
                                'Estado',
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Estado en el cual se llevara a \
                                     cabo el proyecto a registrar.'),
        'municipio_id': fields.many2one(
                                'ept_ent.municipios', 
                                'Municipio',
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Municipio en el cual se llevara a \
                                     cabo el proyecto a registrar.'),
        'parroquia_id': fields.many2one(
                                'ept_ent.parroquias', 
                                'Parroquia',
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                required=True, 
                                help='Parroquia en el cual se llevara a \
                                     cabo el proyecto a registrar.'),
        'sector': fields.char(
                                'Sector',  
                                readonly=False,
                                required=True,
                                help='Sector en el cual se llevara a cabo el proyecto'),
        'coord_este': fields.integer(
                                'Coordenadas Este Inicio',  
                                readonly=False,
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Coordenadas este iniciales de la ubicación\
                                 del proyecto a registrar.'), 
        'coord_norte': fields.integer(
                                'Coordenadas Norte Inicio',  
                                readonly=False,
                                required=True, 
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Coordenadas Norte iniciales de la ubicación\
            del proyecto a registrar.'),
        'coord_este_f': fields.integer(
                                'Coordenadas Este Final',  
                                readonly=False,
                                required=True,
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Coordenadas este finales de la ubicación\
                                 del proyecto a registrar.'), 
        'coord_norte_f': fields.integer(
                                'Coordenadas Norte Final',  
                                readonly=False,
                                required=True,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],}, 
                                help='Coordenadas Norte finales de la ubicación\
                                 del proyecto a registrar.'),
        'huso_id': fields.many2one(
                                'ept_ent.husos', 
                                'Huso Inicial',
                                readonly=False,
                                required=True,  
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                               help='Este es el huso de las coordenadas iniciales donde esta\
                                    ubicado el proyecto a registrar'),
        'husof_id': fields.many2one(
                                'ept_ent.husos', 
                                'Huso Final',
                                readonly=False,
                                required=False,  
                               states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                help='Este es el huso de las coordenadas finales donde esta\
                                ubicado el proyecto a registrar'),
        'aval': fields.boolean('Aval' ),
        'coordenada': fields.boolean('coordenada' ),
        
        'fotos_ids':fields.many2many('ir.attachment',
                                    'ept_cp_fotos_rel',
                                    'proyecto_id',
                                    'foto_id',
                                    'Fotografías',
                                    required=True,
                                    states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},
                                    ),
        'foto_id' : fields.one2many('ir.attachment', 'foto_id', 
                                'Archivos',
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},),
        
        'aval_ids':fields.one2many('ir.attachment', 'aval_id', 
                                'Aval',
                                states={'evaluacion': [('readonly', True)],'cancelado': [('readonly', True)],'negado': [('readonly', True)],'culminado': [('readonly', True)],},),
        'movimiento_ids':fields.many2many('ept.movimientos_cuentas', 
                                          'ept_cp_proyecto_movimiento', 
                                          'proyecto_id', 
                                          'movimiento_id',
                                          'Movimientos',
                                          states={'evaluacion': [('readonly', True)]}, ),
        'historial_ids': fields.one2many(
                                'ept_cp.historial_proyecto', 
                                'proyecto_id', 
                                'Historial', 
                                states={'evaluacion': [('readonly', True)]},
                                help='Historial de los mensajes emitidos para\
                                     el proyecto actual'),
        'periodo_id': fields.many2one(
                            'ept_plf.periodos', 
                            'Periodo', 
                            required=False,
                            ondelete='restrict',
                            help='Periodo en el cual se registro el proyecto'),
        'ciclo_id': fields.many2one(
                            'ept_plf.etapas', 
                            'Ciclo', 
                            required=False,
                            ondelete='restrict',
                            help='Ciclo en el cual se registro el proyecto'),
        'avance':fields.boolean('Proyecto con avance'),
        'editar_migracion':fields.boolean('Migración'),
        
        'cartas_proyecto' : fields.one2many('ir.attachment', 'proyecto_carta_id', 
                                'Cartas',
                               ),
        'attachment_number': fields.function(
                                    _get_attachment_number, 
                                    string='Number of Attachments', 
                                    type="integer"),
        'active':fields.boolean('Activo'),
        'solicitud_cambio':fields.boolean('Solicitud'),
        
        
                }
    _defaults = {
        'state':'carga',
        'partner_id':cp_partner_defecto,
        'avance':False,
        'editar_migracion':False,
        'active':True,
        'solicitud_cambio':False,
        }
    _order = 'create_date desc, id desc'
    
    
    def action_get_attachment_tree_view(self, cr, uid, ids, context=None):
        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'action_attachment')
        action = self.pool.get(model).read(cr, uid, action_id, context=context)
        action['context'] = {'default_res_model': self._name, 'default_res_id': ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', ids)])
        return action
    
    def cp_validar_fecha_inicio(self, cr, uid, ids, fecha_inicio, 
                                                        context=None):
        fechas={}
        mensaje={}
        if fecha_inicio:
            format="%Y"
            anio_actual=date.today()
            anio_actual=anio_actual.strftime(format)
            ano_inicio=fecha_inicio.split('-')
            if int(ano_inicio[0])==int(anio_actual):
                hoy=date.today()
                fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_inicio =datetime.date(fecha_inicio)
                if cmp(hoy,fecha_inicio)==1:
                    mensaje={
                        'title':('Error de fecha'),
                        'message':('La fecha de inicio no puede ser menor\
                                    a la fecha de hoy'),
                        }
                    fechas={
                        'fecha_inicio':'',
                        'fecha_fin':'',
                        }
                else:
                    fechas={
                        'fecha_fin':'',
                        }
            else:
                mensaje={
                    'title':('Error de fecha'),
                    'message':('La fecha de inicio debe estar comprendida dentro del periodo físcal'),
                    }
                fechas={
                    'fecha_inicio':'',
                    'fecha_fin':'',
                    }
        return {
            'warning':mensaje,
            'value':fechas
                }
    
    
    def cambio_status_diferido(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'diferido'},0)
    
    def cp_monto_disponible(self,cr,uid,ids,cuenta_id,context=None):
        monto={}
        cuentas_objeto=self.pool.get('ept.cuentas')
        cuentas_id=cuentas_objeto.search(cr,uid,[('id','=',cuenta_id)])
        cuentas_datos=cuentas_objeto.browse(cr,uid,cuentas_id,context=context)
        monto={
            'monto_disponible':cuentas_datos['monto_actual'],
            }
        return {
            'value':monto
                }
    
    def cp_limpiar_campos_mantenimiento(self,cr,uid,ids,mantenimiento):
        datos={}
        if mantenimiento==True:
            datos={
                        'obra_civil':'',
                        'equipos':'',
                        'maquinaria':'',
                        'vehiculos':'',
                        'materiales_consumo':'',
                        'semoviente':'',
                        }
        return datos
    
                
    def cp_monto_disponible_mantenimieno(self,cr,uid,ids,proyecto_mantenimiento,partner_id,periodo_id,context=None):
        mantenimiento={}
        if proyecto_mantenimiento==True:
            entidades_objeto=self.pool.get('ept_ent.entidades')
            entidades_id=entidades_objeto.search(cr,uid,[('parent_id','=',int(partner_id))])
            entidades_data=entidades_objeto.browse(cr,uid,entidades_id)
            monto_disponible_mantenimiento=entidades_data['monto_disp_mantenimiento']
            mantenimiento['monto_disponible_mantenimiento']=monto_disponible_mantenimiento
        return {'value':mantenimiento}
        
    def cp_buscar_periodo_id(self,cr,uid,ids,partner,context=None):
        periodo={}
        if partner:
            periodo_objeto=self.pool.get('ept_plf.periodos')
            actividad="CARGA DE PROYECTOS"
            periodo_id=periodo_objeto.plf_control_actividades(cr, uid, [],
                                                             int(partner),
                                                               actividad,)
            if periodo_id.keys()[0]!='periodo':
                raise osv.except_osv(
                ('Alerta!'),
                (u'La carga de proyecto no esta habilitada para la fecha de hoy.'))
            else:
                periodo_id=int(periodo_id['periodo'])
                periodo={
                    'periodo_id':periodo_id,
                    }
        return {
            'value':periodo
                }
        
    def cp_validar_monto_proyecto(self,cr,uid,ids,monto_disponible,
                                                monto_proyecto,context=None):
        mensaje={}
        valores={}
        
        if monto_proyecto>monto_disponible:
            valores={
                'monto_proyecto':''
                }
            mensaje={
                    'title':('Error'),
                    'message':('Verifique el monto del proyecto, este no puede\
                                ser mayor al monto disponible en su cuenta'),
                    }
        return {
            'warning':mensaje,
            'value':valores
                }
    
    def cp_validar_fechas_proyecto(self,cr,uid,ids,fecha_inicio,
                                                   fecha_fin, 
                                                   context=None):
        fechas={}
        duracion={}
        mensaje={}
        if fecha_fin:
            format="%Y"
            anio_actual=date.today()
            anio_actual=anio_actual.strftime(format)
            ano_inicio=fecha_fin.split('-')
            if int(ano_inicio[0])==int(anio_actual):
                if validar_fecha(fecha_inicio, fecha_fin).values()[0]!={}:
                    fechas=validar_fecha(fecha_inicio, fecha_fin).values()[1]
                    mensaje=validar_fecha(fecha_inicio, fecha_fin).values()[0]
                    return {
                        'warning':mensaje,
                        'value':fechas
                            }
                else:
                    duracion={
                        'duracion_proyec':calculo_tiempo(fecha_inicio,fecha_fin)
                        }
                    return {
                        'value':duracion
                            }
            else:
                mensaje={
                    'title':('Error de fecha'),
                    'message':('La fecha final del proyecto debe estar comprendida dentro del periodo físcal'),
                    }
                fechas={
                    'fecha_fin':'',
                    }
                return {
                        'warning':mensaje,
                        'value':fechas
                            }
    
    def cp_filtro_estados(self,cr,uid,ids,partner_id,context=None):
        dominio={}
        cuenta={}
        mensaje={}
        if partner_id:
            cuentas_objeto=self.pool.get('ept.cuentas')
            cuentas_id=cuentas_objeto.search(cr,uid,
                            [('tipo_cuenta_id.name','=','PLAN DE INVERSIÓN'),('partner_id','=',partner_id)])
            cuentas_datos=cuentas_objeto.browse(cr,uid,cuentas_id,
                                                                context=context)
            if len(cuentas_datos)==1:
                cuenta={
                    'cuenta_id':cuentas_datos['id']
                    }
            else:
                mensaje={
                    'title':('Aviso!'),
                    'message':('No posee una cuenta de PLAN DE INVERSIÓN asignada.'),}
            entidades_objeto=self.pool.get('ept_ent.entidades')
            entidades_id=entidades_objeto.search(cr,uid,
                                                [('parent_id','=',int(partner_id))])
            entidades_datos=entidades_objeto.browse(cr,uid,entidades_id,
                                                               context=context)
            ids_estados=[]
            for id_estado in entidades_datos['estado_ids']:
                ids_estados.append(int(id_estado))
            dominio={'estado_id': [('id', '=', list(ids_estados))]}
        else:
            dominio={'estado_id': [('id', '=', list([]))]}
        return {'value':cuenta,'domain':dominio,'warning':mensaje,}
        
    def cp_filtro_municipios(self,cr,uid,ids,partner_id,estado_id,campo,
                                                                context=None):
        dominio={}
        if partner_id:
            husos_objeto=self.pool.get('ept_ent.estados')
            husos_id=husos_objeto.search(cr,uid,
                                                [('id','=',estado_id)])
            husos_datos=husos_objeto.browse(cr,uid,husos_id,
                                                        context=context)
            list_id_huso=[]
            for huso in husos_datos['husos_ids']:
                list_id_huso.append(int(huso))

            
            entidades_objeto=self.pool.get('ept_ent.entidades')
            entidades_id=entidades_objeto.search(cr,uid,
                                                [('parent_id','=',partner_id)])
            entidades_datos=entidades_objeto.browse(cr,uid,entidades_id,
                                                               context=context)
            ids_municipios=[]
            municipios_objeto=self.pool.get('ept_ent.municipios')
            municipios_id=municipios_objeto.search(cr,uid,
                                            [('estado_id','=',int(estado_id))])
            for ids in entidades_datos['municipio_ids']:
                ids_municipios.append(int(ids))
            dominio={'municipio_id': [('id', '=', list(set(ids_municipios) & set(municipios_id)))],'huso_id': [('id', '=',list(list_id_huso))],'husof_id': [('id', '=',list(list_id_huso))],}
        else:
            dominio={'municipio_id': [('id', '=', list([]))],'huso_id': [('id', '=',list([]))],'husof_id': [('id', '=',list([]))],}
        return {'value':{campo:''},'domain':dominio}
            
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
                
    def cp_obra_civil(self,cr,uid,ids,obra_civil,subcategoria_id,context=None):
        mensaje={}
        campos={}
        if obra_civil:
            if not subcategoria_id:
                mensaje={
                    'title':('Error'),
                    'message':('Debe seleccionar una subcategoria'),
                    }
                campos={
                    'obra_civil':'',
                    'tipo_obra':'',
                    'cantidad_estimada_obra':'',
                    'unidad_medicion_obra':'',
                    }
                return {'warning':mensaje,'value':campos}
        campos={
            'tipo_obra':'',
            'cantidad_estimada_obra':'',
            'unidad_medicion_obra':'',
                }
        return {
            'value':campos
                }
    
    def cp_total_beneficios_proyecto(self,cr,uid,ids,masculino,campo_valor,
                                                                  femenino,
                                                               campo_total,
                                                             context=None):
        mensaje={}
        campos={}
        if masculino<0 or femenino<0:
            mensaje={
                'title':('Error de valores'),
                'message':('Los valores a introducir en este campo\
                            deben ser mayor a cero'),
                }
            campos={
                campo_valor:'',
                }
            return {'warning':mensaje,'value':campos}
        lista_numeros=[masculino,femenino]                                                
        total={
            campo_total:int(generar_total(lista_numeros))
            }
        return {
                'value':total
                    }
    
    def cp_filtrar_unidades_medidas (self, cr, uid, ids, subcategoria,tipo_obra):
        plf_montos_objeto=self.pool.get('ept_cp.montos_minimos_construccion')
        montos_ids=plf_montos_objeto.search(cr,uid,
                        [('subcategoria_id','=',int(subcategoria))])
        id_unidades=[]
        montos_datos=plf_montos_objeto.browse(cr,uid,montos_ids)
        for registros in montos_datos:
            id_unidades.append(int(registros.unidades_id))
        dominio={'unidad_medicion_obra': [('id', '=', list(id_unidades))]}
        return dominio
    
    def cp_validar_requerimiento_aval(self, cr, uid, ids,subcategoria_id,
                                                               tipo_obra, 
                                                           context=None):
        campos={'aval':False}
        mensaje={}
        dominio={'unidad_medicion_obra': [('id', '=', [])]}
        if tipo_obra:
            ent_tipo_sectores_objeto=self.pool.get('ept_cp.tipo_sectores')
            ent_id=ent_tipo_sectores_objeto.search(cr,uid,
                                            [('id','=',int(subcategoria_id))])
            ent_datos=ent_tipo_sectores_objeto.browse(cr,uid,ent_id,
                                                    context=context)
            if tipo_obra=='construccion':
                dominio=self.cp_filtrar_unidades_medidas (cr, uid, ids,
                                                          subcategoria_id,
                                                          tipo_obra)
                if ent_datos['aval_constr']==True:
                    campos={'aval':True}
                    mensaje={
                        'title':('Aviso!'),
                        'message':('Este proyecto requiere de un aval'),
                            }
            if tipo_obra== 'rehabilitacion': 
                dominio=self.cp_filtrar_unidades_medidas (cr, uid, ids,
                                                          subcategoria_id,
                                                          tipo_obra)
                if ent_datos['aval_rehab']==True:
                    campos={'aval':True}
                    mensaje={
                        'title':('Aviso!'),
                        'message':('Este proyecto requiere de un aval'),
                            }
            if tipo_obra== 'ampliacion':
                dominio=self.cp_filtrar_unidades_medidas (cr, uid, ids,
                                                           subcategoria_id,
                                                           tipo_obra)
                if ent_datos['aval_ampli']==True:
                    campos={'aval':True}
                    mensaje={
                        'title':('Aviso!'),
                        'message':('Este proyecto requiere de un aval'),
                            }
        return {'warning':mensaje,'value':campos,'domain':dominio}
    
    def cp_mensaje_historial_aval(self, cr, uid, ids,aval,vals,context=None):
        mensaje={}
        historial=[]
        descripcion='El proyecto que desea registrar requiere de un aval \
                    para poder ser aprobado'
        descripcion2='Usted ha registrado un aval para este proyecto'
        if aval==True:
            if len(vals)==0:
                historial.append([0,False,{'descripcion':descripcion }])
            else:
                historial.append([0,False,{'descripcion':descripcion2 }])
        return historial

    def cp_mensaje_historial_monto_minimo(self, cr, uid, ids,
                                          obra_civil,
                                          subcategoria_id,tipo_obra,
                                          cantidad,monto_proyecto,
                                          equipos,equipos_ids,maquinaria,
                                          maquinaria_ids,vehiculos,vehiculos_ids,
                                          materiales_consumo,materiales_ids,
                                          semoviente,semoviente_ids,
                                          unidades,
                                          context=None):
        mensaje={}
        historial=[]
        monto_requerido=0.00
        descripcion1='Debería seguir de cerca el presupuesto asignado para el \
                    proyecto ya que el mismo es ajustado respecto a la meta \
                    estimada.'
        descripcion2='Debería considerar aumentar un poco el presupuesto \
                    asignado para ese proyecto para que de esa manera aumenten\
                     sus probabilidades de éxito respecto al mismo.'
        descripcion3='Debería considerar aumentar significativamente el \
                    presupuesto asignado para ese proyecto para que de esa \
                    manera aumenten sus probabilidades de éxito respecto al \
                    mismo.'
        if obra_civil==True:
            cp_construc_obj=self.pool.get('ept_cp.montos_minimos_construccion')
            cp_construc_id=cp_construc_obj.search(cr,uid,
                                    [('subcategoria_id','=',subcategoria_id),('unidades_id','=',int(unidades))],
                                    context=context)
            cp_cosntruc_datos=cp_construc_obj.browse(cr,uid,cp_construc_id,
                                                            context=context)
            if tipo_obra=='construccion':
                monto_requerido=cp_cosntruc_datos['monto_construc']*cantidad
            if tipo_obra=='rehabilitacion':
                monto_requerido=cp_cosntruc_datos['monto_rehabilit']*cantidad
            if tipo_obra=='ampliacion':
                monto_requerido=cp_cosntruc_datos['monto_ampliac']*cantidad
        if equipos==True:
            for i in equipos_ids:
                cp_equipo_obj=self.pool.get('ept_cp.montos_minimos_equipos')
                cp_equipo_id=cp_equipo_obj.search(cr,
                                            uid,[('id','=',int(i.uso_id))],
                                            context=context)
                cp_equipo_datos=cp_equipo_obj.browse(cr,uid,
                                                    cp_equipo_id,
                                                    context=context) 
                monto_requerido+=cp_equipo_datos['monto_minimo']*i.cantidad
        if maquinaria==True:
            for m in maquinaria_ids:
                cp_maqui_obj=self.pool.get('ept_cp.montos_minimos_maquinaria')
                cp_maqui_id=cp_maqui_obj.search(cr,uid,
                                                [('id','=',int(m.uso_id))],
                                                context=context)
                cp_maqui_datos=cp_maqui_obj.browse(cr,uid,cp_maqui_id,
                                                            context=context) 
                monto_requerido+=cp_maqui_datos['monto_minimo']*m.cantidad
        if vehiculos==True:
            for v in vehiculos_ids:
                cp_vehiculo_obj=self.pool.get('ept_cp.montos_minimos_vehiculo')
                cp_vehiculo_id=cp_vehiculo_obj.search(cr,uid,
                                                [('id','=',int(v.tipo_id))],
                                                context=context)
                cp_vehic_datos=cp_vehiculo_obj.browse(cr,uid,cp_vehiculo_id,
                                                            context=context) 
                monto_requerido+=cp_vehic_datos['monto_minimo']*v.cantidad
        if materiales_consumo==True:
            for mc in materiales_ids:
                cp_mc_obj=self.pool.get('ept_cp.montos_minimos_materiales_consumo')
                cp_mc_id=cp_mc_obj.search(cr,uid,[('id','=',int(mc.uso_id))]
                                                              ,context=context)
                cp_mc_datos=cp_mc_obj.browse(cr,uid,cp_mc_id,context=context) 
                monto_requerido+=cp_mc_datos['monto_minimo']*mc.cantidad
        if semoviente==True:
            for sm in semoviente_ids:
                cp_sem_obj=self.pool.get('ept_cp.semovientes')
                cp_sem_id=cp_sem_obj.search(cr,uid,[('id','=',int(sm.especie_id))]
                                                              ,context=context)
                cp_sem_datos=cp_sem_obj.browse(cr,uid,cp_sem_id,context=context) 
                monto_requerido+=cp_sem_datos['monto_minimo']*sm.cantidad
        if monto_requerido>monto_proyecto:
            if monto_proyecto>monto_requerido*0.90:
                historial.append([0,False,{'descripcion':descripcion1 }])
            if monto_proyecto>monto_requerido*0.70:
                historial.append([0,False,{'descripcion':descripcion2 }])
            if monto_proyecto<monto_requerido*0.70:
                historial.append([0,False,{'descripcion':descripcion3 }])
        return historial
            
    def cp_subcaterogia(self,cr,uid,ids,subcategoria):
        datos={
                'semoviente':False,
                'coordenada':False,
                'obra_civil':False,
                'coord_este_f':'',
                'coord_norte_f':'',
                'husof':'',
            }
        if subcategoria:
            sectores_objeto=self.pool.get('ept_cp.tipo_sectores')
            sectores_id=sectores_objeto.search(cr,uid,
                                                [('id','=',int(subcategoria)),
                                                 ('coordenadas','=','True')])
            sectores_datos=sectores_objeto.browse(cr,uid,sectores_id)
            if len(sectores_datos)==1:
                datos={
                    'coordenada':True,
                    'obra_civil':'',
                    'semoviente':False,
                    }
        return {'value':datos}
    
    def cp_porcentaje_mantenimientto(self,cr,uid,ids,periodo,entidad,monto,context=None):
        entidades_objeto=self.pool.get('ept_ent.entidades')
        entidades_id=entidades_objeto.search(cr,uid,[('parent_id','=',int(entidad))])
        entidades_data=entidades_objeto.browse(cr,uid,entidades_id)
        monto_dispo='%.2f' % entidades_data['monto_disp_mantenimiento']
        if float(monto)>float(monto_dispo):
            raise osv.except_osv(
                ('Alerta!'),
                (u'Este proyecto sobrepasa el monto maximo para proyectos de mantenimiento.'))
        else:
            return True
    
    
        
    def cp_historial_many2one(self,cr,uid,ids,dic,campo,valor_viejo,valor_nuevo,context=None):
        fields=self.pool.get('ir.model.fields')
        
        
        fields_id=fields.search(cr,uid,[('name','=',campo,),('model','=','ept_cp.carga_proyecto')])
        fields_datos=fields.browse(cr,uid,fields_id)
        
        if valor_viejo==False:
            valor_viejos='No'
        else:
            
            valor_viejos=valor_viejo[dic]
        mensaje=str(fields_datos['field_description'])+': '+str(valor_viejos)+' para '+str(valor_nuevo[dic])+',  '
        return mensaje
    
    def cp_historial_boolean(self,cr,uid,ids,dic,campo,valor_viejo,valor_nuevo):
        if valor_viejo==False:
            valor_viejo='No'
        else:
            valor_viejo='Si'
        if valor_nuevo==False:
            valor_nuevo='No'
        else:
            valor_nuevo='Si'
        fields=self.pool.get('ir.model.fields')
        fields_id=fields.search(cr,uid,[('name','=',campo,),('model','=','ept_cp.carga_proyecto')])
        fields_datos=fields.browse(cr,uid,fields_id)
        mensaje=str(fields_datos['field_description'])+': '+str(valor_viejo)+' para '+str(valor_nuevo)+',  '
        return mensaje
    
    def cp_historial_modificaciones (self, cr, uid, ids, vals,campos_viejos,valores):
        
        campos={
            'nombre_proyecto':{'tipo':'char','name':''},
            'descripcion_proyecto':{'tipo':'char','name':''},
            'tipo_sector_id':{'tipo':'many2one','name':'name'},
            'categoria_id':{'tipo':'many2one','name':'name'},
            'subcategoria_id':{'tipo':'many2one','name':'name'},
            'fecha_inicio':{'tipo':'char','name':''},
            'fecha_fin':{'tipo':'char','name':''},
            'obra_civil':{'tipo':'boolean','name':''},
            'tipo_obra':{'tipo':'char','name':''},
            'cantidad_estimada_obra':{'tipo':'char','name':''},
            'unidad_medicion_obra':{'tipo':'char','name':'unidad'},
            'equipos':{'tipo':'boolean','name':''},
            'maquinaria':{'tipo':'boolean','name':''},
            'materiales_consumo':{'tipo':'boolean','name':''},
            'vehiculos':{'tipo':'boolean','name':''},
            'semoviente':{'tipo':'boolean','name':''},
            'benef_masculino':{'tipo':'char','name':''},
            'benef_femenino':{'tipo':'char','name':''},
            'empleo_direct_masculino':{'tipo':'char','name':''},
            'empleo_direct_femenino':{'tipo':'char','name':''},
            'empleo_indirect_masculino':{'tipo':'char','name':''},
            'empleo_indirect_femenino':{'tipo':'char','name':''},
            'estado_id':{'tipo':'many2one','name':'estado'},
            'municipio_id':{'tipo':'many2one','name':'municipio'},
            'municipio_id':{'tipo':'many2one','name':'municipio'},
            'parroquia_id':{'tipo':'many2one','name':'parroquia'},
            'coord_este':{'tipo':'char','name':''},
            'coord_norte':{'tipo':'char','name':''},
            'coord_este_f':{'tipo':'char','name':''},
            'coord_norte_f':{'tipo':'char','name':''},
            'huso_id':{'tipo':'many2one','name':'huso'},
            'husof_id':{'tipo':'many2one','name':'huso'},
            'equipos_ids':{'tipo':'one2many','name':''},
            'maquinaria_ids':{'tipo':'one2many','name':''},
            'vehiculos_ids':{'tipo':'one2many','name':''},
            'materiales_ids':{'tipo':'one2many','name':''},
            'semoviente_ids':{'tipo':'one2many','name':''},
            'proyect_mantenimiento':{'tipo':'boolean','name':''},
            'sector':{'tipo':'char','name':''},
        }
        mensaje={}
        cont=0
        mensaje="Usted ha modificado los siguientes campos del proyecto: "
        if len(valores)>=1:
            proyecto_data=self.browse(cr,uid,ids)
            for value in valores:
                dic=campos[value].values()[0]
                if campos[value].values()[1]=='many2one':
                    mensaje=mensaje+str(self.cp_historial_many2one(cr,uid,ids,dic,value,campos_viejos[cont],proyecto_data[value]))
                if campos[value].values()[1]=='char':
                    fields=self.pool.get('ir.model.fields')
                    fields_id=fields.search(cr,uid,[('name','=',value,),('model','=','ept_cp.carga_proyecto')])
                    fields_datos=fields.browse(cr,uid,fields_id)
                    mensaje=mensaje+str(fields_datos['field_description'])+': '+str(campos_viejos[cont])+' para '+str(proyecto_data[value])+',  '
                if campos[value].values()[1]=='boolean':
                    mensaje=mensaje+str(self.cp_historial_boolean(cr,uid,ids,dic,value,campos_viejos[cont],proyecto_data[value]))
                if campos[value].values()[1]=='one2many':
                    fields=self.pool.get('ir.model.fields')
                    fields_id=fields.search(cr,uid,[('name','=',value,),('model','=','ept_cp.carga_proyecto')])
                    fields_datos=fields.browse(cr,uid,fields_id)
                    mensaje=mensaje+str(fields_datos['field_description'])+',  '
                cont+=1
            cp_historial_obj=self.pool.get('ept_cp.historial_proyecto')
            if type(ids)==list:
                ids=ids[0]
            mensaje={
                'descripcion':mensaje,
                'proyecto_id':ids,
                }
            cp_historial_obj.create(cr,uid,mensaje)
        return True
    
    def cp_cambio_state_evaluacion(self,cr,uid,ids,vals,periodo,ciclo,entidad,context=None):
        periodos_obj = self.pool.get('ept_plf.periodos')
        if len(vals)>0:
            actividad='REPARACIÓN DE PROYECTOS'
            reparacion=periodos_obj.plf_control_actividades(cr, uid, [],entidad,actividad,int(ciclo),int(periodo))
            if 'periodo' in reparacion.keys():
                return True
            else:
                mensaje={
                    'title':('Error'),
                    'message':('La actividad de '+actividad+' no esta habilitada'),
                        }
                return {'warning':mensaje}
    
    def editar_dict_url_tree(self, cr, uid, ids, context=None):
        dictamen=self.browse(cr, uid, ids, context=context)[0]
        if dictamen.tipo_valoracion=='valoracion_coordenadas':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas','valoracion_coordenadas')
        if dictamen.tipo_valoracion=='valoracion_general':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_general','valoracion_general')
        if dictamen.tipo_valoracion=='valCoordenadasUre':
            url = "/valoracion/dictamen/%s/%s/%s/%s" % (dictamen.id,dictamen.proyecto_id.id,'valoracion_coordenadas_ures','valCoordenadasUre')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new',
        }
   
    def crear_ficha_proyecto(self,cr,uid,ids,context=None):
        url='descargar/ficha_proyecto/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def crear_carta_cambio_monto(self,cr,uid,carta_x_firmar_data,context=None):
        reportname='ept_carga_proyectos.cambio_monto_proyecto_qweb'
        proyecto_id=self.search(cr,uid,[('id','=',int(carta_x_firmar_data['objeto_principal_id']))])
        proyecto_data=self.browse(cr,uid,proyecto_id)
        docids=[]
        hoy=date.today()
        entidades_obj = self.pool.get('ept_ent.entidades')
        entidades_id=entidades_obj.search(cr,uid,[('parent_id','=',int(proyecto_data['partner_id']))])
        entidades_data=entidades_obj.browse(cr,uid,entidades_id)
        montos_proyectos=carta_x_firmar_data['objeto_rastro_ids']['referncia']
        montos_proyectos=montos_proyectos.split('-')
        monto_viejo=montos_proyectos[0].replace('.',',')
        monto_nuevo=montos_proyectos[1].replace('.',',')
        entidad=entidades_data['parent_id']['name']
        if entidades_data['tipo_entidad_id'].name=='ALCALDÍA':
            titulo='Alcalde (sa)'
        elif entidades_data['tipo_entidad_id'].name=='GOBERNACIÓN':
            titulo='Gobernador (a)'
        else:
            titulo='Alcalde (sa) Mayor'
        
        for user in entidades_data['user_ids']:
            for group in user.groups_id:
                if group.name=='Alcaldes, Gobernadores o Alcalde Mayor':
                    nombre=user.name
        valores={
                'correlativo':carta_x_firmar_data['correlativo'],
                'proyecto_data':proyecto_data,
                'hoy':hoy,
                'nombre':nombre,
                'monto_viejo':monto_viejo,
                'monto_nuevo':monto_nuevo,
                'titulo':titulo,
                'entidad':entidad,
                }
        carta_data = request.registry['report'].get_pdf(cr, uid, docids, reportname, data=valores, context=context)
        return carta_data
    
    def descarga_carta_cambio_monto(self,cr,uid,carta_data,file_name,file_data,context):
        ir_attachment_obj=self.pool.get('ir.attachment')
        cartas_x_firmar_obj=self.pool.get('ept_fir.cartas_x_firmar')
        cp_historial_obj=self.pool.get('ept_cp.historial_proyecto')
        entidades_obj=self.pool.get('ept_ent.entidades')
        users_obj=self.pool.get('res.users')
        mail_message_obj=self.pool.get('mail.message')
        for i in carta_data:
            proyecto_id=carta_data.objeto_principal_id
        proyecto_data=self.browse(cr,uid,proyecto_id)
        partner_id=proyecto_data['partner_id']
        entidades_ids=entidades_obj.search(cr,uid,[('parent_id','=',int(partner_id))])
        entidades_data=entidades_obj.browse(cr,uid,entidades_ids)
        usuarios_ids=[]
        for usuarios in entidades_data['user_ids']:
            usuarios_ids.append(int(usuarios))
        users_ids=users_obj.search(cr,uid,[('id','in',usuarios_ids)])
        users_data=users_obj.browse(cr,uid,users_ids)
        partner_ids=[]
        for users in users_data:
            partner_ids.append(int(users['partner_id']))
        attachment_id = ir_attachment_obj.create(cr,uid,{
            'name': file_name,
            'datas': file_data,
            'datas_fname': file_name,
            'res_model':'ept_cp.carga_proyecto',
            'res_id': int(proyecto_id),
            'proyecto_carta_id': int(proyecto_id),
            'description':'Carta por cambio de monto del proyecto '+proyecto_data['correlativo']
            }, context)
        cartas_x_firmar_obj.write(
                                cr,
                                uid,
                                carta_data.id,
                                {'attachment_id':attachment_id,
                                'state':'firmado'},
                                context)
        ctx={
                'mail_post_autofollow_partner_ids': [], 
                'default_model': 'ept_ent.entidades', 
                'default_res_id':entidades_ids[0], 
                'mail_read_set_read': True, 
                'mail_post_autofollow': True}
        values={
            'body': 'Cambio de monto', 
            'model': 'ept_ent.entidades', 
            'attachment_ids': [(4, attachment_id)], 
            'res_id': entidades_ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, partner_ids]], 
            'subject': False}
        mail_message_obj.create(cr,uid,values,context=ctx)
        
    def registro_solicitud_firma_carta_cambio_monto(self,cr,uid,ids,name_entidad,monto_viejo=None,monto_nuevo=None):
       
        correlativo_carta=self.pool.get('ir.sequence').get(cr,uid,
                                                    'ept_fir.cartas_x_firmar'),
        
        nombre_file=name_entidad+'_monto#'
        if type(ids)==list:
               ids=ids[0]
        referencia=str(monto_viejo)+'-'+str(monto_nuevo)
        list_datos_adicionales=[]
        list_datos_adicionales.append([0,False,{'objeto_ratro':'ept_cp.carga_proyecto', 'objeto_ratro_id':ids, 'referncia':referencia,}])
        value_x_firmar={
            'correlativo':correlativo_carta[0],
            'tipo_cartas':'monto',
            'mensaje':'Su projecto tiene un cambio de monto',
            'referencia':'Carta por cambio de monto de la Entidad '+name_entidad,
            'state':'porfirmar',
            'metodo':'descarga_carta_cambio_monto',
            'objeto_ratro_principal':'ept_cp.carga_proyecto',
            'objeto_principal_id':ids,
            'objeto_rastro_ids':'ept_cp.carga_proyecto',
            'metodoGenerarCartas':'crear_carta_cambio_monto',
            'nombre_file':nombre_file,
            'objeto_rastro_ids':list_datos_adicionales,
            }
        cartas_x_firmar_obj = self.pool.get('ept_fir.cartas_x_firmar')
        cartas_x_firmar_id=cartas_x_firmar_obj.create(cr,uid,value_x_firmar)
        return True
    
    def write(self, cr, uid, ids, vals,modificacion_interna=None,vista_web=None, context=None):
        if modificacion_interna==None:
            modificacion_interna=1
        if vista_web==None:
            vista_web=0
        historial=[]
        cp_historial_obj=self.pool.get('ept_cp.historial_proyecto')
        entidades_objeto=self.pool.get('ept_ent.entidades')
        cuenta_obj=self.pool.get('ept.cuentas')
        vals_modif=vals
        movimientos_cuentas_objeto=self.pool.get('ept.movimientos_cuentas')
        resultado_movimiento={}
        monto_disponible_manteni=0
        valores=vals.keys()
        campos_viejos=[]
        proyecto_datos=self.browse(cr,uid,ids)
        for datos in proyecto_datos:
            monto_actual=cuenta_obj.browse(cr,uid,datos.cuenta_id.id).monto_actual
            migracion=datos.editar_migracion
            status=datos.state
        
        
        for val in ['correlativo','monto_tomado_mantenimiento','coordenada','editar_migracion','aval_ids',
                    'avance','total_benef','empleo_direct_total','empleo_indirect_total','foto_id',
                    'dictamengraph' ,'partner_id','state','aval', 'movimiento_ids', 'historial_ids', 
                    'duracion_proyec','monto_proyecto','valCoordenadas','valGeneral','AsigValCoordenadas',
                    'AsigValGeneral','valCoordenadasUre','coordenada','solicitud_cambio','asignado_cemento_val']:
            if val in valores:
                valores.remove(val)
        for campo in valores:
            campos_viejos.append(proyecto_datos[campo])

        if modificacion_interna==1:
            if 'monto_proyecto' in vals.keys():
                if vals['monto_proyecto']<1:
                    raise osv.except_osv(
                                    ('Error!'),
                                    (u'El monto a registrar para el proyecto debe ser mayor a 0.00.'))
                    
            
            for datos in proyecto_datos:
                entidad_name=datos.partner_id.name
                valCoordenadas=datos.valCoordenadas
                valGeneral=datos.valGeneral
                AsigValCoordenadas=datos.AsigValCoordenadas
                AsigValGeneral=datos.AsigValGeneral
                if migracion!=True:
                    if datos.state=='aprobado' or datos.state=='diferido':
                        if len(vals)>0:
                            if vals.keys()[0]!='monto_proyecto':
                                cambio_status=self.cp_cambio_state_evaluacion(cr,uid,ids,vals,datos.periodo_id,datos.ciclo_id,int(datos.partner_id))
                                if cambio_status==True:
                                    status='carga'
                                    valCoordenadas=False
                                    valGeneral=False
                                    AsigValCoordenadas=False
                                    AsigValGeneral=False
                                else:
                                    if len(vals)==1:
                                        if 'aval_ids' in vals.keys():
                                            status='evaluacion'
                                            valCoordenadas=False
                                            valGeneral=False
                                            AsigValCoordenadas=False
                                            AsigValGeneral=False
                                    else:
                                        raise osv.except_osv(
                                        ('Error!'),
                                        (u'La actividad de Reparación de Proyectos no esta habilitada para la fecha de hoy.'))
                        
                if 'proyect_mantenimiento' in vals.keys():
                    proyec_manten=True
                    if 'monto_proyecto' in vals.keys():
                        if vals['proyect_mantenimiento']==True:
                            monto_evaluar=abs(float(datos.monto_proyecto)-float(vals['monto_proyecto']))
                            self.cp_porcentaje_mantenimientto(cr,uid,ids,int(datos.periodo_id),int(datos.partner_id),vals['monto_proyecto'],)
                        else:
                            proyec_manten=False
                    else:
                        proyec_manten=False
                        if vals['proyect_mantenimiento']==True:
                    
                            self.cp_porcentaje_mantenimientto(cr,uid,ids,int(datos.periodo_id),int(datos.partner_id),datos.monto_proyecto)
                            proyec_manten=True
                else:
                    proyec_manten=datos.proyect_mantenimiento
                    
                    if datos.proyect_mantenimiento==True and 'monto_proyecto' in vals.keys():

                        #~ print 'hola'
                        #~ print 'hola'
                        #~ print 'hola'
                        #~ print 'hola'
                        #~ print 'hola'
                        #~ if datos.monto_proyecto>vals['monto_proyecto']:
                            #~ monto_evaluar=vals['monto_proyecto']
                        #~ else:
                            #~ monto_evaluar=abs(float(datos.monto_proyecto)-float(vals['monto_proyecto']))
                        #~ if datos.monto_proyecto<vals['monto_proyecto']:
                        #~ monto_mante=datos.monto_proyecto-vals['monto_proyecto']
                        #~ resultado=self.cp_porcentaje_mantenimientto(cr,uid,ids,int(datos.periodo_id),int(datos.partner_id),monto_evaluar)

                       
                        if float(datos.monto_proyecto) < float(vals['monto_proyecto']):
                            
                            monto_evaluar=abs(float(datos.monto_proyecto)-float(vals['monto_proyecto']))
                            #~ if datos.monto_proyecto<vals['monto_proyecto']:
                            #~ monto_mante=datos.monto_proyecto-vals['monto_proyecto']
                            resultado=self.cp_porcentaje_mantenimientto(cr,uid,ids,int(datos.periodo_id),int(datos.partner_id),monto_evaluar)

               #~ codigo de ingreso o engreso en el valor tomado de mantenimiento por un proyecto
                if 'proyect_mantenimiento' in vals.keys() and 'monto_proyecto' not in vals.keys():
                    if datos.proyect_mantenimiento==False:
                        monto_mant_ingreso=datos.monto_proyecto
                        resultado_movimiento=movimientos_cuentas_objeto.movimiento_mantenimiento_egreso(cr,uid,monto_mant_ingreso,int(datos.partner_id),proyec_manten,int(datos.cuenta_id),float(datos.monto_proyecto),datos.id,0,0)
                    else:
                        monto_mant_ingreso=datos.monto_proyecto
                        resultado_movimiento=movimientos_cuentas_objeto.movimiento_mantenimiento_ingreso(cr,uid,monto_mant_ingreso,int(datos.partner_id),proyec_manten,int(datos.cuenta_id),float(datos.monto_proyecto),datos.id,0,0)
                accion='Aumento del monto del proyecto'
                acion2='Reducción del monto del proyecto'
                descripcion=datos.correlativo
            
                
                if 'monto_proyecto' in vals.keys():
                    if type(ids)==list:
                        ids=ids[0]
                    if float(datos.monto_proyecto)>float(vals['monto_proyecto']):
                        monto=float(datos.monto_proyecto)-float(vals['monto_proyecto'])
                        resultado_movimiento=movimientos_cuentas_objeto.movimiento_ingreso(
                                                            cr,uid,
                                                            int(datos.cuenta_id),
                                                            monto,
                                                            acion2,
                                                            descripcion,
                                                            self,
                                                            ids,
                                                            int(datos.periodo_id),
                                                            int(datos.partner_id),
                                                            proyec_manten,
                                                            float(vals['monto_proyecto']))
                    if float(datos.monto_proyecto)<float(vals['monto_proyecto']):
                        
                        monto=float(vals['monto_proyecto'])-float(datos.monto_proyecto)
                        
                        resultado_movimiento=movimientos_cuentas_objeto.movimiento_egreso(
                                                            cr,uid,
                                                            int(datos.cuenta_id),
                                                            monto,
                                                            accion,
                                                            descripcion,
                                                            self,
                                                            ids,
                                                            int(datos.periodo_id),
                                                            int(datos.partner_id),
                                                            proyec_manten,
                                                            float(vals['monto_proyecto'])
                                                            )
                    descripcion3='Se realizo un cambio en el monto asignado al \
                                  proyecto de '+str(datos.monto_proyecto)+' a ' \
                                  +str(vals['monto_proyecto'])
                    historial.append([0,False,{'descripcion':descripcion3}])
                #~ monto de mantenimiento actual utilizado por el proyecto 
                monto_tomado_mantenimiento=datos.monto_tomado_mantenimiento
                monto_actual=cuenta_obj.browse(cr,uid,datos.cuenta_id.id).monto_actual
                if 'monto_disponible_mantenimiento_egreso' in resultado_movimiento.keys():
                    monto_disponible_manteni=resultado_movimiento['monto_disponible_mantenimiento_egreso']
                    if 'proyect_mantenimiento' in vals.keys():
                        if datos.proyect_mantenimiento==True and vals['proyect_mantenimiento']==False:
                            entidades_ids=entidades_objeto.search(cr,uid,[('parent_id','=',int(datos.partner_id))])
                            entidades_data=entidades_objeto.browse(cr,uid,entidades_ids)
                            monto_total_mantenimiento=datos.monto_tomado_mantenimiento+float(entidades_data['monto_disp_mantenimiento'])
                            if monto_total_mantenimiento>vals['monto_proyecto'] and float(entidades_data['monto_disp_mantenimiento'])==float(monto_actual):
                                monto_tomado_mantenimiento=monto_disponible_manteni+monto_tomado_mantenimiento
                            else:
                                monto_tomado_mantenimiento=monto_disponible_manteni-monto_tomado_mantenimiento
                        else:
                            monto_tomado_mantenimiento=monto_disponible_manteni+monto_tomado_mantenimiento
                    else:
                        monto_tomado_mantenimiento=monto_tomado_mantenimiento+monto_disponible_manteni
                entidades_ids=entidades_objeto.search(cr,uid,[('parent_id','=',int(datos.partner_id))])
                entidades_data=entidades_objeto.browse(cr,uid,entidades_ids)
                monto_total_mantenimiento=datos.monto_tomado_mantenimiento+float(entidades_data['monto_disp_mantenimiento'])
                if 'monto_disponible_mantenimiento_ingreso' in resultado_movimiento.keys():
                    monto_disponible_manteni=resultado_movimiento['monto_disponible_mantenimiento_ingreso']
                    if 'proyect_mantenimiento' in vals.keys():
                        if datos.proyect_mantenimiento==True and vals['proyect_mantenimiento']==False :
                            if 'monto_proyecto' in vals.keys():
                                if monto_total_mantenimiento>vals['monto_proyecto'] and float(entidades_data['monto_disp_mantenimiento'])==float(monto_actual):
                                    monto_tomado_mantenimiento=monto_disponible_manteni+monto_tomado_mantenimiento
                                else:
                                    monto_tomado_mantenimiento=monto_tomado_mantenimiento-monto_disponible_manteni
                            else:
                                monto_tomado_mantenimiento=monto_tomado_mantenimiento-monto_disponible_manteni
                    else:
                        monto_tomado_mantenimiento=monto_tomado_mantenimiento-monto_disponible_manteni
                if 'movimiento_id_ingreso' in resultado_movimiento.keys():
                    monto_tomado_mantenimiento=datos.monto_tomado_mantenimiento-monto_disponible_manteni
                if 'movimiento_id_egreso' in resultado_movimiento.keys():
                    if  'monto_disponible_mantenimiento_ingreso' in resultado_movimiento.keys():
                        if monto_total_mantenimiento>vals['monto_proyecto'] and float(entidades_data['monto_disp_mantenimiento'])==float(monto_actual):
                            monto_tomado_mantenimiento=datos.monto_tomado_mantenimiento+monto_disponible_manteni
                total_benef=datos.benef_masculino+datos.benef_femenino
                if 'benef_masculino' in vals.keys():
                    total_benef=int(vals['benef_masculino'])+datos.benef_femenino
                if 'benef_femenino' in vals.keys():
                    total_benef=int(vals['benef_femenino'])+datos.benef_masculino
                if 'benef_masculino' in vals.keys() and 'benef_femenino' in vals.keys():
                    total_benef=int(vals['benef_masculino'])+int(vals['benef_femenino'])
                empleo_direct_total=datos.empleo_direct_masculino+datos.empleo_direct_femenino
                if 'empleo_direct_masculino' in vals.keys():
                    empleo_direct_total=int(vals['empleo_direct_masculino'])+datos.empleo_direct_femenino
                if 'empleo_direct_femenino' in vals.keys():
                    empleo_direct_total=int(vals['empleo_direct_femenino'])+datos.empleo_direct_masculino
                if 'empleo_direct_masculino' in vals.keys() and 'empleo_direct_femenino' in vals.keys():
                    empleo_direct_total=int(vals['empleo_direct_masculino'])+int(vals['empleo_direct_femenino'])
                empleo_indirect_total=datos.empleo_indirect_masculino+datos.empleo_indirect_femenino
                if 'empleo_indirect_masculino' in vals.keys():
                    empleo_indirect_total=int(vals['empleo_indirect_masculino'])+datos.empleo_indirect_femenino
                if 'empleo_indirect_femenino' in vals.keys():
                    empleo_indirect_total=int(vals['empleo_indirect_femenino'])+datos.empleo_indirect_masculino
                if 'empleo_indirect_masculino' in vals.keys() and 'empleo_indirect_femenino' in vals.keys():
                    empleo_indirect_total=int(vals['empleo_indirect_masculino'])+int(vals['empleo_indirect_femenino']) 
                if (datos.state=='aprobado' or datos.state=='diferido') and status=='carga':
                    mensaje='Su proyecto cambio de '+datos.state+' para Borrador'
                    mensaje_his={
                        'descripcion':mensaje,
                        'proyecto_id':datos.id,
                        }
                    cp_historial_obj.create(cr,uid,mensaje_his)
                if status=='aprobado':
                    if len(vals)>0:
                        if 'monto_proyecto' == vals.keys()[0]:
                            print 'hola'
                            print 'hola'
                            print 'hola'
                            print 'hola'
                            self.registro_solicitud_firma_carta_cambio_monto(cr,uid,ids,entidad_name,datos.monto_proyecto,vals['monto_proyecto'])
                if vista_web==0:
                    duracion=self.cp_validar_fechas_proyecto(cr,uid,datos.id,
                                                                    datos.fecha_inicio,
                                                                    datos.fecha_fin,)
                    if 'fecha_inicio' in vals.keys():
                        duracion=self.cp_validar_fechas_proyecto(cr,uid,datos.id,
                                                                vals['fecha_inicio'],
                                                                    datos.fecha_fin,)
                    if 'fecha_fin' in vals.keys():
                        duracion=self.cp_validar_fechas_proyecto(cr,uid,datos.id,
                                                                    datos.fecha_inicio,
                                                                    vals['fecha_fin'],)
                                                                    
                    if 'fecha_fin' in vals.keys() and 'fecha_inicio' in vals.keys():
                        duracion=self.cp_validar_fechas_proyecto(cr,uid,datos.id,
                                                                    vals['fecha_inicio'],
                                                                    vals['fecha_fin'],)
                
                    vals.update({
                        'duracion_proyec':duracion.values()[0].values()[0],
                    })
                vals.update({
                    'historial_ids':historial,
                    'total_benef':total_benef,
                    'empleo_direct_total':empleo_direct_total,
                    'empleo_indirect_total':empleo_indirect_total,
                    'state':status,
                    'valCoordenadas':valCoordenadas,
                    'valGeneral':valGeneral,
                    'AsigValCoordenadas':AsigValCoordenadas,
                    'AsigValGeneral':AsigValGeneral,
                    'monto_tomado_mantenimiento':abs(monto_tomado_mantenimiento),
                    
                    })
        modificar=super(ept_cp_carga_proyecto, self).write(cr, uid, ids,vals,context=context) 
        #~ quitar despues de la migracion
        
        if type(ids)==list:
            if len(ids)>0:
                ids=ids[0]
            else:
                ids=0
        if 'avance' not in vals.keys():
            migracion_obj=self.pool.get('ept_mig.proyectos_migrados')
            migracion_id=migracion_obj.search(cr,SUPERUSER_ID,[('proyectos_id','=',ids)])
            if len(migracion_id)==1:
                migracion_obj.write(cr,SUPERUSER_ID,migracion_id,{'actualizado':True})
        for dato in self.browse(cr,uid,ids):
            if len(dato.aval_ids)>1:
                raise osv.except_osv(
                    ('Alerta!'),
                    (u'Debe registrar un solo archivo para el aval del proyecto.'))
            if modificacion_interna==1:
                if dato.aval==True:
                    historial_2=self.cp_mensaje_historial_aval(cr, uid,dato.id,dato.aval,dato.aval_ids)
                    hist={
                        'descripcion':historial_2[0][2].values()[0],
                        'proyecto_id':dato.id
                        }
                    cp_historial_obj.create(cr,uid,hist)
                historial_3=self.cp_mensaje_historial_monto_minimo(cr,uid,
                                                           dato.id,
                                                           dato.obra_civil,
                                                           int(dato.subcategoria_id),
                                                           dato.tipo_obra,
                                                           dato.cantidad_estimada_obra,
                                                           dato.monto_proyecto,
                                                           dato.equipos,
                                                           dato.equipos_ids,
                                                           dato.maquinaria,
                                                           dato.maquinaria_ids,
                                                           dato.vehiculos,
                                                           dato.vehiculos_ids,
                                                           dato.materiales_consumo,
                                                           dato.materiales_ids,
                                                           dato.semoviente,
                                                           dato.semoviente_ids,
                                                           dato.unidad_medicion_obra,)
                if historial_3!=[]:
                    hist_2={
                        'descripcion':historial_3[0][2].values()[0],
                        'proyecto_id':dato.id
                        }
                    cp_historial_obj.create(cr,uid,hist_2)
        if not self.browse(cr,uid,ids)[0].editar_migracion:
            hist_modif=self.cp_historial_modificaciones(cr,uid,ids,vals_modif,campos_viejos,valores)
        return modificar

    def create(self,cr,uid,vals,context=None):
        if vals['monto_proyecto']<=0.00:
            raise osv.except_osv(
            ('Alerta!'),
            (u'El monto a registrar para el proyecto debe ser mayor a 0.00.'))
        vals.update({
            'total_benef':vals['benef_masculino']+vals['benef_femenino'],
            'empleo_direct_total':vals['empleo_direct_masculino']+
                                    vals['empleo_direct_femenino'],
            'empleo_indirect_total':vals['empleo_indirect_masculino']+
                                    vals['empleo_indirect_femenino'],
            })
        actividad='CARGA DE PROYECTOS'
        plf_periodos_objeto=self.pool.get('ept_plf.periodos')
        ept_entidades_objeto=self.pool.get('ept_ent.entidades')
        ept_entidades_id=ept_entidades_objeto.search(cr,uid,[('parent_id','=',vals['partner_id'])])
        id_ent=ept_entidades_id[0]
        autorizacion_fechas=plf_periodos_objeto.plf_control_actividades(
                                                                     cr, 
                                                                uid, [],
                                                int(vals['partner_id']),
                                                             actividad,)
        cod_etapa=autorizacion_fechas.values()[1]
        if autorizacion_fechas.keys()[0]!='periodo':
            raise osv.except_osv(
            ('Alerta!'),
            (u'La carga de proyecto no esta habilitada para la fecha de hoy.'))
        if vals['proyect_mantenimiento']==True:
            self.cp_porcentaje_mantenimientto(cr,uid,[],int(autorizacion_fechas.values()[0]),vals['partner_id'],vals['monto_proyecto'],)
        accion='Registro de proyecto'
        descripcion=''
        movimientos_cuentas_objeto=self.pool.get('ept.movimientos_cuentas')
        correlativo=self.pool.get('ir.sequence').get(cr,uid,
                                                    'ept_cp.carga_proyecto'),
        periodo_id=int(autorizacion_fechas.values()[0])
        plf_perido_datos=plf_periodos_objeto.browse(cr,uid,periodo_id)
        anio=plf_perido_datos['periodo_fiscal']
        resultado_movimiento=movimientos_cuentas_objeto.movimiento_egreso(cr,uid,
                                                                vals['cuenta_id'],
                                                            vals['monto_proyecto'],
                                                            accion,
                                                            descripcion,
                                                            self,
                                                            [],
                                                            periodo_id,
                                                            vals['partner_id'],
                                                            vals['proyect_mantenimiento'],
                                                            vals['monto_proyecto']
                                                            )
        if 'movimiento_id_ingreso' in resultado_movimiento.keys(): 
            movimiento_id=resultado_movimiento['movimiento_id_ingreso']
        if 'movimiento_id_egreso' in resultado_movimiento.keys(): 
            movimiento_id=resultado_movimiento['movimiento_id_egreso']
        monto_tomado_mantenimiento=0
        if len (resultado_movimiento)==2:
            monto_tomado_mantenimiento=resultado_movimiento['monto_disponible_mantenimiento_egreso']
        entidades_data=ept_entidades_objeto.browse(cr,uid,ept_entidades_id)
        vals.update({
            'correlativo':correlativo,
            'periodo_id':int(autorizacion_fechas.values()[0]),
            'ciclo_id':int(autorizacion_fechas.values()[2]),
            'monto_tomado_mantenimiento':monto_tomado_mantenimiento,
            })
        proyecto_id=super(ept_cp_carga_proyecto,self).create(cr,uid,vals,
                                                       context=context)
        for cp in self.browse(cr,uid,proyecto_id):
            duracion=self.cp_validar_fechas_proyecto(cr,uid,proyecto_id,
                                                        cp.fecha_inicio,
                                                         cp.fecha_fin,)
        movimientos_cuentas_objeto.write(cr, uid, [movimiento_id], 
                                                  {'id_rastro':proyecto_id},
                                                  context=context)
        valores={
            'correlativo':'PI-'+str(anio)+'-'+cod_etapa+'-E-'+str(id_ent)+'-'+correlativo[0],
            'duracion_proyec':duracion.values()[0].values()[0],
            'movimiento_ids':[[6, False, [movimiento_id]]],
                } 
        movimiento={
                'name':valores['correlativo']
                }
        movimientos_cuentas_objeto.write(cr, uid, [movimiento_id], movimiento,context=context)
        self.write(cr, uid, [proyecto_id], valores,context=context)
        return proyecto_id

class ir_attachment_inherit(osv.osv):
    _inherit='ir.attachment'
    _columns = {
        'foto_id' : fields.many2one('ept_cp.carga_proyecto', 'Foto', ondelete="cascade"),
        'proyecto_carta_id' : fields.many2one('ept_cp.carga_proyecto', 'Cartas', ondelete="cascade"),
        'aval_id' : fields.many2one('ept_cp.carga_proyecto', 'Aval', ondelete="cascade"),
                }

class ept_cp_equipos(osv.osv):
    _name = 'ept_cp.equipos'
    _rec_name = 'uso_id'
    
    _columns = {
        'proyecto_id': fields.many2one(
                                'ept_cp.carga_proyecto', 
                                'Proyecto', 
                                required=False,
                                ondelete='restrict', 
                                help=''),
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_equipos', 
                                'Uso', 
                                required=True,
                                ondelete='restrict', 
                                help=''),
        'tipo':fields.char(
                            'Tipo',
                            help=''),
        'cantidad': fields.integer(
                                'Cantidad',  
                                readonly=False,   
                                help='Cantidad de equipos a adquirir\
                                 mediante el proyecto a registrar'),
    }
    
class ept_cp_maquinaria(osv.osv):
    _name = 'ept_cp.maquinaria'
    _rec_name = 'uso_id'
    
    _columns = {
        'proyecto_id': fields.many2one(
                                'ept_cp.carga_proyecto', 
                                'Proyecto', 
                                required=False, 
                                ondelete='restrict',
                                help=''),
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_maquinaria', 
                                'Uso', 
                                required=True, 
                                ondelete='restrict',
                                help=''),
        'tipo':fields.char(
                                'Tipo',
                                help=''),
        'cantidad': fields.integer(
                                'Cantidad',  
                                readonly=False,   
                                help='Cantidad de maquinaria a adquirir\
                                 mediante el proyecto a registrar'),
    }
    
class ept_cp_vehiculo(osv.osv):
    _name = 'ept_cp.vehiculo'
    _rec_name = 'uso_id'
    
    _columns = {
        'proyecto_id': fields.many2one(
                                'ept_cp.carga_proyecto', 
                                'Proyecto', 
                                required=False, 
                                ondelete='restrict',
                                help=''),
        'uso_id': fields.many2one(
                            'ept_cp.montos_minimos_vehiculo_uso', 
                            'Uso', 
                            required=True, 
                            ondelete='restrict',
                            help=''),
        'caracteristica_id': fields.many2one(
                                    'ept_cp.montos_minimos_vehiculo_caracteristicas', 
                                    'Caracteristica', 
                                    required=True, 
                                    ondelete='restrict',
                                    help=''),
        'tipo_id': fields.many2one(
                                'ept_cp.montos_minimos_vehiculo_tipo', 
                                'Tipo', 
                                required=True,
                                ondelete='restrict', 
                                help=''),
        'cantidad': fields.integer(
                                'Cantidad',  
                                readonly=False,   
                                help='Cantidad de vehiculos a adquirir\
                                 mediante el proyecto a registrar'),
    }
    
class ept_cp_materiales_consumo(osv.osv):
    _name = 'ept_cp.materiales_consumo'
    _rec_name = 'uso_id'
    
    _columns = {
        'proyecto_id': fields.many2one(
                                'ept_cp.carga_proyecto', 
                                'Proyecto', 
                                required=False, 
                                ondelete='restrict',
                                help=''),
        'uso_id': fields.many2one(
                                'ept_cp.montos_minimos_materiales_consumo', 
                                'Uso', 
                                required=True, 
                                ondelete='restrict',
                                help='Uso que tendra el material a seleccionar\
                                     para el proyecto a registrar'),
        'tipo':fields.char(
                                    'Tipo',
                                    help=''),
        'cantidad': fields.integer(
                                'Cantidad',  
                                readonly=False,   
                                help='Cantidad de materiales de consumo\
                                 a adquirir mediante el proyecto a\
                                  registrar'),
    }

class ept_cp_semoviente(osv.osv):
    _name = 'ept_cp.semovientes_caracteristicas'
    _rec_name = 'especie_id'
    
    _columns = {
        'proyecto_id': fields.many2one(
                            'ept_cp.carga_proyecto', 
                            'Proyecto', 
                            required=False,
                            ondelete='restrict',
                            help=''),
        'especie_id': fields.many2one(
                            'ept_cp.semovientes',
                            
                            'Especie', 
                            ondelete='restrict', 
                            required=False,
                            help=''),
        'grupo_id':fields.many2one(
								'ept_cp.semovientes_grupo_etario',
								'Grupo etario',
								readonly=False,
								required=False,
								help='Grupo etario al cual pertenece grupo etario.' ),
		'uso_id':fields.many2one(
								'ept_cp.semovientes_uso',
								'Uso',
								readonly=False,
								required=False,
								help='Uso al cual pertenece grupo etario.' ),
		'proposito_id':fields.many2one(
								'ept_cp.semovientes_proposito',
								'Proposito',
								readonly=False,
								required=False,
								help='Proposito del semoviente.' ),
        'grupo':fields.char(
                        'Grupo Etario',
                        readonly=False, 
                        help=''),
        'uso':fields.char(
                        'Uso',
                        readonly=False, 
                        help=''),
        'proposito':fields.char(
                        'Proposito',
                        readonly=False, 
                        help=''),
        'cantidad':fields.integer(
                        'Cantidad',
                        readonly=False, 
                        help=''),
        }
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
class ept_cp_historial_proyecto(osv.osv):
    _name = 'ept_cp.historial_proyecto'
    _rec_name = 'descripcion'
    
    _columns = {
        'proyecto_id': fields.many2one(
                            'ept_cp.carga_proyecto', 
                            'Proyecto', 
                            required=False,
                            ondelete='restrict',
                            help='Id del proyecto relacionado al mensaje'),
        'descripcion':fields.char(
                        'Descripción',
                        readonly=True, 
                        help='Descripción de la acción ejecutada.'),
        
    }
    
    _defaults = {
        'create_date':fields.datetime.now,
    }
    
    _order = 'create_date desc, id desc'
    
    


    
    
    
    
