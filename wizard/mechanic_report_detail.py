# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _


class MechanicReportDetail(models.TransientModel):
    _name = 'car.workshop.mechanic.report.detail'

    report_id = fields.Many2one(
        comodel_name='car.workshop.mechanic.report',
        ondelete='cascade',
    )
    start = fields.Datetime(
        related='report_id.start',
    )
    stop = fields.Datetime(
        related='report_id.stop',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
    )
    work_ids = fields.Many2many(
        comodel_name='planned.work',
        compute='_get_work_ids',
    )
    time_spent = fields.Float(
        compute='_get_times',
    )
    duration = fields.Float(
        compute='_get_times',
    )
    diff = fields.Float(
        compute='_get_times',
    )
    to_pay = fields.Float(
        compute='_get_times',
    )

    @api.depends('report_id', 'user_id')
    def _get_work_ids(self):
        Work = self.env['planned.work']
        for record in self:
            record.work_ids = Work.search([
                ('responsible', '=', record.user_id.id),
                ('work_date', '>=', record.start),
                ('work_date', '<=', record.stop),
            ])

    @api.depends('work_ids')
    def _get_times(self):
        for record in self:
            record.time_spent = sum(record.work_ids.mapped('time_spent'))
            record.duration = sum(record.work_ids.mapped('duration'))
            record.diff = sum(record.work_ids.mapped('diff'))
            # record.to_pay = sum(record.work_ids.mapped('to_pay'))
