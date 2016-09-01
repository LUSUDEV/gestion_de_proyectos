#-*-coding:utf-8-*-
from openerp.osv import fields, osv
from openerp.http import request


class ept_cp_tipo_sector(osv.osv): 
    _name='ept_cp.tipo_sectores'
    _rec_name = 'name'
    
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, long):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if context.has_key("default_id"):
                if type(context['default_id'])==int:
                    name=name
            else:
                if record['parent_id']:
                    name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, 
                                         operator='ilike', 
                                         context=None, 
                                         limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, 
                                        limit=limit, context=context)
        if context.has_key("default_id"):
                if type(context['default_id'])==int:
                    ids = self.search(cr, uid, 
                                    [('parent_id','=',context['default_id'])], 
                                    limit=limit, context=context)
                else:
                    ids = self.search(cr, uid, args, 
                                               limit=limit, 
                                               context=context)
        else:
                    ids = self.search(cr, uid, args, 
                                               limit=limit, 
                                               context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    _columns={
        'name':fields.char(
                    'Nombre del sector',
                    size=80,
                    required=True,
                    help='Nombre del sector a registrar'),
        'complete_name': fields.function(
                                    _name_get_fnc, 
                                    type="char", 
                                    string='Nombre'),
        'codigo':fields.char(
                        'Código del sector',
                        size=10,
                        help='Código del sector a registrar'),
        'parent_id': fields.many2one(
                                'ept_cp.tipo_sectores',
                                'Categoria', 
                                select=True, 
                                ondelete='cascade'),
        'child_id': fields.one2many(
                                'ept_cp.tipo_sectores', 
                                'parent_id', 
                                string='Hijo de Categoria'),
        'parent_left': fields.integer(
                                'Left Parent', 
                                select=1),
        'parent_right': fields.integer(
                                'Right Parent', 
                                select=1),
        'active':fields.boolean(
                            'Activo',
                            help='Si esta activo el motor lo incluira en la\
                                   vista...'),
        'aval_constr': fields.boolean(
                                'Aval por construcción' ),
        'aval_ampli': fields.boolean(
                                'Aval por ampliación' ),
        'aval_rehab': fields.boolean(
                                'Aval por rehabilitación' ),
        'coordenadas': fields.boolean(
                                '¿Subcategoría amerita dos pares de coordenadas?' ),
    }
    
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    
    _defaults={
            'active':True,
            'ip':lambda self,cr,uid,context: request.httprequest.remote_addr,
        }

