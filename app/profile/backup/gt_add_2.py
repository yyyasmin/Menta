################## START  ADD GT ################ 
   
@prf.route('/dsply_gt_form_for_add/<int:type>', methods=['GET', 'POST'])
def dsply_gt_form_for_add(type): 

    print ("In dsply_gt_form_for_add")
    
    form = Gt_form()
    
    if type == 1:
        form.gt_type_txt == 'חולשה'       
        form.gt_type = 'Weakness'
        
    elif if type == 2:
        form.gt_type_txt == 'חוזקה'
        form.gt_type = 'Srength'
             
    else:  
        form.gt_type_txt == 'תחום עיניין'        
        form.gt_type = 'Subject'
        
    form.tag.choices=[]
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]

    ### GET Case
    if request.method == 'GET':
        return render_template('./gt/dsply_gt_form_for_add.html', form=form)

@prf.route('/dsply_gt_form_for_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def dsply_gt_form_for_add2(selected_profile_id, type):
	#print(selected_profile_id)    
    general_profile = Profile.query.filter(Profile.title=='general').first()
    if general_profile == None:
        general_profile = Profile('general', 'default', author_id)	
        db.session.add(general_profile)
        std = get_dummy_student()   # Match new general prf to Humpty Dumpty
        std_gt = attach_gt_to_std(std.id, general_profile.id) 
        db.session.commit()
    
    general_profile = profile_select2(general_profile.id)   # save new prf for next setting
    
	return redirect(url_for('profile.dsply_gt_form_for_add', type=type))			

#### POST CASE ####                                                                                     
@prf.route('/gt_to_profile_add/<int:type>', methods=['POST'])
def gt_to_profile_add(type):
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_general_txt_form.html', form=form)

    tag = Tag.query.filter_by(id=form.tag.data).first()

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
        
    elif if type == 2:
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
    
    #######import pdb;; pdb.set_trace()
    general_profile.set_parent(new_gt)
    new_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )


@prf.route('/gt_to_profile_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def gt_to_profile_add2(selected_profile_id, type):

	#print(selected_profile_id)
    if selected_profile_id != 0:
        prf = Profile.query.filter(Profile==selected_profile_id).first()
    else:
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

