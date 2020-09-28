
    ############### START UPDATE GT ################  
 
@prf.route('/dsply_gt_form_for_update', methods=['GET', 'POST'])
def dsply_gt_form_for_update():
          
    updated_prf = Profile.query.filter(Profile.selected==True).first()
    if updated_prf == None:
        flash("Please select a profile to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
        
    updated_gt = General_txt.query.filter(General_txt.selected==True).filter(General_txt.id != updated_prf.id).first()
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
              
    form = Gt_form()

    form.gt_title.data = updated_gt.title
    form.gt_body.data =  updated_gt.body
    form.gt_type.data =  updated_gt.gt_type
    form.gt_type_txt.data = updated_gt.h_name

    form.tag.choices=[]
    
    gt_tag = Tag.query.filter(Tag.body=='default').first()
    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    all_tags = Tag.query.all()    
    for tag in all_tags:
        if updated_gt.is_parent_of(tag):
            gt_tag = tag
            break
    form.tag.default = gt_tag.id
    form.process()
        
    #DEBUG   
    gt = updated_gt
    ##########import pdb; pdb.set_trace()
    #DEBUG

    ### GET Case
    if request.method == 'GET':
        return render_template('./gt/backup/dsply_gt_form_for_update.html', prf=updated_prf, gt=updated_gt, form=form)


@prf.route('/dsply_gt_form_for_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def dsply_gt_form_for_update2(selected_profile_id, selected_gt_id):

    import pdb; pdb.set_trace()
    
    gt = general_txt_select2(selected_gt_id)
    prf = profile_select2(selected_profile_id)
   
    return redirect(url_for('profile.dsply_gt_form_for_update'))			


#### POST CASE ####                                                                                     
@prf.route('/gt_profile_update', methods=['GET', 'POST'])
def gt_profile_update (selected_tag, updated_gt_title, updated_gt_body):
  
    author_id = current_user._get_current_object().id    
        
    updated_profile = Profile.query.filter(Profile.selected==True).first()
    if updated_profile == None:
        flash("Please select a profile to update a part ")
        return redirect(url_for('profile.edit_profile_by_tag') )
  
    updated_profile = profile_select2(updated_profile.id)  
     
    updated_gt = General_txt.query.filter(General_txt.selected==True).filter(General_txt.id != Profile.id).first()    
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile_by_tag') )
          
    updated_gt.title = updated_gt_title
    updated_gt.body =  updated_gt_body
       
    selected_tag = set_gt_category(updated_gt.id, 'Tag', selected_tag.title, "בחר נושא")
        
    db.session.commit()

    updated_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile2_by_tag') )


@prf.route('/gt_profile_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def gt_profile_update2(selected_profile_id, selected_gt_id):

    print(" IN gt_profile_update2", selected_profile_id, selected_gt_id)
    print("")

    form = Gt_form()

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_update.html', form=form)
    
    updated_gt_title = form.gt_title.data
    updated_gt_body =  form.gt_body.data    
    updated_tag =      form.tag.data

    selected_tag = Tag.query.filter_by(id=form.tag.data).first()
  
    prf = Profile.query.filter(Profile.selected==True).first()
    if prf == None:
        flash("Please select a profile first ")
        return redirect(url_for('profile.edit_profile2_by_tag'))		
       
    gt = General_txt.query.filter(General_txt.selected==True).first()   
 
    return gt_profile_update(selected_tag, selected_tag.title, updated_gt_body)
    
    ############## END UPDATE GT ################ 



    ################ END DELETE GT ############## 

@prf.route('/gt_from_profile_delete', methods=['GET', 'POST'])
def gt_from_profile_delete():

    #################import pdb; pdb.set_trace()

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

