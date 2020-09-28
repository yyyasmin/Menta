   
@prf.route('/dsply_gt_form_for_add/<int:type>', methods=['GET'])
def dsply_gt_form_for_add(type): 
    
    form = Gt_form()
        
    profile = Profile.query.filter(Profile.selected=='True').first()
    if profile == None:
        flash ("Please select a profile to add a part for")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
       
    print ("In dsply_gt_form_for_add")
    ##import pdb; pdb.set_trace()
    
    prf = Profile.query.filter(Profile.selected == True).first()
    if prf == None:
        flash("Please select a profile to update a part for")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
        
    form = Gt_form()
    
    if  type == 1:
        form.gt_type_txt = 'חולשה'       
        form.gt_type = 'Weakness'
        fgt_type = 'Weakness'
        
    elif type == 2:
        form.gt_type_txt = 'חוזקה'
        form.gt_type = 'Srength'
        gt_type = 'Srength'
             
    else:  
        form.gt_type_txt = 'תחום עיניין'        
        form.gt_type = 'Subject'
        gt_type = 'Subject'
        
    form.tag.choices=[]
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    tags = Tag.query.all()
    
    if request.method == 'GET':
        return render_template('./gt/dsply_gt_form_for_add.html',  profile=profile, form=form, type=type)
 


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
        prf = general_profile
    
    print(" IN dsply_gt_form_for_add2 prf.id=: ", prf.id)
    prf = profile_select2(prf.id)   # save new prf for next setting
    #import pdb; pdb.set_trace()
    return redirect(url_for('profile.dsply_gt_form_for_add', profile=prf, type=type))			

   
@prf.route('/dsply_gt_form_for_add3/<int:type>', methods=['GET'])
def dsply_gt_form_for_add3(type): 

    #print ("In dsply_gt_form from_gt_sort_order=: ", from['request'])
    
********************************************
    form = Gt_form()

    form.tag.choices=[]

    form.gt_type_txt = 'subject'  # ************* sapposed to be if type == 1 / 2 / 3 : for weak/strn/sbj *******************
    
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    
    profile = Profile.query.filter(Profile.body=='default').first()
    ### GET Case
    
    #import pdb; pdb.set_trace()
    print(request.method)
    
    if request.method == 'GET':
        return render_template('./gt/dsply_gt_form_for_add.html',  profile=profile, form=form, type=3)
        
**************************************************************


#### POST CASE ####                                                                                     
@prf.route('/gt_to_profile_add/<int:type>', methods=['GET', 'POST'])
def gt_to_profile_add(type):

    form = Gt_form()

    form.ar.choices=[]

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #
    #import pdb; pdb.set_trace()
    
    '''
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_form_for_update.html', form=form)
    '''
    print(  request.form)   
#************************
    tag = Tag.query.filter_by(id=form.tag.data).first()
#************************

#***********************************
    #import pdb; set_trace()
    
    gt_tag_name = "gt_tag"
    print( "request.form[gt_tag_name]", request.form[gt_tag_name])
    
    gt_title_name = "gt_title"
    print( "request.form[gt_title_name]", request.form[gt_title_name])
     
    gt_body_name = "gt_body"
    print( "request.form[gt_body_name]", request.form[gt_body_name])
    
#************************************
    

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
    
    ##########import pdb;; pdb.set_trace()
    general_profile.set_parent(new_gt)
    new_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )


@prf.route('/gt_to_profile_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def gt_to_profile_add2(selected_profile_id, type):

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


#### POST CASE ####                                                                                     
@prf.route('/gt_add/<int:type>', methods=['GET', 'POST'])
def gt_add3(type):

    #import pdb; pdb.set_trace()
    #print ("In dsply_gt_form from_gt_sort_order=: ", from['request'])

    form = Gt_form()

    form.tag.choices=[]

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    
    profile = Profile.query.filter(Profile.body=='default').first()
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_add.html', form=form)

    new_gt_title = form.gt_title.data
    new_gt_body = form.gt_body.data
    
    tag = Tag.query.filter_by(id=form.tag.data).first()


    return gt_add(tag.title, new_gt_title, new_gt_body)

    
    #print("In POST gt_add_at_once is :",   from_gt_sort_order)
    ##############old_gt_scrt pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    tags = Tag.query.all()  
    
    new_gt = General_txt.query.filter(General_txt.selected==True).first()
    if new_gt == None:
        new_gt = General_txt.query.filter(General_txt.title=='New gt').first()
        if new_gt == None:
            new_gt = General_txt('New gt', "", author_id)	
        db.session.add(new_gt)
        db.session.commit()
        new_gt = gt_select2(new_gt.id)   # save new gt for next setting

    #print("new_gt  ar tag scrt  gt", new_gt, selected_ar_title, selected_tag_title, selected_scrt_title, new_gt_title)

    #print("request=: ", request.method)

    ##############old_gt_scrt pdb.set_trace()
  
    #POST case

    selected_tag = set_gt_tag(selected_tag_title) 

    new_gt.title = new_gt_title      #Current Description  selection
    new_gt.body =  new_gt_body
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    gt = new_gt    
    std_gt = attach_gt_to_std(std.id, gt.id)  
    ######import pdb;; pdb.set_trace()
    selected_scrt = set_gt_scrt(selected_scrt_title)
        
    new_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile_by_tag'))

 
@prf.route('/gt_add2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def gt_add2(selected_profile_id, type):
   

    form = Gt_form()

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_add.html', form=form)

   
    print(" IN gt_add2", selected_profile_id, type)
    print("form", form)
    print("")
    print("form.gt_title.data", form.gt_title.data)
    print("form.tag.date", form.tag.data)

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
    #import pdb; pdb.set_trace()
    return redirect(url_for('profile.gt_add3', type=type))			
    #return redirect(url_for('profile.dsply_gt_form_for_add', profile=prf, type=type))			
    #return redirect(url_for('profile.gt_add3', profile=prf, type=type))			
 
######## END POST METHOD FOR gt_add ###############

    ################ END GT 3 ###################
    