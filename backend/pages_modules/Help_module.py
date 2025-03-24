from backend.pages_modules.common_imports import *
from backend.webforms import PagesForm

def volunteering():
    volunteering = Pages.query.filter(Pages.page_category == 'wolontariat').first()
    if volunteering is None:
        init_volunteering = Pages()
        init_volunteering.title = 'Wolontariat'
        init_volunteering.description = ''
        init_volunteering.page_category = 'wolontariat'
        db.session.add(init_volunteering)
        db.session.commit()
        volunteering = Pages.query.filter(Pages.page_category == 'wolontariat').first()

    return render_template("how_to_help/volunteering.html", volunteering = volunteering)

def edit_volunteering():

    volunteering = Pages.query.filter(Pages.page_category == 'wolontariat').first()

    form = PagesForm(obj=volunteering)

    if form.validate_on_submit():

        volunteering.description = form.description.data

        db.session.add(volunteering)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('volunteering'))     
    
    form.description.data = volunteering.description    

    return render_template('how_to_help/edit_volunteering.html', form=form)

def in_kind_donations():
    in_kind_donations = Pages.query.filter(Pages.page_category == 'darowiznyrz').first()
    if in_kind_donations is None:
        init_in_kind_donations = Pages()
        init_in_kind_donations.title = 'Darowizny Rzeczowe'
        init_in_kind_donations.description = ''
        init_in_kind_donations.page_category = 'darowiznyrz'
        db.session.add(init_in_kind_donations)
        db.session.commit()
        in_kind_donations = Pages.query.filter(Pages.page_category == 'darowiznyrz').first()

    return render_template("how_to_help/in_kind_donations.html", in_kind_donations = in_kind_donations)

def edit_in_kind_donations():

    in_kind_donations = Pages.query.filter(Pages.page_category == 'darowiznyrz').first()

    form = PagesForm(obj=in_kind_donations)

    if form.validate_on_submit():

        in_kind_donations.description = form.description.data

        db.session.add(in_kind_donations)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('in_kind_donations'))     
    
    form.description.data = in_kind_donations.description    

    return render_template('how_to_help/edit_in_kind_donations.html', form=form)

def financial_donations():
    financial_donations = Pages.query.filter(Pages.page_category == 'darowiznyf').first()
    if financial_donations is None:
        init_financial_donations = Pages()
        init_financial_donations.title = 'Darowizny Rzeczowe'
        init_financial_donations.description = ''
        init_financial_donations.page_category = 'darowiznyf'
        db.session.add(init_financial_donations)
        db.session.commit()
        financial_donations = Pages.query.filter(Pages.page_category == 'darowiznyf').first()

    return render_template("how_to_help/financial_donations.html", financial_donations = financial_donations)

def edit_financial_donations():

    financial_donations = Pages.query.filter(Pages.page_category == 'darowiznyf').first()

    form = PagesForm(obj=financial_donations)

    if form.validate_on_submit():

        financial_donations.description = form.description.data

        db.session.add(financial_donations)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('financial_donations'))     
    
    form.description.data = financial_donations.description    

    return render_template('how_to_help/edit_financial_donations.html', form=form)






