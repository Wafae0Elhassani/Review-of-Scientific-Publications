from odoo import models, fields


class Author(models.Model):
    _name = "revue.author"
    _description = "Auteur de la revue des publications scientifiques"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Adresse e-mail", required=True)
    articles = fields.Many2many("revue.article", "authors", string="Articles")
    image = fields.Binary(string="Image")
    view_type = fields.Selection(
        selection=[("tree", "Tree View"), ("kanban", "Kanban View")],
        string="Type de Vue",
        compute="_compute_view_type",
        store=True,
    )

    def _compute_view_type(self):
        for author in self:
            author.view_type = self.env.context.get("view_type", "tree")
