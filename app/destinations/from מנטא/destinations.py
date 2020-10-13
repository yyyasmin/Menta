from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import User, School, Student, Teacher, Profile, Strength, Weakness, Tag

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

from app.students.students import get_dummy_student

### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
dst = Blueprint(
    'destinations', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2
from app.select.select import destination_select2, goal_select2, resource_select2
from app.select.select import tag_select2, age_range_select2, scrt_select2
							  
from app.students.students import get_dummy_student, destination_to_student_add2, match_destination_to_student2
from app import *

from datetime import datetime
from datetime import date


																		
@dst.route('/destinations_by_tag', methods=['GET', 'POST'])
@login_required
def destinations_by_tag():
	print('IIIIIIIIIIIIIn destination by tag111111111111')	
	
	user = User.query.get_or_404(current_user._get_current_object().id)
	print(current_user._get_current_object().id)

	if request.method == 'GET':
		tags = Tag.query.all()
		##########################import pdb; pdb.set_trace()
		return render_template('edit_tags.html', tags=tags)			


@dst.route('/edit_tag_destinations', methods=['GET', 'POST'])
def edit_tag_destinations():	

    print("In edit_tag_destinations11111111111111 Request is", request)

    destinations = Destination.query.order_by(Destination.title).all() 
    age_ranges = Age_range.query.all()
    tag = Tag.query.filter(Tag.selected==True).first()
    if tag == None:
        flash("Please select a tag first ")
        return redirect(url_for('destinations.edit_tags'))
        
    tags = []
    tags.append(tag)
    #######################import pdb; pdb.set_trace()
    for d in tag.destinations:
        print("dst_id: ", d.destination_id) 
        
    return render_template('edit_dst_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															


                                                                
@dst.route('/edit_tag_destinations2/<int:selected_tag_id>', methods=['GET', 'POST'])
def edit_tag_destinations2(selected_tag_id):

	print("In edit_tag_destinations2222222222222 Request is :", request)
	tag = tag_select2(selected_tag_id)
	print("tag title id is: ", tag.title, tag.id)
	return redirect(url_for('destinations.edit_tag_destinations'))		

                                                                
@dst.route('/reset_and_get_all_destinations', methods=['GET', 'POST'])
def reset_and_get_all_destinations():

    students = Student.query.all() 
    for std in students:
        std.selected=False
        
    destinations = Destination.query.order_by(Destination.title).all() 
    for dst in destinations:
        dst.selected=False
        
    db.session.commit()
    
    return destinations
    

@dst.route('/edit_destinations/<int:from_dst_sort_order>', methods=['GET', 'POST'])
@login_required
def edit_destinations(from_dst_sort_order):

    #destinations = reset_and_get_all_destinations()   
    age_ranges = Age_range.query.all()    
    tags = Tag.query.all() 
    #########################import pdb; pdb.set_trace()
    if from_dst_sort_order == 1: 
        return redirect(url_for('destinations.edit_destinations_by_ABC')) 

    if from_dst_sort_order == 2: 
        return redirect(url_for('destinations.edit_destinations_by_age_range'))

    if from_dst_sort_order == 3: 
        return redirect(url_for('destinations.edit_destinations_by_subject'))

    if from_dst_sort_order == 4: 
        return redirect(url_for('destinations.edit_destinations_by_scrt')) 
        
    if from_dst_sort_order == 10:     # comming from student private dst addition
        return redirect(url_for('students.edit_student_destinations'))

    return redirect(url_for('destinations.edit_destinations_by_subject'))

@dst.route('/edit_destinations_by_age_range', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_age_range():
    #######import pdb; pdb.set_trace()
    destinations = reset_and_get_all_destinations() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    
    #########################import pdb; pdb.set_trace()
    return render_template('edit_dst_by_age_range.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															

@dst.route('/edit_destinations_by_subject', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_subject():
    destinations = reset_and_get_all_destinations() 
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    return render_template('edit_dst_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags)															

@dst.route('/edit_destinations_by_ABC', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_ABC():
    destinations = reset_and_get_all_destinations()   
    age_ranges = Age_range.query.all()
    #########################import pdb; pdb.set_trace()
    return render_template('edit_dst_by_ABC.html', destinations=destinations)															

@dst.route('/edit_destinations_by_scrt', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_scrt():
    destinations = reset_and_get_all_destinations()
    scrts = Scrt.query.all()
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    #########################import pdb; pdb.set_trace()
    #########################import pdb; pdb.set_trace()
    return render_template('edit_dst_by_scrt.html', 
                                            destinations=destinations, 
                                            age_ranges=age_ranges, 
                                            tags=tags,
                                            scrts=scrts)															

#######################START set_dst_as_public
@dst.route('/set_dst_as_public', methods=['GET', 'POST'])
@login_required
def set_dst_as_public():
    dst = Destination.query.filter(Destination.selected==True).first()   
    if dst == None:
        flash ("Please select a destination first")
        redirect(url_for('destinations.edit_dst_by_scrt'))
        
    scrt_public_opt = Scrt.query.filter(Scrt.title=='ציבורי').first()
    if scrt_public_opt == None:
        flash("There is no public option in public security settings list. Please add a publc option via Security settings first")               
        return redirect(url_for('scrts.edit_scrts'))

    dst.scrt_id = scrt_public_opt.id

    db.session.commit()
    
##### delete dst with private in case it wasn't removed automaticaly   
    old_dst = Destination.query.filter(Destination.title ==dst.title and dst.scrt=='private').first()   
    if old_dst != None:
        old_dst.scrt_id = scrt_public_opt.id
        
    old_dst = Destination.query.filter(Destination.title==dst.title and dst.scrt=='פרטי').first()   
    if old_dst != None:
        old_dst.scrt_id = scrt_public_opt.id


    #delete from private in case it wasn,א removed automaticaly

    dst.scrt_id = scrt_public_opt.id

    destinations = Destination.query.order_by(Destination.title).all() 
    scrts = Scrt.query.all()
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 

    db.session.commit()

    #######################import pdb; pdb.set_trace()
    return render_template('edit_dst_by_scrt.html', 
                                            destinations=destinations, 
                                            age_ranges=age_ranges, 
                                            tags=tags,
                                            scrts=scrts)															
#################################END  set_dst_as_public

@dst.route('/set_dst_as_public2/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def set_dst_as_public2(selected_destination_id):
	print("In edit_dsdestination_update2t_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.set_dst_as_public'))		

#################################END set_dst_as_public2

	

						
@dst.route('/show_dummy_student_tree', methods=['GET', 'POST'])
def show_dummy_student_tree():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('select.student_select'))

	print("selected student for tree show is " + str(student.id))	
	print("printing students tree")
	for dest in student.destinations:
		print("dest title: ", dest.destination.title)
		for goal in dest.destination.goals:
			print("dest - goal title", dest.destination.title, goal.title)
	return render_template('show_students_tree.html', student=student)

					
@dst.route('/show_dummy_student_tree2', methods=['GET', 'POST'])
def show_dummy_student_tree2():
	dummy_std = get_dummy_student()	
	print("in show_dummy_student_tree2 dummy_std",  dummy_std.id)
	std = student_select2(dummy_std.id)
	
	return redirect(url_for('destinations.show_dummy_student_tree'))


#### POST CASE ####                                                                                     
@dst.route('/destination_add/<int:from_dst_sort_order>', methods=['POST'])
def destination_add(from_dst_sort_order, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title, new_dst_body):
    
    print("In POST destination_add_at_once is :",   from_dst_sort_order)
    ##########import pdb; pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    ###############import pdb; pdb.set_trace()
    #############import pdb; pdb.set_trace()
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.add(new_destination)
        db.session.commit()
        new_destination = destination_select2(new_destination.id)   # save ne dest for next setting

    print("new_destination  ar tag scrt  dst", new_destination, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title)

    print("request=: ", request.method)

    ##########import pdb; pdb.set_trace()
  
    #POST case

    selected_ar = set_dst_age_range(selected_ar_title)
    selected_tag = set_dst_tag(selected_tag_title) 
    #########import pdb; pdb.set_trace()
    selected_scrt = set_dst_scrt(from_dst_sort_order, selected_scrt_title)

    new_destination.title = new_dst_title      #Current Description  selection
    new_destination.body =  new_dst_body
    
    db.session.commit()

    std = get_dummy_student()   # Match new dst to Humpty Dumpty
    dst = new_destination
    
    std_dst = Std_destination(std.id, dst.id)
    std_dst.student = std
    std_dst.destination = dst
    std.destinations.append(std_dst)
    dst.students.append(std_dst)

    for tag in dst.tags:
        std_tag = Std_tag.query.filter(Std_tag.student_id==std.id).filter(Std_tag.tag_id==tag.tag_id).first()
        if std_tag == None:
            std_tag = Std_tag(std.id, tag.tag_id)
            std_tag.student = std
            std_tag.tag = tag.tag            
            std.tags.append(std_tag)
            tag.tag.students.append(std_tag)
               
    new_destination.selected = False
    db.session.commit()
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
######## END POST METHOD FOR destination_add ###############
                     
################## END Destinatio ADD At ONCE ################  
  
 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_dst_form ################    
@dst.route('/dsply_dst_form/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form(from_dst_sort_order):
    print ("In dsply_dst_form from_dst_sort_order=: ", from_dst_sort_order)

    form = Dst_form()

    form.ar.choices=[]
    form.tag.choices=[]
    form.scrt.choices=[]

    form.ar.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    form.scrt.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_dst_form.html', form=form, from_dst_sort_order=from_dst_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form.html', form=form)

    ar = Age_range.query.filter_by(id=form.ar.data).first()
    tag = Tag.query.filter_by(id=form.tag.data).first()
    scrt = Scrt.query.filter_by(id=form.scrt.data).first()

    ##########import pdb; pdb.set_trace()
    new_dst_title = form.dst_title.data
    new_dst_body = form.dst_body.data
    
    return destination_add(from_dst_sort_order, ar.title, tag.title, scrt.title, new_dst_title, new_dst_body)

################## START  Update destination_update ################    
@dst.route('/dsply_dst_form_for_update/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form_for_update(from_dst_sort_order):

    print ("In dsply_dst_form_for_update from_dst_sort_order=: ", from_dst_sort_order)
    
    updated_dst = Destination.query.filter(Destination.selected==True).first()
    if updated_dst == None:
        flash("Please select a destination to update")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
        

    form = Dst_form()

    form.dst_title.data = updated_dst.title
    form.dst_body.data =  updated_dst.body

    form.ar.choices=[]
    form.tag.choices=[]
    form.scrt.choices=[]

    ### FROM https://github.com/wtforms/wtforms/issues/106
    ### myform.select.default = 2
    ### myform.process() // <-- you missed this :)
    ### FROM https://github.com/wtforms/wtforms/issues/106

    form.ar.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]
    form.ar.default = updated_dst.age_range_id
    form.process()
    
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    form.tag.default = updated_dst.tags[0].tag_id
    form.process()

    form.scrt.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]
    form.scrt.default = updated_dst.scrt_id
    form.process()

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_dst_form_for_update.html', dst=updated_dst, form=form, from_dst_sort_order=from_dst_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form_for_update.html', form=form)

    #######import pdb; pdb.set_trace()
    ######import pdb; pdb.set_trace()
    ar = Age_range.query.filter_by(id=request.form['ar']).first()
    tag = Tag.query.filter_by(id=request.form['tag']).first()
    scrt = Scrt.query.filter_by(id=request.form['scrt']).first()

    ##########import pdb; pdb.set_trace()
    new_updated_dst_title = request.form['title']      #Current Description  selection
    new_updated_dst_body =  request.form['body']
    
    return destination_update(from_dst_sort_order, ar.title, tag.title, scrt.title, new_updated_dst_title, new_updated_dst_body)


@dst.route('/dsply_dst_form_for_update2/<int:selected_destination_id>/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form_for_update2(selected_destination_id, from_dst_sort_order):

    print("In UUUUUUUUUU dsply_dst_form_for_update2 selected_dst_id ", selected_destination_id)
    dst = destination_select2(selected_destination_id)
    return redirect(url_for('destinations.dsply_dst_form_for_update', from_dst_sort_order=from_dst_sort_order))			

############################### END DST Update
                                            
@dst.route('/tag')
def tag():
    tags = Tag.query.all()

    tagArray = []

    for tag in tags:
        tagObj = {}
        tagObj['id'] = tag.id
        tagObj['name'] = tag.title
        tagArray.append(tagObj)

    return jsonify({'tags' : tagArray})

@dst.route('/scrt')
def scrt():
    scrts = Scrt.query.all()

    scrtArray = []

    for scrt in scrts:
        scrtObj = {}
        scrtObj['id'] = scrt.id
        scrtObj['name'] = scrt.title
        scrtArray.append(tagObj)

    return jsonify({'scrts' : scrtArray})
        
################## START  Ddsply_dst_form ################    
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript


#### POST CASE ####                                                                                     
@dst.route('/destination_update/<int:from_dst_sort_order>', methods=['POST'])
def destination_update(from_dst_sort_order, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title, new_dst_body):
    
    print("In POST destination_update_at_once is :",   from_dst_sort_order)
    ##########import pdb; pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    ###############import pdb; pdb.set_trace()
    #############import pdb; pdb.set_trace()
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.update(new_destination)
        db.session.commit()

    print("new_destination  ar tag scrt  dst", new_destination, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title)

    print("request=: ", request.method)

    ##########import pdb; pdb.set_trace()
  
    #POST case

    selected_ar = set_dst_age_range(selected_ar_title)
    selected_tag = set_dst_tag(selected_tag_title) 
    #########import pdb; pdb.set_trace()
    selected_scrt = set_dst_scrt(from_dst_sort_order, selected_scrt_title)

    new_destination.title = new_dst_title      #Current Description  selection
    new_destination.body =  new_dst_body
    
    db.session.commit()
         
    db.session.commit()
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))

######## END POST METHOD FOR destination_update ###############
      

@dst.route('/destination_update2/<int:selected_destination_id>', methods=['GET', 'POST'])
def destination_update2(selected_destination_id):
	print("In edit_dsdestination_update2t_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.dsply_dst_form',  selected_destination_id=selected_destination_id,
                                                                     from_dst_sort_order=0))		

		
@dst.route('/destination_delete_for_good', methods=['GET', 'POST'])
def destination_delete_for_good():
    print(" in destination_delete_for_good ")

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination to delete first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))

    print("dstis", dst)

    print("dst.tags111 BEFORE clear: ", dst.tags)

    db.session.delete(dst)
    db.session.commit()  
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 
        
#delete from index destinations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_delete_for_good2/<int:selected_destination_id>', methods=['GET', 'POST'])
def destination_delete_for_good2(selected_destination_id):
    print ("destination_delete_for_good2 destination is", selected_destination_id )
    #dst = destination_select2(selected_destination_id)
    ########################import pdb; pdb.set_trace()

    dst = destination_select2(selected_destination_id)
    print("dst.title")
    print("In destination_delete_for_good2 After dst selectino 2: " , dst)

    return redirect(url_for('destinations.destination_delete_for_good')) 	


@dst.route('/destination_delete', methods=['GET', 'POST'])
#Here author is user_id
def destination_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination to delete first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))
			
	print ("delete selected destination is " )
	print(destination.id)
	
	destination.hide = True

	db.session.commit()
	#DEBUG
	destination = Destination.query.filter(Destination.selected==True).first()
	print("After commit set hide to True", destination.id, destination.hide)
	#DEBUG
	return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 
		
#delete from index destinations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_delete2/<int:selected_destination_id>', methods=['GET', 'POST'])
#Here author is user_id
def destination_delete2(selected_destination_id):

	print ("SSSSSSSSSSSSSelected destination is", selected_destination_id )
	dest = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.destination_delete'))
    
    
##############START destination's age range###############

@dst.route('/edit_dst_age_range', methods=['GET', 'POST'])
def edit_dst_age_range():
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=1))		
    print("In edit_dst_age_rangess " )
    
    age_ranges = Age_range.query.all()

    #POST CASE
    if request.method == 'POST':
        selected_ar_title = set_dst_age_range()
    
    selected_ar_title = get_selected_ar_title()
    
    return render_template('./sub_forms/ar/edit_ar_for_one_dst.html', 
                                                        dst=dst, 
                                                        age_ranges=age_ranges,
                                                        selected_ar_title=selected_ar_title) 
																
														  		
@dst.route('/edit_dst_age_range2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_dst_age_range2(selected_destination_id, ar_title):
	print("In edit_dst_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_age_range'))		

 ###START set selected age_range		
@dst.route('/set_dst_age_range', methods=['POST'])
def set_dst_age_range(selected_ar_title):
    print("In  set_dst_age_range") 
    
    selected_ar_title = selected_ar_title      #Current Age_range selection

   # POST case
    selected_ar = Age_range.query.filter(Age_range.title == selected_ar_title).first()   
    print("In set_dst_age_range electedar is: ", selected_ar)
    if selected_ar == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    
    selected_ar = age_range_select2(selected_ar.id)    

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst != None:                       
        if dst not in selected_ar.destinations:
            selected_ar.destinations.append(dst)
            dst.age_range_id = selected_ar.id

    db.session.commit() 
    #########################import pdb; pdb.set_trace()
    return selected_ar
 ###END set selected age_range	
    
 ###get selected age_range	
@dst.route('/get_selected_ar_title', methods=['GET', 'POST'])
def get_selected_ar_title():
    tmp_age_range = Age_range.query.filter(Age_range.selected == True).first()
    if tmp_age_range != None:
        selected_ar_title = tmp_age_range.title   
    else:    
        selected_ar_title = ":בחר אופצית אבטחה"        
    return selected_ar_title
###end get selected age_range
 
##############END destination's age range###############


##############START destination's scrt ###############

@dst.route('/edit_dst_scrt', methods=['GET', 'POST'])
def edit_dst_scrt():
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		
    print("In edit_dst_scrtss " )
    scrts = Scrt.query.all()
    
    #POST CASE
    if request.method == 'POST':
        selected_scrt_title = set_dst_scrt(from_dst_sort_order)
    
    selected_scrt_title = get_selected_scrt_title()
    
    return render_template('./sub_forms/scrt/edit_scrt_for_one_dst.html', 
                                                        dst=dst, 
                                                        scrts=scrts,
                                                        selected_scrt_title=selected_scrt_title) 
																				
														  		
@dst.route('/edit_dst_scrt2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_dst_scrt2(selected_destination_id):
	print("In edit_dst_scrtss2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_scrt'))		

	
@dst.route('/set_dst_scrt/<from_dst_sort_order>',  methods=['GET', 'POST'])
def set_dst_scrt(from_dst_sort_order, selected_scrt_title):

    ##############import pdb; pdb.set_trace()set_dst_scrt(from_dst_sort_order)
    
    selected_scrt = selected_scrt_title      #Current Scrt selection
    #########import pdb; pdb.set_trace()
    selected_scrt = Scrt.query.filter(Scrt.title == selected_scrt).first()
    
    print("In set_dst_scrt selected_scrt is: ", selected_scrt)    
    if selected_scrt!= None:
        print("In set_dst_scrt scrt tiltle  is: ", selected_scrt.title)

    if selected_scrt == None or selected_scrt.title=="בחר רמת אבטחה" :
        sa=get_selected_ar_title()
        if sa == None:
            sa="בחר נושא"
            
        sa=get_selected_ar_title()
        if sa == None:
            sa = "בחר נושא"
                    
        st=get_selected_tag_title()
        if st == None:
            st = "בחר נושא"
            
        print("sa st: ", sa, st)
        
        ##########import pdb; pdb.set_trace()
        #flash("יש לבחור רמת אבטחה")
        return dsply_dst_form()
        

    selected_scrt = scrt_select2(selected_scrt.id) 
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst != None:                
        if dst not in selected_scrt.destinations:
            selected_scrt.destinations.append(dst)                
        dst.scrt_id = selected_scrt.id

    db.session.commit()
    
    return selected_scrt.title    
    
###get selected security option	scrt	
@dst.route('/get_selected_scrt_title', methods=['GET', 'POST'])
def get_selected_scrt_title():
    tmp_scrt = Scrt.query.filter(Scrt.selected == True).first()
    if tmp_scrt != None:
        selected_scrt_title = tmp_scrt.title   
    else:
        selected_scrt_title = ":בחר אופצית אבטחה"        
    return selected_scrt_title
###end get selected security option	scrt	 

##############END destination's scrt ###############
 	

	 	
##############START destination's goals###############	

@dst.route('/edit_destinations_goals', methods=['GET', 'POST'])
def edit_destinations_goals():
    ########import pdb; pdb.set_trace()
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		
    print("In edit_destinations_goals : ", destination, destination.selected )
    ##############import pdb; pdb.set_trace()
    return render_template('edit_destinations_goals.html', destination=destination) 
                                                                
														  		
@dst.route('/edit_destinations_goals2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_destinations_goals2(selected_destination_id):
	print("In edit_destination_goals2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_destinations_goals'))		

	
@dst.route('/goal_to_destination_add', methods=['GET', 'POST'])
def goal_to_destination_add(title, body):

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		

    if request.method == 'GET':
        return render_template('./backup/goal_to_destination_add.html', destination=dst)
           

    #########################import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id
    ##############import pdb; pdb.set_trace()
    goal = Goal(title, body, author_id, dst.id)	

    db.session.add(goal)    	
    dst.goals.append(goal) 

    ### Add goal to humpty dumpty Demo std ###
    hd = get_dummy_student()
    hd_std_goal = Std_goal(hd.id, goal.id)
    hd_std_goal.dst_id = dst.id
    hd_std_goal.due_date = date.today()
    hd.goals.append(hd_std_goal)
    ### Add goal to humpty dumpty Demo std ###
        
    db.session.commit()  
    db.session.refresh(goal)
    url = url_for('destinations.edit_destinations_goals' )
    return redirect(url)   

@dst.route('/goal_to_destination_add2/<int:selected_destination_id>', methods=['GET', 'POST'])
def goal_to_destination_add2(selected_destination_id):
	print(selected_destination_id)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.goal_to_destination_add'))			

	
@dst.route('/goal_from_destination_delete', methods=['GET', 'POST'])
def goal_from_destination_delete():
	
	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		


	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal to delete first ")
		return redirect(url_for('select.goal_select'))
			
	print ("delete selected goal is " + goal.title + " from slected destination " + destination.title )

	destination.goals.remove(goal)
	db.session.commit()  

	return redirect(url_for('destinations.edit_destinations_goals')) 

@dst.route('/goal_from_destination_delete2/<int:selected_destination_id><int:selected_goal_id>', methods=['GET', 'POST'])
#Here author is user_id
def goal_from_destination_delete2(selected_destination_id, selected_goal_id):

	std = goal_select2(selected_destination_id)
	dest = goal_select2(selected_goal_id)
	return redirect(url_for('destinations.goal_from_destination_delete')) 	


 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_goal_form ################    
@dst.route('/dsply_goal_form', methods=['GET', 'POST'])
def dsply_goal_form():

    form = Goal_form()

    dst = Destination.query.filter(Destination.selected==True).first()
    form.dst_title = dst.title
    form.dst_body = dst.body
    
    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_goal_form.html', dst=dst, form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form.html', form=form)


    ##########import pdb; pdb.set_trace()
    new_goal_title = form.goal_title.data
    new_goal_body = form.goal_body.data
    
    return goal_to_destination_add(new_goal_title, new_goal_body)


@dst.route('/dsply_goal_form2/<int:selected_destination_id>', methods=['GET', 'POST'])
def dsply_goal_form2(selected_destination_id):
	print(selected_destination_id)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.dsply_goal_form'))			

	
    
################## START  Update destination_update ################    
@dst.route('/dsply_goal_form_for_update', methods=['GET', 'POST'])
def dsply_goal_form_for_update(from_goal_sort_order):

    print ("In dsply_goal_form_for_update from_goal_sort_order=: ")
    
    updated_dst = Destination.query.filter(Destination.selected==True).first()
    if updated_dst == None:
        flash("Please select a destination to update")
        return redirect(url_for('destinations.edit_destinations_goals', from_goal_sort_order=from_goal_sort_order))
        

    form = Goal_form()

    form.goal_title.data = updated_dst.title
    form.goal_body.data =  updated_dst.body

    ### FROM https://github.com/wtforms/wtforms/issues/106
    ### myform.select.default = 2
    ### myform.process() // <-- you missed this :)
    ### FROM https://github.com/wtforms/wtforms/issues/106

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_goal_form_for_update.html', dst=updated_dst, form=form, from_goal_sort_order=from_goal_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form_for_update.html', form=form)

    ##########import pdb; pdb.set_trace()
    new_updated_goal_title = request.form['title']      #Current Description  selection
    new_updated_goal_body =  request.form['body']
    
    return destination_update(new_updated_goal_title, new_updated_goal_body)


@dst.route('/dsply_goal_form_for_update2/<int:selected_destination_id>/<int:from_goal_sort_order>', methods=['GET', 'POST'])
def dsply_goal_form_for_update2(selected_destination_id):

    print("In UUUUUUUUUU dsply_goal_form_for_update2 selected_goal_id ", selected_destination_id)
    dst = destination_select2(selected_destination_id)
    return redirect(url_for('destinations.dsply_goal_form_for_update'))			

############################### END DST Update

##############END destination's goals###############	




##############destination tags###############	

@dst.route('/edit_destinations_tags', methods=['GET', 'POST'])
def edit_destinations_tags():
	
	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=2))
		
	all_tags = Tag.query.all()		
	tags_not_of_destination = list(set(all_tags).difference(set(destination.tags)))  #tags_not_of_destination = all_tags-destination's tags
	for t in tags_not_of_destination:
		print("In edit_destinations_tags T not of destination  is ", t.id)
	return render_template('edit_destination_tags.html', destination=destination, tags_not_of_destination=tags_not_of_destination) 
																
														  		
@dst.route('/edit_destinations_tags2/edit/<int:selected_destination_id>/<int:selected_tag_id>', methods=['GET', 'POST'])
def edit_destinations_tags2(selected_destination_id, selected_tag_id):
	print("In edit_destination_tags2 Request is :", request)
	std = destination_select2(selected_destination_id)
	if selected_tag_id != 0:
		dest = tag_select2(selected_tag_id)
	return redirect(url_for('destinations.edit_destinations_tags'))		

	
@dst.route('/tag_to_destination_add', methods=['GET', 'POST'])
def tag_to_destination_add():
	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=2))		
	
	all_tags = Tag.query.all()
	tags_not_of_destination = list(set(all_tags).difference(set(destination.tags)))  #tags_not_of_destination = all_tags-destination's tags
	for t in tags_not_of_destination:
		print("T is ", t.id)
	if request.method == 'GET':
		return render_template('edit_tags_not_of_destination.html', tags=tags_not_of_destination)

@dst.route('/tag_to_destination_add2/<int:selected_destination_id>', methods=['GET', 'POST'])
def tag_to_destination_add2(selected_destination_id):
	#########################import pdb; pdb.set_trace()
	dst = destination_select2(selected_destination_id)
	print("In tag_to_destination_add2 dst.id =:", dst.id)
	#tag = tag_select2(selected_tag_id)
	print("In tag_to_destination_add2 dst.id =:", dst.id)

	return redirect(url_for('destinations.tag_to_destination_add')) 	
	
	
@dst.route('/match_tag_to_destination', methods=['GET', 'POST'])
def match_tag_to_destination():
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=2))		

    tag = Tag.query.filter(Tag.selected==True).first()	
    if tag == None:
        flash("Please select a tag to delete first ")
        return redirect(url_for('destinations.destinations_by_tag'))

    #########################import pdb; pdb.set_trace()

    destination.tags.append(tag) 
    tag.destinations.append(destination)
    dst_tag(destination.id, tag.id)
       
    db.session.commit()  
    db.session.refresh(tag)

    return redirect(url_for('destinations.edit_destinations_tags')) 	

			
@dst.route('/match_tag_to_destination2/<int:selected_tag_id>', methods=['GET', 'POST'])
def match_tag_to_destination2(selected_tag_id):

	dest = tag_select2(selected_tag_id)
	return redirect(url_for('destinations.match_tag_to_destination')) 	


############# Start Delete dst from tag #############
@dst.route('/dst_from_tag_delete', methods=['GET', 'POST'])
def dst_from_tag_delete():
	########################import pdb; pdb.set_trace()
	tag = Tag.query.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag first ")
		return redirect(url_for('destinations.destinations_by_tag'))

	dst = Destination.query.filter(Destination.selected==True).first()
	if dst == None:
		flash("Please select a dst first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=2))
		
	#print("SSSSSRRRRR IN tag_from_dst_delete   deleteing tag %s from dst %s :",tag.id, dst.id )			
	dst_tag = Dst_Tag.query.filter(Dst_Tag.tag_id == tag.id).filter(Dst_Tag.dst_id==dst.id).first()   #update dst_tag
	if dst_tag:	
		########################import pdb; pdb.set_trace()
		print ("deleting  Dst_TAG  ", dst_tag.destination_id,dst_tag.tag_id)
		db.session.delete(dst_tag)
		db.session.commit()
	
	return  redirect(url_for('destinations.destinations_by_tag'))  #no change in tags staff dsts
		
@dst.route('/dst_from_tag_delete2/delete/<int:selected_dst_id>/<int:selected_tag_id>', methods=['GET', 'POST'])
def dst_from_tag_delete2(selected_dst_id, selected_tag_id):
	#print("In DDDDDDDDDDDD tag_from_dst_delete2")
	std = tag_select2(selected_tag_id)
	if selected_dst_id:
		#print(selected_dst_id)
		tchr = dst_select2(selected_dst_id)
	return  redirect(url_for('tags.dst_from_tag_delete'))  
############# END Delete dst from tag #############

	
@dst.route('/set_dst_tag', methods=['POST'])
def set_dst_tag(selected_tag_title):

    selected_tag_title = selected_tag_title      #Current Tag selection

    selected_tag = Tag.query.filter(Tag.title == selected_tag_title).first()
    
    print("In set_dst_tag selected_tag is: ", selected_tag)
    if selected_tag == None:
        flash("יש לבחור נושא")
        ##########import pdb;pdb.set_trace()
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    

    selected_tag = tag_select2(selected_tag.id)
    selected_dst = Destination.query.filter(Destination.selected==True).first()
   
    #Get existing dst-tag or create new one and set it 
    new_dst_tag = Dst_Tag.query.filter(Dst_Tag.destination_id==selected_dst.id and  Dst_Tag.tag_id==selected_tag.id).first()
    if new_dst_tag == None:
        new_dst_tag = Dst_Tag(selected_dst.id, selected_tag.id)       
    new_dst_tag.destination = selected_dst
    new_dst_tag.tag = selected_tag
    selected_dst.tags.append(new_dst_tag)
    selected_tag.destinations.append(new_dst_tag)

    #########################import pdb; pdb.set_trace()
                                                
    db.session.commit()    
    return selected_tag    
    
###get selected security option	tag	
@dst.route('/get_selected_tag_title', methods=['GET', 'POST'])
def get_selected_tag_title():
    tmp_tag = Tag.query.filter(Tag.selected == True).first()
    if tmp_tag != None:
        selected_tag_title = tmp_tag.title   
    else:
        selected_tag_title = ":בחר נושא"        
    return selected_tag_title
###end get selected security option	tag

##############destination tags###############	


		

