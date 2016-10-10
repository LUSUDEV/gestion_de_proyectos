 # -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw

class resultados_valoracion_ept(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(resultados_valoracion_ept,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
        })
        self.context = context
    
    
        
class report_carta_valoracion_ept(osv.AbstractModel):
    _name = "report.jpv_valoracion.resultado_valoracion_qweb"
    _inherit = "report.abstract_report"
    _template = "jpv_valoracion.resultado_valoracion_qweb"
    _wrapped_report_class = resultados_valoracion_ept
# report_sxw.report_sxw('report.report_carta_valoracion_ept', 'jpv_cp.carga_proyecto', 'local_addons_ep1561/jpv_valoracion/report/report_carta_valoracion_ept.rml', parser=resultados_valoracion_ept,header=False)
