from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
import psycopg2
from flask_ckeditor import CKEditor
from flask_login import UserMixin, LoginManager, login_required, logout_user

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = "Ad0ptujPs4LubK0t4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://application:Ad0ptujPs4LubK0t4@localhost/schronisko'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # Limit przesyłanych zdjęć: 5MB = 5 * 1024 * 1024

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Pages Modules

from backend.pages_modules import Main_page, News_module, Animals_module, Help_module, Knowladge_module, Colaboration_module, Contact_module, Info_module, Login_module

# Baza danych

from backend.models import db, Users, Animals, Types, Categories, Posts, Pages

migrate = Migrate(app, db)


#======================STRONA GLOWNA==========================

@app.route("/")
def home():
    # 1. Ostatnio trafiły
    three_recently_arrived = Animals.query.order_by(
        Animals.date_on.desc()
    ).filter(
        Animals.category_id == 1, 
        Animals.in_shelter == True,
        Animals.is_deleted == False
    ).limit(3)

    # 2. 3 najnowsze posty
    three_latest_posts = Posts.query.order_by(Posts.post_datetime.desc()).filter(Posts.is_deleted == 'FALSE').limit(3)

    for post in three_latest_posts:
        # ucinanie opisu posta do 300 znaków (wyświetla tylko 2 pierwsze paragrafy)
        # (dozwolone tagi: [p, strong, em, s]; dopisywanie brakujących tagów html)
        original_length = len(bleach.clean(post.description))

        soup = BeautifulSoup(post.description, 'html.parser')
        paragraphs = soup.find_all('p')
        first_two_paragraphs = paragraphs[:2]

        post.description = ''
        number_of_chars = 0

        for p in first_two_paragraphs:
            if len(post.description + str(p)) > 300:
                post.description += str(p)[:300-number_of_chars]
                break
            post.description += str(p)
            number_of_chars += len(post.description)

        exit_length = len(bleach.clean(post.description))

        if original_length != exit_length + 1:
            post.description = post.description[0:-4] + " ...</p>"
        
        post.description = bleach.clean(post.description, tags={'p','strong','em','s'}, strip=True)

    # 3. Nasi Seniorzy
    seniors = db.session.query(
        Animals.animal_id,
        Animals.name,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.in_shelter == True,
        Animals.is_deleted == False,
        Animals.date_of_birth <= datetime.now() - timedelta(days=10*365.25)
    ).all()

    # 4. Schronisko w liczbach
    in_schelter = Animals.query.filter(
        Animals.in_shelter == True,
        Animals.is_deleted == False
    ).count()

    dogs = Animals.query.filter(
        Animals.type_id == 1,
        Animals.in_shelter == True,
        Animals.is_deleted == False
    ).count()

    cats = Animals.query.filter(
        Animals.type_id == 2,
        Animals.in_shelter == True,
        Animals.is_deleted == False
    ).count()

    # arrived_in_current_month = Animals.query.filter(
    #     Animals.date_on > f"{datetime.now().year}-{datetime.now().month}-01",
    #     Animals.is_deleted == False
    # ).count()

    arrived = Animals.query.filter(
        Animals.is_deleted == False
    ).count()

    adoption = Animals.query.filter(
        Animals.category_id == 2,
        Animals.in_shelter == False,
        Animals.is_deleted == False
    ).count()

    # found_home = Animals.query.filter(
    #     Animals.in_shelter == False,
    #     Animals.is_deleted == False
    # ).count()

    back_home = Animals.query.filter(
        Animals.category_id == 1,
        Animals.in_shelter == False,
        Animals.is_deleted == False
    ).count()

    return render_template(
        "home.html", 
        three_recently_arrived = three_recently_arrived,
        three_latest_posts = three_latest_posts, 
        seniors = seniors, 
        in_schelter = in_schelter,
        dogs = dogs,
        cats = cats,
        arrived = arrived,
        adoption = adoption,
        back_home = back_home
    )

#=======================AKTUALNOSCI===========================

# Wyświetlanie wszystkich postów
@app.route("/aktualnosci")
def posts():
    return News_module.posts()

# Wyświetlenie szczegółów posta
@app.route("/aktualnosci/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("posts/post.html", post=post)

# Dodawanie nowego posta
@app.route("/aktualnosci/dodaj-post", methods=['GET', 'POST'])
@login_required
def add_post():
    return News_module.add_post()

# Edycja posta
@app.route("/aktualnosci/edytuj-post/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    return News_module.edit_post(id)

# Usuwanie posta
@app.route("/aktualnosci/usun-post/<int:id>")
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    post_to_delete.is_deleted = True

    db.session.add(post_to_delete)
    db.session.commit()
    flash("Usunięto post.")

    return redirect(url_for('posts'))

#=========================ZWIERZETA===========================

@app.route("/zwierzeta")
def animals():
    return render_template("animals/animals.html")

@app.route("/zwierzeta/usuniete")
@login_required
def deleted_animals():
    return Animals_module.deleted_animals()

@app.route("/zwierzeta/<int:id>", methods=['GET','POST'])
def animal(id):
    return Animals_module.animal(id, app.config['UPLOAD_FOLDER'])

@app.route("/zwierzeta/usuniete/<int:id>", methods=['GET','POST'])
@login_required
def deleted_animal(id):
    return Animals_module.deleted_animal(id, app.config['UPLOAD_FOLDER'])

@app.route("/zwierzeta/niedawno-trafily")
def recently_arrived():
    return Animals_module.recently_arrived()

@app.route("/zwierzeta/psy-do-adopcji")
def dogs_to_adoption():
    return Animals_module.dogs_to_adoption()

@app.route("/zwierzeta/koty-do-adopcji")
def cats_to_adoption():
    return Animals_module.cats_to_adoption()

@app.route("/zwierzeta/znalazly-dom")
def found_home():
    return Animals_module.found_home()

@app.route("/zwierzeta/dodaj-zwierze", methods=['GET', 'POST'])
@login_required
def add_animal():
    return Animals_module.add_animal()

@app.route("/zwierzeta/edytuj-zwierze/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_animal(id):
    return Animals_module.edit_animal(id)

@app.route("/zwierzeta/usun-zwierze/<int:id>", methods=['GET','POST'])
@login_required
def delete_animal(id):
    return Animals_module.delete_animal(id)

@app.route("/zwierzeta/usuniete/przywroc-zwierze/<int:id>", methods=['GET','POST'])
@login_required
def restore_animal(id):
    return Animals_module.restore_animal(id)

#===========================JAK POMOC==============================

#Jak pomoc - menu
@app.route("/jak-pomoc")
def how_to_help():
    return render_template("how_to_help/how_to_help.html", how_to_help=how_to_help)

#wolontariat - wyswietl
@app.route("/wolontariat")
def volunteering():
    return Help_module.volunteering()

#wolontariat - edycja
@app.route("/wolontariat/edycja", methods=['GET', 'POST'])
@login_required
def edit_volunteering():
    return Help_module.edit_volunteering()

#darowizny rzeczowe - podglad
@app.route("/darowizny-rzeczowe")
def in_kind_donations():
    return Help_module.in_kind_donations()

#darowizny rzeczowe - edycja
@app.route("/darowizny-rzeczowe/edycja", methods=['GET', 'POST'])
@login_required
def edit_in_kind_donations():
    return Help_module.edit_in_kind_donations()

#darowizny finansowe - podglad
@app.route("/darowizny-finansowe")
def financial_donations():
    return Help_module.financial_donations()

#darowizny finansowe - edycja
@app.route("/darowizny-finansow/edycja", methods=['GET', 'POST'])
@login_required
def edit_financial_donations():
    return Help_module.edit_financial_donations()

#===========================BAZA WIEDZY========================

#Baza wiedzy - menu
@app.route("/baza-wiedzy")
def base_of_knowledge():
    return render_template("base_of_knowledge/base_of_knowledge.html", base_of_knowledge=base_of_knowledge)

#procedura adopcyjna - wyswietlanie
@app.route("/procedura-adopcyjna")
def adoption_procedure():
    return Knowladge_module.adoption_procedure()

#procedura adopcyjna - edycja
@app.route("/procedura-adopcyjna/edycja", methods=['GET', 'POST'])
@login_required
def edit_adoption_procedure():
    return Knowladge_module.edit_adoption_procedure()

#po adopcji - wyswietlanie
@app.route("/po-adopcji")
def after_adoption():
    return Knowladge_module.after_adoption()

#po adopcji - edycja
@app.route("/po-adopcji/edycja", methods=['GET', 'POST'])
@login_required
def edit_after_adoption():
    return Knowladge_module.edit_after_adoption()

#FAQ - podglad
@app.route("/FAQ")
def FAQ():
    return Knowladge_module.FAQ()

#FAQ - edycja
@app.route("/FAQ/edycja", methods=['GET', 'POST'])
@login_required
def edit_FAQ():
    return Knowladge_module.edit_FAQ()

#==========================WSPOLPRACA=========================

#Wspolpraca - menu
@app.route("/wspolpraca")
def collaboration():
    return render_template("collaboration/collaboration.html", collaboration=collaboration)

#Dla szkol - wyswietlanie
@app.route("/dla-szkol")
def for_schools():
    return Colaboration_module.for_schools()

#Dla szkol - edycja
@app.route("/dla-szkol/edycja", methods=['GET', 'POST'])
@login_required
def edit_for_schools():
    return Colaboration_module.edit_for_schools()

#Dla samorzadow - wyswietlanie
@app.route("/dla-samorzadow")
def for_local_government():
    return Colaboration_module.for_local_government()

#Dla samorzadow - edycja
@app.route("/dla-samorzadow/edycja", methods=['GET', 'POST'])
@login_required
def edit_for_local_government():
    return Colaboration_module.edit_for_local_government()

#Dla firm - wyswietlanie
@app.route("/dla-firm")
def for_firms():
    return Colaboration_module.for_firms()

#Dla firm - edycja
@app.route("/dla-firm/edycja", methods=['GET', 'POST'])
@login_required
def edit_for_firms():
    return Colaboration_module.edit_for_firms()

#==========================KONTAKT============================

# Kontakt - podglad tresci
@app.route("/kontakt")
def contact():
    return Contact_module.contact()

# Kontakt - edycja tresci
@app.route("/kontakt/edycja", methods=['GET', 'POST'])
@login_required
def edit_contact():
    return Contact_module.edit_contact()

#==========================LOGOWANIE==========================

#Info o adopcji - podglad tresci
@app.route("/info")
def pages():
    return Info_module.pages()

#Info
@app.route("/info/<int:id>")
def page(id):
    page = Pages.query.get_or_404(id)
    return render_template("info.html", page=page)

#dodanie info
@app.route("/info/dodaj-info", methods=['GET', 'POST'])
@login_required
def add_page():
    return Info_module.add_page()

#Info o adopcji - edycja
@app.route("/info/edycja/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_page(id):
    return Info_module.edit_page(id)

#==========================LOGOWANIE==========================

# Logowanie
@app.route("/logowanie", methods=['GET', 'POST'])
def login():
    return Login_module.login()

# Wylogowywanie
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Zostałeś wylogowany.")
    return redirect(url_for('login'))

# Dashboard
@app.route("/moje-konto", methods=['GET', 'POST'])
@login_required
def dashboard():
    return Login_module.dashboard()

# Tworzenie konta
@app.route("/utworz-konto", methods=['GET', 'POST'])
def create_user():
    return Login_module.create_user()

#=====================BLEDY 404 I 500=========================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500