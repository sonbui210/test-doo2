from odoo import fields
from datetime import date

def migrate(cr, version):
    cr.execute('SELECT id, date_release_char FROM library_book')
    for record_id, old_date in cr.fetchall():
        #test
        #
        new_date = None
        try:
            new_date = fields.Date.to_date(old_date)
        except ValueError:
            if len(old_date) == 4 and old_date.isdigit():
                new_date = date(int(old_date), 1, 1)
            if new_date:
                cr.execute('UPDATE library_book SET date_release=%s',(new_date,))