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

from app.models import User, School, Student, Teacher, General_txt, Profile, Strength, Weakness, Tag

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

from app.students.students import get_dummy_student, attach_gt_to_std

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
from app.select.select import tag_select2, age_range_select2, scrt_select2, gt_type_select2
							  
from app.students.students import get_dummy_student, destination_to_student_add2
from app.gts.gts import get_gt_default, set_child_by_type  

from app import *

from datetime import datetime
from datetime import date

                                                                
@dst.route('/reset_and_get_destinations/<int:scrt_type>', methods=['GET', 'POST'])
def reset_and_get_destinations(scrt_type):
    
    '''
    #DEBUG ONLY - TO BE DELETED
    gts = General_txt.query.all()
    stss = Status.query.all()
    whos = Accupation.query.all()
    d_sts = Status.query.filter(Status.default == True).first()
    d_who = Accupation.query.filter(Accupation.default == True).first()
    i=0
    j=0
    for g in gts:
        for s in stss:
            if g.is_parent_of(s):
                i=1
            if g.type=='todo':
                for w in whos:
                    if g.is_parent_of(w):
                        j=1
        if i==0:
            g.set_parent(d_sts)
        if g.type=='todo':
            if j==0:
                g.set_parent(d_who)
        
    #DEBUG ONLY - TO BE DELETED
    '''
    
    
    students = Student.query.order_by(Student.last_name).order_by(Student.first_name).filter(Student.hide==False).all() 
    for std in students:
        std.selected=False
    
    if scrt_type==1:     # Get only public destinations 
        destinations = get_public_dsts()
           
        #print("Public dsta are: ", destinations)
    
    else:     # Get all destinations
        destinations = Destination.query.filter(Destination.hide==False).order_by(Destination.title).all() 

    gts = General_txt.query.all()
    for gt in gts:
        gt.selected=False
        
    db.session.commit()

    return destinations

############### START get_public_dsts ###############

@dst.route('/get_public_dsts', methods=['GET', 'POST'])
def get_public_dsts():
    
    public_scrt = Scrt.query.filter(Scrt.title=='public' or Scrt.title=='ציבורי').first()
    # Get all public dummy std destinations
    dummy_std = get_dummy_student()
    #dummy_std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==dummy_std.id).filter(Std_general_txt.scrt_id==public_scrt.id).all()   # dummy student has all dsts
    dummy_std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==dummy_std.id).all()   # dummy student has all dsts
    all_destinations = Destination.query.filter(Destination.hide==False).order_by(Destination.title).all()
    return all_destinations
    '''
    public_destinations=[]
    for gt in dummy_std_gts:
        if gt.general_txt in all_destinations:
           public_destinations.append(gt.general_txt) 
    
    ############import pdb;; pdb.set_trace()
    #print("Public dsta are: ", public_destinations)
    return public_destinations
    '''
    
############### END get_public_dsts ###############


@dst.route('/edit_destinations/<int:from_dst_sort_order>', methods=['GET', 'POST'])
@login_required
def edit_destinations(from_dst_sort_order):
    
    print("")
    print("IN destinations/edit_destinations   from_dst_sort_order=: ", from_dst_sort_order)
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()    
    tags = Tag.query.order_by(Tag.title).all() 
    #############################old_dst_scrt pdb.set_trace()
    if from_dst_sort_order == 1: 
        return redirect(url_for('destinations.edit_destinations_by_ABC', from_dst_sort_order=from_dst_sort_order)) 

    if from_dst_sort_order == 2: 
        return redirect(url_for('destinations.edit_destinations_by_age_range', from_dst_sort_order=from_dst_sort_order))

    if from_dst_sort_order == 3: 
        return redirect(url_for('destinations.edit_destinations_by_subject', from_dst_sort_order=from_dst_sort_order))

    if from_dst_sort_order == 4: 
        return redirect(url_for('destinations.edit_destinations_by_scrt', from_dst_sort_order=from_dst_sort_order)) 
        
    if from_dst_sort_order == 10:     # comming from student private dst addition
        return redirect(url_for('students.edit_student_destinations'), from_dst_sort_order=from_dst_sort_order)

    return redirect(url_for('destinations.edit_destinations_by_subject', from_dst_sort_order=from_dst_sort_order))

@dst.route('/edit_destinations_by_age_range', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_age_range():
    ###########old_dst_scrt pdb.set_trace()
    destinations = reset_and_get_destinations(scrt_type=1)     # get only public destinations

    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all() 
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all() 
    ###old_dst_scrt pdb.set_trace()
    #############################old_dst_scrt pdb.set_trace()
    return render_template('edit_dst_by_age_range.html', destinations=destinations, age_ranges=age_ranges, tags=tags, sub_tags=sub_tags)															

@dst.route('/edit_destinations_by_subject', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_subject():
    destinations = reset_and_get_destinations(scrt_type=1)   #get only public destinations 
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all() 

    #DEBUG
    print("")
    print("")
    for tag in tags:
        print("tag", tag.id)
        for sub in sub_tags:
            print("SUB", sub.id)
            for d in destinations:
                if d.is_parent_of(sub):
                    print("DST {0} {1}    SUB: {2} {3}".format(d.id, d.title, sub.id, sub.title))
                if d.is_parent_of(tag):
                    print("DST {0} {1}    TAG: {2} {3}".format(d.id, d.title, tag.id, tag.title))

    return render_template('edit_dst_by_subject.html', destinations=destinations, age_ranges=age_ranges, tags=tags, sub_tags=sub_tags)															



@dst.route('/edit_destinations_by_ABC', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_ABC():
    destinations = reset_and_get_destinations(scrt_type=1)   #get only public destinations   
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    #############################old_dst_scrt pdb.set_trace()
    return render_template('edit_dst_by_ABC.html', destinations=destinations)															


@dst.route('/edit_destinations_by_scrt', methods=['GET', 'POST'])
@login_required
def edit_destinations_by_scrt():
    all_dsts = reset_and_get_destinations(scrt_type=0)   #get all destinations
    #public_destinations = reset_and_get_destinations(scrt_type=1)   #get all destinations
    #private_destinations = list(set(all_dsts).difference(set(public_destinations))) # private_dsts = all_dsts - public_dsts

    scrts = Scrt.query.all()
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all() 
    #############################old_dst_scrt pdb.set_trace()
    #############################old_dst_scrt pdb.set_trace()
    return render_template('edit_dst_by_scrt.html',
                                            destinations=all_dsts,
                                            age_ranges=age_ranges, 
                                            tags=tags,
                                            scrts=scrts)															

            
@dst.route('/show_dst_tree', methods=['GET', 'POST'])
@login_required
def show_dst_tree():

    print("")
    print("IN show_dst_tree ")
    
    #############import pdb; #pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_destinations'))
        
    dst.color_txt = 'green'
    dst.table_color = 'green_table'
    dst.title_color = '#66ff99'
    dst.editable = True
    
    print("")
    print("Dst {0} {1} {2} {3} {4} TREE:", dst, dst.id, dst.color, dst.table_color, dst.title_color )
    print("")
    print("")
    
    dst_goals = []    # Get all dst's goals
    for g in dst.children:
        if g.type=='goal':
            print("")
            print("    ", g, g.id)
            g.color_txt = 'blue'
            g.title_color = '#d6e0f5'
            dst_goals.append(g)

    dst_todos = []    # Get all goal's todos
    for g in dst_goals:
        for t in g.children:
            if t.type=='todo':               
                print("")
                print("      ", t, t.id)
                t.color_txt = 'orange'
                t.title_color = '#ffff99'
                dst_todos.append(t)

    #DEBUG ONLY
    print("")
    print("")
    print("TREE")
    print("D", dst.title, dst.id)
    for g in dst_goals: 
        if dst.is_parent_of(g):
            print("   G", g.title, g.id)
        for t in dst_todos:
            if g.is_parent_of(t):
                print("            T", g.id,  t.id)
    #DEBUG ONLY
    
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()
       
    due_date = date.today()
        
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all()
    print("")
    print("END OF   show_dst_tree  --- CAlling show_dsts_tree total_gts=: ", 1+len(dst_goals)+len(dst_todos))

        
    student_dsts = []    # Get all student's destinations
    student_dsts.append(dst)   
    print("")
    print("")
    print(student_dsts)
       
    return render_template('./tree/dst_tree.html',  
                                            dest=dst, dst=dst, student_dsts=student_dsts,
                                            dst_goals=dst_goals,
                                            dst_todos=dst_todos,
                                            total_gts = 1+len(dst_goals)+len(dst_todos),
                                            whos=whos, statuss=statuss,
                                            )			
               
    
    
@dst.route('/show_dst_tree2/<int:selected_dst_id>', methods=['GET', 'POST'])
@login_required
def show_dst_tree2(selected_dst_id):
    dst = destination_select2(selected_dst_id)
    return redirect(url_for('destinations.show_dst_tree'))


#######################START set_dst_as_public
@dst.route('/set_dst_as_public', methods=['GET', 'POST'])
@login_required
def set_dst_as_public():
    dst = Destination.query.filter(Destination.selected==True).first()   
    if dst == None:
        flash ("Please select a destination first")
        redirect(url_for('destinations.edit_destinations_by_scrt'))
     
    public_scrt = Scrt.query.filter(Scrt.title=='ציבורי').first()
    if public_scrt == None:
        public_scrt = Scrt.query.filter(Scrt.title=='public').first()
        if public_scrt == None:
            flash("There is no public option in public or ציבורי security settings list. Please add a public option via Security settings first")               
            return redirect(url_for('scrts.edit_scrts'))

    dummy_std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==0).filter(Std_general_txt.general_txt_id==dst.id).first()
    dummy_std_dst.scrt_id = public_scrt.id
    
    all_scrts = Scrt.query.all()
    for scrt in all_scrts:
        if dst.is_parent_of(scrt):
            dst.unset_parent(scrt)
      
    dst.children.append(public_scrt)
    
    #print("IN END OF set_dst_as_public dst.children.all() : ", dst.children.all())
    
    
    db.session.commit()
    
    destinations = Destination.query.order_by(Destination.title).all() 
    scrts = Scrt.query.all()
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 

    db.session.commit()

    return render_template('edit_dst_by_scrt.html', 
                                            destinations=destinations, 
                                            age_ranges=age_ranges, 
                                            tags=tags,
                                            scrts=scrts)															
#################################END  set_dst_as_public

@dst.route('/set_dst_as_public2/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def set_dst_as_public2(selected_destination_id):
	#print("In edit_dsdestination_update2t_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.set_dst_as_public'))		

#################################END set_dst_as_public2



					
@dst.route('/show_dummy_student_tree2', methods=['GET', 'POST'])
def show_dummy_student_tree2():
    dummy_std = get_dummy_student()	
    #print("in show_dummy_student_tree2 dummy_std",  dummy_std.id)
    std = student_select2(dummy_std.id)	
    #############import pdb;; pdb.set_trace()
    return redirect(url_for('students.show_student_tree'))


#### POST CASE ####                                                                                     
@dst.route('/destination_add/<int:from_dst_sort_order>', methods=['POST'])
def destination_add(from_dst_sort_order, selected_ar_title, selected_tag_title, selected_sub_tag_title, selected_scrt_title, new_dst_title, new_dst_body):
    
    #print("In POST destination_add_at_once is :",   from_dst_sort_order)
    ##############old_dst_scrt pdb.set_trace()
        
    author_id = current_user._get_current_object().id    

    ##import pdb;  pdb.set_trace()
    
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    ###################old_dst_scrt pdb.set_trace()
    #################old_dst_scrt pdb.set_trace()
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.add(new_destination)
        db.session.commit()
        new_destination = destination_select2(new_destination.id)   # save new dest for next setting

    #print("new_destination  ar tag scrt  dst", new_destination, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title)

    #print("request=: ", request.method)

    ##############old_dst_scrt pdb.set_trace()
  
    #POST case

    selected_ar = set_dst_age_range(selected_ar_title)
    selected_tag = set_dst_tag(selected_tag_title) 
    selected_sub_tag = set_dst_sub_tag(selected_sub_tag_title) 
    #############old_dst_scrt pdb.set_trace()

    new_destination.title = new_dst_title      #Current Description  selection
    new_destination.body =  new_dst_body
    
    default_sts = get_gt_default('Status')
    new_destination.status_id = default_sts.id
    new_destination.set_parent(default_sts)
    
    default_who = get_gt_default('Accupation')
    new_destination.who_id = default_who.id
    new_destination.set_parent(default_who)

    default_scrt = get_gt_default('Scrt')
    new_destination.scrt_id = default_scrt.id
    new_destination.set_parent(default_scrt)
    
    db.session.commit()

    std = get_dummy_student()   # Match new dst to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_destination.id)  
    
    selected_scrt = set_dst_scrt(selected_scrt_title)
        
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

    print("")
    print ("In dsply_dst_form from_dst_sort_order=: ")

    ##import pdb; pdb.set_trace()
    
    form = Dst_form()

    form.ar.choices=[]
    form.tag.choices=[]
    form.scrt.choices=[]

    form.ar.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    form.sub_tag.choices = [(sub_tag.id, sub_tag.title) for sub_tag in Sub_tag.query.all()]
    form.scrt.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_dst_form.html', form=form, from_dst_sort_order=from_dst_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form.html', form=form)

    ar = Age_range.query.filter_by(id=form.ar.data).first()
    tag = Tag.query.filter_by(id=form.tag.data).first()
    sub_tag = Sub_tag.query.filter_by(id=form.sub_tag.data).first()
    scrt = Scrt.query.filter_by(id=form.scrt.data).first()

    ##############old_dst_scrt pdb.set_trace()
    new_dst_title = form.gt_title.data
    new_dst_body = form.gt_body.data

    author_id = current_user._get_current_object().id    
    new_destination = Destination('New dest', "", author_id)	
    db.session.add(new_destination)
    db.session.commit()
    
    new_destination.title = new_dst_title
    new_destination.body = new_dst_body
    
    new_destination.set_parent(ar)
    new_destination.set_parent(tag)
    new_destination.set_parent(sub_tag)
    new_destination.set_parent(scrt)
    
    tag.set_parent(new_destination)
    sub_tag.set_parent(new_destination)
    
    std_gt = attach_gt_to_std(0, new_destination.id)
    db.session.commit()
    
    nd = Destination.query.filter(Destination.title== new_dst_title).first()

    print("")
    print("")
    print("IN END OF dsply_dst_form added dst:")

    print("title: ",nd.title)
    print("body: ",nd.body)
    print("id: ",nd.id)
    print("title: ",nd.children)
    for c in nd.children:
        print("chil: ", c.id, c.title)
    print("std_gt", std_gt.student_id, std_gt.general_txt_id)
    print("std_gt", std_gt.student, std_gt.general_txt)
    print("")
    print("")
    
    
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
   


################## START  Update destination_update ################    
@dst.route('/dsply_dst_form_for_update/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form_for_update(from_dst_sort_order):
    
    updated_dst = Destination.query.filter(Destination.selected==True).first()
    if updated_dst == None:
        flash("Please select a destination to update")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))

    print("")
    print("")
    print("IN dsply_dst_form_for_update2 UPDATED DST IS:", updated_dst.title)
    print("")
    
    form = Dst_form()

    form.gt_title.data = updated_dst.title
    form.gt_body.data =  updated_dst.body

    form.ar.choices=[]
    form.tag.choices=[]
    form.scrt.choices=[]

    form.ar.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]    
    all_ars = Age_range.query.all()
    for ar in all_ars:
        if updated_dst.is_parent_of(ar):
            dst_ar = ar
            break
    else:
        if ar.default == True:
            dst_ar = ar
    form.ar.default = dst_ar.id
    form.process()
    
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    all_tags = Tag.query.all()    
    for tag in all_tags:
        if updated_dst.is_parent_of(tag):
            dst_tag = tag
            break
        else:
            if tag.default == True:
                    dst_tag = tag
    form.tag.default = dst_tag.id
    form.process()
    
    form.sub_tag.choices = [(sub_tag.id, sub_tag.title) for sub_tag in Sub_tag.query.all()]
    all_sub_tags = Sub_tag.query.all()    
    for sub_tag in all_sub_tags:
        if updated_dst.is_parent_of(sub_tag):
            dst_sub_tag = sub_tag
            break
        else:
            if sub_tag.default == True:
                    dst_sub_tag = tag
    form.sub_tag.default = dst_sub_tag.id
    form.process()
    
    form.scrt.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]
    all_scrts = Scrt.query.all()    
    for scrt in all_scrts:
        if updated_dst.is_parent_of(scrt):
            dst_scrt = scrt
            break
        else:
            if scrt.default == True:
                    dst_scrt = scrt
    form.scrt.default = dst_scrt.id
    form.process()
  
    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_dst_form_for_update.html', dst=updated_dst, form=form, from_dst_sort_order=from_dst_sort_order)

    ### POST Case
    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form_for_update.html', dst=updated_dst, form=form, from_dst_sort_order=from_dst_sort_order)

    new_ar = Age_range.query.filter_by(id=request.form['ar']).first()
    set_child_by_type(updated_dst.id, 'Age_range', new_ar)    
    
    tag = Tag.query.filter_by(id=request.form['tag']).first()
    set_child_by_type(updated_dst.id, 'Tag', tag)    

    sub_tag = Sub_tag.query.filter_by(id=request.form['sub_tag']).first()
    set_child_by_type(updated_dst.id, 'Sub_tag', sub_tag)    
        
    scrt = Scrt.query.filter_by(id=request.form['scrt']).first()
    set_child_by_type(updated_dst.id, 'Scrt', scrt)    
    
    updated_dst.title = request.form['title']      #Current Description  selection
    updated_dst.body =  request.form['body']
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==0).filter(Std_general_txt.general_txt_id==updated_dst.id).first()
    if std_gt == None:
        attach_gt_to_std(0, updated_dst.id)
        
    updated_dst.selected=False
    db.session.commit()
      
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))


@dst.route('/dsply_dst_form_for_update2/<int:selected_destination_id>/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form_for_update2(selected_destination_id, from_dst_sort_order):
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
######## END POST METHOD FOR destination_update ###############
      
@dst.route('/destination_delete_for_good', methods=['GET', 'POST'])
def destination_delete_for_good():
    
    #print("IN destination_delete_for_good")
    ############import pdb;; pdb.set_trace()

    
    dst = Destination.query.filter(Destination.selected==True).first()
        
    all_dsts =  Destination.query.all()   # DELETE children if it is not a destinations
    all_goals = Goal.query.all()          # DELETE children if it is not a goal
    all_todos = Todo.query.all()          # DELETE children if it is not a todo
    
    #DEBUG
    '''
    Destination.query.delete()
    Goal.query.delete()
    Todo.query.delete()
    Std_general_txt.query.delete()
    db.session.commit()
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 
    '''
    #DEBUG 
    
    #print("dst: ", dst)
    #print("")
    
    if dst == None:
        flash ("111 Please select a destination to delete first")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 

    #print("IN destination_delete_for_good deleteing dst: ", dst)
    
    for g in dst.children:
         
        for t in g.children:
        
            todo_stds = Std_general_txt.query.filter(Std_general_txt.general_txt_id==t.id).all()
            for ts in todo_stds:
                db.session.delete(ts)
            for c in t.children:
                t.children.remove(c)
            
            g.children.remove(t)
            if t in all_todos:
                db.session.delete(t)
        
        goal_stds = Std_general_txt.query.filter(Std_general_txt.general_txt_id==g.id).all()
        for gs in goal_stds:
            db.session.delete(gs)
                      
        dst.children.remove(g)
        if g in all_goals:
            db.session.delete(g)
    
    dst_stds = Std_general_txt.query.filter(Std_general_txt.general_txt_id==dst.id).all()
    for ds in dst_stds:
        db.session.delete(ds)
        
    db.session.delete(dst)
                
    db.session.commit()
    
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 
        
#delete from index destinations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_delete_for_good2/<int:selected_destination_id>', methods=['GET', 'POST'])
def destination_delete_for_good2(selected_destination_id):
    #print ("destination_delete_for_good2 destination is", selected_destination_id )
    #dst = destination_select2(selected_destination_id)
    ############################old_dst_scrt pdb.set_trace()
    #ds = Destination.query.all()
    #for dst in ds:
     
    dst = destination_select2(selected_destination_id)

    return redirect(url_for('destinations.destination_delete_for_good')) 	


@dst.route('/destination_delete', methods=['GET', 'POST'])
#Here author is user_id
def destination_delete():
	  
    #print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
    #print(current_user.id)

    user = User.query.get_or_404(current_user.id)
    author_id = user.id

    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination to delete first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))
            
    #print(destination.id)

    destination.hide = True
    std_dsts = Std_general_txt.query.filter(Std_general_txt.general_txt_id == destination.id).all()
    for sd in std_dsts:
        sd.hide=True
    for g in destination.children:
        g.hide=True
        std_goals = Std_general_txt.query.filter(Std_general_txt.general_txt_id == g.id).all()
        for sg in std_goals:
            sg.hide=True
        for t in g.children:
            t.hide=True                
            std_todos = Std_general_txt.query.filter(Std_general_txt.general_txt_id == t.id).all()
            for st in std_todos:
                st.hide=True
      
    db.session.commit()
    
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0)) 
        
#delete from index destinations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@dst.route('/destination_delete2/<int:selected_destination_id>', methods=['GET', 'POST'])
#Here author is user_id
def destination_delete2(selected_destination_id):

	#print ("SSSSSSSSSSSSSelected destination is", selected_destination_id )
	dest = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.destination_delete'))
    
    
##############START destination's age range###############

@dst.route('/edit_dst_age_range', methods=['GET', 'POST'])
def edit_dst_age_range():
    dst = Destination.query.filter(Destination.selected==True).filter(Destination.type=='destination').first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=1))		
    #print("In edit_dst_age_rangess DDD dst title is: ",  dst.title  )
    
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
	#print("In edit_dst_age_rangess2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_age_range'))		

 ###START set selected age_range		
@dst.route('/set_dst_age_range/<int:selected_ar_title>', methods=['POST'])
def set_dst_age_range(selected_ar_title):
    #print("In  set_dst_age_range TTT title is: ", selected_ar_title) 
    
    selected_ar_title = selected_ar_title      #Current Age_range selection

   # POST case
    selected_ar = Age_range.query.filter(Age_range.title == selected_ar_title).first()   
    #print("In set_dst_age_range SSSSSSSSS Selected ar is   type: ", selected_ar, selected_ar.type, selected_ar.__tablename__)
    if selected_ar == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_ar = age_range_select2(selected_ar.id) 


    dst = Destination.query.filter(Destination.selected==True).first()

    old_dst_ar=None
    for ar in Age_range.query.all():   #delete the prevois age_range of the updated destination 
        if dst.is_parent_of(ar):
            dst.unset_parent(ar)
            
    #print(" 111 IN set_dst_age_range dst.children is: ", dst.children )
    
    dst.set_parent(selected_ar)
    
    #print(" 222 IN set_dst_age_range dst.children is: ", dst.children )
   
    db.session.commit()

    #####################import pdb;; pdb.set_trace()
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
    #print("In edit_dst_scrtss " )
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
	#print("In edit_dst_scrtss2 Request is :", request)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.edit_dst_scrt'))		


 ###START set selected scrt		
@dst.route('/set_dst_scrt/<int:selected_scrt_title>', methods=['POST'])
def set_dst_scrt(selected_scrt_title):

    selected_scrt_title = selected_scrt_title      #Current Scrt selection

   # POST case
    selected_scrt = Scrt.query.filter(Scrt.title == selected_scrt_title).first()   
    #print("In set_dst_age_range SSSSSSSSS Selected scrt is   type: ", selected_scrt, selected_scrt.type, selected_scrt.__tablename__)
    if selected_scrt == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_scrt = scrt_select2(selected_scrt.id) 

    dst = Destination.query.filter(Destination.selected==True).first()

    old_dst_scrt=None
    for scrt in Scrt.query.all():   #delete the prevois age_range of the updated destination 
        if dst.is_parent_of(scrt):
            old_dst_scrt = scrt
            break
   
    if dst.is_parent_of(old_dst_scrt):
        dst.children.remove(old_dst_scrt)
             
    if  not  dst.is_parent_of(selected_scrt):
        dst.children.append(selected_scrt)
        
    std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==0).filter(Std_general_txt.general_txt_id==dst.id).first()
    if std_dst != None:
       std_dst.scrt_id = selected_scrt.id 
    #old_dst_scrt pdb.set_trace()
    
    db.session.commit() 
    return selected_scrt
 ###END set selected scrt	
     
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
    ############old_dst_scrt pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		
    #print("In edit_destinations_goals : ", destination, destination.selected )
    ##################old_dst_scrt pdb.set_trace()
    return render_template('edit_destinations_goals.html', dst=dst) 
                                                                
														  		
@dst.route('/edit_destinations_goals2/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_destinations_goals2(selected_destination_id):
	#print("In edit_destination_goals2 Request is :", request)
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
           

    #############################old_dst_scrt pdb.set_trace() 	
    author_id = current_user._get_current_object().id
    ##################old_dst_scrt pdb.set_trace()
    goal = Goal(title, body, author_id)
    db.session.add(goal)
    
    ### Add goal to humpty dumpty Demo std ###
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, goal.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    goal.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
    
    dst.set_parent(goal)
    
    db.session.commit()  
    url = url_for('destinations.edit_destinations_goals' )
    return redirect(url)   

@dst.route('/goal_to_destination_add2/<int:selected_destination_id>', methods=['GET', 'POST'])
def goal_to_destination_add2(selected_destination_id):
	#print(selected_destination_id)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.goal_to_destination_add'))			

	
@dst.route('/goal_from_destination_delete', methods=['GET', 'POST'])
def goal_from_destination_delete():
	
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		

    print("IN goal_from_destination_delete  is: ", destination)
    print("")

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal to delete first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		
            
    print("IN goal_from_destination_delete  is: ", destination)
    print("")

    destination.unset_parent(goal)
    db.session.commit()  

    return redirect(url_for('destinations.edit_destinations_goals')) 

@dst.route('/goal_from_destination_delete2/<int:selected_goal_id>', methods=['GET', 'POST'])
#Here author is user_id
def goal_from_destination_delete2(selected_goal_id):

    print("IN goal_from_destination_delete2  selected_goal_id is: ", selected_goal_id)
    print("")

    #dst = destination_select2(selected_destination_id)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('destinations.goal_from_destination_delete')) 	


 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_goal_form ################    
@dst.route('/dsply_goal_form', methods=['GET', 'POST'])
def dsply_goal_form():

    form = Goal_form()

    dst = Destination.query.filter(Destination.selected==True).first()
    form.gt_title = dst.title
    form.gt_body = dst.body
    
    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_goal_form.html', dst=dst, form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form.html', form=form)


    ##############old_dst_scrt pdb.set_trace()
    new_goal_title = form.goal_title.data
    new_goal_body = form.goal_body.data
    
    return goal_to_destination_add(new_goal_title, new_goal_body)


@dst.route('/dsply_goal_form2/<int:selected_destination_id>', methods=['GET', 'POST'])
def dsply_goal_form2(selected_destination_id):
	#print(selected_destination_id)
	dst = destination_select2(selected_destination_id)
	return redirect(url_for('destinations.dsply_goal_form'))			

	
    
################## START  Update destination_update ################    
@dst.route('/dsply_goal_form_for_update', methods=['GET', 'POST'])
def dsply_goal_form_for_update(from_goal_sort_order):

    #print ("In dsply_goal_form_for_update from_goal_sort_order=: ")
    
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
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form_for_update.html', form=form)

    ##############old_dst_scrt pdb.set_trace()
    new_updated_goal_title = request.form['title']      #Current Description  selection
    new_updated_goal_body =  request.form['body']
    
    ##old_dst_scrt pdb.set_trace()    
    #print ("IN dsply_goal_form_for_update")
    
    return destination_update(new_updated_goal_title, new_updated_goal_body)


@dst.route('/dsply_goal_form_for_update2/<int:selected_destination_id>/<int:from_goal_sort_order>', methods=['GET', 'POST'])
def dsply_goal_form_for_update2(selected_destination_id):

    #print("In UUUUUUUUUU dsply_goal_form_for_update2 selected_goal_id ", selected_destination_id)
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

    return render_template('edit_destination_tags.html', destination=destination, tags_not_of_destination=tags_not_of_destination) 
                                                                
														  		
@dst.route('/edit_destinations_tags2/edit/<int:selected_destination_id>/<int:selected_tag_id>', methods=['GET', 'POST'])
def edit_destinations_tags2(selected_destination_id, selected_tag_id):
	#print("In edit_destination_tags2 Request is :", request)
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
	      
	if request.method == 'GET':
		return render_template('edit_tags_not_of_destination.html', tags=tags_not_of_destination)

@dst.route('/tag_to_destination_add2/<int:selected_destination_id>', methods=['GET', 'POST'])
def tag_to_destination_add2(selected_destination_id):
	#############################old_dst_scrt pdb.set_trace()
	dst = destination_select2(selected_destination_id)
	#print("In tag_to_destination_add2 dst.id =:", dst.id)
	#tag = tag_select2(selected_tag_id)
	#print("In tag_to_destination_add2 dst.id =:", dst.id)

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

    #############################old_dst_scrt pdb.set_trace()

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
	############################old_dst_scrt pdb.set_trace()
	tag = Tag.query.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag first ")
		return redirect(url_for('destinations.destinations_by_tag'))

	dst = Destination.query.filter(Destination.selected==True).first()
	if dst == None:
		flash("Please select a dst first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=2))
		
	##print("SSSSSRRRRR IN tag_from_dst_delete   deleteing tag %s from dst %s :",tag.id, dst.id )			
	dst_tag = Dst_Tag.query.filter(Dst_Tag.tag_id == tag.id).filter(Dst_Tag.dst_id==dst.id).first()   #update dst_tag
	if dst_tag:	
		############################old_dst_scrt pdb.set_trace()
		#print ("deleting  Dst_TAG  ", dst_tag.destination_id,dst_tag.tag_id)
		db.session.delete(dst_tag)
		db.session.commit()
	
	return  redirect(url_for('destinations.destinations_by_tag'))  #no change in tags staff dsts
		
@dst.route('/dst_from_tag_delete2/delete/<int:selected_dst_id>/<int:selected_tag_id>', methods=['GET', 'POST'])
def dst_from_tag_delete2(selected_dst_id, selected_tag_id):
	##print("In DDDDDDDDDDDD tag_from_dst_delete2")
	std = tag_select2(selected_tag_id)
	if selected_dst_id:
		##print(selected_dst_id)
		tchr = dst_select2(selected_dst_id)
	return  redirect(url_for('tags.dst_from_tag_delete'))  
############# END Delete dst from tag #############


 ###START set selected age_range		
@dst.route('/set_dst_tag/<int:selected_tag_title>', methods=['POST'])
def set_dst_tag(selected_tag_title):

    #####################import pdb;; pdb.set_trace()
    #print("IN set_dst_tag")
    
   # POST case
    selected_tag = Tag.query.filter(Tag.title == selected_tag_title).first()   
    #print("In set_dst_age_range SSSSSSSSS Selected tag is   type: ", selected_tag, selected_tag.type, selected_tag.__tablename__)
    if selected_tag == None:
        flash("יש לבחור קבוצת גיל")
        return(url_for('destinations.destination_add', from_dst_sort_order=0, selected_ar_title = "בחר קבוצת גיל", selected_tag_title = "בחר נושא", selected_scrt_title = "בחר סוג אבטחה" ))
    
    selected_tag = tag_select2(selected_tag.id) 

    dst = Destination.query.filter(Destination.selected==True).first()

    old_dst_tag=None
    for tag in Tag.query.all():   #delete the prevois age_range of the updated destination 
        if dst.is_parent_of(tag):
            old_dst_tag = tag
            break
            
    if dst.is_parent_of(old_dst_tag):
        dst.children.remove(old_dst_tag)
          
    if  not dst.is_parent_of(selected_tag):
        dst.children.append(selected_tag)
                
    #old_dst_scrt pdb.set_trace()
    
    db.session.commit() 
    return selected_tag
 ###END set selected age_range	
    
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


    
###get selected security option	sub_tag	
@dst.route('/get_selected_sub_tag_title', methods=['GET', 'POST'])
def get_selected_sub_tag_title():
    tmp_sub_tag = Sub_tag.query.filter(Sub_tag.selected == True).first()
    if tmp_sub_tag != None:
        selected_sub_tag_title = tmp_sub_tag.title   
    else:
        selected_sub_tag_title = ":בחר נושא"        
    return selected_sub_tag_title
###end get selected security option	sub_tag


##############destination tags###############	


		

