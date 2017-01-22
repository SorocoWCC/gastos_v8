# -*- coding: utf-8 -*-
 
from openerp import models, fields, api
from openerp.exceptions import Warning

class gasto(models.Model):
    _name = "gasto"
    _description = "Gasto"
    name = fields.Char(string='Detalle', required=True)	
    responsable = fields.Char(compute='_action_responsable', string="Responsable", readonly=True, store=True )	
    state = fields.Selection([('new','Nuevo'), ('done','Procesado')], string='state', readonly=True)
    fecha = fields.Date(string='Fecha', required=True)
    monto = fields.Float(string='Monto:', required=True)
    notas = fields.Text(string='Información Adicional')	
    _defaults = {
    'fecha': fields.Date.today(),
    'state': 'new'
    }

# Nombre del Responsable y Asocia Cierre de caja
    @api.one
    @api.depends('name')
    def _action_responsable(self):
        # Asigna el nombre del responsable
        self.responsable = str(self.env.user.name)
        # Asigna el cierre de caja
        cierre_regular = self.env['cierre'].search([('state', '=', 'new'), ('tipo', '=', 'regular')])
        if cierre_regular.id == False :
            raise Warning ("Error: Proceda a crear un cierre de caja tipo Regular.")
        else :
            self.cierre_id = cierre_regular.id

