# -*- coding: utf-8 -*-

from odoo import _, models, fields, api

from odoo.exceptions import UserError
from odoo import exceptions
import logging
_logger = logging.getLogger(__name__)

class helpdesk_update(models.Model):
    #_inherit = ['mail.thread', 'helpdesk.ticket']
    _inherit = 'helpdesk.ticket'
    #priority = fields.Selection([('all','Todas'),('baja','Baja'),('media','Media'),('alta','Alta'),('critica','Critica')])
    priority = fields.Selection([('0','Todas'),('1','Baja'),('2','Media'),('3','Alta'),('4','Critica')], track_visibility='onchange')
    x_studio_equipo_por_nmero_de_serie = fields.Many2many('stock.production.lot', store=True)
    x_studio_empresas_relacionadas = fields.Many2one('res.partner', store=True, track_visibility='onchange', string='Localidad')
    
    #@api.one
    #@api.depends('team_id', 'x_studio_responsable_de_equipo')
    @api.model
    @api.onchange('team_id', 'x_studio_responsable_de_equipo')
    def cambiar_seguidores(self):
        _logger.info("cambiar_seguidores()")
        _logger.info("self._origin: " + str(self._origin) + ' self._origin.id: ' + str(self._origin.id))
        
        #https://www.odoo.com/es_ES/forum/ayuda-1/question/when-a-po-requires-approval-the-follower-of-the-warehouse-receipt-is-the-approver-i-need-it-to-be-the-user-who-created-the-po-136450
        #log(str(self.message_follower_ids), level='info')
        
        #self._origin.id
        
        ##Busanco subscriptores de modelo helpdesk con id especifico
        #log("id: " + str(record.x_studio_id_ticket), level='info')
        ids = self.env['mail.followers'].search_read(['&', ('res_model', '=', 'helpdesk.ticket'), ('res_id', '=',self.x_studio_id_ticket)], ['partner_id'])
        #log(str(ids), level='info')
        lista_followers_borrar = []
        id_cliente = self.partner_id.id
        #log('id_cliente: ' + str(id_cliente), level='info')
        for id_partner in ids:
            #log(str(id_partner['partner_id'][0]))
            id_guardar = id_partner['partner_id'][0]
            if id_guardar != id_cliente:
                #lista_followers_borrar.append(id_guardar)
                lista_followers_borrar.append(id_partner['id'])
            
        #log(str(lista_followers_borrar), level='info')


        #record.message_subscribe([9978])

        # Diamel Luna Chavelas
        id_test = 826   #Id de Diamel Luna Chavelas
        id_test_res_partner = 7804  #Id de res_partner.name = test


        equipo_de_atencion_al_cliente = 1
        equipo_de_almacen = 2
        equipo_de_distribucion = 3
        equipo_de_finanzas = 4
        equipo_de_hardware = 5
        equipo_de_lecturas = 6
        equipo_de_sistemas = 7
        equipo_de_toner = 8


        responsable_atencion_al_cliente = id_test
        responsable_equipo_de_toner = id_test
        responsable_equipo_de_sistemas = id_test
        responsable_equipo_de_hardware = id_test
        responsable_equipo_de_finanzas = id_test
        responsable_equipo_de_lecturas = id_test
        responsable_equipo_de_distribucion = id_test
        responsable_equipo_de_almacen = id_test

        x_studio_responsable_de_equipo = 'x_studio_responsable_de_equipo'


        ## Por cada caso añadir el id de cada responsable de equipo y modificar para añadir a estos
        ## al seguimiento de los ticket's
        subscritor_temporal = id_test_res_partner


        #record.write({'x_studio_responsable_de_equipo' : responsable_atencion_al_cliente})


        equipo = self.team_id.id

        if equipo == equipo_de_atencion_al_cliente:
            _logger.info("Entrando a if equipo_de_atencion_al_cliente.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            
            #record.message_subscribe([responsable_atencion_al_cliente])                           ##Añade seguidores
            #self._origin.id
            
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_atencion_al_cliente})      ##Asigna responsable de equipo
            _logger.info("regresa: " + str(regresa))
            _logger.info("Saliendo de if equipo_de_atencion_al_cliente............................................................. ")
            
          
          
        if equipo == equipo_de_toner:
            
            _logger.info("Entrando a if equipo_de_toner.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
              
        
            #record.message_subscribe([responsable_equipo_de_toner])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_toner})
            
            _logger.info("Saliendo de if equipo_de_toner............................................................. ")
          

        if equipo == equipo_de_sistemas:
            _logger.info("Entrando a if equipo_de_sistemas.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            #record.message_subscribe([responsable_equipo_de_sistemas])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_sistemas})
            
            _logger.info("Saliendo de if equipo_de_sistemas............................................................. ")
          
          
        if equipo == equipo_de_hardware:
            _logger.info("Entrando a if equipo_de_hardware.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            #record.message_subscribe([responsable_equipo_de_hardware])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_hardware})
            _logger.info("Saliendo de if equipo_de_hardware............................................................. ")
          

        if equipo == equipo_de_finanzas:
            _logger.info("Entrando a if equipo_de_finanzas.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            #record.message_subscribe([responsable_equipo_de_finanzas])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_finanzas})
            _logger.info("Saliendo de if equipo_de_finanzas............................................................. ")
          
        if equipo == equipo_de_lecturas:
            _logger.info("Entrando a if equipo_de_lecturas.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            #record.message_subscribe([responsable_equipo_de_lecturas])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_lecturas})
            _logger.info("Saliendo de if equipo_de_lecturas............................................................. ")
          

        if equipo == equipo_de_distribucion:
            _logger.info("Entrando a if equipo_de_distribucion.............................................................. " )
            
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            #record.message_subscribe([responsable_equipo_de_distribucion])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_distribucion})
            _logger.info("Saliendo de if equipo_de_distribucion............................................................. ")
          

        if equipo == equipo_de_almacen:
            _logger.info("Entrando a if equipo_de_almacen............................................................................ ")
            #id del seguidor(marco)
            #ids_partner =11
            
            
            #for r in self.message_follower_ids:
             #   if(r.partner_id.id!=7219):
              #      ids_partner.append(r.partner_id.id)
               #     _logger.info('hi'+str(r.partner_id.id))
            #self['message_follower_ids']=[(3,11,0)]
            #hasta que se guarda borra el registro
            
            #self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id="+str(self.x_studio_id_ticket)+" and partner_id="+str(ids_partner)+";")
            
            #self['message_follower_ids']=[(6,0,ids_partner)]
            #unsubs = self.message_unsubscribe(partner_ids = [826], channel_ids = None)
            #unsubs=self.env['mail.followers'].sudo().search([('res_model', '=','helpdesk.ticket'),('res_id', '=', self.x_studio_id_ticket),('partner_id', '=', 826)]).unlink()
            #_logger.info('Unsubs: ' + str('hola')+str(self.x_studio_id_ticket))
            
            
            #raise Warning('Entrando a if equipo_de_almacen... ')
            #log("Entrando a if equipo_de_almacen... ", level='info')
            #unsubs = record.sudo().message_unsubscribe(lista_followers_borrar)
            unsubs = False
            for follower in self.message_follower_ids:    
                #record.message_unsubscribe([follower.partner_id.id])
                for follower_borrar in lista_followers_borrar:
                    #log(str(follower.id), level = 'info')
                    #log(str(follower_borrar), level = 'info')
                    if follower_borrar == follower.id:
                        #log(str([follower.partner_id.id]), level = 'info')
                        #log('entro if:', level = 'info')
                        _logger.info('partner_ids: ' + str(follower.partner_id.id) + ' ' + str(follower.partner_id.name))
                        #unsubs = self._origin.sudo().message_unsubscribe(partner_ids = list([follower.partner_id.id]), channel_ids = None)
                        
                        #unsubs = self.sudo().message_unsubscribe_users(partner_ids = [follower.partner_id.id])
                        
                        unsubs = self.env.cr.execute("delete from mail_followers where res_model='helpdesk.ticket' and res_id=" + str(self.x_studio_id_ticket) + " and partner_id=" +  str(follower.partner_id.id) + ";")
                        
                        
                        _logger.info('Unsubs: ' + str(unsubs))
            
            
            
            #record.message_subscribe([responsable_equipo_de_almacen])
            regresa = self._origin.sudo()._message_subscribe(partner_ids=[subscritor_temporal], channel_ids=None, subtype_ids=None)
            #regresa = self.env.cr.execute("insert into mail_followers (res_model, res_id, partner_id) values ('helpdesk.ticket', " + str(self._origin.id) + ", " +  str(subscritor_temporal) + ");")
            _logger.info("regresa: " + str(regresa))
            
            self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_almacen})
            _logger.info('Saliendo de if equipo_de_almacen................................................................................. unsubs = ' + str(unsubs))
            
    
    
    #@api.model
    #@api.multi
    @api.onchange('x_studio_equipo_por_nmero_de_serie')
    #@api.depends('x_studio_equipo_por_nmero_de_serie')
    def actualiza_datos_cliente(self):
        _logger.info("actualiza_datos_cliente()")
        _logger.info("self._origin: " + str(self._origin) + ' self._origin.id: ' + str(self._origin.id))
        
        v = {}
        ids = []
        localidad = []
        for record in self:
            _logger.info('record_ 1: ' + str(self._origin.partner_id))
            _logger.info('record_id 1: ' + str(self._origin.id))
            _my_object = self.env['helpdesk.ticket']
            #v['x_studio_equipo_por_nmero_de_serie'] = {record.x_studio_equipo_por_nmero_de_serie.id}
            
            
            #_logger.info('record_feliz : ' + str(record.x_studio_equipo_por_nmero_de_serie.id))
            #ids.append(record.x_studio_equipo_por_nmero_de_serie.id)
            
            #record['x_studio_equipo_por_nmero_de_serie'] = [(4,record.x_studio_equipo_por_nmero_de_serie.id)]
            
            
            _logger.info('*********x_studio_equipo_por_nmero_de_serie: ')
            _logger.info(str(record.x_studio_equipo_por_nmero_de_serie))
            for numeros_serie in record.x_studio_equipo_por_nmero_de_serie:
                ids.append(numeros_serie.id)
                _logger.info('record_ 2: ' + str(self._origin))
                _logger.info("Numeros_serie")
                _logger.info(numeros_serie.name)
                for move_line in numeros_serie.x_studio_move_line:
                    _logger.info('record_ 3: ' + str(self._origin))
                    _logger.info("move line")
                    #move_line.para.almacen.ubicacion.
                    _logger.info('Cliente info***************************************************************************')
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id)
                    cliente = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.id
                    self._origin.sudo().write({'partner_id' : cliente})
                    record.partner_id = cliente
                    idM=self._origin.id
                    _logger.info("que show"+str(idM))
                    if cliente == []:
                        self.env.cr.execute("update helpdesk_ticket set partner_id = " + cliente + "  where  id = " + idM + ";")
                    v['partner_id'] = cliente
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.phone)
                    cliente_telefono = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.phone
                    self._origin.sudo().write({'x_studio_telefono' : cliente_telefono})
                    record.x_studio_telefono = cliente_telefono
                    if cliente_telefono != []:
                        srtt="update helpdesk_ticket set x_studio_telefono = '" + str(cliente_telefono) + "' where  id = " + str(idM) + ";"
                        _logger.info("update gacho"+srtt)
                        s=self.env.cr.execute("update helpdesk_ticket set x_studio_telefono = '" + str(cliente_telefono) + "' where  id = " + str(idM) + ";")
                        _logger.info("update gacho 2 "+str(s))
                    v['x_studio_telefono'] = cliente_telefono
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.mobile)
                    cliente_movil = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.mobile
                    self._origin.sudo().write({'x_studio_movil' : cliente_movil})
                    record.x_studio_movil = cliente_movil
                    if cliente_movil == []:
                        self.env.cr.execute("update helpdesk_ticket set x_studio_movil = '" + str(cliente_movil) + "' where  id = " +idM + ";")
                    v['x_studio_movil'] = cliente_movil
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.x_studio_nivel_del_cliente)
                    cliente_nivel = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.parent_id.x_studio_nivel_del_cliente
                    self._origin.sudo().write({'x_studio_nivel_del_cliente' : cliente_nivel})
                    record.x_studio_nivel_del_cliente = cliente_nivel
                    if cliente_nivel == []:
                        self.env.cr.execute("update helpdesk_ticket set x_studio_nivel_del_cliente = '" + str(cliente_nivel) + "' where  id = " + idM + ";")
                    v['x_studio_nivel_del_cliente'] = cliente_nivel
                    
                    #localidad datos
                    _logger.info('Localidad info*************************************************************************')
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z)
                    localidad = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.id
                    _logger.info('localidad id: ' + str(localidad))
                    self._origin.sudo().write({'x_studio_empresas_relacionadas' : localidad})
                    record.x_studio_empresas_relacionadas = localidad

                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.phone)
                    #telefono_localidad = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.phone
                    #self._origin.sudo().write({x_studio_telefono_localidad : telefono_localidad})
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.mobile)
                    #movil_localidad = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.mobile
                    #self._origin.sudo().write({x_studio_movil_localidad : movil_localidad})
                    _logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.email)
                    #email_localidad = move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.email
                    #self._origin.sudo().write({x_studio_correo_electrnico_de_localidad : email_localidad})
                    
                    #
                    #_logger.info(move_line.location_dest_id.x_studio_field_JoD2k.x_studio_field_E0H1Z.)
                    
                #self._origin.sudo().write({x_studio_responsable_de_equipo : responsable_equipo_de_distribucion})
            
            #_logger.info(record['x_studio_equipo_por_nmero_de_serie'])
            _logger.info(ids)
            #record['x_studio_equipo_por_nmero_de_serie'] = (6, 0, [ids])
            #record.sudo().write({x_studio_equipo_por_nmero_de_serie : [(6, 0, [ids])] })
        #self._origin.sudo().write({'x_studio_equipo_por_nmero_de_serie' : (4, ids) })
        lista_ids = []
        for id in ids:
            lista_ids.append((4,id))
        #v['x_studio_equipo_por_nmero_de_serie'] = [(4, ids[0]), (4, ids[1])]
        v['x_studio_equipo_por_nmero_de_serie'] = lista_ids
        self._origin.sudo().write({'x_studio_equipo_por_nmero_de_serie' : lista_ids})
        record.x_studio_equipo_por_nmero_de_serie = lista_ids
        """
        if localidad != []:
            srtt="update helpdesk_ticket set x_studio_empresas_relacionadas = " + str(localidad) + " where  id = " + str(idM )+ ";"
            _logger.info("update gacho localidad " + srtt)
            record.x_studio_empresas_relacionadas = localidad
            record['x_studio_empresas_relacionadas'] = localidad
            self.env.cr.execute(srtt)
            #self.env.cr.commit()
            v['x_studio_empresas_relacionadas'] = localidad        
        """
        _logger.info({'value': v})
        _logger.info(v)
        #self._origin.env['helpdesk.ticket'].sudo().write(v)
        
        #res = super(helpdesk_update, self).sudo().write(v)
        #return res
        #return {'value': v}
            
    

                
    """
    @api.model
    def create(self, vals):
        _logger.info('create() +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        _logger.info("self._origin: " + str(self._origin) + ' self._origin.id: ' + str(self._origin.id))
        if vals.get('team_id'):
            vals.update(item for item in self._onchange_team_get_values(self.env['helpdesk.team'].browse(vals['team_id'])).items() if item[0] not in vals)
        if 'partner_id' in vals and 'partner_email' not in vals:
            partner_email = self.env['res.partner'].browse(vals['partner_id']).email
            vals.update(partner_email=partner_email)
        # Manually create a partner now since 'generate_recipients' doesn't keep the name. This is
        # to avoid intrusive changes in the 'mail' module
        if 'partner_name' in vals and 'partner_email' in vals and 'partner_id' not in vals:
            vals['partner_id'] = self.env['res.partner'].find_or_create(
                formataddr((vals['partner_name'], vals['partner_email']))
            )

        # context: no_log, because subtype already handle this
        ticket = super(HelpdeskTicket, self.with_context(mail_create_nolog=True)).create(vals)
        if ticket.partner_id:
            ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
            ticket._onchange_partner_id()
        if ticket.user_id:
            ticket.assign_date = ticket.create_date
            ticket.assign_hours = 0
        
        
        
        
        
        #record.message_subscribe([9978])
        #raise Warning('entro')
        # Diamel Luna Chavelas
        id_test = 826   #Id de Diamel Luna Chavelas
        id_test_res_partner = 7804



        equipo_de_atencion_al_cliente = 1
        equipo_de_almacen = 2
        equipo_de_distribucion = 3
        equipo_de_finanzas = 4
        equipo_de_hardware = 5
        equipo_de_lecturas = 6
        equipo_de_sistemas = 7
        equipo_de_toner = 8


        responsable_atencion_al_cliente = id_test
        responsable_equipo_de_toner = id_test
        responsable_equipo_de_sistemas = id_test
        responsable_equipo_de_hardware = id_test
        responsable_equipo_de_finanzas = id_test
        responsable_equipo_de_lecturas = id_test
        responsable_equipo_de_distribucion = id_test
        responsable_equipo_de_almacen = id_test

        x_studio_responsable_de_equipo = 'x_studio_responsable_de_equipo'


        ## Por cada caso añadir el id de cada responsable de equipo y modificar para añadir a estos
        ## al seguimiento de los ticket's
        subscritor_temporal = id_test_res_partner


        #record.write({'x_studio_responsable_de_equipo' : responsable_atencion_al_cliente})


        equipo = self.team_id.id

        if equipo == equipo_de_atencion_al_cliente:
            _logger.info('entro a equipo_de_atencion_al_cliente')
            #record.message_subscribe([responsable_atencion_al_cliente])                           ##Añade seguidores
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_atencion_al_cliente})      ##Asigna responsable de equipo

        if equipo == equipo_de_toner:
            _logger.info('entro a equipo_de_toner')
            #record.message_subscribe([responsable_equipo_de_toner])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_toner})

        if equipo == equipo_de_sistemas:
            _logger.info('entro a equipo_de_sistemas')
            #record.message_subscribe([responsable_equipo_de_sistemas])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_sistemas})

        if equipo == equipo_de_hardware:
            _logger.info('entro a equipo_de_hardware')
            #record.message_subscribe([responsable_equipo_de_hardware])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_hardware})

        if equipo == equipo_de_finanzas:
            _logger.info('entro a equipo_de_finanzas')
            #record.message_subscribe([responsable_equipo_de_finanzas])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_finanzas})

        if equipo == equipo_de_lecturas:
            _logger.info('entro a equipo_de_lecturas')
            #record.message_subscribe([responsable_equipo_de_lecturas])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_lecturas})

        if equipo == equipo_de_distribucion:
            _logger.info('entro a equipo_de_distribucion')
            #record.message_subscribe([responsable_equipo_de_distribucion])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_distribucion})

        if equipo == equipo_de_almacen:
            _logger.info('entro a equipo_de_almacen')
            #record.message_subscribe([responsable_equipo_de_almacen])
            self.message_subscribe([subscritor_temporal])
            self.write({x_studio_responsable_de_equipo : responsable_equipo_de_almacen})
        
        
        
        return ticket
    """