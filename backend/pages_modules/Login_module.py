from backend.pages_modules.common_imports import *
from backend.webforms import LoginForm, UserForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from flask_login import current_user

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Zalogowano.")
                return redirect(url_for('dashboard'))
            else:
                flash("Nieprawidłowe hasło. Spróbuj ponownie.")
        else:
            flash("Nieprawidłowa nazwa użytkownika. Spróbuj ponownie.")
    return render_template("login/login.html", form=form)

def dashboard():
    form = UserForm()
    id = current_user.user_id
    user_to_update = Users.query.get_or_404(id)
    
    form.submit.label.text = 'Zmień'

    if request.method == 'POST':
        user_to_update.username = request.form['username']
        user_to_update.name = request.form['name']
        user_to_update.surname = request.form['surname']
        user_to_update.email = request.form['email']

        try:
            db.session.commit()
            flash("Zapisano zmiany.")
        except:
            flash("Nie można zapisać zmian.")
        return render_template("login/dashboard.html", form=form, user_to_update=user_to_update)

    form.username.data = user_to_update.username
    form.name.data = user_to_update.name
    form.surname.data = user_to_update.surname
    form.email.data = user_to_update.email
    
    return render_template("login/dashboard.html", form=form)

def create_user():
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password_hash.data)
            user = Users(
                name = form.name.data,
                surname = form.surname.data,
                username = form.username.data,
                email = form.email.data,
                password_hash = hashed_password
                )
            db.session.add(user)
            db.session.commit()

        form.name.data = ''
        form.surname.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        form.password_hash2.data = ''

        flash("Utworzono konto.")
        return render_template("login/create_user.html", form=form)
    return render_template("login/create_user.html", form=form)
