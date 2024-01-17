from odoo import models, fields


class Reviewer(models.Model):
    _name = "revue.reviewer"
    _description = "Réviseur dans la revue des publications scientifiques"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Adresse e-mail", required=True)
    articles_reviewed = fields.Many2many("revue.article", string="Articles révisés")
    image = fields.Binary(string="Image")
    view_type = fields.Selection(
        selection=[("tree", "Tree View"), ("kanban", "Kanban View")],
        string="Type de Vue",
        compute="_compute_view_type",
        store=True,
    )

    def _compute_view_type(self):
        for reviewer in self:
            reviewer.view_type = self.env.context.get("view_type", "tree")
