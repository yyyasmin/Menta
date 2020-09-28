
#### POST CASE ####                                                                                     
@dst.route('/destination_update/<int:from_dst_sort_order>', methods=['POST'])
def destination_update(from_dst_sort_order, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title, new_dst_body):
    
    print("In POST destination_update_at_once is :",   from_dst_sort_order)
    #######import pdb; pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    ############import pdb; pdb.set_trace()
    ##########import pdb; pdb.set_trace()
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.update(new_destination)
        db.session.commit()

    print("new_destination  ar tag scrt  dst", new_destination, selected_ar_title, selected_tag_title, selected_scrt_title, new_dst_title)

    print("request=: ", request.method)

    #######import pdb; pdb.set_trace()
  
    #POST case

    selected_ar = set_dst_age_range(selected_ar_title)
    selected_tag = set_dst_tag(selected_tag_title) 
    ######import pdb; pdb.set_trace()
    selected_scrt = set_dst_scrt(from_dst_sort_order, selected_scrt_title)

    new_destination.title = new_dst_title      #Current Description  selection
    new_destination.body =  new_dst_body
    
    db.session.commit()
         
    db.session.commit()
    return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=from_dst_sort_order))

######## END POST METHOD FOR destination_update ###############
      