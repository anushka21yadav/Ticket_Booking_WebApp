from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Movies, Venue, Booking
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

views = Blueprint('views', __name__)


@views.route('/admin_login_home', methods=['GET', 'POST'])
@login_required
def admin_login_home():
    print(current_user)
    all_movies = Movies.query.all() 
    all_venue = Venue.query.all()
    return render_template("home_admin.html", movies = all_movies, venue = all_venue, admin = current_user)


@views.route('/user_signup_home')
@login_required
def user_signup_home():
    return redirect(url_for("views.user_login_home"))    
 

@views.route('/admin_signup_home', methods=['GET', 'POST'])
@login_required
def admin_signup_home():
    return redirect(url_for("views.admin_login_home"))   


@views.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        m_name = request.form.get("moviename")
        m_venue = request.form.get("venuename")
        m_price = request.form.get("movieprice")
        m_tags = request.form.get("movietags")
        m_capacity = request.form.get("moviecapacity")
        venue = Venue.query.all()
        flag = False
        for v in venue:
            if (v.venue_name == m_venue):
                new_movie = Movies(movie_name = m_name, movie_venue = m_venue, movie_price = m_price, movie_tags = m_tags, movie_capacity = m_capacity)
                db.session.add(new_movie)
                db.session.commit()
                flag = True
        if flag:
            flash("New entry added to Movie Table.")   
        else:
            flash("Entered Venue Name does not exists in Venue Table.")    
        return redirect(url_for('views.add_movie'))

    return render_template("add_movie.html", admin = current_user)


@views.route('/add_venue', methods=['GET', 'POST'])
@login_required
def add_venue():
    if request.method == 'POST':
        v_name = request.form.get("venuename")
        v_place = request.form.get("venueplace")
        v_location = request.form.get("venuelocation")

        new_venue = Venue(venue_name = v_name, venue_place = v_place, venue_location = v_location)
        db.session.add(new_venue)
        db.session.commit()
        flash("New entry added to Venue Table.")
        return redirect(url_for("views.add_venue"))

    return render_template("add_venue.html", admin = current_user)      


@views.route('/delete_movie/<int:id>')
@login_required
def delete_movie(id):
    movie_to_delete = Movies.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("views.admin_login_home"))


@views.route('/delete_venue/<int:id>')
@login_required
def delete_venue(id):
    venue_to_delete = Venue.query.get(id)
    movies = Movies.query.all()
    flag = False
    for i in movies:
        if i.movie_venue == venue_to_delete.venue_name:
            db.session.delete(i)
            db.session.delete(venue_to_delete)
            db.session.commit()
            flag = True
    if flag == False:
        db.session.delete(venue_to_delete)
        db.session.commit()        
    return redirect(url_for("views.admin_login_home"))


@views.route('/view_page_movie/<int:id>', methods=['GET', 'POST'])
@login_required
def view_page_movie(id):
    movie_to_view = Movies.query.get(id)
    print(movie_to_view)
    return render_template("update_movie.html", movie_to_view = movie_to_view, admin = current_user)    


@views.route('/update_movie/<int:id>', methods=['GET', 'POST'])
@login_required
def update_movie(id):
    movie_to_update = Movies.query.get(id)
    print(movie_to_update)
    if request.method == 'POST':
        venue = Venue.query.all()
        m_venue = request.form.get("venuename")
        flag = False
        for v in venue:
            if (v.venue_name == m_venue):
                movie_to_update.movie_name = request.form.get('moviename')
                movie_to_update.movie_venue = request.form.get('venuename')
                movie_to_update.movie_price = request.form.get('movieprice')     
                movie_to_update.movie_tags = request.form.get('movietag')
                movie_to_update.movie_capacity = request.form.get('moviecapacity')
                db.session.commit()
                flag = True
        if flag:
            flash("Details updated in Movie Table.")   
        else:
            flash("Entered Venue Name does not exists in Venue Table.")    
        return redirect(url_for('views.admin_login_home', id = id))     


@views.route('/view_page_venue/<int:id>', methods=['GET', 'POST'])
@login_required
def view_page_venue(id):
    venue_to_view = Venue.query.get(id)
    print(venue_to_view)
    return render_template("update_venue.html", venue_to_view = venue_to_view, admin = current_user)    


@views.route('/update_venue/<int:id>', methods=['GET', 'POST'])
@login_required
def update_venue(id):
    venue_to_update = Venue.query.get(id)
    print(venue_to_update)
    if request.method == 'POST':
        print("step 1")
        venue_to_update.venue_name = request.form.get('venuename')
        venue_to_update.venue_place = request.form.get('venueplace')     
        venue_to_update.venue_location = request.form.get('venuelocation')
        db.session.commit()
        flash("Details updated in Venue Table.") 
        return redirect(url_for("views.admin_login_home"))  


@views.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    search = request.form.get("search")
    movie = Movies.query.all()
    venue = Venue.query.all()
    movie_search = {}
    venue_search = {}
    if request.method == 'POST':
        for i in movie:
            print("asd")
            print(i)
            movie_search[i.movie_venue] = []
            print(movie_search)
            if i.movie_name == search:
                print("match")
                movie_search[i.movie_venue].append((i.movie_name, i.movie_id, i.avg_rating_s, i.movie_capacity))
                print(movie_search)
                return render_template("search.html", search_list = movie_search, search = search, user = current_user)  
            else:
                for i in venue:
                    venue_search[i.venue_name] = []
                    if i.venue_name == search or i.venue_location == search or i.venue_place == search:
                        for j in movie:
                            if j.movie_venue == i.venue_name:
                                venue_search[j.movie_venue].append((j.movie_name, j.movie_id, j.avg_rating_s, j.movie_capacity))
                                print(venue_search)
                venue_search_2={}
                for key, value in venue_search.items():
                    if value != []:
                        venue_search_2[key] = value
                print(venue_search_2)   
                print("a")     
                return render_template("search.html", search_list = venue_search_2, search = search, user = current_user)     
        return render_template("search.html", search_list = movie_search, search = search, user = current_user)      
    return ('hellod')

@views.route('/user_login_home', methods=['GET', 'POST'])
@login_required
def user_login_home():
        print(current_user)
        venue = Movies.query.group_by(Movies.movie_venue)
        movie = Movies.query.all()
        dict={}
        for i in venue:
            dict[i.movie_venue]=[]
            for j in movie:
                if i.movie_venue == j.movie_venue:
                    dict[i.movie_venue].append((j.movie_name, j.movie_id, j.avg_rating_s, j.movie_capacity)) 
        recomd=[]
        for i in movie:
            if (i.avg_rating_s >= 4):
                recomd.append(i)      
            
        return render_template("user_home.html", dict = dict, recomd = recomd, user = current_user)
        

@views.route('/booking_page/<int:id>', methods=['GET', 'POST'])
@login_required
def booking_page(id):
    print(id)
    movie = Movies.query.get(id)
    return render_template('booking_page.html', movie = movie, user = current_user)

@views.route('/housefull', methods=['GET', 'POST'])
@login_required
def housefull():
    flash("Sorry, this Show is HOUSEFULL.")
    return redirect(url_for("views.user_login_home"))


@views.route('/booking_page_2/<int:id>', methods=['GET', 'POST'])
@login_required
def booking_page_2(id):
    try: 
        movie = Movies.query.get(id)
        movie_capacity = movie.movie_capacity
        movie_price = movie.movie_price
        print("a")

        if request.method == 'POST':
            print("b")
            seats = request.form.get('seats')
            print(seats)
            if (int(seats) <= int(movie_capacity)):
                cost = int(seats)*int(movie_price)
            return render_template("booking_page_2.html", movie = movie, seats = seats, cost = cost, user = current_user)
    except:
        flash("You have entered seats more than available seats.")  
        return redirect(url_for("views.booking_page", id = id))
    
    
@views.route('/flash_success/<int:seats>/<int:cost>/<int:id>', methods=['GET', 'POST'])
@login_required
def flash_success(seats, cost, id):
    movie = Movies.query.get(id)
    movie_capacity = movie.movie_capacity
    new_capacity = int(movie_capacity)-int(seats)
    movie.movie_capacity = new_capacity
    new_booking = Booking(booking_movie_name = movie.movie_name, booking_venue = movie.movie_venue, booking_seats = seats, booking_cost = cost, booking_user = current_user.user_name)
    db.session.add(new_booking)
    db.session.commit()
    flash("Booking Successfull")
    return render_template("booking_page_2.html", movie = movie, seats = seats, cost = cost, user = current_user)
    

@views.route('/booking_summary', methods=['GET', 'POST'])
@login_required
def booking_summary():
    booking_all = Booking.query.all()
    booking_summary=[]
    for i in booking_all:
        if (i.booking_user == current_user.user_name):
            booking_summary.append(i)
    return render_template("booking_summary.html", booking_summary = booking_summary, user = current_user)


@views.route('/booking_rating_s/<int:id>/<int:rate>', methods=['GET', 'POST'])
@login_required
def booking_rating_s(id, rate):
    booking = Booking.query.all()
    for i in booking:
        if (i.booking_id == id):
            i.booking_rateing_s = rate
            db.session.commit()
        
    movies = Movies.query.group_by(Movies.movie_name)
    avg_rating_s={}
    for i in movies:
        print("b")
        avg_rating_s[i.movie_name] = 0
        sum = 0
        count = 0
        for j in booking:
            if i.movie_name == j.booking_movie_name:
                sum = sum + int(j.booking_rateing_s)   
                count = count + 1
                avg_rating_s[i.movie_name] = "{:.2f}" .format(sum/count)
    print(avg_rating_s)

    for i in movies:
        for key, value in avg_rating_s.items():
            if i.movie_name == key:
                i.avg_rating_s = value
                db.session.commit()

    booking_all = Booking.query.all()
    booking_summary=[]
    for i in booking_all:
        if (i.booking_user == current_user.user_name):
            booking_summary.append(i)
    flash("Rating submitted successfully ")           
    return render_template("booking_summary.html", booking_summary = booking_summary, user = current_user)    


@views.route('/booking_rating_v/<int:id>/<int:rate>', methods=['GET', 'POST'])
@login_required
def booking_rating_v(id, rate):
    booking = Booking.query.all()
    for i in booking:
        if (i.booking_id == id):
            i.booking_rateing_v = rate
            db.session.commit()
        
    venue = Venue.query.all()
    avg_rating_v={}
    for i in venue:
        print("b")
        avg_rating_v[i.venue_name] = 0 
        sum = 0
        count = 0
        for j in booking:
            if i.venue_name == j.booking_venue:
                sum = sum + int(j.booking_rateing_v)   
                count = count + 1
                avg_rating_v[i.venue_name] = "{:.2f}" .format(sum/count)
    print(avg_rating_v)

    for i in venue:
        for key, value in avg_rating_v.items():
            if i.venue_name == key:
                i.avg_rating_v = value
                db.session.commit()
    
    booking_all = Booking.query.all()
    booking_summary=[]
    for i in booking_all:
        if (i.booking_user == current_user.user_name):
            booking_summary.append(i) 
    flash("Rating submitted successfully ")           
    return render_template("booking_summary.html", booking_summary = booking_summary, user = current_user)       


@views.route('/cancel_booking/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel_booking(id):
    print(id)
    booking_to_cancel = Booking.query.get(id)
    print(booking_to_cancel)
    db.session.delete(booking_to_cancel)
    db.session.commit()
    
    booking = Booking.query.all()

    movies = Movies.query.group_by(Movies.movie_name)
    avg_rating_s={}
    for i in movies:
        print("b")
        avg_rating_s[i.movie_name] = 0
        sum = 0
        count = 0
        for j in booking:
            if i.movie_name == j.booking_movie_name:
                sum = sum + int(j.booking_rateing_s)   
                count = count + 1
                avg_rating_s[i.movie_name] = "{:.2f}" .format(sum/count)
    print(avg_rating_s)

    for i in movies:
        for key, value in avg_rating_s.items():
            if i.movie_name == key:
                i.avg_rating_s = value
                db.session.commit()

    venue = Venue.query.all()
    avg_rating_v={}
    for i in venue:
        print("b")
        avg_rating_v[i.venue_name] = 0 
        sum = 0
        count = 0
        for j in booking:
            if i.venue_name == j.booking_venue:
                sum = sum + int(j.booking_rateing_v)   
                count = count + 1
                avg_rating_v[i.venue_name] = "{:.2f}" .format(sum/count)
    print(avg_rating_v)

    for i in venue:
        for key, value in avg_rating_v.items():
            if i.venue_name == key:
                i.avg_rating_v = value
                db.session.commit()            
    return redirect(url_for("views.booking_summary")) 
   

@views.route('/trends')
@login_required
def trends():
    movies = Movies.query.group_by(Movies.movie_name)
    avg_rating_show = {}
    for i in movies:
        avg_rating_show[i.movie_name] = i.avg_rating_s 
    print(avg_rating_show)   
    s_x_axis = avg_rating_show.keys()
    s_y_axis = avg_rating_show.values()

    fig = plt.figure(figsize = (10, 5))
    plt.bar(s_x_axis, s_y_axis, color = 'orange')
    plt.xlabel("Show")
    plt.ylabel("Average Rating") 
    plt.savefig("website\static\image1.png")
    #plt.show()

    venue = Venue.query.all()
    avg_rating_venue = {}
    for i in venue:
        avg_rating_venue[i.venue_name] = i.avg_rating_v 
    print(avg_rating_venue)   
    v_x_axis = avg_rating_venue.keys()
    v_y_axis = avg_rating_venue.values()

    fig = plt.figure(figsize = (10, 5))
    plt.bar(v_x_axis, v_y_axis, color = 'purple',  width = 0.5)
    plt.xlabel("Venue")
    plt.ylabel("Average Rating") 
    plt.savefig("website\static\image2.png")
    return render_template("summary.html", user = current_user)
       
       
    
