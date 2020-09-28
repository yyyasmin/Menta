 ###############START destination_ADD_AT ONCE	
@dst.route('/destination_add_at_once/<int:from_dst_sort_order>', methods=['GET', 'POST'])
def destination_add_at_once(from_dst_sort_order):
    print("In destination_add_at_once")

    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    #import pdb; pdb.set_trace()
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
   
    selected_ar = set_dst_age_range()


        

    selected_tag = set_dst_tag()
    

       
    selected_scrt = set_dst_scrt()

                                       
    title = request.form['title']      #Current Description  selection
    body = request.form['description']
    
        
    selected_ar = Age_range.query.filter(Age_range.selected==True).first()
    selected_tag = Tag.query.filter(Tag.selected==True).first()
    selected_scrt = Scrt.query.filter(Scrt.selected==True).first()
                    
    dummy_std = get_dummy_student()
    dummy_std.destinations.append(new_destination)
    
    new_destination.selected = False
    db.session.commit()
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))
                      
################## END DEstinatio ADD At ONCE ################    
 