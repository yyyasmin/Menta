from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db
from app.models import User, Teacher, Student, Profile, Strength, Weakness, Role

from app.forms import LoginForm, EditForm
from app.select.select import star_select2

from app.templates import *

from sqlalchemy import update

from app.content_management import Content

from sqlalchemy import text # for execute SQL raw SELECT ...


#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
#################
#### imports ####
#################

from flask import Blueprint

from app import forms
#try move to __init__
from app.models import User, Star, Teacher, Profile, Strength, Weakness, Role

################
#### config ####
################

star1 = Blueprint(
    'stars', __name__,
    template_folder='templates'
) 
from app.select.select import student_select2, teacher_select2
from app import *


@star1.route('/teacher_home' )
@login_required
def star_home():
	print("in teacher_home")
	return render_template('form6.html')

	
@star1.route('/edit_stars')
@login_required
def edit_stars():

    print("")
    print("")
    print ("IN edit_stars ")
    stars = Star.query.filter(Star.hide==False).all()
    return render_template('edit_stars.html',stars=stars)
                            
                            								
@star1.route('/star_add', methods=['GET', 'POST'])
@login_required
def star_add():

    print("")
    print("")
    print ("IN teacher_add ")    

    author_id = current_user._get_current_object().id
      
    if request.method == 'GET':
        return render_template('add_star.html')
           
    title = request.form.get('title')
    body = request.form.get('body')
    logo_name = request.form.get('logo_name')

    star = Star.query.filter(Star.title==title).first()
    if star != None:
        flash("בית ספר בשם זה קיים במערכת")
        return edit_stars()

    star = Star( title, body, author_id)
    star.logo_name = logo_name
    db.session.add(star)	
      
    db.session.commit()  
    db.session.refresh(star)
    # test insert res
    return edit_stars()


@star1.route('/star_update/<int:selected_star_id>', methods=['GET', 'POST'])
@login_required
def star_update(selected_star_id):
        
    star = star_select2(selected_star_id)
        
    star = Star.query.filter(Star.id==selected_star_id).first()
    if star==None:
        flash ("אין כזב כוכב")
        return edit_stars()

    if request.method == 'GET':
        #print("GET render update_teacher.html")
        return render_template('update_star.html', star=star)

    star.title = request.form.get('title')
    star.body = request.form.get('body')

    db.session.commit()  
    db.session.refresh(star)
    return edit_stars()


@star1.route('/star_delete', methods=['GET', 'POST'])
@login_required
def star_delete():

    star = Star.query.filter(Star.selected==True).first()
    if star == None:
        flash("Please select a star to delete first ")
        return redirect(url_for('select.star_select'))
            
    star.hide = True
    star.selected = False
    db.session.commit()  
    return edit_stars()

	
@star1.route('/star_delete2/<int:selected_star_id>', methods=['GET', 'POST'])
@login_required
def star_delete2(selected_star_id):

	star = star_select2(selected_star_id)
	return star_delete()

	
@star1.route('/dsply_star_logo2/<int:selected_star_id>', methods=['GET', 'POST'])
@login_required
def dsply_star_logo2(selected_star_id):

    star = star_select2(selected_star_id)
    user = current_user._get_current_object()
    
    star.selected=False
    db.session.commit()
    
    return edit_stars()
    

@star1.route('/star', methods=['GET', 'POST'])
def star():

    print("")
    print("IN STAR")
    
    stars = []
    
    star = Star.query.filter(Star.title=='עצמאות').first()
    if star == None:
        star = Star('עצמאות')
        db.session.add(star)
        db.session.commit()
    stars.append(star)

    star = Star.query.filter(Star.title=='אופטימיות').first()
    if star == None:
        star = Star('אופטימיות')
        db.session.add(star)
        db.session.commit()
    stars.append(star)
    
    star = Star.query.filter(Star.title=='קשר קרוב וטוב').first()
    if star == None:
        star = Star('קשר קרוב וטוב')
        db.session.add(star)
        db.session.commit()
    stars.append(star)
      
    star = Star.query.filter(Star.title=='אהבה עצמית').first()
    if star == None:
        star = Star('אהבה עצמית')
        db.session.add(star)
        db.session.commit()
    stars.append(star)
    
    print("")
    print("")
    for s in stars:
        print("STARRRRR: ", s.id, s.title)
    
    return render_template('dsply_stars.html', stars=stars)
    