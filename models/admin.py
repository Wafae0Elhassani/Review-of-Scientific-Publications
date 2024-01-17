from odoo import models, fields, api
from datetime import date


class Admin(models.TransientModel):
    _name = "revue.admin"
    _description = "Administration des Auteurs"

    author_id = fields.Many2one("revue.author", string="Auteur")
    action = fields.Selection(
        [("publish", "Publier"), ("reject", "Rejeter")], string="Action"
    )
    article_ids = fields.Many2many(
        "revue.article",
        string="Articles à gérer",
        domain=[("status", "=", "under_review")],
    )
    review_info = fields.Html(string="Informations sur la révision", readonly=True)

    @api.onchange("article_ids")
    def update_review_info(self):
        self.review_info = ""
        for article in self.article_ids.filtered(lambda a: a.status == "under_review"):
            for review in article.review_ids:
                reviewer_name = review.reviewer.name if review.reviewer else "Inconnu"
                self.review_info += f"<b>Réviseur:  {reviewer_name} <br> <b>Commentaires de la révision: {review.comments}<br> <b>Statut de la révision: {review.status}<br/><br/>"

    def perform_action(self):
        under_review_articles = self.article_ids.filtered(
            lambda a: a.status == "under_review"
        )
        if self.action == "publish":
            under_review_articles.write(
                {
                    "status": "published",
                    "publication_date": date.today(),
                    "archive_date": date.today(),
                }
            )
        elif self.action == "reject":
            under_review_articles.write({"status": "rejected"})

        return {"type": "ir.actions.act_window_close"}
