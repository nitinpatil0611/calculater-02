from odoo import models, fields, api, _

class SaleApprovalWizard(models.TransientModel):
    _name = 'sale.approval.wizard'
    _description = 'Sale Approval Wizard'

    user_id = fields.Many2one(
        'res.users',
        string="Select Approver",
        required=True,
        domain=lambda self: [('id', '!=', self.env.uid)]
    )

    def action_confirm_approver(self):
        order = self.env['sale.order'].browse(
            self.env.context.get('active_id')
        )

        order.write({
            'approver_id': self.user_id.id,
            'approval_state': 'pending'
        })

        # Create activity for the selected approver
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if activity_type:
            self.env['mail.activity'].create({
                'activity_type_id': activity_type.id,
                'summary': 'Quotation Approval Request',
                'note': _('Quotation %s requires your approval.') % order.name,
                'res_id': order.id,
                'res_model_id': self.env['ir.model']._get('sale.order').id,
                'user_id': self.user_id.id,
            })
        
        # Log message in chatter
        order.message_post(body=_("Approval request sent to %s") % self.user_id.name)
