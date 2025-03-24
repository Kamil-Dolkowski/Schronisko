from backend.pages_modules.common_imports import *
from backend.webforms import PagesForm

def adoption_procedure():
    adoption_procedure = Pages.query.filter(Pages.page_category == 'proceduraadopcyjna').first()
    if adoption_procedure is None:
        init_adoption_procedure = Pages()
        init_adoption_procedure.title = 'Procedura adopcyjna'
        init_adoption_procedure.description = ''
        init_adoption_procedure.page_category = 'proceduraadopcyjna'
        db.session.add(init_adoption_procedure)
        db.session.commit()
        adoption_procedure = Pages.query.filter(Pages.page_category == 'proceduraadopcyjna').first()

    return render_template("base_of_knowledge/adoption_procedure.html", adoption_procedure = adoption_procedure)

def edit_adoption_procedure():

    adoption_procedure = Pages.query.filter(Pages.page_category == 'proceduraadopcyjna').first()

    form = PagesForm(obj=adoption_procedure)

    if form.validate_on_submit():

        adoption_procedure.description = form.description.data

        db.session.add(adoption_procedure)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('adoption_procedure'))     
    
    form.description.data = adoption_procedure.description    

    return render_template('base_of_knowledge/edit_adoption_procedure.html', form=form)

def after_adoption():
    after_adoption = Pages.query.filter(Pages.page_category == 'poadopcji').first()
    if after_adoption is None:
        init_after_adoption = Pages()
        init_after_adoption.title = 'Po adopcji'
        init_after_adoption.description = ''
        init_after_adoption.page_category = 'poadopcji'
        db.session.add(init_after_adoption)
        db.session.commit()
        after_adoption = Pages.query.filter(Pages.page_category == 'poadopcji').first()

    return render_template("base_of_knowledge/after_adoption.html", after_adoption = after_adoption)

def edit_after_adoption():

    after_adopion = Pages.query.filter(Pages.page_category == 'poadopcji').first()

    form = PagesForm(obj=after_adopion)

    if form.validate_on_submit():

        after_adopion.description = form.description.data

        db.session.add(after_adopion)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('after_adoption'))     
    
    form.description.data = after_adopion.description    

    return render_template('base_of_knowledge/edit_after_adoption.html', form=form)

def FAQ():
    FAQ = Pages.query.filter(Pages.page_category == 'faq').first()
    if FAQ is None:
        init_FAQ = Pages()
        init_FAQ.title = 'FAQ'
        init_FAQ.description = ''
        init_FAQ.page_category = 'faq'
        db.session.add(init_FAQ)
        db.session.commit()
        FAQ = Pages.query.filter(Pages.page_category == 'faq').first()

    return render_template("base_of_knowledge/FAQ.html", FAQ = FAQ)

def edit_FAQ():

    FAQ = Pages.query.filter(Pages.page_category == 'faq').first()

    form = PagesForm(obj=FAQ)

    if form.validate_on_submit():

        FAQ.description = form.description.data

        db.session.add(FAQ)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('FAQ'))     
    
    form.description.data = FAQ.description    

    return render_template('base_of_knowledge/edit_FAQ.html', form=form)
