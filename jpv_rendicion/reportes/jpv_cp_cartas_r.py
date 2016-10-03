 # -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw

class jpv_cp_cancelacion_proyecto(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(jpv_cp_cancelacion_proyecto,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_carta_cambio_monto_jpv(osv.AbstractModel):
    _name = "report.jpv_rendicion.cancelacion_proyecto_qweb"
    _inherit = "report.abstract_report"
    _template = "jpv_rendicion.cancelacion_proyecto_qweb"
    _wrapped_report_class = jpv_cp_cancelacion_proyecto
# report_sxw.report_sxw('report.report_carta_cambio_monto_jpv', 'jpv_cp.carga_proyecto', 'local_addons_ep1561/jpv_carga_proyectos/report/report_carta_cambio_monto_jpv.rml', parser=jpv_cp_cancelacion_proyecto,header=False)
