
################## START  Update profile_update ################    
@prf.route('/dsply_gt_form_for_update', methods=['GET', 'POST'])
def dsply_gt_form_for_update():
    
    updated_gt = General_txt.query.filter(General_txt.selected==True).first()
    if updated_gt == None:
        flash("Please select a profile part to update")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3))
        
    #print("IIIIIIIIIIIIn dsply_gt_form_for_update2 Updated prf is", updated_gt.title)

    form = Gt_form()

    form.title.data = updated_gt.title
    form.body.data =  updated_gt.body

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
        return render_template('dsply_gt_form_for_update.html', update_gt=updated_gt, form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_update.html', form=form)

    tag = Tag.query.filter_by(id=request.form['tag']).first()

    new_updated_gt_title = request.form['title']      #Current Description  selection
    new_updated_gt_body =  request.form['body']
      
    return gt_to_profile_add(tag.title, new_updated_gt_title, new_updated_gt_body)


@prf.route('/dsply_gt_form_for_update2/<int:selected_gt_id>', methods=['GET', 'POST'])
def dsply_gt_form_for_update2(selected_gt_id):
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.dsply_gt_form_for_update'))			

############################### END DST Update
   