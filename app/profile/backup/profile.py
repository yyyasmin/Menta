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
from app.select.select import tag_select2, age_range_select2, scrt_select2, specific_gt_type_select2
							  
from app.students.students import get_dummy_student, attach_gt_to_std
from app import *

from datetime import datetime
from datetime import date


############################ START PROFILE #################################
                                                                
@prf.route('/reset_and_get_profile', methods=['GET', 'POST'])
def reset_and_get_profile():

    students = Student.query.order_by(Student.last_name).order_by(Student.first_name).filter(Student.hide==False).all() 
    for std in students:
        std.selected=False
    
    profile = Profile.query.filter(Profile.hide==False).first()    

    gts = General_txt.query.all()
    for gt in gts:
        gt.selected=False
        
    db.session.commit()

    return profile


    ############### START EDIT PROFILE ###############

@prf.route('/edit_profile/<int:from_prf_sort_order>', methods=['GET', 'POST'])
@login_required
def edit_profile(from_prf_sort_order):

    age_ranges = Age_range.query.order_by(Age_range.title).all()    
    tags = Tag.query.order_by(Tag.title).all()
    
    if from_prf_sort_order == 1: 
        return redirect(url_for('profile.edit_profile_by_ABC')) 

    if from_prf_sort_order == 3: 
        return redirect(url_for('profile.edit_profile_by_tag'))
      
    return redirect(url_for('profile.edit_profile_by_tag'))

@prf.route('/edit_profile_by_tag', methods=['GET', 'POST'])
@login_required
def edit_profile_by_tag():
    profile = reset_and_get_profile()   
    tags = Tag.query.order_by(Tag.title).all()
    print("In edit_profile_by_tag ")
    return render_template('edit_prf_by_tag.html', profile=profile, tags=tags)															

@prf.route('/edit_profile_by_ABC', methods=['GET', 'POST'])
@login_required
def edit_profile_by_ABC():
    profile = reset_and_get_profile()   #get only public profile   
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
    ########import pdb;; pdb.set_trace()
    
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
   
@prf.route('/dsply_gt_form_for_add/<int:type>', methods=['GET'])
def dsply_gt_form_for_add(type): 

    print ("In dsply_gt_form_for_add")
    
    prf = Profile.query.filter(Profile.selected == True).first()
    if prf == None:
        flash("Please select a profile to update a part for")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
        
    form = Gt_form()
    
    if  type == 1:
        form.gt_type_txt == 'חולשה'       
        form.gt_type = 'Weakness'
        
    elif type == 2:
        form.gt_type_txt == 'חוזקה'
        form.gt_type = 'Srength'
             
    else:  
        form.gt_type_txt == 'תחום עיניין'        
        form.gt_type = 'Subject'
        
    form.tag.choices=[]
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]

    return render_template('./gt/backup/add_gt_form.html', profile=prf, form=form, type=type)
    #return render_template('./gt/dsply_gt_form_for_add.html', profile=prf, form=form, type=type)


@prf.route('/dsply_gt_form_for_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def dsply_gt_form_for_add2(selected_profile_id, type):
       
    print(selected_profile_id) 
    prf = Profile.query.filter(Profile.id == selected_profile_id).first()
    if prf == None:
        general_profile = Profile.query.filter(Profile.title=='general').first()
        if general_profile == None:
            general_profile = Profile('general', 'default', author_id)	
            db.session.add(general_profile)
            std = get_dummy_student()   # Match new general prf to Humpty Dumpty
            std_gt = attach_gt_to_std(std.id, general_profile.id) 
            db.session.commit()
            
    print(" IN dsply_gt_form_for_add2 prf.id=: ", prf.id)
    prf = profile_select2(prf.id)   # save new prf for next setting

    return redirect(url_for('profile.dsply_gt_form_for_add', profile=prf, type=type))			

#### POST CASE ####                                                                                     
@prf.route('/gt_to_profile_add/<int:type>', methods=['GET', 'POST'])
def gt_to_profile_add(type):

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #
    import pdb; pdb.set_trace()
    print(" IN gt_to_profile_add request.form: ", request.form)
    '''
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_form_for_update.html', form=form)
    '''
#************************
    tag = Tag.query.filter_by(id=form.tag.data).first()
#************************
    

    ##############old_prf_scrt pdb.set_trace()
    new_gt_title = form.gt_title.data
    new_gt_body =  form.gt_body.data
        
    print("In gt_to_profile_add tag_title is :", selected_tag_title)
    print("")
    print("In gt_to_profile_add new_gt_title is :", new_gt_title)
    print("")
    print("In gt_to_profile_add new_gt_body is :", new_gt_body)
    print("")
    print("In gt_to_profile_add gt_type is :", type)
     
    author_id = current_user._get_current_object().id    
                
    general_profile = Profile.query.filter(Profile.selected==True).first()
    if general_profile == None:
        flash("Please select a profile to add apart to ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
    
    if type == 1:
        gt_type_txt == 'חולשה'       
        gt_type = 'Weakness'
        
    elif type == 2:
        gt_type_txt == 'חוזקה'
        gt_type = 'Srength'
             
    else:  
        gt_type_txt == 'תחום עיניין'        
        gt_type = 'Subject'
     
    new_gt = eval(gt_type).query.filter(eval(gt_type).title==new_gt_title).filter(eval(gt_type).body==new_gt_body).first()            
    
    print(" new_gt", new_gt, new_gt.id)
    print("")
    print(" new_gt_id",new_gt.id)
    print("")
    print("gt type  ", eval(gt_type), gt, eval(gt_type))
    print("")
    
    if new_gt == None:
        new_gt = eval(gt_type)(new_gt_title, new_gt_body, author_id)
        db.session.add(new_gt)
        db.session.commit()
        
    print("new_gt.id  ", new_gt.id)
    
    new_gt = general_txt_select2(new_gt.id)
    
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    new_gt.gt_type = gt_type
    new_gt.gt_type_txt = gt_type_txt
                
    selected_tag = set_gt_category(gt, 'Tag', selected_tag_title, new_gt.id, "בחר נושא")
    
    #DEBUG
    for c in new_gt.children.all():
        print("CCCCCCCCCCC IN gt_to_profile_add new_gt's children - c: c.id:   ", c, c.id)
    #DEBUG
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_gt.id) 
    
    ########import pdb;; pdb.set_trace()
    general_profile.set_parent(new_gt)
    new_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )


@prf.route('/gt_to_profile_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def gt_to_profile_add2(selected_profile_id, type):

#***********************************
     
    gt_tag_name = "gt_tag"
    print( "request.form[gt_tag_name]", request.form[gt_tag_name])
    
    gt_title_name = "gt_title"
    print( "request.form[gt_title_name]", request.form[gt_title_name])
     
    gt_body_name = "gt_body"
    print( "request.form[gt_body_name]", request.form[gt_body_name])
    
#************************************

    print(selected_profile_id)
    
    prf = Profile.query.filter(Profile==selected_profile_id).first()
        
    if prf == None:
        prf = Profile.query.filter(Profile.title=='general').first()
        if prf == None:
            prf = Profile('general', 'default', author_id)	
            db.session.add(prf)
            std = get_dummy_student()   # Match new general prf to Humpty Dumpty
            std_gt = attach_gt_to_std(std.id, prf.id) 
            db.session.commit()

    prf = profile_select2(prf.id)   # save new prf for next setting

    return redirect(url_for('profile.gt_to_profile_add', type=type))			

    ################## END  ADD GT ################ 


    ############### START UPDATE GT ################  
 
@prf.route('/dsply_gt_form_for_update', methods=['GET', 'POST'])
def dsply_gt_form_for_update():
    
    updated_gt = General_txt.query.filter(General_txt.selected==True).first()
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
         
    updated_prf = Profile.query.filter(Profile.selected==True).first()
    if updated_prf == None:
        flash("Please select a profile to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
            
    #print("IIIIIIIIIIIIn dsply_gt_form_for_update2 Updated prf is", updated_gt.title)

    form = Gt_form()

    form.title.data = updated_gt.title
    form.body.data =  updated_gt.body
    form.gt_type.data =  updated_gt.gt_type
    form.gt_type_txt.data =  updated_gt.gt_type_txt

    form.tag.choices=[]

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    all_tags = Tag.query.all()    
    for tag in all_tags:
            if updated_gt.is_parent_of(tag):
                gt_tag = tag
                break
    form.tag.default = gt_tag.id
    form.process()

    ### GET Case
    if request.method == 'GET':
        return render_template('./gt/dsply_gt_form_for_update.html', prf=updated_prf, update_gt=updated_gt, form=form)


@prf.route('/dsply_gt_form_for_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def dsply_gt_form_for_update2(selected_profile_id, selected_gt_id):
    if selected_gt_id == 0:        
        prf = Profile.query.filter(Profile.body=='default').first()
    else:
        prf = Profile.query.filter(Profile.id).first()
        
    prf = general_txt_select2(prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.dsply_gt_form_for_update'))			


#### POST CASE ####                                                                                     
@prf.route('/gt_profile_update', methods=['POST'])
def gt_profile_update():

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_update.html', form=form)
        
    #import pdb; pdb.set_trace()
    tag = Tag.query.filter_by(id=form.tag.data).first()


    updated_gt_title = request.form['title']      #Current Description  selection
    updated_gt_body =  request.form['body']
    updated_gt_type =  request.form['gt_type']
    updated_gt_type_txt =  request.form['type_txt']
         
    print("In gt_profile_update tag_title is :", updated_gt_title)
    print("")
    print("In gt_profile_update updated_gt_body is :", updated_gt_body)
    print("")
    print("In gt_profile_update updated_gt_type is :", updated_gt_type)
    print("")
    print("In gt_profile_update updated_gt_type_txt is :", updated_gt_type_txt)
    print("")
    print("In gt_profile_update tag is :", tag)
    print("")
    
    author_id = current_user._get_current_object().id    
                
    updated_profile = Profile.query.filter(Profile.selected==True).first()
    if updated_profile == None:
        flash("Please select a profile to update a part ")
        return redirect(url_for('profile.edit_profile_by_tag') )

    ###import pdb; pdb.set_trace()
    print(" IN gt_profile_update   updated_gt  is:  " , updated_gt)
    print("")  
    print(" IN gt_profile_update   updated_gt.gt_type_txt     is: " , updated_gt.gt_type_txt)
    print("")
       
    updated_profile = profile_select2(updated_profile.id)   # save new prf for next setting
    
    updated_gt = eval(gt).query.filter(eval(gt).title==updated_gt_title).filter(eval(gt).body==updated_gt_body).first()        
    
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile_by_tag') )

    print("IN gt_profile_update updated_gt.id  - BEFORE select  ", updated_gt.id)
    
    updated_gt = general_txt_select2(updated_gt.id)
    
    print("IN gt_profile_update updated_gt.id  - AFTER select ", updated_gt.id)    
     
    updated_gt.title = updated_gt_title
    updated_gt.body =  updated_gt_body
    updated_gt.type =  updated_gt_type
    updated_gt.type_txt =  updated_gt_type_txt
                
    selected_tag = set_gt_category(gt, 'Tag', selected_tag_title, updated_gt.id, "בחר נושא")
    
    print(" IN gt_profile_update Seted Tag to : ", selected_tag)
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, updated_gt.id) 
    
    ########import pdb;; pdb.set_trace()
    updated_profile.set_parent(updated_gt)
    updated_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile_by_tag') )


@prf.route('/gt_profile_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def gt_profile_update2(selected_profile_id, selected_gt_id):
    if selected_gt_id == 0:        
        prf = Profile.query.filter(Profile.body=='default').first()
    else:
        prf = Profile.query.filter(Profile.id).first()
        
    prf = general_txt_select2(prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.gt_profile_update'))
    
    ############## END UPDATE GT ################ 



    ################ END DELETE GT ############## 

@prf.route('/gt_from_profile_delete', methods=['GET', 'POST'])
def gt_from_profile_delete():

    ##import pdb; pdb.set_trace()

    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('profile.edit_profile_by_tag', from_prf_sort_order=0))		

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

    return redirect(url_for('profile.edit_profile_by_tag')) 


@prf.route('/gt_from_profile_delete2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
def gt_from_profile_delete2(selected_profile_id, selected_gt_id):
    print(" IN gt_from_profile_delete2:  selected_profile_id, selected_gt_id", selected_profile_id, selected_gt_id)
    prf = Profile.query.filter(Profile.body=='default').first()
    prf = profile_select2(prf.id)

    gt = general_txt_select2(selected_gt_id)
    
    return redirect(url_for('profile.gt_from_profile_delete')) 	

    ################## END DELETE GT ################ 



    ############ START GT CATEGORY (TAG) #############
    																 	
 ###START set selected category		
@prf.route('/set_gt_category/<int:selected_category_title>/<int:selected_gt_id>', methods=['GET', 'POST'])
def set_gt_category(Gt, Category, selected_category_title, selected_gt_id, str_msg):

    #################import pdb;; pdb.set_trace()
    #print("IN set_prf_category")
    
   # POST case
    selected_category = eval(Category).query.filter(eval(Category).title == selected_category_title).first()   
    #print("In set_prf_age_range SSSSSSSSS Selected category is   type: ", selected_category, selected_category.type, selected_category.__tablename__)
    if selected_category == None:
        flash(str_msg)
        return(url_for('profile.edit_profile'))
    
    selected_category = general_txt_select2(selected_category.id) 

    gt = eval(Gt).query.filter(eval(Gt).selected==True).first()
    if gt == None:
        flash("Please select a subject first")
        return(url_for('profile.edit_profile', from_prf_sort_order=3))

    for category in eval(Category).query.all():   #delete the prevois category of the updated profile and ser the new one
        if gt.is_parent_of(category):
            gt.unset_parent(category)
            gt.set_parent(selected_category)
           
    gt.set_parent(selected_category)  # Uncase there is no previous category for gt 
    
    db.session.commit() 
    return selected_category
 ###END set selected age_range	
    
###get selected security option	category	
@prf.route('/get_selected_category_title', methods=['GET', 'POST'])
def get_selected_category_title(msg):
    tmp_category = eval(Category).query.filter(eval(Category).selected == True).first()
    if tmp_category != None:
        selected_category_title = tmp_category.title   
    else:
        selected_category_title = "msg"        
    return selected_category_title
###end get selected security option	category


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
		

