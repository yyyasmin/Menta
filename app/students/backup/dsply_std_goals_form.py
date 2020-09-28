
################## START  Update destination_update ################    
@dst.route('/update_std_goal_form, methods=['GET', 'POST'])
def update_std_goal_form():

    print ("In update_std_goal_form from_dst_sort_order ")
    
    updated_std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if updated_std_goal == None:
        flash("Please select a student's goal to update")
        return redirect(url_for('students.edit_student_goals')
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    status = Status.query.filter_by(id=request.form['status']).first()
    updated_std_goal.status_id = status.id
    updated_std_goal.status_title = status.title
    updated_std_goal.status_color = status.color
    
    updated_std_goal.due_date = request.form['due_date']

    db.session.commit() 


@dst.route('/update_std_goal_form2/<int:selected_std_goal_id>', methods=['GET', 'POST'])
def update_std_goal_form2(selected_std_goal_id):

    print("In UUUUUUUUUU dsply_dst_form_for_update2 selected_dst_id ", selected_destination_id)
    std_goal = std_goal_select2(selected_std_goal_id)
    return dsply_std_goal_form()			

############################### END DST Update
                                            