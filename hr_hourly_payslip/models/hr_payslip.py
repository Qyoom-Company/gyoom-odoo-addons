# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models


class HrPayslip(models.Model):
    """Class for the inherited model hr_payslip"""
    _inherit = 'hr.payslip'

    total_hours = fields.Float(string='Total Hours',
                               compute='_compute_total_hours',
                               help='Total worked hours of the employee in the'
                                    ' selected period of time.', digits=(16, 4))
    total_logged_hours = fields.Float(string='Total Hours Logged Manually by Manager',
                               compute='_compute_manuall_total_hours',
                               help='Total Logged worked hours of the employee in the'
                                    ' selected period of time.', digits=(16, 4))

    hour_based_salary = fields.Float(string='Hour Based Salary',
                                     help='Salary based on the worked hours '
                                          'for the employee',
                                     compute='_compute_hour_based_salary')
    show_total_hours = fields.Boolean(string='Related Boolean', default=False,
                                      help='Will show total_hours in the view'
                                           ' only if hourly_payslip is enabled'
                                           ' in the hr_contract.')
    show_total_manually_hours = fields.Boolean(string='Related Boolean', default=False,
                                      help='Will show total_hours in the view'
                                           ' only if hourly_payslip is enabled'
                                           ' in the hr_contract.')

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        """This function helps to show the Total Hours field if the hourly
            payslip is available for the employee."""
        if self.contract_id and self.contract_id.hourly_payslip is True:
            self.show_total_hours = True
        if self.contract_id and self.contract_id.hourly_manually_logs is True:
            self.show_total_manually_hours = True

    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_total_hours(self):
        """Function to compute total worked hours for the particular employee
           for the given period of date."""
        for record in self:
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', record.date_from),
                ('check_in', '<=', record.date_to)
            ])
            record.total_hours = sum(attendances.mapped('worked_hours'))

    def _compute_manuall_total_hours(self):
        """Function to compute manually logged total hours for the particular employee
           for the given period of date."""
        for record in self:
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', record.date_from),
                ('check_in', '<=', record.date_to)
            ])
            record.total_logged_hours = sum(attendances.mapped('working_hours_manager'))

    @api.depends('total_hours')
    def _compute_hour_based_salary(self):
        """Function to compute salary based on the worked hours for the
            employee"""
        for record in self:
            record.hour_based_salary = self.env['hr.contract'].search(
                [('employee_id', '=', record.employee_id.id),
                 ('state', '=', 'open')]).hourly_wage * record.total_hours
