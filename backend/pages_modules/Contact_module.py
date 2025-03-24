from backend.pages_modules.common_imports import *
from backend.webforms import PagesForm


def contact():
    contact = Pages.query.filter(Pages.page_category == 'kontakt').first()
    if contact is None:
        init_contact = Pages()
        init_contact.title = 'Kontakt'
        init_contact.description = ''
        init_contact.page_category = 'kontakt'
        db.session.add(init_contact)
        db.session.commit()
        contact = Pages.query.filter(Pages.page_category == 'kontakt').first()

    return render_template("contact/contact.html", contact=contact)

def edit_contact():

    entry = Pages.query.filter(Pages.page_category == 'kontakt').first()

    form = PagesForm(obj=entry)

    if form.validate_on_submit():

        entry.description = form.description.data

        db.session.add(entry)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('contact'))     
    
    form.description.data = entry.description    

    return render_template('contact/edit_contact.html', form=form)












