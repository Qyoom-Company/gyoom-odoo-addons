from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    @api.depends('parent_id')
    def _compute_coach(self):
        for employee in self:
            manager = employee.parent_id

            # Set the coach_id based on the manager
            if manager and not employee.coach_id:
                employee.coach_id = manager

            # Also set the attendance_manager_id to the same manager if it exists
            if manager:
                employee.attendance_manager_id = manager.user_id
            else:
                employee.attendance_manager_id = False
