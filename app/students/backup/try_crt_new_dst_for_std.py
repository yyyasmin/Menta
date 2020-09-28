#################### create_new_dst_for_std ##################
return redirect(url_for('students.edit_student_destinations2', selected_student_id=, selected_destination_id=))

@std.route('/create_new_dst_for_std', methods=['GET', 'POST'])
def create_new_dst_for_std():
###############START destination_ADD	
    print("In destination_add")

    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
 
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.add(new_destination)
        db.session.commit()
        new_destination = destination_select2(new_destination.id)   # save ne dest for next setting
    
    print("new_destination", new_destination)
    
    if request.method == 'GET': 
        return render_template('add_destination.html', 
                                            dst=new_destination,
                                            age_ranges=age_ranges,                                           
                                            tags=tags,
                                            scrts=scrts,
                                            selected_ar_title = "בחר קבוצת גיל", 
                                            selected_tag_title = "בחר נושא",
                                            selected_scrt_title = "בחר סוג אבטחה",
                                            from_dst_sort_order=from_dst_sort_order)
    #POST case
   
    if request.form['submit'] == 'submit_age_range':
        print("Submit", request.form['submit'])
        selected_ar = set_dst_age_range()

        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
            

    if request.form['submit'] == 'submit_tag':
        selected_tag = set_dst_tag()
        
        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
           
    if request.form['submit'] == 'submit_scrt':
        selected_scrt = set_dst_scrt()

        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()
                                           
    if request.form['submit'] == 'submit_description': 
        title = request.form['title']      #Current Description  selection
        body = request.form['description']
        
        last_selected_ar = Age_range.query.filter(Age_range.selected == True).first()
        last_selected_tag = Tag.query.filter(Tag.selected == True).first()
        last_selected_scrt = Scrt.query.filter(Scrt.selected == True).first()

        new_destination.title = title
        new_destination.body = body
        new_destination.age_range_id = last_selected_ar.id
                
        selected_ar_title = get_selected_ar_title()
        selected_tag_title = get_selected_tag_title()
        selected_scrt_title = get_selected_scrt_title()

            
    if request.form['submit'] == 'Back to destinations list':    # Save setting and call edit destinations
        selected_ar = Age_range.query.filter(Age_range.selected==True).first()
        selected_tag = Tag.query.filter(Tag.selected==True).first()
        selected_scrt = Scrt.query.filter(Scrt.selected==True).first()
                        
        dummy_std = get_dummy_student()
        dummy_std.destinations.append(new_destination)
        
        new_destination.selected = False
        db.session.commit()
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
                      
################## END Submit Back to destinations list ################    
 
################## For all options except for 'Back to dest list ################            
    db.session.commit()
    return render_template('add_destination.html', 
                                            dst=new_destination,
                                            age_ranges=age_ranges,
                                            tags=tags,
                                            scrts=scrts,
                                            selected_ar_title = selected_ar_title, 
                                            selected_tag_title = selected_tag_title,
                                            selected_scrt_title = selected_scrt_title,
                                            from_dst_sort_order=from_dst_sort_order)                      

###############END destination_ADD##########################
       

    #########################################################################
    ### set private seurity option and disable security option selection  ###
    ### for private student which happens when                            ### 
    ### user wants to add a specific destination only to his student      ###
    #########################################################################

 
                                       
#################### END create_new_dst_for_std ##################