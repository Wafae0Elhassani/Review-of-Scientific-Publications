from odoo import models, fields, api


class Article(models.Model):
    _name = "revue.article"
    _description = "Article de la revue des publications scientifiques"

    name = fields.Char(string="Titre", required=True)
    authors = fields.Many2many("revue.author", string="Auteurs")
    keywords = fields.Many2many("revue.keyword", string="Mots-clés")
    abstract = fields.Text(string="Résumé")
    content = fields.Html(string="Contenu")
    attachment = fields.Binary(string="Fichier attaché")
    attachment_filename = fields.Char(string="Nom du fichier")
    status = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submitted", "Soumis"),
            ("under_review", "En révision"),
            ("accepted", "Accepté"),
            ("rejected", "Rejeté"),
            ("published", "Publié"),
        ],
        default="submitted",
        string="Statut",
        readonly=True,
    )
    review_ids = fields.One2many("revue.review", "article_id", string="Révisions")
    publication_date = fields.Date(string="Date de publication", readonly=True)
    archive_date = fields.Date(string="Date d'archivage", readonly=True)

    @api.model
    def create(self, values):
        attachment_data = values.pop("attachment", False)
        attachment_filename_data = values.pop("attachment_filename", False)
        new_record = super(Article, self).create(values)
        if attachment_data:
            new_record.write(
                {
                    "attachment": attachment_data,
                    "attachment_filename": attachment_filename_data,
                }
            )
        return new_record
