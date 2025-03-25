from backend.pages_modules.common_imports import *
from datetime import datetime, timedelta

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