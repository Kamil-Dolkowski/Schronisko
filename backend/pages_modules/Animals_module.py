from backend.pages_modules.common_imports import *
import os
from backend.webforms import AnimalMigrateForm, AnimalForm
from werkzeug.utils import secure_filename
import uuid

ANIMALS_PER_PAGE = 12

def deleted_animals():
    page = request.args.get('page', 1, type=int)

    deleted_animals = db.session.query(
        Animals.animal_id,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.is_deleted == True
    )

    animals_page = deleted_animals.paginate(page=page, per_page=ANIMALS_PER_PAGE, error_out=True)
    
    return render_template(
        "animals/deleted_animals.html", 
        animals=animals_page, 
        pages_elements=animals_page, 
        url_name='deleted_animals'
    )

def animal(id, upload_folder):
    animal = Animals.query.get_or_404(id)

    if animal.is_deleted == True:
        abort(404)

    form = AnimalMigrateForm()

    if form.validate_on_submit():
        if form.recently_arrived.data:
            animal.category_id = 1
            animal.in_shelter = True
            flash("Zmieniono kategorię na: 'Niedawno trafiły'")
        if form.to_adoption.data:
            animal.category_id = 2
            animal.in_shelter = True
            flash("Zmieniono kategorię na: 'Do adopcji'")
        if form.found_home.data:
            animal.in_shelter = False
            flash("Zmieniono kategorię na: 'Znalazły dom'")

        db.session.add(animal)
        db.session.commit()

        return redirect(url_for('animal', id=animal.animal_id))

    path = upload_folder + 'animals/' + str(id) + '/' 
    is_dir = os.path.isdir(path)

    if is_dir:
        all_files = os.listdir(path)
        images = [img for img in all_files if os.path.isfile(os.path.join(path, img))]
    else:
        images=None

    return render_template("animals/animal.html", animal=animal, images=images, form=form)

def deleted_animal(id, upload_folder):
    animal = Animals.query.get_or_404(id)

    if animal.is_deleted == False:
        abort(404)

    path = upload_folder + 'animals/' + str(id) + '/' 
    is_dir = os.path.isdir(path)

    if is_dir:
        all_files = os.listdir(path)
        images = [img for img in all_files if os.path.isfile(os.path.join(path, img))]
    else:
        images=None

    return render_template("animals/deleted_animal.html", animal=animal, images=images)

def recently_arrived():
    page = request.args.get('page', 1, type=int)

    animals = db.session.query(
        Animals.animal_id,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.category_id == 1,
        Animals.in_shelter == True,
        Animals.is_deleted == False
    )

    animals_page = animals.paginate(page=page, per_page=ANIMALS_PER_PAGE, error_out=True)

    return render_template(
        "animals/recently_arrived.html", 
        animals=animals_page, 
        pages_elements=animals_page, 
        url_name='recently_arrived'
    )

def dogs_to_adoption():
    page = request.args.get('page', 1, type=int)

    animals = db.session.query(
        Animals.animal_id,
        Animals.name,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.category_id == 2,
        Animals.type_id == 1,
        Animals.in_shelter == True,
        Animals.is_deleted == False
    )

    animals_page = animals.paginate(page=page, per_page=ANIMALS_PER_PAGE, error_out=True)

    return render_template(
        "animals/dogs_to_adoption.html", 
        animals=animals_page, 
        pages_elements=animals_page, 
        url_name='dogs_to_adoption'
    )

def cats_to_adoption():
    page = request.args.get('page', 1, type=int)

    animals = db.session.query(
        Animals.animal_id,
        Animals.name,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.category_id == 2,
        Animals.type_id == 2,
        Animals.in_shelter == True,
        Animals.is_deleted == False
    )

    animals_page = animals.paginate(page=page, per_page=ANIMALS_PER_PAGE, error_out=True)

    return render_template(
        "animals/cats_to_adoption.html", 
        animals=animals_page, 
        pages_elements=animals_page, 
        url_name='cats_to_adoption'
    )

def found_home():
    page = request.args.get('page', 1, type=int)

    animals = db.session.query(
        Animals.animal_id,
        Animals.name,
        Animals.sex,
        Animals.age,
        Animals.weight,
        Animals.number,
        Animals.box,
        Animals.title_img_name
    ).filter(
        Animals.in_shelter == False,
        Animals.is_deleted == False
    )

    animals_page = animals.paginate(page=page, per_page=ANIMALS_PER_PAGE, error_out=True)

    return render_template(
        "animals/found_home.html", 
        animals=animals_page, 
        pages_elements=animals_page, 
        url_name='found_home'
    )

def add_animal(upload_path):
    form = AnimalForm()

    types = Types.query.all()
    type_choices = []
    for type in types:
        type_choices.append((type.type_id, type.name))
    form.type.choices = type_choices

    categories = Categories.query.all()
    category_choices = []
    for category in categories:
        category_choices.append((category.category_id, category.name))
    form.category.choices = category_choices
    
    if form.validate_on_submit():
        
        if form.title_img.data:
            safe_filename = secure_filename(form.title_img.data.filename)
            title_img_name = str(uuid.uuid1()) + "_" + safe_filename
        else:
            title_img_name = None

        new_animal = Animals(
            category_id = form.category.data,
            in_shelter = True,
            name = form.name.data,
            type_id = form.type.data, 
            sex = form.sex.data,
            castration_sterilization = form.castration_sterilization.data,
            age = form.age.data,
            fur = form.fur.data,
            weight = form.weight.data,
            number = form.number.data,
            box = form.box.data,
            attitude_to_dogs = form.attitude_to_dogs.data,
            attitude_to_cats = form.attitude_to_cats.data,
            attitude_to_people = form.attitude_to_people.data,
            character = form.character.data,
            description = form.description.data,
            title_img_name = title_img_name
        )

        db.session.add(new_animal)
        db.session.commit()

        # Zapisywanie plików 
        if form.title_img.data or any(img.filename for img in form.images.data):
            catalog_path = os.path.join(upload_path, 'animals', str(new_animal.animal_id))
            os.makedirs(catalog_path, exist_ok=True)

            if form.title_img.data:
                file_path = os.path.join(catalog_path, title_img_name)
                form.title_img.data.save(file_path)

            if any(img.filename for img in form.images.data):
                for file in form.images.data:
                    safe_filename = secure_filename(file.filename)
                    img_name = str(uuid.uuid1()) + "_" + safe_filename

                    file_path = os.path.join(catalog_path, img_name)
                    file.save(file_path)

        flash("Dodano zwierzę.")

        return redirect(url_for('add_animal'))

    return render_template("animals/add_animal.html", form=form)

def edit_animal(id, upload_path):
    form = AnimalForm()

    animal = Animals.query.get_or_404(id)

    types = Types.query.all()
    type_choices = []
    for type in types:
        type_choices.append((type.type_id, type.name))
    form.type.choices = type_choices

    categories = Categories.query.all()
    category_choices = []
    for category in categories:
        category_choices.append((category.category_id, category.name))
    form.category.choices = category_choices

    if form.validate_on_submit():
        
        if form.title_img.data:
            safe_filename = secure_filename(form.title_img.data.filename)
            title_img_name = str(uuid.uuid1()) + "_" + safe_filename
        else:
            title_img_name = None
        
        animal.category_id = form.category.data,
        animal.in_shelter = True,
        animal.name = form.name.data,
        animal.type_id = form.type.data, 
        animal.sex = form.sex.data,
        animal.castration_sterilization = form.castration_sterilization.data,
        animal.age = form.age.data,
        animal.fur = form.fur.data,
        animal.weight = form.weight.data,
        animal.number = form.number.data,
        animal.box = form.box.data,
        animal.attitude_to_dogs = form.attitude_to_dogs.data,
        animal.attitude_to_cats = form.attitude_to_cats.data,
        animal.attitude_to_people = form.attitude_to_people.data,
        animal.character = form.character.data,
        animal.description = form.description.data,
        animal.title_img_name = title_img_name

        db.session.add(animal)
        db.session.commit()

        # Zapisywanie plików 
        if form.title_img.data or any(img.filename for img in form.images.data):
            catalog_path = os.path.join(upload_path, 'animals', str(animal.animal_id))
            os.makedirs(catalog_path, exist_ok=True)

            if form.title_img.data:
                file_path = os.path.join(catalog_path, title_img_name)
                form.title_img.data.save(file_path)

            if any(img.filename for img in form.images.data):
                for file in form.images.data:
                    safe_filename = secure_filename(file.filename)
                    img_name = str(uuid.uuid1()) + "_" + safe_filename

                    file_path = os.path.join(catalog_path, img_name)
                    file.save(file_path)

        flash("Zapisano zmiany!")

        return redirect(url_for('edit_animal'))

    form.type.data = animal.type_id
    form.category.data = animal.category_id
    form.name.data = animal.name
    form.age.data = animal.age
    form.sex.data = animal.sex
    form.castration_sterilization.data = animal.castration_sterilization
    form.weight.data = animal.weight
    form.fur.data = animal.fur
    form.number.data = animal.number
    form.box.data = animal.box
    form.attitude_to_dogs.data = animal.attitude_to_dogs
    form.attitude_to_cats.data = animal.attitude_to_cats
    form.attitude_to_people.data = animal.attitude_to_people
    form.character.data = animal.character
    form.description.data = animal.description

    form.submit.label.text = 'Zapisz'

    return render_template("animals/edit_animal.html", form=form)

def delete_animal(id):
    animal_to_delete = Animals.query.get_or_404(id)

    if animal_to_delete.is_deleted == True:
        abort(404)

    animal_to_delete.is_deleted = True

    db.session.add(animal_to_delete)
    db.session.commit()
    flash("Usunięto zwierzę.")

    return redirect(url_for('animals'))

def restore_animal(id):
    animal_to_restore = Animals.query.get_or_404(id)

    if animal_to_restore.is_deleted == False:
        abort(404)
    
    animal_to_restore.is_deleted = False

    db.session.add(animal_to_restore)
    db.session.commit()
    flash("Przywrócono zwierzę.")

    return redirect(url_for('deleted_animals'))
