  

#### POST CASE ####                                                                                     
@std.route('/std_part_to_prf_add/<int:dsply_direction>', methods=['GET', 'POST'])
def std_part_to_prf_add(new_gt_type, new_gt_id, new_gt_title, new_gt_body, tag_id, dsply_direction):

    print("")
    print("")
    
    print(" IN std_part_to_prf_add")

    if tag_id == 0:
        tag = Tag.query.filter(Tag.selected==True).first()
        if tag == None:
            flash ("יש לבחור נושא")
            return std_edit_profile(0)
        tag_id = tag.id
            

    print("TAG-ID ", tag_id)
    print("")
    print("")
    tag = Tag.query.filter(Tag.id==tag_id).first()
    
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("TAG: ", tag, tag.id)
    print("")
    print("")

    profile = Profile.query.filter(Profile.selected=='True').first()
    if profile == None:
        flash("Please select a profile to add a part to ")
        return redirect(url_for('students.std_edit_profile', dsply_direction=dsply_direction) ) 
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/38309131/wtforms-post-with-selectfield-not-working
    ##print ("form.validate_on_submit", form.validate_on_submit)
    
    print("In std_part_to_prf_add profile is :", profile, profile.id)
    print("")    
    print("")    
    print("In std_part_to_prf_add new_gt_title is :", new_gt_title)
    print("")    
    print("In std_part_to_prf_add new_gt_id is :", new_gt_id)
    print("")
    print("In std_part_to_prf_add new_gt_body is :", new_gt_body)
    print("")
    print("In std_part_to_prf_add gt_type is :", new_gt_type)
    print("")
    print("")
    print(" *** In std_part_to_prf_add TAG is :", tag, tag.id)
    print("")    print("")
    
    author_id = current_user._get_current_object().id 
    
    new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).id==new_gt_id).first()
    if new_gt == None:    
        new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).title==new_gt_title). \
                                         filter(eval(new_gt_type).body==new_gt_body).first()
        if new_gt == None:
            new_gt = eval(new_gt_type)(new_gt_title, new_gt_body, author_id)
            db.session.add(new_gt)
            db.session.commit()
        
    #print("new_gt.id  ", new_gt.id)
    
    #new_gt = general_txt_select3(new_gt.id)
    
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    
    db.session.add(new_gt)
    db.session.commit()
    
    #new_gt = general_txt_select3(new_gt.id)
    all_tag =  Tag.query.filter(Tag.body=='all').first()
    
    new_gt.set_parent(tag)
    new_gt.set_parent(all_tag)

    tag.set_parent(new_gt)
    all_tag.set_parent(new_gt)

    scrt = Scrt.query.filter(Scrt.body=='Private').first()
    if scrt == None:
        flash ("No such Secirity option: Private")
        redirect(url_for('gts.edit_gts'))
        
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("new_gt", new_gt)
    print("new_gt", new_gt.id, new_gt.title)
    print("scrt", scrt)
    print("scrt", scrt.id, scrt.title)
    print("")
    print("")

    new_gt.set_parent(scrt)
    scrt.set_parent(new_gt)
       
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_gt.id) 
    
    ####################################import pdb;; pdb.set_trace()
    profile.set_parent(new_gt)
    profile.set_parent(tag)
    
    humpty_prf = Profile.query.filter(Profile.body==str(get_dummy_student().id)).first()
    humpty_prf.set_parent(new_gt)
    humpty_prf.set_parent(tag)
    
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("Hynpty prf", humpty_prf.id, humpty_prf.title, humpty_prf.body)
    print("Add Part: ", new_gt.id, new_gt.title, new_gt.body)
    print("")
   
    #selected_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    ##print(" In END OF gt_to_profile_add SUB_GT =: " ,selected_sub_tag, selected_sub_tag.id)
    ##print(" In END OF gt_to_profile_add NEW_GT =: " ,new_gt.id,  new_gt.gt_type)
    
    new_gt.selected = False
    db.session.commit()
    
    return std_edit_profile(dsply_direction)
          

@std.route('/std_part_to_prf_add3/<int:tag_id>/<int:dsply_direction>', methods=['GET', 'POST'])
def std_part_to_prf_add3(tag_id, dsply_direction):

    print("")
    print("")
    
    print(" IN std_part_to_prf_ADD3")
    
    if tag_id == 0:
        tag = Tag.query.filter(Tag.selected==True).first()
        if tag == None:
            flash ("יש לבחור נושא")
            return std_edit_profile(0)
        tag_id = tag.id
            
            
    print("TAG-ID ", tag_id)
    print("")
    print("")
       
    #################import pdb; pdb.set_trace()
    
    #print("request.form['gt_title'] ",   request.form['gt_title'])
    #print("request.form['gt_body'] ",    request.form['gt_body'])
    #print("request.form['class_name'] ", request.form['class_name'])

    new_gt_title =  request.form['gt_title']
    new_gt_body =  request.form['gt_body']
    new_gt_type =  request.form['class_name']
        
    return std_part_to_prf_add(new_gt_type, 0, new_gt_title, new_gt_body, tag_id, dsply_direction) 


