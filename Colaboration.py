from common_imports import *
from webforms import PagesForm

def for_schools():
    for_schools = Pages.query.filter(Pages.page_category == 'dlaszkol').first()
    if for_schools is None:
        init_for_schools = Pages()
        init_for_schools.title = 'Dla szkol'
        init_for_schools.description = ''
        init_for_schools.page_category = 'dlaszkol'
        db.session.add(init_for_schools)
        db.session.commit()
        for_schools = Pages.query.filter(Pages.page_category == 'dlaszkol').first()

    return render_template("collaboration/for_schools.html", for_schools = for_schools)

def edit_for_schools():

    for_schools = Pages.query.filter(Pages.page_category == 'dlaszkol').first()

    form = PagesForm(obj=for_schools)

    if form.validate_on_submit():

        for_schools.description = form.description.data

        db.session.add(for_schools)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('for_schools'))     
    
    form.description.data = for_schools.description    

    return render_template('collaboration/edit_for_schools.html', form=form)

def for_local_government():
    for_local_government = Pages.query.filter(Pages.page_category == 'dlasamorzadow').first()
    if for_local_government is None:
        init_for_local_government = Pages()
        init_for_local_government.title = 'Dla samorzadow'
        init_for_local_government.description = ''
        init_for_local_government.page_category = 'dlasamorzadow'
        db.session.add(init_for_local_government)
        db.session.commit()
        for_local_government = Pages.query.filter(Pages.page_category == 'dlasamorzadow').first()

    return render_template("collaboration/for_local_government.html", for_local_government = for_local_government)

def edit_for_local_government():

    for_local_government = Pages.query.filter(Pages.page_category == 'dlasamorzadow').first()

    form = PagesForm(obj=for_local_government)

    if form.validate_on_submit():

        for_local_government.description = form.description.data

        db.session.add(for_local_government)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('for_local_government'))     
    
    form.description.data = for_local_government.description    

    return render_template('collaboration/edit_for_local_government.html', form=form)

def for_firms():
    for_firms = Pages.query.filter(Pages.page_category == 'dlafirm').first()
    if for_firms is None:
        init_for_firms = Pages()
        init_for_firms.title = 'Dla firm'
        init_for_firms.description = ''
        init_for_firms.page_category = 'dlafirm'
        db.session.add(init_for_firms)
        db.session.commit()
        for_firms = Pages.query.filter(Pages.page_category == 'dlafirm').first()

    return render_template("collaboration/for_firms.html", for_firms = for_firms)

def edit_for_firms():

    for_firms = Pages.query.filter(Pages.page_category == 'dlafirm').first()

    form = PagesForm(obj=for_firms)

    if form.validate_on_submit():

        for_firms.description = form.description.data

        db.session.add(for_firms)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('for_firms'))     
    
    form.description.data = for_firms.description    

    return render_template('collaboration/edit_for_firms.html', form=form)
