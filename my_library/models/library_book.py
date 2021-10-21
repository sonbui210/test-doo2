# # -*- coding: utf-8 -*-
# import logging
#
# from odoo import models, fields, api
# from odoo.exceptions import UserError
# from odoo.tools.translate import _
# from odoo.tests.common import Form
#
# logger = logging.getLogger(__name__)
#
#
# class LibraryBook(models.Model):
#     _name = 'library.book'
#     _description = 'Library Book'
#
#
#     short_name = fields.Char("Short name")
#     name = fields.Char('Title', required=True)
#     date_release = fields.Date('Release Date')
#     date_updated = fields.Date("Date Updated")
#     notes = fields.Text("Notes")
#     author_ids = fields.Many2many('res.partner', string='Authors')
#     category_id = fields.Many2one('library.book.category', string='Category')
#
#     state = fields.Selection([
#         ('draft', 'Unavailable'),
#         ('available', 'Available'),
#         ('borrowed', 'Borrowed'),
#         ('lost', 'Lost')],
#         'State', default="draft")
#
#     manager_remarks = fields.Text("Manager remarks")
#
#     isbn = fields.Char("ISBN")
#
#     old_edition = fields.Many2one("library.book", string="Ole Edition")
#
#     pages = fields.Integer("Number Of Pages")
#
#     cost_price = fields.Float("Book Cost")
#
#     cover = fields.Binary("Book Cover")
#
#     out_of_print = fields.Boolean("Out Of Print?")
#
#     reader_rating = fields.Float(
#         "Reader Avarage Rating",
#         digits=(14,4),
#     )
#
#     currency_id = fields.Many2one("res.currency", string="Currency")
#     retail_price = fields.Monetary("Retail Price")
#
#     publisher_id = fields.Many2one("res.partner", string="Publisher",
#                                    ondelete="set null",
#                                    context={},
#                                    domain=[],)
#
#     @api.model
#     def _update_book_price(self):
#         logger.info("Method update_book_price called from XML*****************************************************************************************************************************************************")
#         all_books = self.search([])
#         for book in all_books:
#             book.cost_price +=100
#
#     # @api.model
#     # def update_book_price(self, category, amount_to_increase):
#     #     logger.info("Method update_book_price called from XML*****************************************************************************************************************************************************")
#     #     category_books = self.search([("category_id","=", category.id)])
#     #     for book in category_books:
#     #         book.cost_price += amount_to_increase
#
#     @api.model
#     def _get_average_cost(self):
#         gruoped_result = self.read_group(
#             [("cost_price", "!=", False)], #Domain
#             ["category_id", "cost_price:avg"], #Fields to access
#             ["category_id"] #group_by
#         )
#         return gruoped_result
#
#     def groupped_data(self):
#         data = self._get_average_cost()
#         logger.info("Grouped Data %s" % data)
#         print(data)
#
#     def name_get(self):
#         result = []
#         for book in self:
#             authors = book.author_ids.mapped("name")
#             name = "%s (%s)" % (book.name, ", ".join(authors))
#             result.append((book.id, name))
#             return result
#
#     @api.model
#     def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
#         args = [] if args is None else args.copy()
#         if not(name == "" and operator == "ilike"):
#             args += ["|", "|",
#                      ("name", operator, name),
#                      ("isbn", operator, name),
#                      ("author_ids.name", operator, name)]
#         return super(LibraryBook, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
#
#     @api.model
#     def is_allowed_transition(self, old_state, new_state):
#         allowed = [('draft', 'available'),
#                    ('available', 'borrowed'),
#                    ('borrowed', 'available'),
#                    ('available', 'lost'),
#                    ('borrowed', 'lost'),
#                    ('lost', 'available')]
#         return (old_state, new_state) in allowed
#
#     def change_state(self, new_state):
#         for book in self:
#             if book.is_allowed_transition(book.state, new_state):
#                 book.state = new_state
#             else:
#                 message = _('Moving from %s to %s is not allowed') % (book.state, new_state)
#                 raise UserError(message)
#
#     def make_available(self):
#         self.change_state('available')
#
#     def make_borrowed(self):
#         self.change_state('borrowed')
#
#     def make_lost(self):
#         self.ensure_one()
#         self.change_state('lost')
#         if not self.env.context.get("avoid_deactivate"):
#             self.active=False
#
#     def log_all_library_members(self):
#         library_member_model = self.env['library.member']  # This is an empty recordset of model library.member
#         all_members = library_member_model.search([])
#         print("ALL MEMBERS:", all_members)
#         return True
#
#
#     def create_categories(self):
#         categ1 = {
#             'name': 'Child category 1',
#             'description': 'Description for child 1'
#         }
#         categ2 = {
#             'name': 'Child category 2',
#             'description': 'Description for child 2'
#         }
#         parent_category_val = {
#             'name': 'Parent category',
#             'description': 'Description for parent category',
#             'child_ids': [
#                 (0, 0, categ1),
#                 (0, 0, categ2),
#             ]
#         }
#         # Total 3 records (1 parent and 2 child) will be craeted in library.book.category model
#         record = self.env['library.book.category'].create(parent_category_val)
#         return True
#
#     def change_release_date(self):
#         self.ensure_one()
#         self.date_release = fields.Date.today()
#
#     def find_book(self):
#         domain = [
#             '|',
#                 '&', ('name', 'ilike', 'Book Name'),
#                      ('category_id.name', '=', 'Category Name'),
#                 '&', ('name', 'ilike', 'Book Name 2'),
#                      ('category_id.name', '=', 'Category Name 2')
#         ]
#         books = self.search(domain)
#         logger.info('Books found: %s', books)
#         return True
#
#     # Filter recordset
#     def filter_books(self):
#         all_books = self.search([])
#         filtered_books = self.books_with_multiple_authors(all_books)
#         logger.info('Filtered Books: %s', filtered_books)
#
#     @api.model
#     def books_with_multiple_authors(self, all_books):
#         def predicate(book):
#             if len(book.author_ids) > 1:
#                 return True
#         return all_books.filtered(predicate)
#
#     # Traversing recordset
#     def mapped_books(self):
#         all_books = self.search([])
#         books_authors = self.get_author_names(all_books)
#         logger.info('Books Authors: %s', books_authors)
#
#     @api.model
#     def get_author_names(self, all_books):
#         return all_books.mapped('author_ids.name')
#
#     # Sorting recordset
#     def sort_books(self):
#         all_books = self.search([])
#         books_sorted = self.sort_books_by_date(all_books)
#         logger.info('Books before sorting: %s', all_books)
#         logger.info('Books after sorting: %s', books_sorted)
#
#     @api.model
#     def sort_books_by_date(self, all_books):
#         return all_books.sorted(key='date_release')
#
#
#     @api.model
#     def create(self, values):
#         if self.user_has_groups("my_library.acl_book_librarian"):
#             if 'manager_remarks' in values:
#                 raise UserError(
#                     "You are not allowed to modify "
#                     + "manager_remarks"
#                 )
#         return super(LibraryBook, self).create(values)
#
#     def write(self, values):
#         if self.user_has_groups("my_library.acl_book_librarian"):
#             if "manager_remarks" in values:
#                 raise UserError(
#                     "You are not allowed to modify "
#                     + "manager_remarks"
#                 )
#         return super(LibraryBook, self).write(values)
#
#     def book_rent(self):
#         self.ensure_one()
#         if self.state != "available":
#             raise UserError(_("Book is not available for renting"))
#         rent_as_superuser = self.env["library.book.rent"].sudo()
#         rent_as_superuser.create({
#             "book_id": self.id,
#             "borrower_id": self.env.user.partner_id.id,
#         })
#         return True
#
#     def average_book_occupation(self):
#         self.flush()
#         sql_query = """
#             SELECT
#                 lb.name,
#                 avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
#             FROM
#                 library_book_rent AS lbr
#             JOIN
#                 library_book as lb ON lb.id = lbr.book_id
#             WHERE lbr.state = 'returned'
#             GROUP BY lb.name;"""
#
#         self.env.cr.execute(sql_query)
#
#         result = self.env.cr.fetchall()
#         logger.info("Average book occupation: %s", result)
#         print(result)
#
#
#     def return_all_books(self):
#         self.ensure_one()
#         wizard = self.env['library.return.wizard']
#         with Form(wizard) as return_form:
#             return_form.borrower_id = self.env.user.partner_id
#             record = return_form.save()
#             record.books_returns()
#
#
#
# class LibraryMember(models.Model):
#
#     _name = 'library.member'
#     _inherits = {'res.partner': 'partner_id'}
#     _description = "Library member"
#
#     partner_id = fields.Many2one('res.partner', ondelete='cascade')
#     date_start = fields.Date('Member Since')
#     date_end = fields.Date('Termination Date')
#     member_number = fields.Char()
#     date_of_birth = fields.Date('Date of birth')
#
#
# class ResPartner(models.Model):
#
#     _inherit = "res.partner"
#
#     published_book_ids = fields.One2many("library.book", "publisher_id", string="Published Books")
#     authored_book_ids = fields.Many2many(
#         "library.book",
#         string="Authored Books",
#     )
#
#
# # class LibraryRentWizard(models.TransientModel):
# #     _name = "library.rent.wizard"
# #
# #     borrower_id = fields.Many2one("res.partner", string="Borrower")
# #     book_ids = fields.Many2many("library.book", string="Books")
# #
# #     def add_book_rents(self):
# #         rentModel = self.env["library.book.rent"]
# #         for wiz in self:
# #             for book in wiz.book_ids:
# #                 rentModel.create({
# #                     "borrower_id": wiz.borrower_id.id,
# #                     "book_id": book.id
# #                 })
#


# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tests.common import Form


import logging

_logger = logging.getLogger(__name__)


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    active = fields.Boolean(default=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State', default="available")
    cost_price = fields.Float('Book Cost')
    category_id = fields.Many2one('library.book.category')

    def make_available(self):
        self.ensure_one()
        self.state = 'available'

    def make_borrowed(self):
        self.ensure_one()
        self.state = 'borrowed'

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False

    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError(_('Book is not available for renting'))
        rent_as_superuser = self.env['library.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id,
        })

    def average_book_occupation(self):
        self.flush()
        sql_query = """
            SELECT
                lb.name,
                avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
            FROM
                library_book_rent AS lbr
            JOIN
                library_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
            GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        _logger.info("Average book occupation: %s", result)

    def return_all_books(self):
        self.ensure_one()
        wizard = self.env['library.return.wizard']
        with Form(wizard) as return_form:
            return_form.borrower_id = self.env.user.partner_id
            record = return_form.save()
            record.books_returns()