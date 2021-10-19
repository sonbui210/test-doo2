from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class LibraryBookRent(models.Model):
    _name = "library.book.rent"

    book_id = fields.Many2one("library.book", "Book", required=True)
    borrower_id = fields.Many2one("res.partner", "Borroer", required=True)
    state = fields.Selection([
        ("ongoing", "Ongoing"),
        ("returned", "Returned")],
        "State", default="ongoing", required=True)
    rent_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()


    @api.model
    def create(self, vals):
        book_rec = self.env["library.book"].browse(vals["book_id"])
        book_rec.make_borrowed()
        return super(LibraryBookRent, self).create(vals)

    def book_return(self):
        self.ensure_one()
        self.book_id.make_available()
        self.write({
            "state": "returned",
            "return_date": fields.Date.today()
        })