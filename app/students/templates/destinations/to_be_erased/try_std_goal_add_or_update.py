#		
@std.route('/std_goal_add_or_update', methods=['GET', 'POST'])
def std_goal_add_or_update():
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination to delete first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))

    now = date.today
    
                
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    print("&&&&&&&&&& In goal_to_destination_of_student_add std dst goal now: ", std, dst, goal, now)
   
    import pdb; pdb.set_trace()
    
    due_date = request["due_date"]
    status = request["status"]
    
    std_goal = Due_date.query.filter(Due_date.goal_id==goal.id).first()
    if std_goal == None:       #Crate new goal-due_date for student
        std_goal = Due_date(std.id, goal.id, due_date, status)
        std.goals.append(std_goal)
    else:                      # update student due_date-goal
        std_goal.status = status     
        std_goal.due_date = due_date
            
    db.session.commit()  
    db.session.refresh(std)    
    
    return render_template('./destinations/edit_student_destinations.html', std=std, dst=dst)
  
***************************************

    updated_dst = destination_select2(selected_destination_id)
    if updated_dst == None:
        flah("please select a destination to update ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
    print("\n\n")
    print("In destination_update for dst start: ", updated_dst.title)
    print("Updateing dst : ", updated_dst.title)

    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all() 

    
    selected_ar_title = get_selected_ar_title()
    selected_tag_title = get_selected_tag_title()
    selected_scrt_title = get_selected_scrt_title()
    
    if request.method == 'GET':
        print("GGGGGGGGGGGGGGET")
        return render_template('update_destination.html',
                            dst = updated_dst,
                            age_ranges=age_ranges,
                            tags=tags, 
                            scrts=scrts,
                            selected_ar_title=selected_ar_title, 
                            selected_tag_title=selected_tag_title,
                            selected_scrt_title=selected_scrt_title,
                            from_dst_sort_order=from_dst_sort_order)
                            
                                              	    
    if request.form['submit'] == 'submit_ar':
        print("In destination_update for dst submit_ar: ", updated_dst.title)
        print("Updateing dst : ", updated_dst.title)

        selected_ar = set_dst_age_range()
        
        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
           

    if request.form['submit'] == 'submit_tag':
        print("In destination_update for dst submit_tag: ", updated_dst.title)
        print("Updateing dst : ", updated_dst.title)

        selected_tag = set_dst_tag()
        
        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
             
    if request.form['submit'] == 'submit_scrt':
        print("In destination_update for dst submit_scrt: ", updated_dst.title)
        print("Updateing dst : ", updated_dst.title)

        #selected_scrt = set_dst_scrt()
        selected_scrt=set_dst_scrt()

        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
                                        
    if request.form['submit'] == 'submit_description': 
        print("In destination_update for dst submit_description: ", updated_dst.title)
        print("Updateing dst : ", updated_dst.title)

        print ("REauest methos is: ", request.form['submit'])
        ########import pdb; pdb.set_trace()
        title = request.form['title']     
        body = request.form['description']
        
        updated_dst.title = title
        updated_dst.body = body

        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
                   
        
    if request.form['submit'] == 'Back to destinations list':    # Save setting and call edit destinations
        updated_tag = Tag.query.filter(Tag.selected==True).first()
        updated_ar = Age_range.query.filter(Age_range.selected==True).first()
        updated_scrt = Scrt.query.filter(Scrt.selected==True).first()
        
        updated_dst.age_range_id = updated_ar.id
        updated_dst.scrt_id = updated_scrt.id
        
        updated_dst_tag = Dst_Tag.query.filter(Dst_Tag.destination_id==updated_dst.id and  Dst_Tag.tag_id==updated_tag.id).first()
        if updated_dst_tag == None:
            updated_dst = Dst_Tag(update_dst.id, updated_tag.id)       
            updated_dst.destination = update_dst
            updated_dst.tag = updated_tag
            updated_tag.destinations.append(updated_dst_tag)
            updated_dst.tags.append(updated_dst_tag)
     
        ########import pdb; pdb.set_trace()
            db.session.commit()
            update_dst.selected = False
            return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
################## END Submit Back to destinations list ################ 

### For all submit options except for back to list###
    db.session.commit()
    return render_template('update_destination.html', 
                                                dst = updated_dst,
                                                age_ranges=age_ranges,
                                                tags=tags, 
                                                scrts=scrts,
                                                selected_ar_title=selected_ar_title, 
                                                selected_tag_title=selected_tag_title,
                                                selected_scrt_title=selected_scrt_title,
                                                from_dst_sort_order=from_dst_sort_order)                                

###End Update destination########################
