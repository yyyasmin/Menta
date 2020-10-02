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

from app.models import User, School, Student, Teacher, Profile, Strength, Weakness, Tag, Destination, Goal, General_txt

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
gt = Blueprint(
    'gts', __name__,
    template_folder='templates'
)   


from app.select.select import student_select2, goal_select2, resource_select2
from app.select.select import profile_select2, strength_select2, general_txt_select2, specific_gt_type_select2
 
from app import *
from datetime import datetime
																		

@gt.route('/edit_gts', methods=['GET', 'POST'])
@login_required
def edit_gts():

    #DEBUG ONLY

    #DEBUG ONLY
    
    #gts = General_txt.query.order_by(General_txt.class_name).order_by(General_txt.title).all() 
    gts = General_txt.query.all() 

    '''
    print("")
    for g in gts:
        print("g g.class_name", g, g.class_name)
        print("")
    '''
    
    i=0
    for g in gts:
        g.odd = (i%2 == 1)
       
    #################import pdb; pdb.set_trace()
    return render_template('edit_gts.html', gts=gts)							
		
        
@gt.route('/gt_add', methods=['GET', 'POST'])
@login_required
def gt_add():

    #################import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id
			
    if request.method == 'GET':
        return render_template('add_gt.html')
        
    from_age = int(request.form.get('from_age'))
    to_age = int(request.form.get('to_age'))     
    
    class_name = request.form.get('class_name')
    
    new_gt_title = request.form.get('title')
    new_gt_body = request.form.get('body')
    
    gt = eval(class_name).query.filter(eval(class_name).title==new_gt_title).first()
    if gt == None:
        if class_name == 'Age_range':
            gt = eval(class_name)(new_gt_title, new_gt_body, from_age, to_age, author_id)	
        else:
            gt = eval(class_name)(new_gt_title, new_gt_body, author_id)	
    else:
        flash ("This Category allready exist")
        return edit_gts()
        
    gt.class_name = class_name
    gt.gt_type = class_name
    
    gt.title = new_gt_title
    gt.body = new_gt_body
    
    gt.h_name = request.form.get('h_name')
    gt.e_name = request.form.get('e_name')
        
    gt.default = request.form.get('default')=='on'
    
    print("")
    print("IN gt_add request.form.get('default'): ", request.form.get('default'))
    print("IN gt_add from_age-to_age: ", from_age, to_age)
    print("IN gt_add class_name: ", class_name)
    print("")
    print("")
        
    gt.color_txt = request.form.get('color_name_txt')
    gt.color = get_color(gt.color_txt)
    
    db.session.add(gt)    

    parent_title = request.form.get('parent')
    if parent_title != '' and parent_title != []  and parent_title != None:        
        parent_class_name = request.form.get('parent_class_name')
        parent = eval(parent_class_name).query.filter(eval(parent_class_name).title==parent_title).first()
        if parent != None: 
            parent.set_parent(gt)
    
    child_title = request.form.get('child')
    if child_title != '' and child_title != []  and child_title != None:        
        child_class_name = request.form.get('child_class_name')
        child = eval(child_class_name).query.filter(eval(child_class_name).title==child_title).first()
        if child != None: 
            gt.set_parent(child)

    db.session.commit() 
    
    gt = general_txt_select2(gt.id)
    flash ("קטגוריה {0} {1} הוספה בהצלחה!j".format(gt.class_name, gt.title))
    url = url_for('gts.edit_gts')
    return redirect(url)   
	
#update selected gt
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@gt.route('/gt_update/<int:selected_gt_id>', methods=['GET', 'POST'])
@login_required
def gt_update(selected_gt_id):

    gt = General_txt.query.filter(General_txt.id == selected_gt_id).first()
    if gt == None:
        flash("Please select a Category to update first")
        return edit_gts()
			
    if request.method == 'GET':
        #print("GET render update_gt.html")
        return render_template('update_gt.html', gt=gt)
        
    gt.h_name = request.form.get('h_name')
    gt.e_name = request.form.get('e_name')
   
    gt.class_name = request.form.get('class_name')   
    gt.gt_type = gt.class_name
      
    gt.color_txt = request.form.get('color_name_txt')
    gt.color = get_color(gt.color_txt)
     
    gt.title = request.form.get('title')
    gt.body = request.form.get('body')


    gt.default = request.form.get('default') == 'on'
    
    if gt.class_name == 'Age_range':        
        gt.from_age = int(request.form.get('from_age'))
        gt.to_age =   int(request.form.get('to_age'))     
       
    print("")
    print("IN gt_update gt.default: ", gt.default)
    print("")
    print("")
        
    ###import pdb; pdb.set_trace()
    
    parent_title = request.form.get('parent')
    if parent_title != None and parent_title != []  and parent_title != '':        
        parent_class_name = request.form.get('parent_class_name')
        parent = eval(parent_class_name).query.filter(eval(parent_class_name).title==parent_title).first()
        if parent != None: 
            parent.set_parent(gt)
    
    child_title = request.form.get('child')
    if child_title != None and child_title != []  and child_title != '':        
        child_class_name = request.form.get('child_class_name')
        child = eval(child_class_name).query.filter(eval(child_class_name).title==child_title).first()
        if child != None: 
            gt.set_parent(child)

    db.session.commit()  
    db.session.refresh(gt)
	
    return redirect(url_for('gts.edit_gts'))
	
		
@gt.route('/gt_delete_for_good', methods=['GET', 'POST'])
@login_required
#Here author is user_id
def gt_delete_for_good():

    gt = General_txt.query.filter(General_txt.selected==True).first()
    if gt == None:
        flash("Please select a gt to delete first ")
        return redirect(url_for('gts.edit_gts'))
            
    print("")
    print ("delete for good selected gt is " )
    print(gt.id, gt.title) 
    print("")
        
    all_gts = General_txt.query.all()   # Remove gt from its parent
    for g in all_gts:
        if g.is_parent_of(gt):
            g.unset_parent(gt)
                 
    std_gs = Std_general_txt.query.filter(Std_general_txt.general_txt_id == gt.id).all()
    for std_g in std_gs:
        std = Student.query.filter(Student.id == std_g.student_id).first()
        if std != None:
            if std.general_txts != []:
                if std_g in std.general_txts:
                    std.general_txts.remove(std_g)
                    
        gt = General_txt.query.filter(General_txt.id == std_g.general_txt_id).first()
        if std_g in gt.students:
            std.students.remove(std_g)
    
        gts = gt.children
        while gts !=  []:
            for c in gts:
                std_cs = Std_general_txt.query.filter(Std_general_txt.general_txt_id == c.id).all()
                for std_c in std_cs:
                    db.session.delete(std_c)
                db.session.delete(c)
            gts = c.children
                   
    db.session.delete(gt)
            
    db.session.commit()
            
    flash ("Deleted " + gt.title + " object Successfully")
            
    return redirect(url_for('gts.edit_gts')) 
		
#delete from index gts list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@gt.route('/gt_delete_for_good2/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required

def gt_delete_for_good2(selected_gt_id):

    #print ("SSSSSSSSSSSSSelected gt is" )
    ################import pdb; pdb.set_trace()
    general_txt_select2(selected_gt_id)
    return redirect(url_for('gts.gt_delete_for_good')) 	


@gt.route('/gt_delete', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def gt_delete():

    user = User.query.get_or_404(current_user.id)
    author_id = user.id

    gt = General_txt.query.filter(General_txt.selected==True).first()
    if gt == None:
        flash("Please select a gt to delete first ")
        return redirect(url_for('gts.edit_gts'))

    gt.hide = True

    db.session.commit()
    return redirect(url_for('gts.edit_gts')) 
        
#delete from index gts list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@gt.route('/gt_delete2/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
def gt_delete2(selected_gt_id):

	#print ("SSSSSSSSSSSSSelected gt is", selected_gt_id )
	gt = general_txt_select2(selected_gt_id)
	return redirect(url_for('gts.gt_delete'))

    ############ START GT CATEGORY (TAG) #############
    																 	
 ###START set selected category		
@gt.route('/set_gt_category/<int:selected_category_title>/<int:selected_gt_id>', methods=['GET', 'POST'])
def set_gt_category(gt_id, Ctg_of_gt_type, selected_category_title, str_msg):

    ##############import pdb; pdb.set_trace()
    #print("IN set_prf_category")
    
   # POST case
    #example: get Tag=='Math'
    selected_category = eval(Ctg_of_gt_type).query.filter(eval(Ctg_of_gt_type).title == selected_category_title).first()   
    if selected_category == None:
        flash(str_msg)
        return(url_for('students.index'))
        
    selected_category = specific_gt_type_select2(selected_category.id, Ctg_of_gt_type)    #Example: selcted Tag='Math'
    
    ###################import pdb; pdb.set_trace()
    
    gt = General_txt.query.filter(General_txt.id==gt_id).first()    #Example: select Subject='אוהב לצייר'
    
    if gt == None:
        flash("Please select a category first")
        return(url_for('gts.edit_gts'))
    
    # For example: get all Tags
    all_ctgs = eval(Ctg_of_gt_type).query.all()   # Example: get all Tags
    ####################import pdb; pdb.set_trace()
    for ctg in all_ctgs:   #delete the prevois category of the updated profile and set the new one
        if gt.is_parent_of(ctg):
            gt.unset_parent(ctg)
            gt.set_parent(selected_category)
           
    gt.set_parent(selected_category)  # Uncase there is no previous category for gt 
    
    ####################import pdb; pdb.set_trace()
    
    db.session.commit() 
    return selected_category
 ###END set selected age_range	
    
###get selected option	category	
@gt.route('/get_selected_category_title', methods=['GET', 'POST'])
def get_selected_category_of_gt(Ctg_type, gt):
    ###############import pdb; pdb.set_trace()
    #print(" IN get_selected_category_of_gt Ctg_type", Ctg_type)  
    #print(" IN get_selected_category_of_gt gt", gt)  
    #print("")
    #print("")
    
    if gt.children.all() != None:
        for c in gt.children.all():
            if c.gt_type == Ctg_type:
                return c
    return None
    
    # Example: Get selected Tag of gt 

###get selected option	category	

     
###get selected security option	category	
@gt.route('/get_categories_of', methods=['GET', 'POST'])
def get_categories_of(gt):

    gt_categories =  General_txt.query.filter(General_txt.body == gt.type).distinct().all()
    
    ###########import pdb; pdb.set_trace()
    
    return gt_categories


@gt.route('/get_color', methods=['GET', 'POST'])
@login_required
def get_color(color):
                       
    if color=='אדום':
        c = '#ff0000'
    elif color=='כחול':
        c = '#0000cc'
    elif color=='צהוב':
        c = '#ffcc00'
    elif color=='כתום':
        c = '#ff981a'            
    elif color=='ירוק':
        c = '#00b300'

    elif color=='lblue':
        c = '#e6ffff'
    elif color=='lyellow':
        c = '#ffffcc'  
    elif color=='lorange':
        c = '#ffe066'
    elif color=='lorange':
        c = '#ffcc66'            
    elif color=='lgreen':
        c = '#ccffcc'
    elif color=='lred':
        c = '#ffcccc'        
    elif color=='lpurple':
        c = '#ffe6ff'        

    elif color=='red':
        c = '#ff0000'
    elif color=='blue':
        c = '#0000cc'
    elif color=='yellow':
        c = '#ffcc00'
    elif color=='orange':
        c = '#ff981a'            
    elif color=='green':
        c = '#00b300'        
    elif color=='purple':
        c = '#cc00cc'        

    else:
        c = '#000000'
        
    return c

   
###get selected default option	category	
@gt.route('/get_gt_default', methods=['GET', 'POST'])
def get_gt_default(class_name):
    gt = eval(class_name).query.filter(eval(class_name).default==True).first()    
    return gt 
    
###get default child gt	
@gt.route('/get_gt_default', methods=['GET', 'POST'])
def get_default_child(gt_id, child_type):

    print("")
    print("")    
    print("IN get_default_child SUB_CHILD_TYPE:" , child_type)
    
    gt = General_txt.query.filter(General_txt==gt_id).first()
    gt_children = eval(child_type).query.all()
    for c in gt_children:
        if gt.is_parent_of(c) and c.default==True:
            gt_default_child = c
    print("IN gts/get_default_child  gt_default_child:", gt_default_child)
    print("")
    print("")    
    return gt_default_child 
    
###get default child gt	
@gt.route('/get_gt_default', methods=['GET', 'POST'])
def get_child_by_type(gt_id, child_type):

    print("")
    print("")    
    print("IN get_child_by_type --- gt_id={0}, child_type={1}".format( gt_id, child_type))
    print("")
        
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    print("IN get_child_by_type --- gt=",  gt.body)

    gt_child = None
    gt_children = eval(child_type).query.all()
    for c in gt_children:
        if gt.is_parent_of(c):
            gt_child = c
            print("IN GTS/get_child_by_type  GT_CHILD:", gt_child.title, gt_child.body, gt_child.id)
            print("")
            print("") 
    return gt_child
    
###get default child gt	
@gt.route('/get_gt_default', methods=['GET', 'POST'])
def set_child_by_type(gt_id, child_type, new_gt_child):

    print("")
    print("")    
    print("IN set_child_by_type --- gt_id={0}, child_type={1}".format( gt_id, child_type))
    print("")
    
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    print("GT IS:", gt.title)

    prev_gt_child = get_child_by_type(gt_id, child_type)
    
    if prev_gt_child == None:
        gt.set_parent(new_gt_child)
        print("There is no current child for GT {0} of type {1}. Setting GT as parent of {2}".format(gt.title, child_type, new_gt_child.title))
        db.session.commit()
        return new_gt_child 
        
    print("prev_gt_child:", prev_gt_child, prev_gt_child.id)
    print("new_gt_child:",  new_gt_child, new_gt_child.id)
    
    if prev_gt_child != new_gt_child:
        print(" IN set_child_by_type: SETTING new_gt_child {0} to gt {1}".format(new_gt_child.id, gt.id))
        gt.unset_parent(prev_gt_child)
        gt.set_parent(new_gt_child)
        print("IN GTS/set_child_by_type  GT_CHILD: old_chile={0} new_gt={1}".format(prev_gt_child.id, new_gt_child.id)) 
    else:
        print("IN GTS/set_child_by_type  PREV AND NEW CHILD GTS ARE THE SAME".format(prev_gt_child.id, new_gt_child.id))  
    
    print("")
    print("")
    db.session.commit()
    
    return new_gt_child 