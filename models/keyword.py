from odoo import models, fields


class Keyword(models.Model):
    _name = "revue.keyword"
    _description = "Mot-clé de la revue des publications scientifiques"

    name = fields.Char(string="Mot-clé", required=True)
    articles = fields.Many2many("revue.article", string="Articles liés")
