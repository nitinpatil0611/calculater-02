from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='draft', tracking=True, copy=False)

    approver_id = fields.Many2one('res.users', string='Approver', tracking=True, copy=False)
    approval_date = fields.Datetime(string='Approval/Rejection Date', tracking=True, copy=False)
    approved_by_id = fields.Many2one('res.users', string='Approved/Rejected By', tracking=True, copy=False)

    def action_approve(self):
        for order in self:
            if order.approver_id and order.approver_id != self.env.user:
                raise UserError(_("Only the assigned approver can approve this quotation."))
            
            order.write({
                'approval_state': 'approved',
                'approval_date': fields.Datetime.now(),
                'approved_by_id': self.env.user.id,
            })
            # Log activity
            order.message_post(body=_("Quotation Approved by %s") % self.env.user.name)
            # Mark activity as done
            self._mark_approval_activity_done('approved')

    def action_reject(self):
        for order in self:
            if order.approver_id and order.approver_id != self.env.user:
                raise UserError(_("Only the assigned approver can reject this quotation."))
            
            order.write({
                'approval_state': 'rejected',
                'approval_date': fields.Datetime.now(),
                'approved_by_id': self.env.user.id,
            })
            # Log activity
            order.message_post(body=_("Quotation Rejected by %s") % self.env.user.name)
            # Mark activity as done
            self._mark_approval_activity_done('rejected')

    def _mark_approval_activity_done(self, status):
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if activity_type:
            activities = self.env['mail.activity'].search([
                ('res_id', '=', self.id),
                ('res_model', '=', 'sale.order'),
                ('activity_type_id', '=', activity_type.id),
                ('summary', '=', 'Quotation Approval Request')
            ])
            for activity in activities:
                activity.action_feedback(feedback=_("Quotation %s") % status.capitalize())

    def action_confirm(self):
        for order in self:
            if order.approval_state != 'approved':
                raise UserError(_("You cannot confirm a quotation that is not approved."))
        return super(SaleOrder, self).action_confirm()























































































































































































































































































































































