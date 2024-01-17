from odoo import models, fields, api
from datetime import date


class Review(models.Model):
    _name = "revue.review"
    _description = "Révision d'un article dans la revue des publications scientifiques"

    reviewer = fields.Many2one("res.partner", string="Réviseur", required=True)
    article_id = fields.Many2one("revue.article", string="Article", required=True)
    comments = fields.Text(string="Commentaires de la révision")
    status = fields.Selection(
        [
            ("pending", "En attente"),
            ("approved", "Approuvé"),
            ("rejected", "Rejeté"),
        ],
        default="pending",
        string="Statut de la révision",
    )

    @api.model
    def create(self, values):
        review = super(Review, self).create(values)

        if "status" in values and "article_id" in values:
            article = self.env["revue.article"].browse(values["article_id"])
            if article:
                if (
                    values["status"] == "approved"
                    and article.status != "under_review"
                    and article.status != "published"
                    and article.status != "rejected"
                ):
                    article.write(
                        {
                            "status": "under_review",
                        }
                    )
                elif (
                    values["status"] == "rejected"
                    and article.status != "under_review"
                    and article.status != "published"
                    and article.status != "rejected"
                ):
                    article.write({"status": "under_review"})

        return review

    def write(self, values):
        result = super(Review, self).write(values)

        if "status" in values:
            self._update_article_status(values)

        return result

    def _update_article_status(self, values):
        article = self.env["revue.article"].browse(self.article_id.id)
        if article and "status" in values:
            if (
                values["status"] == "approved"
                and article.status != "under_review"
                and article.status != "published"
                and article.status != "rejected"
            ):
                article.write(
                    {
                        "status": "under_review",
                    }
                )
            elif (
                values["status"] == "rejected"
                and article.status != "under_review"
                and article.status != "published"
                and article.status != "rejected"
            ):
                article.write(
                    {
                        "status": "under_review",
                    }
                )
