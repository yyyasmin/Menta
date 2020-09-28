 
### FROM https://www.youtube.com/watch?v=I2dJuNwlIH0&feature=youtu.be
### FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
################## START  Ddsply_goal_form ################    
@dst.route('/dsply_goal_form', methods=['GET', 'POST'])
def dsply_goal_form():

    form = Goal_form()

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_goal_form.html', form=form)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form.html', form=form)


    ########import pdb; pdb.set_trace()
    new_goal_title = form.goal_title.data
    new_goal_body = form.goal_body.data
    
    return goal_add(new_goal_title, new_goal_body)

################## START  Update destination_update ################    
@dst.route('/dsply_goal_form_for_update', methods=['GET', 'POST'])
def dsply_goal_form_for_update(from_goal_sort_order):

    print ("In dsply_goal_form_for_update from_goal_sort_order=: ")
    
    updated_dst = Destination.query.filter(Destination.selected==True).first()
    if updated_dst == None:
        flash("Please select a destination to update")
        return redirect(url_for('destinations.edit_destinations_goals', from_goal_sort_order=from_goal_sort_order))
        

    form = Goal_form()

    form.goal_title.data = updated_dst.title
    form.goal_body.data =  updated_dst.body

    ### FROM https://github.com/wtforms/wtforms/issues/106
    ### myform.select.default = 2
    ### myform.process() // <-- you missed this :)
    ### FROM https://github.com/wtforms/wtforms/issues/106

    ### GET Case
    if request.method == 'GET':
        return render_template('dsply_goal_form_for_update.html', dst=updated_dst, form=form, from_goal_sort_order=from_goal_sort_order)

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_goal_form_for_update.html', form=form)

    ########import pdb; pdb.set_trace()
    new_updated_goal_title = request.form['title']      #Current Description  selection
    new_updated_goal_body =  request.form['body']
    
    return destination_update(new_updated_goal_title, new_updated_goal_body)


@dst.route('/dsply_goal_form_for_update2/<int:selected_destination_id>/<int:from_goal_sort_order>', methods=['GET', 'POST'])
def dsply_goal_form_for_update2(selected_destination_id):

    print("In UUUUUUUUUU dsply_goal_form_for_update2 selected_goal_id ", selected_destination_id)
    dst = destination_select2(selected_destination_id)
    return redirect(url_for('destinations.dsply_goal_form_for_update'))			

############################### END DST Update