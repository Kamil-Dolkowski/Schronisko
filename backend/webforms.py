from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, ValidationError, SelectField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    description = CKEditorField("Opis", validators=[DataRequired()])
    title_img = FileField("Zdjęcie tytułowe", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    images = MultipleFileField("Galeria zdjęć", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    submit = SubmitField("Dodaj")

class UserForm(FlaskForm):
    name = StringField("Imię", validators=[DataRequired()])
    surname = StringField("Nazwisko", validators=[DataRequired()])
    username = StringField("Nazwa użytkownika", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Hasło", validators=[DataRequired(), EqualTo('password_hash2', message='Podane hasła muszą być te same.')])
    password_hash2 = PasswordField("Potwierdź hasło", validators=[DataRequired()])
    submit = SubmitField("Utwórz")  

class LoginForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")

class PagesForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    description = CKEditorField("Opis", validators=[DataRequired()])
    title_img = FileField("Zdjęcie tytułowe", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    images = MultipleFileField("Galeria zdjęć", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    submit = SubmitField("Zapisz")

class AnimalForm(FlaskForm):
    category = SelectField("Kategoria", choices=[], validators=[DataRequired()], coerce=int)
    name = StringField("Imię", validators=[Optional()])
    type = SelectField("Gatunek", choices=[], validators=[DataRequired()], coerce=int)
    sex = SelectField("Płeć", choices=[('samiec','samiec'), ('samica','samica')], validators=[DataRequired()])
    castration_sterilization = SelectField("Kastracja/sterylizacja", choices=[('true','tak'), ('false','nie')], validators=[], coerce=lambda x: x == 'true')
    age = IntegerField("Wiek", validators=[Optional()])
    fur = StringField("Futro", validators=[Optional()])
    weight = IntegerField("Waga (kg)", validators=[Optional()])
    number = StringField("Numer", validators=[DataRequired()])
    box = StringField("Boks", validators=[DataRequired()])
    attitude_to_dogs = StringField("Stosunek do psów", validators=[Optional()])
    attitude_to_cats = StringField("Stosunek do kotów", validators=[Optional()])
    attitude_to_people = StringField("Stosunek do ludzi", validators=[Optional()])
    character = StringField("Charakter", validators=[Optional()])
    description = CKEditorField("Opis", validators=[DataRequired()])
    title_img = FileField("Zdjęcie tytułowe", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    images = MultipleFileField("Galeria zdjęć", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Obsługiwane rozszerzenia: png, jpg, jpeg')])
    submit = SubmitField("Dodaj") 

class AnimalMigrateForm(FlaskForm):
    recently_arrived = SubmitField("Niedawno trafiły") 
    to_adoption = SubmitField("Do adopcji") 
    found_home = SubmitField("Znalazły dom")

class AnimalSearch(FlaskForm):
    sex_options = [
        (None,'Wszystkie'), 
        ('samiec','Samiec'), 
        ('samica','Samica')
    ]
    age_options = [
        (None,'Wszystkie'),
        (1,'Do 1 roku'),
        ('wszystkie','1-4 lata'),
        ('wszystkie','5-9 lat'),
        ('wszystkie','10 lat i więcej')
    ]
    weight_options = [
        (None,'Wszystkie'),
        (1,'Do 5 kg'),
        ('wszystkie','5-14 kg'),
        ('wszystkie','15-30 kg'),
        ('wszystkie','31-45 kg'),
        ('wszystkie','45 kg i więcej')
    ]

    name_or_number = StringField("Imię lub numer", validators=[Optional()])
    type = SelectField("Gatunek", choices=[], validators=[Optional()], coerce=int)
    category = SelectField("Kategoria", choices=[], validators=[Optional()], coerce=int)
    sex = SelectField("Płeć", choices=sex_options, validators=[Optional()], coerce=lambda x: x == None)
    age = SelectField("Wiek", choices=age_options, validators=[Optional()], coerce=lambda x: x == None)
    weight = SelectField("Waga", choices=weight_options, validators=[Optional()], coerce=lambda x: x == None)
    seniors = BooleanField("Seniorzy")
    submit = SubmitField("Szukaj")