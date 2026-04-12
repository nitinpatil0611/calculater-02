{
    'name': 'Sale Order Approval Workflow33',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom approval workflow for Sales Quotations',
    'description': """
        This module replaces the direct 'Confirm' button in Sales Quotations with a 'Get Approval' workflow.
        - Adds a 'Get Approval' button that opens a popup to select an approver.
        - The selected approver can Approve or Reject the quotation.
        - Tracks approval/rejection status, user, and timestamp.
        - Displays approval information in the quotation list and activities.
    """,
    'author': 'Manus',
    'depends': ['sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_approval_wizard_view.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
