# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers import main
from openerp import SUPERUSER_ID
from openerp.addons.website_apiform.controladores import panel, base_tools
from openerp.addons.web.controllers import main
from openerp.addons.jpv_usuarios.controladores import jpv_use_users_c
#~ from openerp.addons.jpv_rendicion.controladores import jpv_rnd_rendicion_c
import openerplib
import json
import os

class website(main.Home):
    __HOST="10.251.4.92"
    __PORT=8069
    __DATABASE="sisfci"
    __LOGIN="admin"
    __PASWORD="1234qwer"
    @http.route('/', auth='public', website=True)
    def index(self,**kw):
        redirect=request.httprequest.url_root+'paginas/home'
        if request.session.login:
            return self.home()
        return http.request.website.render('jpv_index.index',
                                        {'mensaje':'no',
                                         'redirect':redirect})

    @http.route('/paginas/proyecto', auth='public', website=True)
    def proyecto(self):        
        return http.request.website.render('jpv_index.proyecto')

    @http.route('/paginas/financiamiento', auth='public', website=True)
    def financiamiento(self):        
        return http.request.website.render('jpv_index.financiamiento')

    @http.route('/paginas/estadistica', auth='public', website=True)
    def estadistica(self):        
        return http.request.website.render('jpv_index.estadistica')
        
    @http.route('/paginas/home', auth='public', website=True)
    def home(self,**w):
        return http.request.website.render('jpv_index.home')

    @http.route('/web/login', auth='public',methods=['POST'], website=True)
    def login(self,redirect=None,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        main.ensure_db()
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID
        values = request.params.copy()
        if not redirect:
            redirect=request.httprequest.url_root
        values['redirect'] = redirect
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied: 
            values['databases'] = None
        if http.request.httprequest.method == 'POST':
            old_uid = http.request.uid
            uid = http.request.session.authenticate(http.request.session.db, http.request.params['login'], http.request.params['password'])
            if uid is not False:
                values['error']=''
                if uid:
                    return http.redirect_with_hash('/')
                return http.redirect_with_hash(redirect)
        values['error']='Error Usuario/Clave'
        return http.request.website.render('jpv_index.index',{
                                                        'mensaje':values['error']
                                                        })
    
    @http.route('/plan_inversion_redirec', auth='public', website=True)
    def plan_inveraion_redirec(self):
        cr, uid, context = request.cr, request.uid, request.context
        menu_obj = request.registry['ir.ui.menu']
        menu_id=menu_obj.search(cr,SUPERUSER_ID,[('name','=','Registro de Entidades')])
        url='/web#view_type=kanban,model=jpv_ent.entidades#view_type=kanban&model=jpv_ent.entidades&menu_id=%d' % menu_id[0]
        return request.redirect(url)
        
    @http.route('/jpv/manual', auth='user', website=True)
    def jpv_manual(self):
        addons_path = http.addons_manifest['jpv_index']['addons_path']
        ruta_manual=os.path.join(addons_path,'jpv_index','documentos', 'Instructivo_jpv.pdf')
        manual = open(ruta_manual, "r",buffering = 0)  
        data_manual=manual.read()
        manual.close()  
        return request.make_response(data_manual,
                headers=[('Content-Disposition',
                                main.content_disposition('Instructivo_jpv.pdf')),
                         ('Content-Type', 'application/pdf;charset=utf8'),
                         ('Content-Length', len(data_manual))],
                cookies={'fileToken': '212123f4646546'})
                
    @http.route('/jpv/doc/clasificacion', auth='user', website=True)
    def jpv_clasificacion(self):
        addons_path = http.addons_manifest['jpv_index']['addons_path']
        ruta_manual=os.path.join(addons_path,'jpv_index','documentos', 'SISTEMA_CLASIFICACION_DE_PROYECTOS.pdf')
        manual = open(ruta_manual,"r",buffering = 0)  
        data_manual=manual.read()
        manual.close()  
        return request.make_response(data_manual,
                headers=[('Content-Disposition',
                                main.content_disposition('SISTEMA_CLASIFICACION_DE_PROYECTOS.pdf')),
                         ('Content-Type', 'application/pdf;charset=utf8'),
                         ('Content-Length', len(data_manual))],
                cookies={'fileToken': '212123f4646546'})
    
    @http.route('/prueba', auth='public',methods=['POST'],type="http", website=True)
    def prueba(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        connection = openerplib.get_connection(
                            hostname=self.__HOST,
                            port=self.__PORT,
                            database=self.__DATABASE,
                            login=self.__LOGIN,
                            password=self.__PASWORD);
        
        project_obpp_obj = connection.get_model("project.project")
        project_obpp_data = project_obpp_obj.read([107529],[
                                                'name',
                                                'amount',
                                                'duration',
                                                'investment_sector_id',
                                                
                                                ])
        resultado={'estado':1,'proyectos':project_obpp_data}
        resultado=json.dumps( resultado, ensure_ascii=False, encoding='utf8')
        return resultado
                                                        
    @http.route('/prueba2', auth='public',type="http", website=True)
    def pruebas(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        connection = openerplib.get_connection(
                            hostname=self.__HOST,
                            port=self.__PORT,
                            database=self.__DATABASE,
                            login=self.__LOGIN,
                            password=self.__PASWORD);
        
        project_obpp_obj = connection.get_model("project.project")
        project_obpp_data = project_obpp_obj.read([107529],[
                                                'name',
                                                'amount',
                                                'duration',
                                                'investment_sector_id',
                                                
                                                ])
        resultado={'estado':1,'proyectos':project_obpp_data}
        resultado=json.dumps( resultado, ensure_ascii=False, encoding='utf8')
        return resultado

    
            




    
    
    
    
    
    
    
    
    
