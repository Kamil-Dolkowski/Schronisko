from common_imports import *
from webforms import PagesForm

def pages():
    pages = Pages.query.order_by(Pages.page_id.desc())
    
    for page in pages:
        # ucinanie opisu posta do 300 znaków (wyświetla tylko 2 pierwsze paragrafy)
        # (dozwolone tagi: [p, strong, em, s]; dopisywanie brakujących tagów html)
        original_length = len(bleach.clean(page.description))

        soup = BeautifulSoup(page.description, 'html.parser')
        paragraphs = soup.find_all('p')
        first_two_paragraphs = paragraphs[:2]

        page.description = ''
        number_of_chars = 0

        for p in first_two_paragraphs:
            if len(page.description + str(p)) > 300:
                page.description += str(p)[:300-number_of_chars]
                break
            page.description += str(p)
            number_of_chars += len(page.description)

        exit_length = len(bleach.clean(page.description))

        if original_length != exit_length + 1:
            page.description = page.description[0:-4] + " ...</p>"
        
        page.description = bleach.clean(page.description, tags={'p','strong','em','s'}, strip=True)
    return render_template("pages.html", pages=pages)

def add_page():
    form = PagesForm()
    if form.validate_on_submit():
        page = Pages(
            title = form.title.data, 
            description = form.description.data
            )
        
        form.title.data = ''
        form.description.data = ''

        db.session.add(page)
        db.session.commit()
        flash("Dodano info!")

    return render_template("add_info.html", form=form)

def edit_page(id):

    page = Pages.query.get_or_404(id)

    form = PagesForm(obj=page)

    if form.validate_on_submit():
        
        page.title = form.title.data, 
        page.description = form.description.data
        
        form.title.data = ''
        form.description.data = ''

        db.session.add(page)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('page', id=page.page_id))  
      
    form.title.data = page.title
    form.description.data = page.description
    return render_template('edit_info.html', form=form)