 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_gt_form ################    
@gt.route('/dsply_gt_form', methods=['GET', 'POST'])
def dsply_gt_form_for_add3():
    #print ("In dsply_gt_form from_gt_sort_order=: ", from_gt_sort_order)

    form = Gt_form()

    form.tag.choices=[]

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_gt_form_for_add.html', form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form.html', form=form)

    tag = Tag.query.filter_by(id=form.tag.data).first()

    ##############old_gt_scrt pdb.set_trace()
    new_gt_title = form.gt_title.data
    new_gt_body = form.gt_body.data
    return gt_add(tag.title, new_gt_title, new_gt_body)


#### POST CASE ####                                                                                     
@gt.route('/gt_add', methods=['POST'])
def gt_add(selected_tag_titlenew_gt_title, new_gt_body):
    
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
    #####import pdb;; pdb.set_trace()
    selected_scrt = set_gt_scrt(selected_scrt_title)
        
    new_gt.selected = False
    db.session.commit()
    return redirect(url_for('profile.edit_profile_by_tag'))
    
######## END POST METHOD FOR gt_add ###############
