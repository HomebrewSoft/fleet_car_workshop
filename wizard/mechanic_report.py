# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

from odoo import api, fields, models, _


class MechanicReport(models.TransientModel):
    _name = 'car.workshop.mechanic.report'

    start = fields.Datetime(
        default=fields.Datetime.now(),
    )
    stop = fields.Datetime(
    )
    detail_ids = fields.One2many(
        comodel_name='car.workshop.mechanic.report.detail',
        inverse_name='report_id',
    )

    @api.multi
    def get_detail(self):
        self.detail_ids.unlink()
        Details = self.env['car.workshop.mechanic.report.detail']
        for user in self.env['res.users'].search([]):
            self.detail_ids += Details.create({
                'report_id': self.id,
                'user_id': user.id,
            })
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
