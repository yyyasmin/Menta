###############START destination_ADD_AT ONCE	
@dst.route('/get_destination_add/<int:from_dst_sort_order>/<selected_ar_title>/<selected_tag_title>/<selected_scrt_title>', methods=['POST'])
def get_destination_add(from_dst_sort_order, selected_ar_title, selected_tag_title, selected_scrt_title):
    
    print("In destination_add_at_once is :",   from_dst_sort_order)
    if from_dst_sort_order == 0:
        import pdb; pdb.set_trace()
        
    author_id = current_user._get_current_object().id    
            
    age_ranges = Age_range.query.all()
    tags = Tag.query.all()    
    scrts = Scrt.query.all()  
    #####import pdb; pdb.set_trace()
    ###import pdb; pdb.set_trace()
    new_destination = Destination.query.filter(Destination.selected==True).first()
    if new_destination == None:
        new_destination = Destination.query.filter(Destination.title=='New dest').first()
        if new_destination == None:
            new_destination = Destination('New dest', "", author_id)	
        db.session.add(new_destination)
        db.session.commit()
        new_destination = destination_select2(new_destination.id)   # save ne dest for next setting

    print("new_destination  ar tag scrt ", new_destination, selected_ar_title, selected_tag_title, selected_scrt_title)
    '''
    selected_ar_title = "בחר קבוצת גיל"
    selected_tag_title = "בחר נושא"
    selected_scrt_title = "בחר סוג אבטחה"  
    '''
    print("request=: ", request.method)

    import pdb; pdb.set_trace()
    
    if request.method == 'GET' :
        return render_template('add_destination_at_once.html', 
                                            dst=new_destination,
                                            age_ranges=age_ranges,                                           
                                            tags=tags,
                                            scrts=scrts,
                                            selected_ar_title = selected_ar_title, 
                                            selected_tag_title =selected_tag_title,
                                            selected_scrt_title = selected_scrt_title,
                                            from_dst_sort_order=from_dst_sort_order)

                      
################## END DEstinatio ADD At ONCE ################    