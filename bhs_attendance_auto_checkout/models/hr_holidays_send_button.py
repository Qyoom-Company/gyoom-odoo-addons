from datetime import timedelta, datetime
from odoo import models, api, _
import logging

# Set up logging
_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def send_holiday_reminders(self):
        _logger.info("Starting to send holiday reminders.")

        # Retrieve all upcoming holiday records from resource.calendar.leaves
        upcoming_holidays = self.env['resource.calendar.leaves'].search([])  # Adjust this search query as needed
        _logger.info("Found %d holiday records.", len(upcoming_holidays))

        if not upcoming_holidays:
            _logger.warning("No holiday records found. No emails will be sent.")
            return

        for holiday in upcoming_holidays:
            _logger.info("Processing holiday: %s",
                         holiday.name)  # Assuming 'name' is a field that describes the holiday

            # Construct the email body
            # email_body = (
            #     f"<p>Dear Team,</p>"
            #     f"<p>This is a reminder for the upcoming holiday: <strong>{holiday.name}</strong>.</p>"
            #     f"<p>Please take note of this date:</p>"
            #     f"<p><strong>Date:</strong> {holiday.date_from}</p>"
            #     f"<p>Kind regards,<br/>Your Company Name</p>"
            # )

            email_body = (
                f"<p>فريقنا العزيز،</p>"
                f"<p>هذا تذكير بالعطلة القادمة: <strong>{holiday.name}</strong>.</p>"
                f"<p>يرجى ملاحظة هذا التاريخ:</p>"
                f"<p><strong>التاريخ:</strong> {holiday.date_from}</p>"
                f"<p>مع أطيب التحيات،<br/></p>"
            )

            # Get the recipients - adjust this as per your needs
            recipients = ['recipient@example.com']  # You can fetch recipients from a different model if needed

            # Send the email
            try:
                mail_values = {
                    'subject': f"Reminder: Upcoming Holiday - {holiday.name}",
                    'body_html': email_body,
                    'email_to': ','.join(recipients),
                    'email_from': self.env.user.email or 'no-reply@example.com',
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()
                _logger.info("Email sent for holiday: %s", holiday.name)
            except Exception as e:
                _logger.error("Failed to send email for holiday %s: %s", holiday.name, str(e))

        _logger.info("Completed sending holiday reminders.")
