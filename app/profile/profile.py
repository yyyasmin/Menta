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
prf = Blueprint(
    'profile', __name__,
    template_folder='templates'
) 
  
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2
from app.select.select import general_txt_select2, subject_select2, resource_select2
from app.select.select import tag_select2, sub_tag_select2, age_range_select2, scrt_select2, specific_gt_type_select2
							  
from app.students.students import get_dummy_student, attach_gt_to_std, get_author_id
from app.students.students import reset_and_get_profile #It is in students file due to circular import problem 

from app.gts.gts import get_categories_of, set_gt_category, set_gt_category, get_selected_category_of_gt

from app import *

from datetime import datetime
from datetime import date


############################ START PROFILE #################################


    ############### START EDIT PROFILE ###############

@prf.route('/edit_profile/<int:from_prf_sort_order>', methods=['GET', 'POST'])
@login_required
def edit_profile(from_prf_sort_order):

    print("in edit_profile from_prf_sort_order={0} ,".format(from_prf_sort_order)) 
    print("")
    
    age_ranges = Age_range.query.order_by(Age_range.title).all()    
    tags = Tag.query.order_by(Tag.title).all()
    
    if from_prf_sort_order == 1: 
        return redirect(url_for('profile.edit_profile_by_ABC')) 

    if from_prf_sort_order == 3: 
        return redirect(url_for('profile.edit_profile2_by_tag'))
      
    return redirect(url_for('profile.edit_profile2_by_tag'))

from flask import json
@prf.route('/edit_profile2_by_tag', methods=['GET', 'POST'])
@login_required
def edit_profile2_by_tag():
    return redirect(url_for('students.std_edit_profile2', selected_student_id=get_dummy_student().id))
   
    '''
    print("")
    print("IN edit_profile2_by_tag")
    print("")
    
    
    tags = Tag.query.order_by(Tag.title).all()
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        for t in tags:
            if t.default==True:
                default_tag = t


    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all()
    
    #####import pdb;;; pdb.set_trace()
    
    default_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if default_sub_tag == None:
        for st in sub_tags:
            if default_tag.is_parent_of(st) and st.default==True:
                default_sub_tag = st
    
    profile = reset_and_get_profile(0)

    print("")
    for t in tags:
        print("t", t.id)
        for s in sub_tags:
            print("s", s.id)
            if t.is_parent_of(s):
                print("tag {0} IS PARENT OF  {1}".format(t.id, s.id))
    print("")
    print("")
    print("sub_tags", sub_tags)



    prf_subjects=[]
    all_subjects = Subject.query.all()
    for s in all_subjects:
        if profile.is_parent_of(s):
            prf_subjects.append(s)
        
    prf_weaknesses=[]
    all_weaknesses = Weakness.query.all()
    for s in all_weaknesses:
        if profile.is_parent_of(s):
            prf_weaknesses.append(s)
        
    prf_strengths=[]
    all_strengths = Strength.query.all()
    for s in all_strengths:
        if profile.is_parent_of(s):
            prf_strengths.append(s)
            
            
   
    user = User.query.get_or_404(current_user._get_current_object().id)
    author_id = user.id
    
    sbj = Subject.query.filter(Subject.title=='Subject_data').first()
    if sbj==None:
        sbj = Subject('Subject_data', 'Subject_data', author_id)
       
    strn = Strength.query.filter(Strength.title=='Subject_data').first()
    if strn==None:
        strn = Strength('Strength_data', 'Strength_data', author_id)
       
    weak = Weakness.query.filter(Weakness.title=='Subject_data').first()
    if weak==None:
        weak = Weakness('Weakness', 'Weakness', author_id)
    
    return render_template('./profile/std_profile2/std_edit_profile2.html', profile=profile, 
                            sbj=sbj, strn=strn, weak=weak,
                            tags=tags, default_tag=default_tag,
                            sub_tags=sub_tags, default_sub_tag=default_sub_tag,
                            prf_subjects=prf_subjects, 
                            prf_weaknesses=prf_weaknesses, 
                            prf_strengths=prf_strengths)															
    '''


@prf.route('/edit_profile_by_ABC', methods=['GET', 'POST'])
@login_required
def edit_profile_by_ABC():
    profile = reset_and_get_profile(0)   #get only public profile   
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    #############################old_prf_scrt pdb.set_trace()
    return render_template('edit_prf_by_ABC.html', profile=profile)
    
    ################ END EDIT PROFILE ###############

    ################ START UPDATE PROFILE ###############
#### POST CASE ####                                                                                     
@prf.route('/profile_update/<int:from_prf_sort_order>', methods=['POST'])
def profile_update(from_prf_sort_order, selected_ar_title, selected_tag_title, selected_scrt_title, new_prf_title, new_prf_body):
    
    ##old_prf_scrt pdb.set_trace()    
    #print ("IN profile_update")
        
    #print("In POST profile_update_at_once is :",   from_prf_sort_order)
    ##############old_prf_scrt pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    tags = Tag.query.all()  
    
    updated_prf = Profile.query.filter(Profile.selected==True).first()
    if updated_prf == None:
        flash("Please select a profile to update first ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=from_prf_sort_order))
  
    #POST case

    selected_tag = set_prf_tag(selected_tag_title) 
    
    updated_prf.title = new_prf_title
    updated_prf.body = new_prf_body

    db.session.commit()
         
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=from_prf_sort_order))
      
@prf.route('/profile_update2/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_update2(selected_profile_id):
	#print("In profile_update2 Request is :", request)
	prf = profile_select2(selected_profile_id)
	return redirect(url_for('profile.dsply_form',  selected_profile_id=selected_profile_id,
                                                                     from_prf_sort_order=0))		
    ################ END UPDATE PROFILE ###############


    ################ START DELETE PROFILE ################
                                                                    
@prf.route('/profile_delete_for_good', methods=['GET', 'POST'])
def profile_delete_for_good():
    
    #print("IN profile_delete_for_good")
    ############################import pdb;;; pdb.set_trace()
    
    prf = Profile.query.filter(Profile.selected==True).first()
    
    
    profile =  Profile.query.first()    # DELETE children if it is not a profile
    all_subjects = Subject.query.all()  # DELETE children if it is not a subject
        
    if prf == None:
        flash ("111 Please select a profile to delete first")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=0)) 

    #print("IN profile_delete_for_good deleteing prf: ", prf)
    
    for g in prf.children.all():
         
        subject_stds = Std_general_txt.query.filter(Std_general_txt.general_txt_id==g.id).all()
        for gs in subject_stds:
            db.session.delete(gs)
                      
        prf.children.remove(g)
        if g in all_subjects:
            db.session.delete(g)
    
    prf_stds = Std_general_txt.query.filter(Std_general_txt.general_txt_id==prf.id).all()
    for ds in prf_stds:
        db.session.delete(ds)
        
    db.session.delete(prf)
                
    db.session.commit()
    
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=0)) 
        
#delete from index profile list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@prf.route('/profile_delete_for_good2/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_delete_for_good2(selected_profile_id):
    #print ("profile_delete_for_good2 profile is", selected_profile_id )
    #prf = profile_select2(selected_profile_id)
    ############################old_prf_scrt pdb.set_trace()
    #ds = Profile.query.all()
    #for prf in ds:
     
    prf = profile_select2(selected_profile_id)

    return redirect(url_for('profile.profile_delete_for_good')) 	


@prf.route('/profile_delete', methods=['GET', 'POST'])
#Here author is user_id
def profile_delete():
	  
    #print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
    #print(current_user.id)

    user = User.query.get_or_404(current_user.id)
    author_id = user.id

    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile to delete first ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=0))
            
    #print(profile.id)

    profile.hide = True
    std_prfs = Std_general_txt.query.filter(Std_general_txt.general_txt_id == profile.id).all()
    for sd in std_prfs:
        sd.hide=True
    for g in profile.children.all():
        g.hide=True
        std_subjects = Std_general_txt.query.filter(Std_general_txt.general_txt_id == g.id).all()
        for sg in std_subjects:
            sg.hide=True

    db.session.commit()
    
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=0)) 
        
#delete from index profile list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@prf.route('/profile_delete2/<int:selected_profile_id>', methods=['GET', 'POST'])
#Here author is user_id
def profile_delete2(selected_profile_id):

	#print ("SSSSSSSSSSSSSelected profile is", selected_profile_id )
	prf = profile_select2(selected_profile_id)
	return redirect(url_for('profile.profile_delete'))
    
    ################ END DELETE PROFILE ################

############################ END PROFILE #################################
    


############################## START GT #################################

    ################## START  ADD GT ################ 

#### POST CASE ####                                                                                     
@prf.route('/gt_to_profile_add', methods=['GET', 'POST'])
def gt_to_profile_add(new_gt_type, new_gt_title, new_gt_body):
   

    profile = Profile.query.filter(Profile.selected=='True').first()
    if profile == None:
        flash("Please select a profile to add a part to ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
    
    '''
    for t in Tag.query.all():
        if profile.is_parent_of(t):
            selected_tag = t
            break

    for st in Sub_tag.query.all():
        if profile.is_parent_of(st):
            selected_sub_tag = st
            break
    '''
    selected_tag = Tag.query.filter(Tag.selected==True).first()
    if selected_tag == None:
        for t in Tag.query.all():
            if t.default==True:
                selected_tag = t 
        
    selected_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if selected_sub_tag == None:
        for st in Sub_tag.query.all():
            if (st.default==True) and (t.is_parent_of(st)):
                selected_tag = t 
        
    #######import pdb; pdb.set_trace()

    print ("In gt_to_profile_add BEFOR VVVVVVVVVVVVVVV validate type, new_gt_title, new_gt_body, new_gt_type, tag  sub_tag : ", 
                                                            type, new_gt_title, new_gt_body, new_gt_type,
                                                            selected_tag.id, selected_sub_tag.id)
    print("")
    print("")
    
              
            
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)
    
    print("In gt_to_profile_add profile is :", profile, profile.id)
    print("")    
    print("In gt_to_profile_add sub_tag_title is :",  selected_sub_tag,  selected_sub_tag.id)
    print("")  
    print("In gt_to_profile_add tag_title is :", selected_tag, selected_tag.id)
    print("")
    print("In gt_to_profile_add new_gt_title is :", new_gt_title)
    print("")
    print("In gt_to_profile_add new_gt_body is :", new_gt_body)
    print("")
    print("In gt_to_profile_add gt_type is :", new_gt_type)
    
    author_id = current_user._get_current_object().id    
    
    ### CHANgE subject to Subject ###
    new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).title==new_gt_title).filter(eval(new_gt_type).body==new_gt_body).first()            

    if new_gt == None:
        new_gt = eval(new_gt_type)(new_gt_title, new_gt_body, author_id)
        db.session.add(new_gt)
        db.session.commit()
        
    print("new_gt.id  ", new_gt.id)
    
    new_gt = general_txt_select2(new_gt.id)
    
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    
    db.session.add(new_gt)
    db.session.commit()
    
    #new_gt = general_txt_select2(new_gt.id)
    new_gt.set_parent(selected_sub_tag)
    new_gt.set_parent(selected_tag)
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_gt.id) 
    
    ###########################import pdb;; pdb.set_trace()
    profile.set_parent(new_gt)
    
    
    print(" In BEFORE COMMIT the END OF gt_to_profile_add new_gt.gt_type =: " ,new_gt.id,  new_gt.gt_type)
    
    new_gt.selected = False
    db.session.commit()
    
    #DEBUG
    new_gt = General_txt.query.filter(General_txt.id== new_gt.id).first()
    print(" In BEFORE AFTER the END OF gt_to_profile_add new_gt.gt_type =: " ,new_gt.id,  new_gt.gt_type)
    print("")
    #DEBUG
    
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )
          

@prf.route('/gt_to_profile_add2', methods=['GET', 'POST'])
def gt_to_profile_add2():

    print("")
    print("")
    print("")
    print(" IN gt_to_profile_add2 type=:")
    print("")
    print("")
    
    author_id = current_user._get_current_object().id    
    
    form = Gt_form()

    ######import pdb; pdb.set_trace()
    
    print("request.form['gt_title'] ",   request.form['gt_title'])
    print("request.form['gt_body'] ",    request.form['gt_body'])
    print("request.form['class_name'] ", request.form['class_name'])
        
    new_gt_title =  request.form['gt_title']
    new_gt_body =  request.form['gt_body']
    new_gt_type =  request.form['class_name']
    
 
    print("  IN END OF gt_to_profile_add2 --- GT: ",new_gt_type, new_gt_title, new_gt_body)
    print("")
    print("")
    return gt_to_profile_add(new_gt_type, new_gt_title, new_gt_body) 

    ################## END  ADD GT ################ 


    ############### START UPDATE GT ################  

#### POST CASE ####                                                                                     
@prf.route('/profile_gt_update2/<int:selected_gt_id>', methods=['GET', 'POST'])
def profile_gt_update2(selected_gt_id):
        
    #author_id = current_user._get_current_object().id    
   
    updated_gt = General_txt.query.filter(General_txt.id==selected_gt_id).first()    
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile_by_tag') )
          
    updated_gt.title = request.form['gt_title']
    updated_gt.body =  request.form['gt_body']
  
    print("")
    print("IN END OF profile_gt_update2")
    print("UPDATE  gt {0}  WITH:  title {1}   body {2}". format(updated_gt.id, updated_gt.title, updated_gt.body)) 
    print("")
    print("")
    
    db.session.commit()

    updated_gt.selected = False
    db.session.commit()
    
    return edit_profile2_by_tag()

    ############## END UPDATE GT ################ 



    ################ END DELETE GT ############## 

@prf.route('/gt_from_profile_delete', methods=['GET', 'POST'])
def gt_from_profile_delete():

    ##########################import pdb; pdb.set_trace()

    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('profile.edit_profile_by_tag'))		

    gts = General_txt.query.filter(General_txt.selected==True).all()
    if gts == None:
        flash("Please select a gt to delete first ")
        return redirect(url_for('select.edit_profile_by_tag'))
           
    for gt in gts:
        if profile.is_parent_of(gt):
                profile.unset_parent(gt)    
                gt.selected = False
                break    
         
    print ("deleted  profile from gt  ",  profile, profile.id,  gt, gt.id  )

    db.session.commit()  

    return redirect(url_for('profile.edit_profile2_by_tag')) 


@prf.route('/gt_from_profile_delete2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
def gt_from_profile_delete2(selected_profile_id, selected_gt_id):
    print(" IN gt_from_profile_delete2:  selected_profile_id, selected_gt_id", selected_profile_id, selected_gt_id)
    prf = Profile.query.filter(Profile.id==selected_profile_id).first()

    gt = general_txt_select2(selected_gt_id)
    prf = profile_select2(prf.id)
    
    return redirect(url_for('profile.gt_from_profile_delete')) 	

    ################## END DELETE GT ################ 



    ############### START TAG ################
###get selected security option	tag	
@prf.route('/get_selected_tag_title', methods=['GET', 'POST'])
def get_selected_tag_title():
    tmp_tag = Tag.query.filter(Tag.selected == True).first()
    if tmp_tag != None:
        selected_tag_title = tmp_tag.title   
    else:
        selected_tag_title = ":בחר נושא"        
    return selected_tag_title
###end get selected security option	tag

                                          
@prf.route('/tag')
def tag():
    tags = Tag.query.all()

    tagArray = []

    for tag in tags:
        tagObj = {}
        tagObj['id'] = tag.id
        tagObj['name'] = tag.title
        tagArray.append(tagObj)

    return jsonify({'tags' : tagArray})
    
        ############### END TAG ################
 
    ############ START GT CATEGORY (TAG) #############
 
######################### END GT #################################
		
