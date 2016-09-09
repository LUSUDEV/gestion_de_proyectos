 # -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw

class ept_cp_cambio_monto(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(ept_cp_cambio_monto,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        print 'hola mundo'
        return 'hola mundo'

        
class report_carta_cambio_monto_ept(osv.AbstractModel):
    _name = "report.ept_carga_proyectos.cambio_monto_proyecto_qweb"
    _inherit = "report.abstract_report"
    _template = "ept_carga_proyectos.cambio_monto_proyecto_qweb"
    _wrapped_report_class = ept_cp_cambio_monto
# report_sxw.report_sxw('report.report_carta_cambio_monto_ept', 'ept_cp.carga_proyecto', 'local_addons_ep1561/ept_carga_proyectos/report/report_carta_cambio_monto_ept.rml', parser=ept_cp_cambio_monto,header=False)
