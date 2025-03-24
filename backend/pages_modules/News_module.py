from backend.pages_modules.common_imports import *
from backend.webforms import PostForm
from werkzeug.utils import secure_filename
import uuid
from flask_login import current_user
import os

def posts():
    posts = Posts.query.order_by(Posts.post_datetime.desc()).filter(Posts.is_deleted == 'FALSE')
    
    for post in posts:
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
    return render_template("posts/posts.html", posts=posts)

def add_post():
    form = PostForm()

    if form.validate_on_submit():
        if form.title_img.data:
            safe_filename = secure_filename(form.title_img.data.filename)
            title_img_name = str(uuid.uuid1()) + "_" + safe_filename
        else:
            title_img_name = None

        new_post = Posts(
            title = form.title.data, 
            author_id = current_user.user_id,
            description = form.description.data,
            title_img_name = title_img_name
            )

        db.session.add(new_post)
        db.session.commit()

        # Zapisywanie plików
        if form.title_img.data or any(file.filename for file in form.images.data):
            catalog_path = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', str(new_post.post_id))
            os.makedirs(catalog_path, exist_ok=True)

            if form.title_img.data:
                file_path = os.path.join(catalog_path, title_img_name)
                form.title_img.data.save(file_path)

            if any(file.filename for file in form.images.data):
                for file in form.images.data:
                    safe_filename = secure_filename(file.filename)
                    img_name = str(uuid.uuid1()) + "_" + safe_filename

                    file_path = os.path.join(catalog_path, img_name)
                    file.save(file_path)

        flash("Dodano post!")

    return render_template("posts/add_post.html", form=form)

def edit_post(id):
    post = Posts.query.get_or_404(id)

    form = PostForm()

    if form.validate_on_submit():
        
        post.title = form.title.data, 
        post.author_id = current_user.user_id,
        post.description = form.description.data
        
        form.title.data = ''
        form.description.data = ''

        db.session.add(post)
        db.session.commit()
        flash("Zapisano zmiany!")

        return redirect(url_for('post', id=post.post_id))
    
    form.title.data = post.title
    form.description.data = post.description
    return render_template('posts/edit_post.html', form=form)

