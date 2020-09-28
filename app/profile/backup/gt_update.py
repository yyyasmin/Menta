
    ############### START UPDATE GT ################  
  
@prf.route('/dsply_form_for_update', methods=['GET', 'POST'])
def dsply_form_for_update():

    import pdb; pdb.set_trace()
    
    updated_prf = Profile.query.filter(Profile.selected==True).first()
    if updated_prf == None:
        flash("Please select a profile to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
   
    updated_gt = General_txt.query.filter(General_txt.selected==True).first()
    if updated_gt == None:
        flash("Please select a profile to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
                
    print("IIIIIIIIIIIIn dsply_form_for_update2 Updated prf  gt is", updated_prf.title, updated_gt.title)

    form = Gt_form()

    form.title.data = updated_gt.title
    form.body.data =  updated_gt.body
    form.body.gt_type_txt =  updated_gt.gt_type_txt
    form.body.gt_type =  updated_gt.gt_type

    form.tag.choices=[]

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    all_tags = Tag.query.all()    
    for tag in all_tags:
            if updated_prf.is_parent_of(tag):
                prf_tag = tag
                break
    form.tag.default = prf_tag.id
    form.process()

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_form_for_update.html', prf=updated_prf, gt=updated_gt, form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_form_for_update.html', form=form)

    tag = Tag.query.filter_by(id=request.form['tag']).first()

    updated_prf_title = request.form['title']      #Current Description  selection
    updated_prf_body =  request.form['body']
      
    return profile_update(from_prf_sort_order,tag.title, updated_prf_title, updated_prf_body)


@prf.route('/dsply_form_for_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def dsply_form_for_update2(selected_profile_id, selected_gt_id):
    default_prf = Profile.query.filter(Profile.body=='default').first()
    prf = profile_select2(default_prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.dsply_form_for_update'))			

################## START  GT UPDATE  ################  
  

################## START GT UPDATE ################ 
 
@prprf.route('/dsply_gt_form_for_update', methods=['GET', 'POST'])
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


@prprf.route('/dsply_gt_form_for_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def dsply_gt_form_for_update2(selected_profile_id, selected_gt_id):
    if selected_gt_id == 0:        
        prf = Profile.query.filter(Profile.body=='default').first()
    else:
        prf = Profile.query.filter(Profile.id).first()
        
    prf = general_txt_select2(prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.dsply_gt_form_for_update'))			

################## END GT UPDATE ################ 



#### POST CASE ####                                                                                     
@prf.route('/gt_profile_update', methods=['POST'])
def gt_profile_update():

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_update.html', form=form)

    tag = Tag.query.filter_by(id=request.form['tag']).first()

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

    ##import pdb; pdb.set_trace()
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
    
    print{" IN gt_profile_update Seted Tag to : ", selected_tag)
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, updated_gt.id) 
    
    #######import pdb;; pdb.set_trace()
    updated_profile.set_parent(updated_gt)
    updated_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile_by_tag') )



@prprf.route('/gt_profile_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def gt_profile_update2(selected_profile_id, selected_gt_id):
    if selected_gt_id == 0:        
        prf = Profile.query.filter(Profile.body=='default').first()
    else:
        prf = Profile.query.filter(Profile.id).first()
        
    prf = general_txt_select2(prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.gt_profile_update'))
    
    ############### START UPDATE GT ################  
