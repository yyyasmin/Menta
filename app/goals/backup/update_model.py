
################## START  Update destination_update ################    
@dst.route('/dsply_dst_form_for_update/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def dsply_dst_form_for_update(from_dst_sort_order):

    print ("In dsply_dst_form_for_update from_dst_sort_order=: ", from_dst_sort_order)
    
    updated_dst = Destination.query.filter(Destination.selected==True).first()
    if updated_dst == None:
        flash("Please select a destination to update")
        redirect(url_for('edit_destinations', from_dst_sort_order))
        

    form = Dst_form()

    form.ar.choices=[]
    form.tag.choices=[]
    form.scrt.choices=[]

    form.ar.choices = [(ar.id, ar.title) for ar in Age_range.query.all()]
    form.ar.default = updated_dst.ar_id

    form.tag.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    form.tag.default = updated_dst.tag_id

    form.scrt.choices = [(scrt.id, scrt.title) for scrt in Scrt.query.all()]
    form.scrt.default = updated_dst.scrt_id

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_dst_form_for_update.html', form=form, from_dst_sort_order=from_dst_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_dst_form_for_update.html', form=form)

    ar = Age_range.query.filter_by(id=form.ar.data).first()
    tag = Tag.query.filter_by(id=form.tag.data).first()
    scrt = Scrt.query.filter_by(id=form.scrt.data).first()

    ###import pdb; pdb.set_trace()
    new_updated_dst_title = form.dst_title.data
    new_updated_dst_body = form.dst_body.data
    
    return destination_add(from_dst_sort_order, ar.title, tag.title, scrt.title, new_updated_dst_title, new_updated_dst_body)


###############################
            
